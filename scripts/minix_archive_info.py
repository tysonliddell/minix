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
    hdr_raw = f.read(HEADER_SIZE)
    if hdr_raw == b'':
        return None
    else:
        return Header(
            name=bytes.decode(hdr_raw[0:14], encoding="ascii").rstrip("\0"),
            time=int.from_bytes(to_nbo(hdr_raw[14:18]), byteorder="big"),
            uid=hdr_raw[18],
            gid=hdr_raw[19],
            mode=int.from_bytes(to_nbo(hdr_raw[20:22]), byteorder="big"),
            size=int.from_bytes(to_nbo(hdr_raw[22:26]), byteorder="big"),
        ), hdr_raw

def parse_file(f):
    magic = int.from_bytes(f.read(MAGIC_SIZE), byteorder="little")
    assert magic == MAGIC
    while(True):
        result = parse_header(f)
        if result is None:
            break

        hdr,_ = result
        print(f"Object {hdr.name} of size {hdr.size} found")
        aligned_size = hdr.size + int(hdr.size & 1) # align to even address
        _object_bytes = f.read(aligned_size)

def move(f, member_name, anchor_name):
    magic = int.from_bytes(f.read(MAGIC_SIZE), byteorder="little")
    assert magic == MAGIC
    members = []
    while(True):
        result = parse_header(f)
        if result is None:
            break

        hdr,hdr_raw = result
        aligned_size = hdr.size + int(hdr.size & 1) # align to even address
        object_bytes = f.read(aligned_size)
        members.append((hdr, hdr_raw, object_bytes))

    member_idx, anchor_idx = None, None
    for i,(hdr,_,_) in enumerate(members):
        if hdr.name == member_name:
            member_idx = i
        elif hdr.name == anchor_name:
            anchor_idx = i

    if member_idx is None or anchor_idx is None:
        print("Error finding members")
        exit(1)

    member = members.pop(member_idx)
    members.insert(anchor_idx, member)

    f.seek(MAGIC_SIZE)
    for (_, hdr_raw, obj) in members:
        f.write(hdr_raw)
        f.write(obj)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file',
        type=str,
        help='MINIX archive file to be read',
    )
    parser.add_argument(
        '-m',
        '--move',
        nargs=2,
        metavar=('X','Y'),
        type=str,
        help='Move member X before member Y. Does not handle duplicate members!',
    )
    args = parser.parse_args()

    if args.move:
        member,anchor_member = args.move
        with open(args.file, 'r+b') as f:
            move(f, member, anchor_member)
    else:
        with open(args.file, 'rb') as f:
            parse_file(f)
