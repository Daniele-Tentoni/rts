import pytest
from rts.controllers.time_controller import DELTA_TIME
from rts.models.game_entity import GameEntity

from rts.sprites.soldier import Soldier

@pytest.fixture
def sample_soldier() -> Soldier:
  return Soldier(GameEntity(0, 0, [0, 0, 0], [0, 0]), [0, 0], 0, 0)

def test_simple_soldier_increment_initiative(sample_soldier: Soldier):
  prev_init = sample_soldier.initiative
  sample_soldier.update()
  assert prev_init + 0.11 * DELTA_TIME == sample_soldier.initiative

def test_simple_soldier_reset_initiative(sample_soldier: Soldier):
  for i in range(0, 10):
    sample_soldier.update()
  assert abs(sample_soldier.initiative - 0.10) < 1e-16
