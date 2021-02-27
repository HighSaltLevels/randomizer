""" Config handler """
import os
import logging
from pathlib import Path

import yaml

from constants import DEFAULT_CONFIG

DEFAULT_CONFIG_PATH = os.path.join(str(Path.home()), ".config/randomizer")
os.makedirs(DEFAULT_CONFIG_PATH, exist_ok=True)


class Config(dict):
    """ Yaml configuration handler """

    def __init__(self, path):
        super().__init__()

        self._path = path
        self._config = None

        if os.path.isfile(path):
            try:
                self._config = yaml.safe_load(path)

            except Exception as error:
                err = (
                    "Got permission denied loading configuration file!"
                    if isinstance(error, PermissionError)
                    else "Unexpected error occured loading configuration file!"
                )
                logging.critical(err)
                logging.info("Try re-installing to resolve this error.")
                raise

        else:
            logging.warning("Configuration file not found! Using defaults.")
            self.set_default()

        self.update(self._config)

    def write(self):
        """ Write the config back to disk """
        with open(self._path, "w") as stream:
            stream.write(yaml.dump(self._config))

    def set_default(self):
        """ Load default values into the config """
        self._config = DEFAULT_CONFIG
