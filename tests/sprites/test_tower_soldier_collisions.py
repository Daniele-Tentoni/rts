from typing import Callable
from unittest.mock import MagicMock, patch
import pytest
from rts.controllers.entity_controller import EntityController
from rts.models.game_entity import GameEntity

from rts.sprites.ruler import Ruler
from rts.sprites.soldier import Soldier
from rts.sprites.tower import Tower

color = [0, 0, 0]
size = [1, 1]

@pytest.fixture
def ruler() -> Ruler:
    def _ruler():
        return Ruler(GameEntity(1, 1, color, size), 1)
    
    return _ruler

@pytest.fixture
def tower(ruler: Ruler) -> Callable[[float, float, Ruler], Tower]:
    default_ruler = ruler()
    
    def _tower(x: float, y: float, owner: Ruler):
        owned_by = owner if owner else default_ruler
        return Tower(GameEntity(x, y, color, size), owned_by, 1, color, size, 1)
    
    return _tower

@pytest.fixture
def soldier():
    def _soldier(x: float, y: float, tower: Tower):
        return Soldier(GameEntity(x, y, color, size), [x, y], 0, tower, 1)

    return _soldier

@patch("rts.sprites.tower.Tower._update_soldiers_label")
@patch("rts.sprites.tower.Tower._update_level_label")
def test_soldier_tower_collision(mock: MagicMock,mock2: MagicMock, tower: Callable[[float, float, Ruler], Tower], soldier, ruler):
    r1 = ruler()
    r2 = ruler()
    t1: Tower = tower(0, 0, r1)
    t2: Tower = tower(1, 1, r2)
    s1: Soldier = soldier(1, 1, t1)
    s1.target = t2
    e = EntityController()
    e.reset()
    e.register_entity(t1)
    e.register_entity(t2)
    e.register_entity(s1)
    
    # Entities doesn't move, collision appen between s1 and t2.
    assert s1.rect.colliderect(t2.rect)
    assert not s1.rect.colliderect(t1.rect)
    e.game_entities.update(delta=0)
    assert s1 not in e.entities(Soldier)
    assert not s1.alive()
