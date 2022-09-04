""" Base Stat Editor Module """

from random import randint

from config import CONFIG


class InvalidConfigError(Exception):
    """raised when configuration values are invalid"""


class StatRandomizer:
    """Base Stat Randomizer"""

    def __init__(self, game_config, rom_data):
        self._game_config = game_config
        self._rom_data = rom_data

        self._filters = None

    def set_filters(self, base_filters, growth_filters):
        """Randomize bases and growths"""
        self._filters = {
            "bases": base_filters,
            "growths": growth_filters,
        }

    @property
    def rom_data(self):
        """Make rom_data read only. Should only modify things one at a time"""
        return self._rom_data

    def randomize(self):
        """Randomize the stats"""
        self.randomize_character_stats()

        if "class" not in self._filters["bases"]:
            self.randomize_class_stats()

        return self._rom_data

    def randomize_character_stats(self):
        """Randomize character stats that are not filtered out"""
        for character in self._game_config.characters:
            for stat_type in {"bases", "growths"}:
                if character.kind not in self._filters[stat_type]:
                    if stat_type == "bases":
                        self._randomize_character_stat(
                            character,
                            CONFIG["randomize"]["stats"]["bases"][character.kind][
                                "minimum"
                            ],
                            CONFIG["randomize"]["stats"]["bases"][character.kind][
                                "maximum"
                            ],
                            self._game_config.char_stats.totals.bases,
                            self._game_config.char_stats.offsets.bases,
                        )
                    else:
                        self._randomize_character_stat(
                            character,
                            CONFIG["randomize"]["stats"]["growths"][character.kind][
                                "minimum"
                            ],
                            CONFIG["randomize"]["stats"]["growths"][character.kind][
                                "maximum"
                            ],
                            self._game_config.char_stats.totals.growths,
                            self._game_config.char_stats.offsets.growths,
                        )

    # pylint: disable=too-many-arguments
    def _randomize_character_stat(self, character, min_, max_, num_stats, offset):
        """Write a random number between {min_} and {max} to the character stats"""
        for _id in character.id:
            first_stat = (
                self._game_config.char_stats.first
                + (_id * self._game_config.sizes.character)
                + offset
            )
            for idx in range(num_stats):
                self._rom_data[first_stat + idx] = get_rand(min_, max_)

    def randomize_class_stats(self):
        """Use CONFIG values to randomize bases of classes"""
        min_ = CONFIG["randomize"]["stats"]["bases"]["class"]["minimum"]
        max_ = CONFIG["randomize"]["stats"]["bases"]["class"]["maximum"]
        for class_idx in range(self._game_config.totals.class_):
            first_stat = (
                self._game_config.class_stats.first
                + (class_idx * self._game_config.sizes.class_)
                + self._game_config.class_stats.offsets.bases
            )
            for idx in range(self._game_config.class_stats.totals.bases):
                self._rom_data[first_stat + idx] = get_rand(min_, max_)


class StatModifier:
    """Base Stat Modifier"""

    def __init__(self, game_config, rom_data):
        self._game_config = game_config
        self._rom_data = rom_data

        self._filters = None

    def set_filters(self, base_filters, growth_filters):
        """Modify bases and growths"""
        self._filters = {
            "bases": base_filters,
            "growths": growth_filters,
        }

    @property
    def rom_data(self):
        """Make rom_data read only. Should only modify things one at a time"""
        return self._rom_data

    def modify(self):
        """Modify bases and growths"""
        for character in self._game_config.characters:
            for stat_type in {"bases", "growths"}:
                if character.kind not in self._filters[stat_type]:
                    self._modify_character_stat(character, stat_type)

        return self._rom_data

    def _modify_character_stat(self, character, stat_type):
        """Use CONFIG values to modify the character"""
        num_stats = (
            self._game_config.char_stats.totals.bases
            if stat_type == "bases"
            else self._game_config.char_stats.totals.growths
        )
        offset = (
            self._game_config.char_stats.offsets.bases
            if stat_type == "bases"
            else self._game_config.char_stats.offsets.growths
        )
        for char_id in character.id:
            first_stat = (
                self._game_config.char_stats.first
                + (char_id * self._game_config.sizes.character)
                + offset
            )
            for idx in range(num_stats):
                stat = (
                    self._rom_data[first_stat + idx]
                    + CONFIG["modify"]["stats"][stat_type][character.kind]["modifier"]
                )
                # Floor at 0 and ceiling at 255
                stat = 0 if stat < 0 else stat
                stat = 255 if stat > 255 else stat

                self._rom_data[first_stat + idx] = stat


def get_rand(minimum, maximum):
    """Generate a random number between {minimum} and {maximum}"""
    try:
        return randint(minimum, maximum)
    except ValueError:
        raise InvalidConfigError from ValueError
