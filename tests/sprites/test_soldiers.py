import pytest
from rts.controllers.entity_controller import EntityController
from rts.models.game_entity import GameEntity
from rts.sprites.ruler import Ruler

from rts.sprites.soldier import Soldier
from rts.sprites.tower import Tower


@pytest.fixture
def sample_soldier() -> Soldier:
    return Soldier(GameEntity(0, 0, [0, 0, 0], [0, 0]), [0, 0], 0, None, 0)


@pytest.fixture
def delta() -> int:
    return 1


def test_simple_soldier_increment_initiative(
    sample_soldier: Soldier, delta: int
):
    prev_init = sample_soldier.initiative
    sample_soldier.update(delta=delta)
    assert (
        prev_init + sample_soldier.initiative_step * 1
        == sample_soldier.initiative
    )


def test_simple_soldier_reset_initiative(sample_soldier: Soldier, delta: int):
    for i in range(0, 100):
        sample_soldier.update(delta=delta)
    assert abs(sample_soldier.initiative - 0.11) < 1e-16

def test_collision_between_soldiers():
    r1 = Ruler(GameEntity(0, 0, [0, 0, 0], [0, 0]), 1)
    r2 = Ruler(GameEntity(0, 0, [0, 0, 0], [0, 0]), 1)
    t1 = Tower(GameEntity(0, 0, [0, 0, 0], [0, 0]), r1, 1, [0, 0, 0], [0, 0], 0.1)
    t2 = Tower(GameEntity(0, 0, [0, 0, 0], [0, 0]), r2, 1, [0, 0, 0], [0, 0], 0.1)
    s1 = Soldier(GameEntity(0, 0, [0, 0, 0], [1, 1]), [0, 0], 0, t1, 0)
    s2 = Soldier(GameEntity(0, 1, [0, 0, 0], [1, 1]), [0, 0], 0, t2, 0)
    e = EntityController()
    e.register_entity(s1)
    e.register_entity(s2)
    s1.update(1)
    print(e.entity_dict[Soldier])
    assert s1 in e.entity_dict[Soldier]
    assert s2 in e.entity_dict[Soldier]
    
def test_collision_between_soldiers():
    r1 = Ruler(GameEntity(0, 0, [0, 0, 0], [0, 0]), 1)
    r2 = Ruler(GameEntity(0, 0, [0, 0, 0], [0, 0]), 1)
    t1 = Tower(GameEntity(0, 0, [0, 0, 0], [0, 0]), r1, 1, [0, 0, 0], [0, 0], 0.1)
    t2 = Tower(GameEntity(0, 0, [0, 0, 0], [0, 0]), r2, 1, [0, 0, 0], [0, 0], 0.1)
    s1 = Soldier(GameEntity(0, 1, [0, 0, 0], [1, 1]), [0, 0], 0, t1, 0)
    s2 = Soldier(GameEntity(0, 1, [0, 0, 0], [1, 1]), [0, 0], 0, t2, 0)
    e = EntityController()
    e.register_entity(s1)
    e.register_entity(s2)
    s1.update(1)
    print(e.entity_dict[Soldier])
    assert s1 not in e.entity_dict[Soldier]
    assert s2 not in e.entity_dict[Soldier]
