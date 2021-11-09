""" FE8 Override Class for editing characters """

from random import randint

from rom_editors.character_editor import CharacterEditor
from rom_editors.fe8.item_editor import FE8ItemEditor


class FE8CharacterEditor(CharacterEditor):
    """ FE8 Character Editor Override """

    def __init__(self, game_config, rom_data, class_mode, mix_promotes):
        super().__init__(game_config, rom_data, class_mode, mix_promotes)
        # Override the item editor
        self._item_editor = FE8ItemEditor(self._rom_data, self._game_config)

    def randomize_palettes(self):
        """ Randomize the character palettes based on filters """
        # Need to override the method because FE8 treats palettes differently
        characters = self._game_config["classes"]["characters"]
        palette_stats = self._game_config["classes"]["palette_stats"]
        prom_stats = self._game_config["classes"]["promotion_stats"]
        for character in characters:
            if characters[character]["kind"] not in self._filters:
                for _id in characters[character]["id"]:
                    # Randomize all palettes
                    pos = palette_stats["first_palette"] + (
                        palette_stats["total_bytes"] * _id
                    )
                    for idx in range(palette_stats["total_bytes"]):
                        rand = randint(0, palette_stats["num_palettes"])
                        self._rom_data[pos + idx] = rand

                    # Set palette classes to newly randomized classes
                    # Use both promotion 1 and promotion 2. If unit does not promote,
                    # Both values also get set to 0

                    # Use the first character location to get the new class
                    new_class = self._rom_data[characters[character]["location"][0]]

                    # Set base class first
                    pos = (
                        palette_stats["first_class"]
                        + (palette_stats["total_bytes"] * _id)
                        + palette_stats["base_class_offset"]
                    )
                    self._rom_data[pos] = new_class

                    # Set the 2 promotion classes
                    pos = (
                        palette_stats["first_class"]
                        + (palette_stats["total_bytes"] * _id)
                        + palette_stats["promoted_class_offset"]
                    )
                    new_prom_class = prom_stats["first"] + (
                        prom_stats["total_bytes"] * new_class
                    )
                    for idx in range(palette_stats["num_promoted_classes"]):
                        self._rom_data[pos + idx] = self._rom_data[new_prom_class + idx]
