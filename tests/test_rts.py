import pytest

from rts.tower import Tower

from rts.constants import (
  TOWER_WIDTH,
  TOWER_HEIGHT,
)

from rts import __version__

@pytest.fixture
def example_key_data(pressed_key):
  def helper():
    tmp = [0] * 300
    tmp[pressed_key] = 1
    return tmp
  return helper

TOWER_STARTING_X = 10
TOWER_STARTING_Y = 10

@pytest.fixture
def create_simple_tower():
  return 1

def test_version():
  assert __version__ == '0.1.0'

def test_tower_initial_position():
  tower = Tower(TOWER_STARTING_X, TOWER_STARTING_Y)
  assert tower.rectangle.top == TOWER_STARTING_Y
  assert tower.rectangle.left == TOWER_STARTING_X
