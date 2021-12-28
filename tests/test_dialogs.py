""" Test Suite for dialogs """

from unittest import mock

import pytest

from dialogs import VersionPrompt


@pytest.fixture(name="m_ver_prompt")
def create_mock_version_prompt():
    """ Create a VersionPrompt object with mocked __init__ """
    with mock.patch.object(VersionPrompt, "__init__", lambda a, b, c: None):
        m_ver_prompt = VersionPrompt(None, "mock")
        m_ver_prompt.combo_box = mock.MagicMock()
        m_ver_prompt.close = mock.MagicMock()
        m_ver_prompt.setLayout = mock.MagicMock()
        m_ver_prompt.show = mock.MagicMock()
        yield m_ver_prompt


def test_set_version(m_ver_prompt):
    """ Test the set_version method """
    with mock.patch.dict("dialogs.CONFIG") as m_config:
        m_ver_prompt.combo_box.currentText.return_value = "foo"
        m_ver_prompt.set_version()
        assert m_config["fe_version"] == "foo"


def test_build_ui(m_ver_prompt):
    """ Test the build_ui method """
    with mock.patch("dialogs.QLabel"):
        with mock.patch("dialogs.QComboBox"):
            with mock.patch("dialogs.QPushButton"):
                with mock.patch("dialogs.QGridLayout"):
                    m_ver_prompt.build_ui()
                    m_ver_prompt.setLayout.assert_called_once()
                    m_ver_prompt.show.assert_called_once()


def test_init():
    """ Test the init since the other tests use a mocked version """
    with mock.patch("dialogs.VersionPrompt.build_ui") as m_build:
        ver_prompt = VersionPrompt()
        m_build.assert_called_once()

    assert ver_prompt.combo_box is None
