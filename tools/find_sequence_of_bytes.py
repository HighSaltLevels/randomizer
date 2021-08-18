#!/usr/bin/env python3

""" Tool to find the location(s) of a sequence of bytes """

import sys

USAGE = """
Use this tool to find a sequence or many sequences of bytes and their locations.
Usage: python3 find_sequence_of_bytes.py <ROMPATH>

For Example: python3 find_sequence_of_bytes.py /path/to/rom.gba 24ac4b36

"""


def _parse_hex(hex_str):
    if len(hex_str) % 2:
        print("Hex array must be in groups of 2. Please include necessary zeros")
        sys.exit(0)

    return [int(hex_str[idx : idx + 2], 16) for idx in range(0, len(hex_str), 2)]


def _find(rom, search_bytes):
    positions = []

    print(f"Reading Rom {rom}")
    with open(rom, "rb") as stream:
        rom_data = bytearray(stream.read())

    print(f"Looking for {[hex(byte) for byte in search_bytes]}")
    for position, _ in enumerate(rom_data):
        for pos, _ in enumerate(search_bytes):
            if rom_data[position + pos] != search_bytes[pos]:
                break
        else:
            positions.append(hex(position))

    if positions:
        print(f"Found that array at {positions}")
    else:
        print("Could not find that array anywhere :(")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(USAGE)
        sys.exit(0)

    int_arr = _parse_hex(sys.argv[2])
    _find(sys.argv[1], int_arr)
