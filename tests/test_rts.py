import pytest

from rts import __version__
import rts.sprites.tower

TOWER_STARTING_X = 10
TOWER_STARTING_Y = 10


@pytest.fixture
def create_simple_tower() -> rts.sprites.tower.Tower:
    return rts.sprites.tower.Tower(TOWER_STARTING_X, TOWER_STARTING_Y)
