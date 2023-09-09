from pygame import Surface
import pytest
from rts.config import TEXT_COLOR
from rts.models.game_entity import GameEntity
from rts.sprites.route import Route
from rts.sprites.ruler import Ruler
from rts.sprites.tower import Tower

@pytest.fixture
def make_tower():
    r1 = Ruler(GameEntity(0, 0, [0, 0, 0], [0, 0]), 1)
    
    def _make_tower(x = 0, y = 0):
        return Tower(GameEntity(x, y, [0, 0, 0], [0, 0]), r1, 1, [0, 0, 0], [0, 0], 1)
    
    return _make_tower

@pytest.fixture
def sample_route(make_tower) -> Route:
    t1: Tower = make_tower(0, 0)
    t2: Tower = make_tower(1, 1)
    return Route(t1, t2)

def test_over_without_update(sample_route: Route):
    mouse_pos = [0, 0]
    assert not sample_route.over(mouse_pos)

def test_over_with_update(sample_route: Route):
    mouse_pos = [0, 0]
    sample_route.update(0, Surface([2, 2]))
    assert sample_route.over(mouse_pos)

def test_not_over(sample_route: Route):
    mouse_pos = [2, 2]
    sample_route.update(0, Surface([2, 2]))
    assert not sample_route.over(mouse_pos)

def test_width_not_over(sample_route: Route):
    mouse_pos = [2, 2]
    sample_route.update(0, Surface([2, 2]))
    sample_route.over(mouse_pos)
    assert sample_route.width == 2
    assert sample_route.color == TEXT_COLOR

def test_width_over(sample_route: Route):
    mouse_pos = [1, 1]
    sample_route.update(0, Surface([2, 2]))
    sample_route.over(mouse_pos)
    assert sample_route.width == 4
    assert sample_route.color == "green"
