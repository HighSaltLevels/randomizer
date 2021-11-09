""" Base Stat Editor Module """

from random import randint

from config import CONFIG


class InvalidConfigError(Exception):
    """ raised when configuration values are invalid """


class StatRandomizer:
    """ Base Stat Randomizer """

    def __init__(self, game_config, rom_data):
        self._game_config = game_config
        self._rom_data = rom_data
        self._character_stats = game_config["classes"]["character_stats"]
        self._class_stats = self._game_config["classes"]["class_stats"]

        self._filters = None

    def set_filters(self, base_filters, growth_filters):
        """ Randomize bases and growths"""
        self._filters = {
            "bases": base_filters,
            "growths": growth_filters,
        }

    @property
    def rom_data(self):
        """ Make rom_data read only. Should only modify things one at a time """
        return self._rom_data

    def randomize(self):
        """ Randomize the stats """
        for stat_type in {"bases", "growths"}:
            self.randomize_character_stats(stat_type)

        if "class" not in self._filters["bases"]:
            self.randomize_class_stats()

        return self._rom_data

    def randomize_class_stats(self):
        """ Use CONFIG values to randomize bases of classes """
        for class_idx in range(self._class_stats["num_classes"]):
            first_stat = (
                self._class_stats["first"]
                + (class_idx * self._class_stats["total_bytes"])
                + self._class_stats["bases_offset"]
            )
            min_ = CONFIG["randomize"]["stats"]["bases"]["class"]["minimum"]
            max_ = CONFIG["randomize"]["stats"]["bases"]["class"]["maximum"]
            for stat_offset in range(self._class_stats["num_bases"]):
                rand = randint(min_, max_)
                self._rom_data[first_stat + stat_offset] = rand

    def randomize_character_stats(self, stat_type):
        """ Use CONFIG values to randomize bases and growths """
        characters = self._game_config["classes"]["characters"]
        for character in characters:
            kind = characters[character]["kind"]
            if kind not in self._filters[stat_type]:
                for char_id in characters[character]["id"]:
                    first_stat = (
                        self._character_stats["first"]
                        + (char_id * self._character_stats["total_bytes"])
                        + self._character_stats[f"{stat_type}_offset"]
                    )
                    min_ = CONFIG["randomize"]["stats"][stat_type][kind]["minimum"]
                    max_ = CONFIG["randomize"]["stats"][stat_type][kind]["maximum"]
                    for stat_offset in range(self._character_stats[f"num_{stat_type}"]):
                        try:
                            rand = randint(min_, max_)
                        except ValueError:
                            raise InvalidConfigError from ValueError
                        self._rom_data[first_stat + stat_offset] = rand


class StatModifier:
    """ Base Stat Modifier """

    def __init__(self, game_config, rom_data):
        self._game_config = game_config
        self._rom_data = rom_data
        self._character_stats = game_config["classes"]["character_stats"]

        self._filters = None

    def set_filters(self, base_filters, growth_filters):
        """ Modify bases and growths"""
        self._filters = {
            "bases": base_filters,
            "growths": growth_filters,
        }

    @property
    def rom_data(self):
        """ Make rom_data read only. Should only modify things one at a time """
        return self._rom_data

    def modify(self):
        """ Modify bases and growths """
        for stat_type in {"bases", "growths"}:
            self.modify_character_stats(stat_type)

        return self._rom_data

    def modify_character_stats(self, stat_type):
        """ Use CONFIG values to modify bases and growths """
        characters = self._game_config["classes"]["characters"]
        for character in characters:
            self.modify_character_stat(stat_type, characters, character)

    def modify_character_stat(self, stat_type, characters, character):
        """ Use CONFIG values to modify the character """
        kind = characters[character]["kind"]
        if kind not in self._filters[stat_type]:
            for char_id in characters[character]["id"]:
                first_stat = (
                    self._character_stats["first"]
                    + (char_id * self._character_stats["total_bytes"])
                    + self._character_stats[f"{stat_type}_offset"]
                )
                for stat_offset in range(self._character_stats[f"num_{stat_type}"]):
                    stat = (
                        self._rom_data[first_stat + stat_offset]
                        + CONFIG["modify"]["stats"][stat_type][kind]["modifier"]
                    )
                    stat = 0 if stat < 0 else stat
                    stat = 255 if stat > 255 else stat

                    self._rom_data[first_stat + stat_offset] = stat
