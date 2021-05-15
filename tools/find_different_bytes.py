#!/usr/bin/env python3

""" Tool to find differences between 2 ROMs """

import sys
import json

USAGE = """
Use this tool to find differences between ROMS.
Usage:

python3 find_different_bytes.py <ROM1> <ROM2>

"""


def _main(rom_1, rom_2):
    print("Reading Roms")
    with open(rom_1, "rb") as stream:
        rom_1_data = bytearray(stream.read())

    with open(rom_2, "rb") as stream:
        rom_2_data = bytearray(stream.read())

    print("Locating Differences")
    different_bytes = {}
    length = len(rom_1_data) or len(rom_2_data)
    for idx in range(length):
        if rom_1_data[idx] != rom_2_data[idx]:
            different_bytes[str(hex(idx))] = {
                "rom1": hex(rom_1_data[idx]),
                "rom2": hex(rom_2_data[idx]),
            }

    print(f"Differences:\n{json.dumps(different_bytes, indent=2)}")
    print(f"Total number of differences: {len(different_bytes)}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(USAGE)
        sys.exit(0)

    _main(sys.argv[1], sys.argv[2])
