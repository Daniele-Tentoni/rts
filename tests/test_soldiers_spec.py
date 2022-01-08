import pytest

from rts.sprites.soldier import Soldier
from rts.sprites.tower import Tower

def test_soldier_raise_init_ex():
  with pytest.raises(ValueError) as v_error:
    Soldier(None)
    assert v_error.value == "tower_mother argument must be valued"

def test_soldier_created_with_tower():
  tower = Tower(0, 0)
  soldier = Soldier(tower)
  assert soldier.tower == tower