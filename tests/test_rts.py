import pytest

from rts import __version__
from rts.tower import Tower

TOWER_STARTING_X = 10
TOWER_STARTING_Y = 10

@pytest.fixture
def create_simple_tower() -> Tower:
  return Tower(TOWER_STARTING_X, TOWER_STARTING_Y)

def test_version():
  assert __version__ == '0.1.0'

def test_tower_initial_position(create_simple_tower: Tower):
  assert create_simple_tower.rect.top == TOWER_STARTING_Y
  assert create_simple_tower.rect.left == TOWER_STARTING_X
