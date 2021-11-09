""" conftest.py for building shared fixtures """

from unittest import mock

import pytest


@pytest.fixture(name="m_config")
def create_mock_config():
    """ Patch in a MagicMock() object for CONFIG """
    with mock.patch("controller.CONFIG") as m_config:
        yield m_config
