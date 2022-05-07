import pytest
import rts.config

from unittest.mock import MagicMock, patch


@pytest.fixture
def empty_configs() -> dict:
    # Create file
    with patch("toml.load") as load:
        load.return_value = {}
        rts.config.parsed = rts.config._load_configs()
        load.assert_called_once()
        yield rts.config.parsed
    del rts.config.parsed


@pytest.fixture
def mocked_configs() -> dict:
    # Create file
    with patch("toml.load") as load:
        load.return_value = {"advanced": {"fps_label_visibility": int(False)}}
        rts.config.parsed = rts.config._load_configs()
        load.assert_called_once()
        yield rts.config.parsed
    del rts.config.parsed


@pytest.fixture
def mock_config():
    # Mock configs
    # Yield config
    # Delete config
    pass


def test_read_default_setting(empty_configs: dict):
    assert rts.config.parsed == dict()
    assert empty_configs == dict()
    default_setting = rts.config.defaults["advanced"]["fps_label_visibility"]
    current_setting = rts.config._get("advanced.fps_label_visibility")
    assert default_setting == current_setting


def test_read_custom_setting(mocked_configs: dict):
    custom_setting = rts.config.parsed["advanced"]["fps_label_visibility"]
    current_setting = rts.config._get("advanced.fps_label_visibility")
    assert custom_setting == current_setting


def test_custom_setting_different_from_default(mocked_configs: dict):
    default_setting = rts.config.defaults["advanced"]["fps_label_visibility"]
    current_setting = rts.config._get("advanced.fps_label_visibility")
    assert default_setting != current_setting

@patch("toml.load")
@patch("os.path.exists")
@patch("rts.config._save_configs")
def test_missing_config_file(save: MagicMock, exists: MagicMock, load: MagicMock):
    load.side_effect = FileNotFoundError('mocked')
    exists.return_value = True
    empty_dict = dict()
    assert rts.config._load_configs() == empty_dict
    save.assert_called_once_with(empty_dict, create_if_missing=True)

@patch("toml.load")
@patch("os.path.exists")
@patch("os.makedirs")
@patch("rts.config._save_configs")
def test_missing_config_dir(save: MagicMock, dirs: MagicMock, exists: MagicMock, load: MagicMock):
    load.side_effect = FileNotFoundError('mocked')
    exists.return_value = False
    rts.config._load_configs()
    dirs.assert_called_once_with(rts.config.config_path, exist_ok=True)
    save.assert_called_once_with(dict(), create_if_missing=True)
