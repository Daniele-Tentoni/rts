"""Contains all configurations for the RTS project.

Use this module to load and save custom configurations or retrieve the recommended ones.

Add new immutable configurations as Literals like::
    FONT_NAME = "Arial"
    RULER_COLOR = (255, 0, 255)

Add new mutable configurations following those steps:

1. Add new default configuration, ordered alphabetical and grouped semantically::
    defaults = {...
        "key": "value",
    }

2. Create `get_` and `set_` methods::
    def get_key() -> Type:
        return _get(key)

    def set_key(value: Type) -> None:
        _set(key, value)

.. note:
  If you retrieve a default configuration and you try to save it without changes, it will not be stored in the stored custom configuration file.
"""

import os
from typing import Any
import toml
from xdg import xdg_config_home

# _called_from_test = False
"""Support for pytest mocking"""

FONT_NAME = "Arial"
FONT_SIZE = 20

GAME_NAME = "Real Time Strategy"

PLAYERS_NUMBER = 1

RULER_COLOR = (255, 0, 255)
RULER_HEIGHT = 15
RULER_WIDTH = 15
RULER_SIZE = (RULER_WIDTH, RULER_HEIGHT)

TEXT_COLOR = (127, 255, 127)

TOWER_COLOR = (100, 100, 100)
TOWER_WIDTH = 25
TOWER_HEIGHT = 25
TOWER_SIZE = (TOWER_WIDTH, TOWER_HEIGHT)
# Soldiers number limits per level for towers
# TODO: Maybe change name? Not compulsory
LIMIT_PER_LEVEL = [2, 5, 10, 20, 50]

SCREEN_COLOR = (21, 21, 21)
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

SOLDIER_COLOR = (0, 255, 255)
SOLDIER_RADIUS_AROUND_TOWER = 10
SOLDIER_HEIGHT = 10
SOLDIER_WIDTH = 10
SOLDIER_SIZE = (SOLDIER_WIDTH, SOLDIER_HEIGHT)

# Multiplatform way to get current user's home directory (https://stackoverflow.com/a/53222876/10220116)
config_path = os.path.join(
    os.environ.get("APPDATA") or xdg_config_home(), "rts"
)
config_file = os.path.join(config_path, "settings.toml")
"""File path to settings.toml"""


def _load_configs() -> dict:
    """Loads settings at runtime

    Create the settings file if is the first time running the application and calling this module.
    """
    try:
        return toml.load(config_file)
    except FileNotFoundError:
        if not os.path.exists(config_path):
            os.makedirs(config_path, exist_ok=True)

        empty_dict = dict()
        _save_configs(empty_dict, create_if_missing=True)
        return empty_dict


def _save_configs(configs: dict, create_if_missing: bool = False) -> None:
    """Save the current settings writing in the dotfile"""
    mode = "w+" if create_if_missing else "w"
    with open(config_file, mode, encoding="utf-8") as w:
        toml.dump(configs, w)


defaults = {
    "advanced": {
        # pygame_gui require UILabel visibility as int
        "fps_label_visibility": int(True)
    }
}
"""Default configurations.

.. warning:
  Don't change it at runtime if you wanna keep your updated configurations.
"""

# Loads config when importing the module
parsed = dict()  # if _called_from_test else _load_configs()
"""
Currently parsed configs.

.. warning:
    Don't change it at runtime if you wanna keep your updated configurations.
"""


def get_fps_label_visibility() -> bool:
    return _get("advanced.fps_label_visibility")


def set_fps_label_visibility(value: bool):
    _set("advanced.fps_label_visibility", value)


def _get(setting: str):
    """Get a setting from file or defaults

    Get a setting value from settings file or defaults dict if not specified in the settings file.

    :param setting: setting key to read
    :type setting: str
    :return: setting value
    :rtype: Any

    .. note:
      This function doesn't have any side effect, it doesn't write the settings file or modify parsed dict or defaults one.
    """
    parts = setting.split(".")
    p = parsed
    for part in parts:
        p = p[part] if part in p.keys() else defaults[part]

    return p


def _set(setting: str, value: Any):
    """Set a setting value in the settings file

    Set a setting value in the settings file navigate each dict section until the final one. This will produce the corresponding toml section.

    For example, calling `_set("a.b.c", 1)` will produce the following toml file::

        [a.b]
        c = 1

    :param setting: setting key to write
    :type setting: str
    :param value: value to write
    :type value: Any
    """
    parts = setting.split(".")
    p = parsed
    for part in parts[: len(parts) - 1]:
        if part not in p.keys():
            p[part] = dict()

        p = p[part]

    p[parts[len(parts) - 1]] = value
    _save_configs(parsed)
