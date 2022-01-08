import pytest

from rts.tower import Tower
from rts.soldier import Soldier

def test_soldier_raise_init_ex():
  with pytest.raises(ValueError) as v_error:
    soldier = Soldier(None)
    assert v_error.value == "tower_mother argument must be valued"

def test_soldier_created_with_tower():
  tower = Tower(0, 0)
  soldier = Soldier(tower)
  assert soldier.tower == tower