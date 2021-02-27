""" Module for loading all the vertical and horizontal separators """

from PyQt5.QtWidgets import QFrame


def _create_separator(widget):
    """ Init and create base separator QFrame """
    separator = QFrame(widget)
    separator.setLineWidth(2)
    separator.setMidLineWidth(1)
    separator.setFrameShadow(QFrame.Sunken)

    return separator


def create_v_sep(widget):
    """ Init and create vertical separator """

    separator = _create_separator(widget)
    separator.setFrameShape(QFrame.VLine)

    return separator


def create_h_sep(widget):
    """ Init and create horiaontal separator """
    separator = _create_separator(widget)
    separator.setFrameShape(QFrame.HLine)

    return separator
