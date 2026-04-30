import argparse
from dataclasses import dataclass

MAGIC = 0o177545
MAGIC_SIZE = 2
HEADER_SIZE = 26

@dataclass
class Header:
    name: str
    time: int
    uid: int
    gid: int
    mode: int
    size: int

# convert a sequence of 16-bit, little endian words to network byte order
def to_nbo(bytes_):
    assert len(bytes_) % 2 == 0
    result_bytes = []

    i = 0
    while (i < len(bytes_)):
        result_bytes.append(bytes_[i+1])
        result_bytes.append(bytes_[i])
        i += 2

    return bytes(result_bytes)
    
def parse_header(f):
    hdr = f.read(HEADER_SIZE)
    if hdr == b'':
        return None
    else:
        return Header(
            name=bytes.decode(hdr[0:14], encoding="ascii"),
            time=int.from_bytes(to_nbo(hdr[14:18]), byteorder="big"),
            uid=hdr[18],
            gid=hdr[19],
            mode=int.from_bytes(to_nbo(hdr[20:22]), byteorder="big"),
            size=int.from_bytes(to_nbo(hdr[22:26]), byteorder="big"),
        )

def parse_file(f):
    magic = int.from_bytes(f.read(MAGIC_SIZE), byteorder="little")
    assert magic == MAGIC
    while(hdr := parse_header(f)):
        print(f"Object {hdr.name} of size {hdr.size} found")
        aligned_size = hdr.size + int(hdr.size & 1) # align to even address
        _object_bytes = f.read(aligned_size)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file',
        type=str,
        help='MINIX archive file to be read',
    )
    args = parser.parse_args()

    with open(args.file, 'rb') as f:
        parse_file(f)
