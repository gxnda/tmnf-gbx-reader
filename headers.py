import struct

def __read_user_data_chunks(fb, header_entries, read_heavy_chunks=True):
    """
    Returns a list of tuples containing the chunk ID and the chunk data.
    :param fb:
    :param header_entries:
    :param read_heavy_chunks:
    :return:
    """
    chunk_data: list[tuple[int, bytes]] = []
    for chunk_id, chunk_size, heavy_chunk in header_entries:
        if heavy_chunk:
            if read_heavy_chunks:
                print("Reading heavy chunk: ", chunk_id)
                chunk = fb.read(chunk_size)
                chunk_data.append((chunk_id, chunk))
            else:
                print("Skipping heavy chunk: ", chunk_id)
                fb.seek(chunk_size, 1)  # 1 = SEEK_CUR (current position)
        else:
            print("Reading light chunk: ", chunk_id)
            chunk = fb.read(chunk_size)
            chunk_data.append((chunk_id, chunk))

    return chunk_data


def read_user_data(fb, size):
    num_header_chunks = struct.unpack("<I", fb.read(4))[0]
    header_entries = []
    for _ in range(num_header_chunks):
        chunk_id = struct.unpack("<I", fb.read(4))[0]
        chunk_size = struct.unpack("<I", fb.read(4))[0]
        heavy_chunk = chunk_size & 0x80000000 != 0
        header_entries.append((chunk_id, chunk_size & 0x7FFFFFFF, heavy_chunk))

    return __read_user_data_chunks(fb, header_entries, read_heavy_chunks=True)


def read_header(fb):
    headers = {}

    # Makes sure the file is a GBX file
    magic: tuple[bytes, ...] = struct.unpack(">3s", fb.read(3))[0]
    if magic != b"GBX":
        raise ValueError("Invalid GBX file")

    # Checks uint16 version
    version: int = struct.unpack("<h", fb.read(2))[0]
    headers["version"] = version
    print(version)
    if version != 6:
        raise ValueError(f"Invalid GBX version, expected "
                         f"6, got {version}.")

    fb.seek(1, 1)  # 1 = SEEK_CUR (current position)

    headers["is_ref_table_compressed"]: bool = struct.unpack(
        "<c", fb.read(1))[0] == b"C"
    headers["is_body_compressed"]: bool = struct.unpack(
        "<c", fb.read(1))[0] == b"C"

    # Next byte is unknown
    fb.seek(1, 1)  # 1 = SEEK_CUR (current position)

    # Class ID of main class instance
    headers["uint32_class_id"]: int = struct.unpack(
        "<I", fb.read(4))[0]

    headers["user_data_size"]: int = struct.unpack(
        "<I", fb.read(4))[0]  # uint32

    user_data = read_user_data(fb, headers["user_data_size"])

    headers["num_nodes"]: int = struct.unpack(
        "<I", fb.read(4))[0]  # uint32

    return headers, user_data
