""" Controller test module """

from unittest import mock

from controller import handler, combo_box_handler, browse_handler


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
