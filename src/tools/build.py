# build.sh
# Creates a 360K .img flopply image file containing a bootable MINIX image.

from dataclasses import dataclass

PROG_ORG = 1536         # where kernel begins in abs mem
SECTOR_SIZE = 512
EXEC_MAGIC = 0x04100301
SEP_MAGIC = 0x04200301  # separate I & D program
KERNEL_D_MAGIC = 0x526F # identifies kernel data space
FS_MM_D_MAGIC = 0xDADA
HEADER_LEN = 0x20
FLOPPY_360K_SIZE = 360*1024
CLICK_ALIGN = 16
CLICK_SHIFT = 4
DS_OFFSET = 4           # position of DS written in kernel text seg

def u16le(i_val):
    return i_val.to_bytes(2, "little")

def le_to_int(bytes_):
    return int.from_bytes(bytes_, "little")

@dataclass
class HeaderInfo:
    text_size: int
    data_size: int
    bss_size: int
    entry_point: int
    total_mem_alloc: int
    symbols_size: int
    is_sep: bool

    def total_size(self):
        return self.text_size + self.data_size + self.bss_size

    def i_d_bss_len(self):
        if self.is_sep:
            return self.text_size, self.data_size + self.bss_size
        else:
            return 0, self.text_size + self.data_size + self.bss_size

    def print_sizes(self, name):
        print("{:>6}  text={:>5}  data={:>5}  bss={:>5}  tot={:>5}  hex={:>5X}  {}".format(
            name, self.text_size, self.data_size, self.bss_size, self.total_size(),
            self.total_size(), ("Separate I & D" if self.is_sep else "")
        ))

    @classmethod
    def from_bytes(cls, bytes_):
        magic = le_to_int(bytes_[0:4])
        if magic == EXEC_MAGIC:
            is_sep = False
        elif magic == SEP_MAGIC:
            is_sep = True
        else:
            raise ValueError(f"Bad exec magic {magic:#x}")

        assert HEADER_LEN == bytes_[4], "Bad header length field"

        hdr = cls(
            text_size=le_to_int(bytes_[8:12]),
            data_size=le_to_int(bytes_[12:16]),
            bss_size=le_to_int(bytes_[16:20]),
            entry_point=le_to_int(bytes_[20:24]),
            total_mem_alloc=le_to_int(bytes_[24:28]),
            symbols_size=le_to_int(bytes_[28:32]),
            is_sep=is_sep,
        )

        if is_sep:
            assert hdr.text_size % CLICK_ALIGN == 0, f"Bad text size {hdr.text_size}"

        return hdr

def strip_and_pad(exec_bytes):
    header = HeaderInfo.from_bytes(exec_bytes[:HEADER_LEN])
    program = exec_bytes[HEADER_LEN:] + b'\x00'*header.bss_size
    padding = (-len(program)) % CLICK_ALIGN
    header.bss_size += padding
    return header, program + b'\x00' * padding

