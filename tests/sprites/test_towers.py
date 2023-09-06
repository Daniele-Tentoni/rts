import pytest
from rts.models.game_entity import GameEntity

from rts.sprites.tower import Tower


@pytest.fixture
def sample_tower() -> Tower:
    return Tower(
        GameEntity(0, 0, [0, 0, 0], [0, 0]),
        None,
        level=1,
        soldier_color=[0, 0, 0],
        soldier_size=[0, 0],
        soldier_gen_ratio=1.0,
    )


@pytest.fixture
def delta() -> int:
    return 1000


def test_simple_tower(sample_tower: Tower, delta: int):
    assert sample_tower._reached_max_soldiers() == True
    sample_tower._update_soldiers_pool(delta)
    assert sample_tower.soldier_gen_pool == 1000


def test_soldier_creation(sample_tower: Tower):
    assert sample_tower.soldiers_number == 0
    sample_tower._update_soldiers_pool(2000)
    sample_tower.create_soldiers()
    assert sample_tower.soldiers_number == 2


def test_level_increment(sample_tower: Tower):
    assert sample_tower.level == 1
    sample_tower._update_soldiers_pool(2000)
    sample_tower.create_soldiers()
    assert sample_tower.level == 2


def test_level_decrement(sample_tower: Tower):
    sample_tower.level = 2
    assert sample_tower.soldiers_number == 0
    sample_tower.soldier_died()
    assert sample_tower.level == 1
