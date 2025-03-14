import numpy as np
import sys


def read(file):
    with open(file, "rb") as f:
        magic = f.read(4)
        if magic not in [b"STAN", b"NATS"]:
            raise ValueError(f"Invalid magic bytes {magic}, expected STAN")

        little_endian = magic == b"STAN"

        header_size = (
            int.from_bytes(f.read(8), "little" if little_endian else "big")
            - 1  # null terminator
        )
        header = f.read(header_size).decode("utf-8")
        header_row = header.split(",")
        columns = len(header_row)

        # next multiple of 8
        start = (12 + header_size + 7) & ~7
        f.seek(start)
        buf = f.read()

    if len(buf) % 8 != 0:
        raise ValueError("Invalid file size")
    rows = len(buf) // (columns * 8)

    data = np.ndarray(
        shape=(rows, columns), dtype="<f8" if little_endian else ">f8", buffer=buf
    )

    return (header_row, data)


if __name__ == "__main__":
    header, data = read(sys.argv[1])
    print(header)
    print(data)
    print(data.mean(axis=0))
