""" Main entrypoint """

import logging

from app import Randomizer
from config import DEFAULT_CONFIG_PATH

LOG_LEVEL = logging.INFO
LOG_PATH = f"{DEFAULT_CONFIG_PATH}/randomizer.log"

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=LOG_LEVEL, handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()]
)


def _main():
    randomizer = Randomizer()
    try:
        randomizer.start()

    except Exception as error:
        LOGGER.error("Something crashed :(")
        LOGGER.info("You can check the logs at %s", LOG_PATH)
        LOGGER.exception(error)
        raise


if __name__ == "__main__":
    _main()
