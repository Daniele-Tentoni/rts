import pytest
from rts.models.game_entity import GameEntity

from rts.sprites.soldier import Soldier


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
