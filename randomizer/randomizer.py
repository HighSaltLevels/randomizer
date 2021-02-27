""" Module for loading the app UI """

import sys

from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon

from ui_elements import label, spinbox, check_box, combo_box
from ui_elements.separator import create_v_sep, create_h_sep
from config import Config, DEFAULT_CONFIG_PATH

APP = QApplication([])


class Randomizer(QWidget):
    """ Randomizer GUI """

    def __init__(self, parent=None, title="Randomizer"):
        super().__init__(parent)

        self.setWindowTitle(title)

        self.setWindowIcon(QIcon(f"{DEFAULT_CONFIG_PATH}/randomizer.ico"))

        self.labels = label.create_labels(self)
        self.check_boxes = check_box.create_check_boxes()
        self.spin_boxes = spinbox.create_spin_boxes(self)
        self.combo_boxes = combo_box.create_combo_boxes()

        randomize_button = QPushButton("Randomize!", self)

        top_left_grid = self.create_top_left_grid()
        top_right_grid = self.create_top_right_grid()
        bottom_left_grid = self.create_bottom_left_grid()
        bottom_right_grid = self.create_bottom_right_grid()

        top_grid = QGridLayout()
        top_grid.addLayout(top_left_grid, 1, 0)
        top_grid.addWidget(create_v_sep(self), 1, 1)
        top_grid.addLayout(top_right_grid, 1, 2)

        bottom_grid = QGridLayout()
        bottom_grid.addLayout(bottom_left_grid, 0, 0)
        bottom_grid.addWidget(create_v_sep(self), 0, 1)
        bottom_grid.addLayout(bottom_right_grid, 0, 2)

        main_grid = QGridLayout(self)

        main_grid.addWidget(self.labels["randomize"], 0, 0)
        main_grid.addWidget(create_h_sep(self), 1, 0)
        main_grid.addLayout(top_grid, 2, 0)
        main_grid.addWidget(create_h_sep(self), 3, 0)
        main_grid.addWidget(self.labels["modify"], 4, 0)
        main_grid.addWidget(create_h_sep(self), 5, 0)
        main_grid.addLayout(bottom_grid, 6, 0)
        main_grid.addWidget(randomize_button, 7, 0)

        self.setLayout(main_grid)

        self.config = Config(f"{DEFAULT_CONFIG_PATH}/spec.yml")

    def create_top_left_grid(self):
        """ Create the left half of the main grid """
        grid = QGridLayout()
        grid.addWidget(self.labels["bases"], 0, 0, 1, 0)
        grid.addWidget(create_h_sep(self), 1, 0, 1, 0)

        grid.addWidget(self.labels["playable_bases"], 2, 0)
        grid.addWidget(self.check_boxes["pb_enabled"], 2, 1)
        grid.addWidget(self.labels["pb_minimum"], 3, 0)
        grid.addWidget(self.spin_boxes["pb_min"], 3, 1)
        grid.addWidget(self.labels["pb_maximum"], 4, 0)
        grid.addWidget(self.spin_boxes["pb_max"], 4, 1)
        grid.addWidget(create_h_sep(self), 5, 0, 1, 0)

        grid.addWidget(self.labels["boss_bases"], 6, 0)
        grid.addWidget(self.check_boxes["bb_enabled"], 6, 1)
        grid.addWidget(self.labels["bb_minimum"], 7, 0)
        grid.addWidget(self.spin_boxes["bb_min"], 7, 1)
        grid.addWidget(self.labels["bb_maximum"], 8, 0)
        grid.addWidget(self.spin_boxes["bb_max"], 8, 1)
        grid.addWidget(create_h_sep(self), 9, 0, 1, 0)

        grid.addWidget(self.labels["other_bases"], 10, 0)
        grid.addWidget(self.check_boxes["ob_enabled"], 10, 1)
        grid.addWidget(self.labels["ob_minimum"], 11, 0)
        grid.addWidget(self.spin_boxes["ob_min"], 11, 1)
        grid.addWidget(self.labels["ob_maximum"], 12, 0)
        grid.addWidget(self.spin_boxes["ob_max"], 12, 1)
        grid.addWidget(create_h_sep(self), 13, 0, 1, 0)

        grid.addWidget(self.labels["class_bases"], 14, 0)
        grid.addWidget(self.check_boxes["cb_enabled"], 14, 1)
        grid.addWidget(self.labels["cb_minimum"], 15, 0)
        grid.addWidget(self.spin_boxes["cb_min"], 15, 1)
        grid.addWidget(self.labels["cb_maximum"], 16, 0)
        grid.addWidget(self.spin_boxes["cb_max"], 16, 1)
        grid.addWidget(create_h_sep(self), 17, 0, 1, 0)

        grid.addWidget(self.labels["etc"], 18, 0, 1, 0)
        grid.addWidget(create_h_sep(self), 19, 0, 1, 0)
        grid.addWidget(self.labels["force_master_seal"], 20, 0)
        grid.addWidget(self.check_boxes["master_seal_enabled"], 20, 1)

        return grid

    def create_top_right_grid(self):
        """ Create the right half of the main grid """
        grid = QGridLayout()
        grid.addWidget(self.labels["growths"], 0, 0, 1, 0)
        grid.addWidget(create_h_sep(self), 1, 0, 1, 0)

        grid.addWidget(self.labels["playable_growths"], 2, 0)
        grid.addWidget(self.check_boxes["pg_enabled"], 2, 1)
        grid.addWidget(self.labels["pg_minimum"], 3, 0)
        grid.addWidget(self.spin_boxes["pg_min"], 3, 1)
        grid.addWidget(self.labels["pg_maximum"], 4, 0)
        grid.addWidget(self.spin_boxes["pg_max"], 4, 1)
        grid.addWidget(create_h_sep(self), 5, 0, 1, 0)

        grid.addWidget(self.labels["boss_growths"], 6, 0)
        grid.addWidget(self.check_boxes["bg_enabled"], 6, 1)
        grid.addWidget(self.labels["bg_minimum"], 7, 0)
        grid.addWidget(self.spin_boxes["bg_min"], 7, 1)
        grid.addWidget(self.labels["bg_maximum"], 8, 0)
        grid.addWidget(self.spin_boxes["bg_max"], 8, 1)
        grid.addWidget(create_h_sep(self), 9, 0, 1, 0)

        grid.addWidget(self.labels["other_growths"], 10, 0)
        grid.addWidget(self.check_boxes["og_enabled"], 10, 1)
        grid.addWidget(self.labels["og_minimum"], 11, 0)
        grid.addWidget(self.spin_boxes["og_min"], 11, 1)
        grid.addWidget(self.labels["og_maximum"], 12, 0)
        grid.addWidget(self.spin_boxes["og_max"], 12, 1)
        grid.addWidget(create_h_sep(self), 13, 0, 1, 0)

        grid.addWidget(self.labels["characters"], 14, 0, 1, 0)
        grid.addWidget(create_h_sep(self), 15, 0, 1, 0)

        grid.addWidget(self.labels["p_enabled"], 16, 0)
        grid.addWidget(self.check_boxes["p_enabled"], 16, 1)
        grid.addWidget(self.labels["b_enabled"], 17, 0)
        grid.addWidget(self.check_boxes["b_enabled"], 17, 1)
        grid.addWidget(self.labels["o_enabled"], 18, 0)
        grid.addWidget(self.check_boxes["o_enabled"], 18, 1)

        return grid

    def create_bottom_left_grid(self):
        """ Create the bottom left part of the main grid """
        grid = QGridLayout()
        grid.addWidget(self.labels["mod_bases"], 0, 0, 1, 0)
        grid.addWidget(create_h_sep(self), 1, 0, 1, 0)

        grid.addWidget(self.labels["mod_playable_bases"], 2, 0)
        grid.addWidget(self.check_boxes["mpb_enabled"], 2, 1)
        grid.addWidget(self.labels["mod_pb"], 3, 0)
        grid.addWidget(self.spin_boxes["pb_mod"], 3, 1)
        grid.addWidget(create_h_sep(self), 4, 0, 1, 0)

        grid.addWidget(self.labels["mod_boss_bases"], 5, 0)
        grid.addWidget(self.check_boxes["mpb_enabled"], 5, 1)
        grid.addWidget(self.labels["mod_bb"], 6, 0)
        grid.addWidget(self.spin_boxes["bb_mod"], 6, 1)
        grid.addWidget(create_h_sep(self), 7, 0, 1, 0)

        grid.addWidget(self.labels["mod_other_bases"], 8, 0)
        grid.addWidget(self.check_boxes["mob_enabled"], 8, 1)
        grid.addWidget(self.labels["mod_ob"], 9, 0)
        grid.addWidget(self.spin_boxes["ob_mod"], 9, 1)

        return grid

    def create_bottom_right_grid(self):
        """ Create the bottom right part of the main grid """
        grid = QGridLayout()
        grid.addWidget(self.labels["mod_growths"], 0, 0, 1, 0)
        grid.addWidget(create_h_sep(self), 1, 0, 1, 0)

        grid.addWidget(self.labels["mod_playable_growths"], 2, 0)
        grid.addWidget(self.check_boxes["mpg_enabled"], 2, 1)
        grid.addWidget(self.labels["mod_pg"], 3, 0)
        grid.addWidget(self.spin_boxes["pg_mod"], 3, 1)
        grid.addWidget(create_h_sep(self), 4, 0, 1, 0)

        grid.addWidget(self.labels["mod_boss_growths"], 5, 0)
        grid.addWidget(self.check_boxes["mbg_enabled"], 5, 1)
        grid.addWidget(self.labels["mod_bg"], 6, 0)
        grid.addWidget(self.spin_boxes["bg_mod"], 6, 1)
        grid.addWidget(create_h_sep(self), 7, 0, 1, 0)

        grid.addWidget(self.labels["mod_other_growths"], 8, 0)
        grid.addWidget(self.check_boxes["mog_enabled"], 8, 1)
        grid.addWidget(self.labels["mod_og"], 9, 0)
        grid.addWidget(self.spin_boxes["og_mod"], 9, 1)

        return grid

    def start(self):
        """ Start the app """
        self.show()
        sys.exit(APP.exec_())
