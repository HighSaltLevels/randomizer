""" Main entrypoint """

import logging

from app import Randomizer
from config import CONFIG_PATH

LOG_LEVEL = logging.INFO
LOG_PATH = f"{CONFIG_PATH}/randomizer.log"

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=LOG_LEVEL, handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()]
)


def _main():
    try:
        randomizer = Randomizer()
        randomizer.start()

    except Exception:
        LOGGER.error("Something crashed :(")
        LOGGER.info("You can try reinstalling the randomizer")
        LOGGER.info("Or you can check the logs at %s", LOG_PATH)
        raise


if __name__ == "__main__":
    _main()
