import pytest

from rts.sprites.soldier import Soldier
from rts.sprites.tower import (Tower, limits_per_level)

@pytest.fixture
def create_simple_tower() -> Tower:
  return Tower(0, 0)

def test_spawn_a_soldier(create_simple_tower: Tower):
  """A newly created tower could spawn a soldier.

  Any newly created tower could spawn a soldier because it haven't reached the limit.

  Args:
      create_simple_tower (Tower): newly created tower from the fixture.
  """
  assert isinstance(create_simple_tower.spawn_soldier(), Soldier)

def test_reach_maximum_soldiers(create_simple_tower: Tower):
  """A tower could spawn soldiers until reach the limit.

  Args:
      create_simple_tower (Tower): newly created tower from the fixture.
  """
  for limits in limits_per_level:
    # Reach the maximum
    for n in range(0, limits[1]):
      assert isinstance(create_simple_tower.spawn_soldier(), Soldier)

    # Assert the we can't spawn another soldier.
    assert len(create_simple_tower.soldiers) is limits[1]
    assert create_simple_tower.spawn_soldier() is None
