""" Controller test module """

from unittest import mock

import pytest

from constants import FEVersions
from controller import (
    handler,
    combo_box_handler,
    browse_handler,
    RandomizerHandler,
    _get_filters,
)
from rom_editors.stat_editor import InvalidConfigError
from versions import VERSION_LOCATION

# m_config is not used in arguments but it's put in some tests so that the method
# calls are ignored.
# pylint: disable=unused-argument

# Some tests can only work by using protected attributes and methods.
# pylint: disable=protected-access


@pytest.fixture(name="m_config")
def create_mock_config():
    """ Patch in a MagicMock() object for CONFIG """
    with mock.patch("controller.CONFIG") as m_config:
        yield m_config


@pytest.fixture(name="m_get_filters")
def create_mock_get_filters():
    """ Patch in a MagicMock() object for controller._get_filters """
    with mock.patch("controller._get_filters") as m_get_filt:
        yield m_get_filt


def test_handler(m_config):
    """ Test the handler for saving states of UI elements """
    # Test without toggling
    elements = {"spin_boxes": [mock.MagicMock() for _ in range(5)]}
    handler("path", elements, toggle=False)
    for element in elements["spin_boxes"]:
        element.setDisabled.assert_not_called()

    m_config.update_by_path.assert_called_once_with("path", elements)
    m_config.write.assert_called_once()
    m_config.reset_mock()

    # Test with toggling
    handler("path", elements, toggle=True)
    for element in elements["spin_boxes"]:
        element.setDisabled.assert_called_once()

    m_config.update_by_path.assert_called_once_with("path", elements)
    m_config.write.assert_called_once()


def test_combo_box_handler(m_config):
    """ Test the combo box handler will update selection and save data """
    combo_box_handler("foo")
    m_config.update_combo_box.assert_called_once_with("foo")
    m_config.write.assert_called_once()


def test_browse_handler(m_config):
    """ Test the browse handler will prompt and save rom path """
    m_app = mock.MagicMock()
    m_app.file_browser.exec_.return_value = True
    m_app.file_browser.selectedFiles.return_value = ["path"]

    browse_handler(m_app)

    m_app.line_edits["rom_edit"].setText.assert_called_once_with("path")
    m_config.write.assert_called_once()


def test_randomize(m_config, m_app):
    """ Test the randomize method of controller """
    handle = RandomizerHandler(m_app)
    m_rom_data = (VERSION_LOCATION + 1) * b"0"
    m_open = mock.mock_open(read_data=m_rom_data)
    with mock.patch("builtins.open", m_open):
        with mock.patch("dialogs.VersionPrompt") as m_version:
            with mock.patch("controller.RandomizerHandler._randomize_all"):
                handle.randomize()
                # Check that data was read in correctly
                assert handle.rom_data == m_rom_data
                # Version should be unkown. Make sure user was prompted
                assert m_version.exec_.called_once()

    # Test handling IOError
    with mock.patch("builtins.open", side_effect=IOError("foo")):
        handle.randomize()
        m_app.labels["status"].setText.assert_called_with("Status: Error! foo")

    # Test handling random generic exceptions
    with mock.patch("builtins.open", m_open):
        with mock.patch(
            "controller.RandomizerHandler._randomize_all", side_effect=Exception("bar")
        ):
            with mock.patch("dialogs.VersionPrompt"):
                handle.randomize()
                m_app.labels["status"].setText.assert_called_with("Status: Error! bar")

    # Test FE7 sav file was also moved during FE7 randomization
    with mock.patch("builtins.open", m_open):
        with mock.patch("controller.RandomizerHandler._randomize_all"):
            with mock.patch("controller.get_fe_version") as m_fe_version:
                m_fe_version.return_value = FEVersions.FE7
                with mock.patch("shutil.copy") as m_copy:
                    handle.randomize()
                    m_copy.assert_called()

                # Test IOError during final write
                with mock.patch("shutil.copy", side_effect=IOError("baz")):
                    handle.randomize()
                    m_app.labels["status"].setText.assert_called_with(
                        "Status: Error! baz"
                    )


@mock.patch("controller.RandomizerHandler._modify_stats")
@mock.patch("controller.RandomizerHandler._randomize_characters")
@mock.patch("controller.RandomizerHandler._edit_promotions")
@mock.patch("controller.RandomizerHandler._randomize_stats")
def test_randomize_all(m_rand_stats, m_edit_prom, m_rand_char, m_mod_stats, m_app):
    """ Test the _randomize_all method in the controller """
    handle = RandomizerHandler(m_app)
    # Test not editing promotions
    with mock.patch.dict(
        "controller.CONFIG",
        {"randomize": {"classes": {"all_master_seals": {"enabled": False}}}},
    ):
        handle._randomize_all()
        m_edit_prom.assert_not_called()
        for obj in {m_rand_stats, m_rand_char, m_mod_stats}:
            obj.assert_called_once()
            obj.reset_mock()

    # Test not editing promotions
    with mock.patch.dict(
        "controller.CONFIG",
        {"randomize": {"classes": {"all_master_seals": {"enabled": True}}}},
    ):
        handle._randomize_all()
        for obj in {m_edit_prom, m_rand_stats, m_rand_char, m_mod_stats}:
            obj.assert_called_once()
            obj.reset_mock()

    # Test invalid config error
    m_rand_stats.side_effect = InvalidConfigError("foo")
    # Mock out the QDialog box
    with mock.patch("controller.QMessageBox"):
        handle._randomize_all()


def test_randomize_characters(m_app, m_get_filters):
    """ Test the randomize_characters method in controller """
    handle = RandomizerHandler(m_app)
    with mock.patch("controller.create_character_editor"):
        handle._randomize_characters()


def test_randomize_stats(m_app, m_get_filters):
    """ Test the randomize_stats method in controller """
    handle = RandomizerHandler(m_app)
    with mock.patch("controller.create_stat_randomizer"):
        handle._randomize_stats()


def test_modify_stats(m_app, m_get_filters):
    """ Test the modify_stats method in controller """
    handle = RandomizerHandler(m_app)
    with mock.patch("controller.create_stat_modifier"):
        handle._modify_stats()


def test_edit_promotions(m_app):
    """ Test the modify_stats method in controller """
    handle = RandomizerHandler(m_app)
    with mock.patch("controller.create_prom_editor"):
        handle._edit_promotions()


def test_get_filters():
    """ Test the _get_filters method """
    config = {
        "foo": {"enabled": True},
        "bar": {"enabled": False},
        "baz": {"enabled": True},
    }
    filters = _get_filters(config, ["bar"])
    assert "bar" in filters
    assert "foo" not in filters
    assert "baz" not in filters
