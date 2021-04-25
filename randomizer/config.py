""" Config handler """
import os
import logging
from pathlib import Path

import yaml

from constants import DEFAULT_CONFIG

DEFAULT_CONFIG_PATH = os.path.join(str(Path.home()), ".config/randomizer")
FE8_CONFIG_PATH = os.path.join(str(Path.home()), ".config/randomizer/FE8.yml")

os.makedirs(DEFAULT_CONFIG_PATH, exist_ok=True)


class ConfigError(Exception):
    """ Raised when there is an unexpected error during config operations """


class Config(dict):
    """ Yaml configuration handler """

    def __init__(self, path):
        super().__init__()

        self._path = path

        if os.path.isfile(path):
            try:
                with open(path) as stream:
                    self.update(yaml.safe_load(stream))

            except Exception as error:
                err = (
                    "Got permission denied loading configuration file!"
                    if isinstance(error, PermissionError)
                    else "Unexpected error occured loading configuration file!"
                )
                logging.critical(err)
                raise ConfigError("Try re-installing to resolve this error.") from error

        else:
            logging.warning("Configuration file not found! Using defaults.")
            self.set_default()

    def write(self):
        """ Write the config back to disk """
        with open(self._path, "w") as stream:
            stream.write(yaml.dump(dict(self)))

    def set_default(self):
        """ Load default values into the config """
        self.update(DEFAULT_CONFIG)

    def update_combo_box(self, selection):
        """ Update the config based on the combo box selection """
        self["randomize"]["classes"]["mode"] = selection

    def update_by_path(self, path, elements):
        """ Update the config based on UI elements and the path """
        if "randomize" in path:
            location = self["randomize"]["stats"]
            if "bases" in path:
                location = location["bases"]

            elif "growths" in path:
                location = location["growths"]

            else:
                location = self._get_other_location(path)
                location["enabled"] = elements["check_box"].isChecked()
                return

            location = self._get_location(path, curr_location=location)
            if elements.get("check_box"):
                location["enabled"] = elements["check_box"].isChecked()
            location["minimum"] = elements["spin_boxes"][0].value()
            location["maximum"] = elements["spin_boxes"][1].value()

        else:
            location = self["modify"]["stats"]
            if "bases" in path:
                location = location["bases"]

            else:
                location = location["growths"]

            location = self._get_location(path, curr_location=location)
            if elements.get("check_box"):
                location["enabled"] = elements["check_box"].isChecked()
            location["modifier"] = elements["spin_boxes"][0].value()

    @staticmethod
    def _get_location(path, curr_location):
        """ Get the location based on playable, boss, other, or class """
        if "playable" in path:
            return curr_location["playable"]

        if "boss" in path:
            return curr_location["boss"]

        if "other" in path:
            return curr_location["other"]

        return curr_location["class"]

    def _get_other_location(self, path):
        """ Get the location of other configs that are not bases or growths """
        for kind in ("playable", "boss", "other"):
            if kind in path:
                return self["randomize"]["classes"][kind]

        if "promotes" in path:
            return self["randomize"]["mix_promotes"]

        return self["randomize"]["classes"]["all_master_seals"]


CONFIG = Config(f"{DEFAULT_CONFIG_PATH}/spec.yml")
