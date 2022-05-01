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

import os
from pathlib import Path
from typing import Any
import toml


# Multiplatform way to get current user's home directory (https://stackoverflow.com/a/4028943/10220116)
home = str(Path.home())
rts_dot_dir = os.path.join(home, ".rts")
settings_path = os.path.join(rts_dot_dir, "settings.toml")
print("Imported settings")
try:
    parsed = toml.load(settings_path)
except FileNotFoundError:
    if not os.path.exists(rts_dot_dir):
        os.mkdir(rts_dot_dir)

    with open(settings_path, "w+", encoding="utf-8") as w:
        toml.dump(dict(), w)

    parsed = dict()

defaults = {
    "advanced": {
        "fps_label_visibility": int(
            True
        )  # pygame_gui require UILabel visibility as int
    }
}

if parsed:
    print(f"def: {defaults}")
    print(f"par: {parsed}")


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
    print(f"parts {parts}")
    p = parsed
    for part in parts[: len(parts) - 1]:
        if part not in p.keys():
            p[part] = dict()

        p = p[part]
        print(f"Try to set {p}")
    p[parts[len(parts) - 1]] = value
    print(f"Lets write {p}")
    _save()


def _save():
    """Save the current settings writing in the dotfile"""
    with open(settings_path, "w", encoding="utf-8") as w:
        print(f"Write {parsed}")
        toml.dump(parsed, w)
