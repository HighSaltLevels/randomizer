""" Check box controllers """

import logging
import os
import shutil
import uuid

from PyQt5.QtWidgets import QMessageBox
import yaml

import dialogs
from rom_editors import (
    create_character_editor,
    create_stat_randomizer,
    create_stat_modifier,
    create_prom_editor,
)
from rom_editors.stat_editor import InvalidConfigError
from versions import FEVersions, get_fe_version
from config import CONFIG, CONFIG_MAP

LOGGER = logging.getLogger(__name__)
ALL_KINDS = {"playable", "boss", "other", "class"}
CHARACTER_KINDS = {"playable", "boss", "other"}


def handler(path, elements, toggle=True):
    """ Toggle the state of the ui elements """
    for element in elements.get("spin_boxes", []):
        if toggle:
            element.setDisabled(element.isEnabled())

    CONFIG.update_by_path(path, elements)
    LOGGER.info("Saving configuration")
    CONFIG.write()


def combo_box_handler(selection):
    """ Set the state of the combo box in the config """
    CONFIG.update_combo_box(selection)
    LOGGER.info("Saving configuration")
    CONFIG.write()


def browse_handler(app):
    """ Allow the user to browse for a ROM path """
    if app.file_browser.exec_():
        selected_path = app.file_browser.selectedFiles()[0]
        app.line_edits["rom_edit"].setText(selected_path)
        CONFIG["rom_path"] = selected_path
        LOGGER.info("Saving Rom Path")
        CONFIG.write()


class RandomizerHandler:
    """ RandomizerHandler Class for keeping up with versioning """

    def __init__(self, app):
        self._rom_data = None
        self._game_config = None
        self._version = FEVersions.UNKNOWN
        self._app = app

    @property
    def rom_data(self):
        """ Only allow modifying of the ROM Data within this class """
        return self._rom_data

    def randomize(self):
        """ Load the rom, get the FE version, load the config based on version, edit the rom """

        # Load the rom and game config
        input_rom = self._app.line_edits["rom_edit"].text()
        try:
            with open(input_rom, "rb") as stream:
                self._rom_data = bytearray(stream.read())

            self._version = get_fe_version(self._rom_data)
            self._app.labels["status"].setText(f"{self._version} detected")

            # Prompt for a version if not correctly detected
            if self._version == FEVersions.UNKNOWN:
                dialogs.VersionPrompt(self._app).exec_()
                self._version = CONFIG["fe_version"]

            config_path = CONFIG.get_path(self._version)
            with open(config_path) as stream:
                self._game_config = yaml.safe_load(stream)

        except IOError as error:
            self._app.labels["status"].setText(f"Status: Error! {error}")
            return

        # Perform all requested randomization
        self._randomize_all()

        # Write out the final ROM giving it a piece of UUID
        path, ext = os.path.splitext(input_rom)
        rand = str(uuid.uuid4()).split("-")[0]
        output_rom = f"{path}-{rand}{ext}"
        with open(output_rom, "wb") as stream:
            stream.write(self._rom_data)

        # If this is FE7, include save data to bypass tutorial
        # and the several soft locking opportunities that come
        # with it.
        if self._version == FEVersions.FE7:
            output_sav = f"{path}-{rand}.sav"
            shutil.copy(CONFIG_MAP[self._version].replace(".yml", ".sav"), output_sav)

        self._app.labels["status"].setText(f"Status: Successfully wrote {output_rom}")

    def _randomize_all(self):
        """ Perform all requested randomizations """

        self._randomize_characters()

        if CONFIG["randomize"]["classes"]["all_master_seals"]["enabled"]:
            self._edit_promotions()

        try:
            self._randomize_stats()
        except InvalidConfigError:
            msg_box = QMessageBox()
            msg_box.setText(
                "You cannot have a randomize range where the maximum is greater than minimum"
            )
            msg_box.setWindowTitle("Error: Invalid Configuration")
            msg_box.setIcon(QMessageBox.Warning)
            self._app.labels["status"].setText("Error: Invalid Configuration")

            msg_box.exec_()
            return

        self._modify_stats()

    def _randomize_characters(self):
        """ Randomize the characters based on version """

        filters = _get_filters(CONFIG["randomize"]["classes"], CHARACTER_KINDS)

        class_mode = CONFIG["randomize"]["classes"]["mode"]
        mix_promotes = CONFIG["randomize"]["mix_promotes"]["enabled"]

        char_editor = create_character_editor(
            self._game_config,
            self._rom_data,
            class_mode,
            mix_promotes,
            self._version,
        )
        char_editor.set_filters(filters)
        char_editor.randomize()
        self._rom_data = char_editor.rom_data

    def _randomize_stats(self):
        """ Randomize bases and growths """

        base_filters = _get_filters(CONFIG["randomize"]["stats"]["bases"], ALL_KINDS)
        growth_filters = _get_filters(
            CONFIG["randomize"]["stats"]["growths"], CHARACTER_KINDS
        )

        stat_randomizer = create_stat_randomizer(
            self._game_config, self._rom_data, self._version
        )
        stat_randomizer.set_filters(base_filters, growth_filters)
        stat_randomizer.randomize()
        self._rom_data = stat_randomizer.rom_data

    def _modify_stats(self):
        """ Modify bases and growths """
        base_filters = _get_filters(CONFIG["modify"]["stats"]["bases"], CHARACTER_KINDS)
        growth_filters = _get_filters(
            CONFIG["modify"]["stats"]["growths"], CHARACTER_KINDS
        )

        stat_modifier = create_stat_modifier(
            self._game_config, self._rom_data, self._version
        )
        stat_modifier.set_filters(base_filters, growth_filters)
        stat_modifier.modify()
        self._rom_data = stat_modifier.rom_data

    def _edit_promotions(self):
        """ Make all promotion items master seals """
        prom_editor = create_prom_editor(
            self._game_config, self._rom_data, self._version
        )
        prom_editor.make_all_master_seals()
        prom_editor.add_classes_to_promotion()
        self._rom_data = prom_editor.rom_data


def _get_filters(config, kinds):
    """ Look up filters based on config path """
    return [kind for kind in kinds if not config[kind]["enabled"]]
