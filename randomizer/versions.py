""" Helper module for determining versions of roms """
from constants import FEVersions

VERSION_LOCATION = 0xAE
LOCATION_VERSION_MAP = {
    0x45: FEVersions.FE6,
    0x37: FEVersions.FE7,
    0x38: FEVersions.FE8,
}


def get_fe_version(rom_data):
    """Attempt to determine Fire Emblem Version"""
    try:
        return LOCATION_VERSION_MAP[rom_data[VERSION_LOCATION]]
    except KeyError:
        return FEVersions.UNKNOWN
