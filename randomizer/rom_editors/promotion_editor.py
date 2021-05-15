""" Module for editing promotions and promotional items """


def _set_item_information(game_config, rom_data):
    """ Change the appearance of all promotion items to master seals """
    offsets = game_config["items"]["offsets"]
    prom_config = game_config["items"]["promotional"]
    for prom_item in prom_config["items"]:
        location = prom_config["items"][prom_item]["item_location"]
        for category in {"name", "description", "use_screen"}:
            for idx in range(len(game_config["items"]["master_seal"][category])):
                rom_data[location + offsets[category] + idx] = game_config["items"][
                    "master_seal"
                ][category][idx]

        for category in {"icon", "use"}:
            rom_data[location + offsets[category]] = game_config["items"][
                "master_seal"
            ][category]

    return rom_data


def _parse_pointer(pointer):
    """ Return the 3 bytes that make up the pointer in reversed order (little endian) """
    str_repr = str(hex(pointer)).split("x")[1]
    assert (
        len(str_repr) == 6
    ), f"New location should only be 3 bytes. Was actually {str_repr}"

    return int(str_repr[-2:], 16), int(str_repr[2:4], 16), int(str_repr[:2], 16)


def _add_classes_to_promotion(game_config, rom_data):
    """ Add all unpromoted classes to all promotion items """
    prom_items = game_config["items"]["promotional"]["items"]
    classes_to_add = game_config["items"]["promotional"]["classes_to_add"]
    for item in prom_items:
        new_loc = prom_items[item]["new_location"]
        # Set the pointers to the new location
        for pointer in prom_items[item]["pointers"]:
            loc_bytes = _parse_pointer(new_loc)

            for idx, _ in enumerate(loc_bytes):
                rom_data[pointer + idx] = loc_bytes[idx]

        # Set classes in new location
        for idx, _ in enumerate(classes_to_add):
            rom_data[new_loc + idx] = classes_to_add[idx]

        # Write a zero at the ned to signal end of class list
        rom_data[new_loc + len(classes_to_add)] = 0

    return rom_data


def make_all_master_seals(game_config, rom_data):
    """ Change all promotion items to master seals """
    rom_data = _set_item_information(game_config, rom_data)
    rom_data = _add_classes_to_promotion(game_config, rom_data)

    return rom_data
