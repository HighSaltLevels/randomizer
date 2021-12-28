""" Test Suite for config.py """

import os
from pathlib import Path
from unittest import mock

import pytest
import yaml

from constants import DEFAULT_CONFIG, FEVersions
from config import Config, ConfigError, CONFIG_MAP


TEST_CONFIG = os.path.join(str(Path.home()), "config.yml")


def setup():
    """ Create a mocked config file for testing """
    data = {"foo": "bar"}
    with open(TEST_CONFIG, "w") as config_file:
        config_file.write(yaml.dump(data))


def teardown():
    """ Delete the mocked config file """
    try:
        os.remove(TEST_CONFIG)
    except FileNotFoundError:
        pass


@pytest.fixture(name="config")
def create_config():
    """ Create a test config file and remove it after done """
    setup()
    yield Config(TEST_CONFIG)
    teardown()


def test_init():
    """ Test creation of Config object """
    # Test that it uses default config if config file is not present
    # Delete existing test config if already present
    if os.path.isfile(TEST_CONFIG):
        teardown()
        assert not os.path.isfile(
            TEST_CONFIG
        ), "Test config file should be removed for this test"

    config = Config(TEST_CONFIG)
    assert config == DEFAULT_CONFIG

    # Test issue reading config
    setup()
    with mock.patch("config.Config.update", side_effect=Exception):
        with pytest.raises(ConfigError) as error:
            config = Config(TEST_CONFIG)
            assert str(error) == "Try re-installing to resolve this error."

    # This test doesn't use the config fixture so we must manually teardown
    teardown()


def test_get_path(config):
    """ Test the get_path method """
    for version in {FEVersions.FE6, FEVersions.FE7, FEVersions.FE8}:
        assert config.get_path(version) == CONFIG_MAP[version]


def test_write(config):
    """ Test the write method """
    if os.path.isfile(TEST_CONFIG):
        teardown()
        assert not os.path.isfile(
            TEST_CONFIG
        ), "Test config file should be removed for this test"
    config.write()
    assert os.path.isfile(TEST_CONFIG), "Config was not written after calling write()"


def test_update_combo_box(config):
    """ Test the update_combo_box method """
    config["randomize"] = {"classes": {"mode": "foo"}}
    config.update_combo_box("bar")
    assert (
        config["randomize"]["classes"]["mode"] == "bar"
    ), "Mode was not properly updated"


def test_update_by_path(config):
    """ Test the update_by_path method """
    config.set_default()
    m_elements = {
        "check_box": mock.MagicMock(),
        "spin_boxes": [mock.MagicMock(), mock.MagicMock()],
    }
    m_elements["check_box"].isChecked.return_value = True
    m_elements["spin_boxes"][0].value.return_value = 1
    m_elements["spin_boxes"][1].value.return_value = 101

    # Test randomize bases and growths
    for _type in {"bases", "growths"}:
        for kind in {"playable", "boss", "other", "class"}:
            if _type == "growths" and kind == "class":
                # There's no randomizing class growths
                continue

            config.update_by_path(f"randomize/{_type}/{kind}", m_elements)
            assert config["randomize"]["stats"][_type][kind]["enabled"]
            assert config["randomize"]["stats"][_type][kind]["minimum"] == 1
            assert config["randomize"]["stats"][_type][kind]["maximum"] == 101

    # Test randomize palettes
    for kind in {"playable", "boss", "other"}:
        config.update_by_path(f"randomize/palettes/{kind}", m_elements)
        assert config["randomize"]["characters"]["palettes"][kind]["enabled"]

    # Test other locations
    for kind in {"playable", "boss", "other"}:
        config.update_by_path(f"randomize/{kind}", m_elements)
        assert config["randomize"]["classes"][kind]["enabled"]

    # Test promotes
    config.update_by_path("randomize/promotes", m_elements)
    assert config["randomize"]["mix_promotes"]["enabled"]

    # Test master selas
    config.update_by_path("randomize/all_master_seals", m_elements)
    assert config["randomize"]["classes"]["all_master_seals"]["enabled"]

    # Test modify bases and growths
    for _type in {"bases", "growths"}:
        for kind in {"playable", "boss", "other"}:
            config.update_by_path(f"modify/{_type}/{kind}", m_elements)
            assert config["modify"]["stats"][_type][kind]["enabled"]
            assert config["modify"]["stats"][_type][kind]["modifier"] == 1
