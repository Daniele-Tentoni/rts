from unittest.mock import MagicMock, patch
from pygame_gui import UIManager
import pytest

from rts.controllers.time_controller import TimeController

@pytest.fixture
@patch("rts.controllers.time_controller.get_fps_label_visibility")
def sample_time_controller(mock: MagicMock):
    mock.return_value = True
    return TimeController(UIManager((800, 600)))

def test_delta(sample_time_controller: TimeController):
    assert sample_time_controller.update(1000) == 0

def test_double_delta(sample_time_controller: TimeController):
    assert sample_time_controller.update(500) == 0.5
    assert sample_time_controller.update(500) == 0
