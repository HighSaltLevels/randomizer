"""
DO NOT EDIT THIS FILE!!!!

This is an auto-generated file for bundling the Fire
Emblem configs into memory instead of on disk.

Instead, please run "./tools/generate_specs.py"
to create a configuration file
"""

# pylint: disable=too-many-lines,too-few-public-methods,line-too-long
import json


class AbstractSpecObj:
    """Object representation of each dict"""

    def __init__(self, _dict):
        self.__dict__.update(_dict)


class Spec:
    """Spec enumeration"""

    FE6 = json.loads(json.dumps(FE6PLACEHOLDER), object_hook=AbstractSpecObj)
    FE7 = json.loads(json.dumps(FE7PLACEHOLDER), object_hook=AbstractSpecObj)
    FE8 = json.loads(json.dumps(FE8PLACEHOLDER), object_hook=AbstractSpecObj)
