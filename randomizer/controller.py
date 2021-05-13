""" Check box controllers """

import logging
import os
import uuid

from PyQt5.QtWidgets import QMessageBox
import yaml

from rom_editors.character_editor import CharacterEditor
from rom_editors.item_editor import make_all_master_seals
from rom_editors.stat_editor import StatRandomizer, StatModifier, InvalidConfigError
from config import CONFIG, FE8_CONFIG_PATH

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


def randomizer_handler(app):
    """ Begin the randomization process """

    input_rom = app.line_edits["rom_edit"].text()
    try:
        with open(input_rom, "rb") as stream:
            rom_data = bytearray(stream.read())

        with open(FE8_CONFIG_PATH) as stream:
            fe8_config = yaml.safe_load(stream)

    except IOError as error:
        app.labels["status"].setText(f"Status: Error! {error}")
        return

    rom_data = _randomize_characters(fe8_config, rom_data)

    if CONFIG["randomize"]["classes"]["all_master_seals"]["enabled"]:
        rom_data = make_all_master_seals(fe8_config, rom_data)

    try:
        rom_data = _randomize_stats(fe8_config, rom_data)
    except InvalidConfigError:
        msg_box = QMessageBox()
        msg_box.setText(
            "You cannot have a randomize range where the maximum is greater than minimum"
        )
        msg_box.setWindowTitle("Error: Invalid Configuration")
        msg_box.setIcon(QMessageBox.Warning)
        app.labels["status"].setText("Error: Invalid Configuration")

        msg_box.exec_()
        return

    rom_data = _modify_stats(fe8_config, rom_data)

    path, ext = os.path.splitext(input_rom)
    rand = str(uuid.uuid4()).split("-")[0]
    output_rom = f"{path}-{rand}{ext}"

    with open(output_rom, "wb") as stream:
        stream.write(rom_data)

    app.labels["status"].setText(f"Status: Successfully wrote {output_rom}")


def _randomize_characters(fe8_config, rom_data):
    """ Randomize the characters """

    filters = _get_filters(CONFIG["randomize"]["classes"], CHARACTER_KINDS)

    class_mode = CONFIG["randomize"]["classes"]["mode"]
    mix_promotes = CONFIG["randomize"]["mix_promotes"]["enabled"]

    char_editor = CharacterEditor(fe8_config, rom_data, class_mode, mix_promotes)
    char_editor.set_filters(filters)
    return char_editor.randomize()


def _randomize_stats(fe8_config, rom_data):
    """ Randomize bases and growths """

    base_filters = _get_filters(CONFIG["randomize"]["stats"]["bases"], ALL_KINDS)
    growth_filters = _get_filters(
        CONFIG["randomize"]["stats"]["growths"], CHARACTER_KINDS
    )

    stat_randomizer = StatRandomizer(fe8_config, rom_data)
    stat_randomizer.set_filters(base_filters, growth_filters)
    return stat_randomizer.randomize()


def _modify_stats(fe8_config, rom_data):
    """ Modify bases and growths """
    base_filters = _get_filters(CONFIG["modify"]["stats"]["bases"], CHARACTER_KINDS)
    growth_filters = _get_filters(CONFIG["modify"]["stats"]["growths"], CHARACTER_KINDS)

    stat_modifier = StatModifier(fe8_config, rom_data)
    stat_modifier.set_filters(base_filters, growth_filters)
    return stat_modifier.modify()


def _get_filters(config, kinds):
    """ Look up filters based on config path """
    return [kind for kind in kinds if not config[kind]["enabled"]]
