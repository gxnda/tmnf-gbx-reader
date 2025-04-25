import struct


def decompress_reference_table(fb):
    raise NotImplementedError("Not implemented yet")


def read_reference_table(fb, header_entries):
    if header_entries["is_ref_table_compressed"]:
        fb = decompress_reference_table(fb)

    reference_table = {}

    num_external_nodes = struct.unpack("<I", fb.read(4))[0]
    if num_external_nodes > 0:
        ancestor_level = struct.unpack("<I", fb.read(4))[0]
        num_sub_folders = struct.unpack("<I", fb.read(4))[0]
        for _ in range(num_sub_folders): # TODO: implement subfolders recursively
            sub_folder_name = struct.unpack("<I", fb.read(4))[0]
            num_sub_folders = struct.unpack("<I", fb.read(4))[0]
            for _ in range(num_sub_folders):
                sub_folder_name = struct.unpack("<I", fb.read(4))[0]
                print(sub_folder_name)

        # TODO: implement external nodes
        pass