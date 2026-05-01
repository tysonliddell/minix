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
ALIGN = 16
CLICK_SHIFT = 4
DS_OFFSET = 4           # position of DS written in kernel text seg

@dataclass
class HeaderInfo:
    text_size: int
    data_size: int
    bss_size: int
    entry_point: int
    total_mem_alloc: int
    symbols_size: int
    is_sep: bool

    def total_mem(self):
        return self.text_size + self.data_size + self.bss_size

    def i_d_bss_len(self):
        if self.is_sep:
            return self.text_size, self.data_size + self.bss_size
        else:
            return 0, self.text_size + self.data_size + self.bss_size

    @classmethod
    def from_bytes(cls, bytes_):
        magic = int.from_bytes(bytes_[0:4], "little")
        if magic == EXEC_MAGIC:
            is_sep = False
        elif magic == SEP_MAGIC:
            is_sep = True
        else:
            raise ValueError(f"Bad exec magic {magic:#x}")

        assert HEADER_LEN == bytes_[4], "Bad header length field"

        hdr = cls(
            text_size=int.from_bytes(bytes_[8:12], "little"),
            data_size=int.from_bytes(bytes_[12:16], "little"),
            bss_size=int.from_bytes(bytes_[16:20], "little"),
            entry_point=int.from_bytes(bytes_[20:24], "little"),
            total_mem_alloc=int.from_bytes(bytes_[24:28], "little"),
            symbols_size=int.from_bytes(bytes_[28:32], "little"),
            is_sep=is_sep,
        )

        if is_sep:
            assert hdr.text_size % ALIGN == 0, f"Bad text size {hdr.text_size}"

        print("text={}  data={}  bss={}  tot={}  hex={}  {}\n".format(
            hdr.text_size, hdr.data_size, hdr.bss_size, hdr.total_mem(),
            hdr.total_mem(), ("Separate I & D" if hdr.is_sep else "")
        ))

        return hdr

def strip_and_pad(exec_bytes):
    header = HeaderInfo.from_bytes(exec_bytes[:HEADER_LEN])
    program = exec_bytes[HEADER_LEN:] + b'\x00'*header.bss_size
    padding = (-len(program)) % ALIGN
    header.bss_size += padding
    return header, exec_bytes[HEADER_LEN:] + b'\x00' * padding

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
    bootblok_padded[504:506] = num_sectors.to_bytes(2, "little")
    bootblok_padded[506:508] = (ds_fsck >> CLICK_SHIFT).to_bytes(2, "little")
    bootblok_padded[508:510] = pc_fsck.to_bytes(2, "little")
    bootblok_padded[510:512] = (cs_fsck >> CLICK_SHIFT).to_bytes(2, "little")

    # check magic
    assert (
        KERNEL_D_MAGIC == int.from_bytes(kernel_padded[kernel_header.text_size:][:2], "little")
    ), "Bad kernel data magic"
    assert (
        FS_MM_D_MAGIC == int.from_bytes(fs_padded[fs_header.text_size:][:2], "little")
    ), "Bad fs data magic"
    assert (
        FS_MM_D_MAGIC == int.from_bytes(mm_padded[mm_header.text_size:][:2], "little")
    ), "Bad mm data magic"

    # patch kernel
    pos = kernel_header.text_size   # start of data section
    for prog_hdr in [kernel_header, mm_header, fs_header, init_header]:
        text_size, data_size = prog_hdr.i_d_bss_len()
        kernel_padded[pos:][:2] = (text_size >> CLICK_SHIFT).to_bytes(2, "little")
        kernel_padded[pos+2:][:2] = (data_size >> CLICK_SHIFT).to_bytes(2, "little")
        pos += 2

    kernel_ds = PROG_ORG
    if kernel_header.is_sep:
        kernel_ds += kernel_header.text_size
    kernel_padded[DS_OFFSET:][:2] = (kernel_ds >> CLICK_SHIFT).to_bytes(2, "little")

    # patch fs
    init_org = PROG_ORG + minix_size - len(init_padded)
    init_text_size, init_data_size = init_header.i_d_bss_len()
    fs_padded[4:6] = (init_org >> CLICK_SHIFT).to_bytes(2, "little")
    fs_padded[6:8] = (init_text_size >> CLICK_SHIFT).to_bytes(2, "little")
    fs_padded[8:10] = (init_data_size >> CLICK_SHIFT).to_bytes(2, "little")

    # create boot image
    raw_image = bytearray()
    raw_image.extend(bootblok_padded)
    raw_image.extend(kernel_padded)
    raw_image.extend(mm_padded)
    raw_image.extend(fs_padded)
    raw_image.extend(init_padded)
    raw_image.extend(fsck_padded)

    assert (
        len(raw_image) <= FLOPPY_360K_SIZE
    ), "Not enough space on 360K floppy for boot image"

    raw_image = raw_image.ljust(FLOPPY_360K_SIZE, b'\x00')
    return raw_image

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

    # TODO: write image back to file
    with open(args.out_file, 'wb') as out:
        pass
