""" Stat Editor Module """

from random import randint

from config import CONFIG


class StatRandomizer:
    """ Stat randomizer """

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

    def randomize(self):
        """ Randomize bases and growths """
        for stat_type in {"bases", "growths"}:
            self._randomize_character_stats(stat_type)

        if "class" not in self._filters["bases"]:
            self._randomize_class_stats()

        return self._rom_data

    def _randomize_character_stats(self, stat_type):
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
                        rand = randint(min_, max_)
                        self._rom_data[first_stat + stat_offset] = rand

    def _randomize_class_stats(self):
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