def build_360k_floppy_image(bootblok, kernel, mm, fs, init, fsck):
    bootblok_padded = bootblok.ljust(SECTOR_SIZE, b'\x00')
    kernel_header, kernel_padded = strip_and_pad(kernel)
    mm_header, mm_padded = strip_and_pad(mm)
    fs_header, fs_padded = strip_and_pad(fs)
    init_header, init_padded = strip_and_pad(init)
    fsck_header, fsck_padded = strip_and_pad(fsck)

    image_size = (
        len(bootblok_padded) + len(kernel_padded) + len(mm_padded)
        + len(fs_padded) + len(init_padded) + len(fsck_padded)
    )

    # patch bootblok
    minix_size = (
        len(kernel_padded) + len(mm_padded) + len(fs_padded) + len(init_padded)
    )
    total_mem = minix_size + len(fsck_padded)
    num_sectors = (total_mem // SECTOR_SIZE) + int(total_mem % SECTOR_SIZE > 0)
    cs_fsck = PROG_ORG + minix_size
    ds_fsck = cs_fsck + (fsck_header.text_size if fsck_header.is_sep else 0)
    pc_fsck = 0
    bootblok_padded[504:506] = u16le(num_sectors)
    bootblok_padded[506:508] = u16le(ds_fsck >> CLICK_SHIFT)
    bootblok_padded[508:510] = u16le(pc_fsck)
    bootblok_padded[510:512] = u16le(cs_fsck >> CLICK_SHIFT)

    # check magic
    assert (
        KERNEL_D_MAGIC == le_to_int(kernel_padded[kernel_header.text_size:][:2])
    ), "Bad kernel data magic"
    assert (
        FS_MM_D_MAGIC == le_to_int(fs_padded[fs_header.text_size:][:2])
    ), "Bad fs data magic"
    assert (
        FS_MM_D_MAGIC == le_to_int(mm_padded[mm_header.text_size:][:2])
    ), "Bad mm data magic"

    # patch kernel
    pos = kernel_header.text_size   # start of data section
    for prog_hdr in [kernel_header, mm_header, fs_header, init_header]:
        text_size, data_size = prog_hdr.i_d_bss_len()
        kernel_padded[pos:pos+2] = u16le(text_size >> CLICK_SHIFT)
        kernel_padded[pos+2:pos+4] = u16le(data_size >> CLICK_SHIFT)
        pos += 4

    kernel_ds = PROG_ORG
    if kernel_header.is_sep:
        kernel_ds += kernel_header.text_size
    kernel_padded[DS_OFFSET:DS_OFFSET+2] = u16le(kernel_ds >> CLICK_SHIFT)

    # patch fs
    init_org = PROG_ORG + minix_size - len(init_padded)
    init_text_size, init_data_size = init_header.i_d_bss_len()
    off = fs_header.text_size + 4 # info to addr 4 in fs data space
    fs_padded[off:off+2] = u16le(init_org >> CLICK_SHIFT)
    fs_padded[off+2:off+4] = u16le(init_text_size >> CLICK_SHIFT)
    fs_padded[off+4:off+6] = u16le(init_data_size >> CLICK_SHIFT)

    # create boot image
    raw_image = bytearray()
    raw_image.extend(bootblok_padded)
    raw_image.extend(kernel_padded)
    raw_image.extend(mm_padded)
    raw_image.extend(fs_padded)
    raw_image.extend(init_padded)
    raw_image.extend(fsck_padded)

    print_stats(kernel_header, mm_header, fs_header, init_header, fsck_header, minix_size, len(raw_image)-512)

    assert (
        len(raw_image) <= FLOPPY_360K_SIZE
    ), "Not enough space on 360K floppy for boot image"

    print(f"Padded {len(raw_image)} byte image with zeroes to make 360K disk image.")
    raw_image = raw_image.ljust(FLOPPY_360K_SIZE, b'\x00')
    return raw_image

def print_stats(kernel_header, mm_header, fs_header, init_header, fsck_header, minix_image_size, total_size):
    assert (
        minix_image_size == kernel_header.total_size() + mm_header.total_size()
            + fs_header.total_size() + init_header.total_size()
    )

    kernel_header.print_sizes("kernel")
    mm_header.print_sizes("mm")
    fs_header.print_sizes("fs")
    init_header.print_sizes("init")
    print(" "*47 + "-"*5 + " "*6 + "-"*5)
    print("Operating system size  {:>29}      {:>5X}".format(minix_image_size, minix_image_size))
    print(f"\nTotal size including fsck is {total_size}.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Build a MINIX boot disk")
    parser.add_argument("bootblok", type=str)
    parser.add_argument("kernel", type=str)
    parser.add_argument("mm", type=str)
    parser.add_argument("fs", type=str)
    parser.add_argument("init", type=str)
    parser.add_argument("fsck", type=str)
    parser.add_argument("out_file", type=str)
    args = parser.parse_args()

    with (
        open(args.bootblok, 'rb') as bootblok,
        open(args.kernel,'rb') as kernel,
        open(args.mm, 'rb') as mm,
        open(args.fs,'rb') as fs,
        open(args.init, 'rb') as init,
        open(args.fsck,'rb') as fsck,
    ):
        image = build_360k_floppy_image(
            bootblok=bytearray(bootblok.read()),
            kernel=bytearray(kernel.read()),
            mm=bytearray(mm.read()),
            fs=bytearray(fs.read()),
            init=bytearray(init.read()),
            fsck=bytearray(fsck.read()),
        )

    with open(args.out_file, 'wb') as out:
        out.write(image)
