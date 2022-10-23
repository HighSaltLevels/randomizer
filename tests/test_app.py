""" Test Suite for the app """

from unittest import mock

from app import Randomizer


def test_init(m_app):
    """Test the init since the other tests use a mocked version"""
    rand = Randomizer()
    with mock.patch("app.sys.exit"):
        with mock.patch.object(rand, "show") as m_show:
            rand.start()
            m_app.exec_.assert_called_once()
            m_show.assert_called_once()
