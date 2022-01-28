""" conftest.py for building shared fixtures """

from unittest import mock

import pytest


@pytest.fixture(name="m_app")
def create_mock_app():
    """ Patch in a MagicMock() object for QApplication """
    with mock.patch("app.APP") as m_app:
        yield m_app


@pytest.fixture(name="rom_data")
def create_64_byte_rom_data():
    """ Create a 64 byte bytearray """
    return bytearray(byte for byte in range(64))
