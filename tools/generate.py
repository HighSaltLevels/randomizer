#!/usr/bin/env python3
"""
Tool for converting the Fire Emblem yaml configs to
consumable python source to be bundled in the final
binary.
"""
import os
import json
import sys
import yaml


def read_file(file_, mode):
    """Read a file and return its contents"""
    print(f"Reading {file_}...")
    if not os.path.isfile(file_):
        raise RuntimeError(
            f'Could not locate "{file_}" please run this tool from the base '
            "project directory."
        )

    with open(file_, mode) as reader:
        return reader.read()


def write_file(file_, contents):
    """Write {contents} to the {file_}"""
    print(f"Writing {file_}...")
    with open(file_, "w") as writer:
        writer.write(contents)


def run_black(name):
    """Run the black formatter to clean it up"""
    filepath = f"randomizer/{name}.py"

    # Doesn't matter if it fails or not
    print(f"Attempting to run the black formatter on {filepath}")
    os.system(f"black {filepath}")


def _main():
    """Convert the yaml to consumable python"""
    spec_template = read_file("tools/spec.template.py", "r")
    for version in {"FE6", "FE7", "FE8"}:
        config = yaml.safe_load(read_file(f"config/{version}.yml", "r"))
        spec_template = spec_template.replace(
            f"{version}PLACEHOLDER", json.dumps(config)
        )
    write_file("randomizer/spec.py", spec_template)

    save_data = read_file("config/FE7.sav", "rb")
    save_template = read_file("tools/save.template.py", "r").replace(
        "FE7DATAPLACEHOLDER", str(save_data)
    )
    write_file("randomizer/save.py", save_template)

    for name in {"spec", "save"}:
        try:
            if sys.argv[1] == "--no-black":
                print("Skipping black formatter")
                return
        except IndexError:
            pass

        run_black(name)


if __name__ == "__main__":
    _main()
