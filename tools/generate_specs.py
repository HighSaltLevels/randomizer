#!/usr/bin/env python3
"""
Tool for converting the Fire Emblem yaml configs to
consumable python source to be bundled in the final
binary.
"""
import os
import json
import yaml


def read_file(file_):
    """ Read a file and return its contents """
    print(f"Reading {file_}...")
    if not os.path.isfile(file_):
        raise RuntimeError(
            f'Could not locate "{_file}" please run this tool from the base '
            "project directory."
        )

    with open(file_) as reader:
        return reader.read()

def write_file(file_, contents):
    """ Write {contents} to the {file_} """
    print(f"Writing {file_}...")
    with open(file_, "w") as writer:
        writer.write(contents)

def run_black():
    """ Run the black formatter to clean it up """
    # Doesn't matter if it fails or not
    print("Attempting to run the black formatter")
    os.system("black randomizer/spec.py")

def _main():
    """ Convert the yaml to consumable python """
    template = read_file("tools/spec.template.py")
    for version in {"FE6", "FE7", "FE8"}:
        config = yaml.safe_load(read_file(f"config/{version}.yml"))
        template = template.replace(f"{version}PLACEHOLDER", json.dumps(config))

    write_file("randomizer/spec.py", template)
    run_black()

if __name__ == "__main__":
    _main()
