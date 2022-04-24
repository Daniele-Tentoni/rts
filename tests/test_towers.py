import pytest

from rts.sprites.soldier import Soldier
from rts.sprites.tower import (Tower, LIMIT_PER_LEVEL)

@pytest.fixture
def create_simple_tower() -> Tower:
  return Tower(0, 0)
