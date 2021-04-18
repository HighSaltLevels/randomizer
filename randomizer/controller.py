""" Check box controllers """

import logging
from config import CONFIG

LOGGER = logging.getLogger(__name__)


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


def browse_handler(file_browser, line_edit):
    """ Allow the user to browse for a ROM path """
    if file_browser.exec_():
        selected_path = file_browser.selectedFiles()[0]
        line_edit.setText(selected_path)
        CONFIG["rom_path"] = selected_path
        LOGGER.info("Saving Rom Path")
        CONFIG.write()
