""" Various quick dialog windows """

from PyQt5.QtWidgets import QDialog, QGridLayout, QPushButton, QComboBox, QLabel
from PyQt5.QtGui import QIcon

from versions import FEVersions
from config import DEFAULT_CONFIG_PATH, CONFIG


class VersionPrompt(QDialog):
    """ Version prompt dialog """

    PROMPT = (
        "Warning: Unknown Fire Emblem Version detected!\nYou can try to randomize using the "
        "settings from\nthe games listed below instead:"
    )

    def __init__(self, parent=None, title="Unsupported Version"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(f"{DEFAULT_CONFIG_PATH}/randomizer.ico"))

        self.combox_box = None

        self.build_ui()

    def build_ui(self):
        """ Build the GUI """
        label = QLabel(self.PROMPT, self)

        self.combo_box = QComboBox(self)
        for version in FEVersions:
            if version != FEVersions.UNKNOWN:
                self.combo_box.addItem(version)

        button = QPushButton("OK", self)
        button.clicked.connect(self.set_version)

        grid = QGridLayout()
        grid.addWidget(label, 0, 0)
        grid.addWidget(self.combo_box, 1, 0)
        grid.addWidget(button, 2, 0)

        self.setLayout(grid)
        self.show()

    def set_version(self):
        """ Set the version in the config to use for later """
        CONFIG["fe_version"] = self.combo_box.currentText()
        self.close()
