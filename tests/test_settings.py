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
