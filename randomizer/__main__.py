""" Main entrypoint """

import logging

from config import DEFAULT_CONFIG_PATH
from randomizer import Randomizer

LOG_PATH = f"{DEFAULT_CONFIG_PATH}/output.log"


def _main():
    logging.basicConfig(filename=LOG_PATH, level=logging.DEBUG)
    randomizer = Randomizer()
    try:
        randomizer.start()

    except Exception as error:
        logging.error("Something crashed :(")
        logging.info("You can check the logs at %s", LOG_PATH)
        logging.exception(error)
        raise


if __name__ == "__main__":
    _main()
