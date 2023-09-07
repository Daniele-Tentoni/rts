import pytest

from rts.controllers.entity_controller import EntityController
from rts.models.game_entity import GameEntity
from rts.sprites.soldier import Soldier

@pytest.fixture
def sample_entity_controller():
    c = EntityController()
    yield c
    c.reset()
    del c

@pytest.fixture
def sample_soldier():
    return Soldier(GameEntity(0, 0, [0, 0, 0], [0, 0]), [0, 0], 0, None, 0)

def test_empty_dict(sample_entity_controller: EntityController):
    assert len(sample_entity_controller.game_entities) == 0
    assert len(sample_entity_controller.entity_dict) == 0

def test_call_entities_create_new_group(sample_entity_controller: EntityController):
    assert len(sample_entity_controller.entities(Soldier).sprites()) == 0
    assert len(sample_entity_controller.entity_dict) == 1
    assert len(sample_entity_controller.game_entities) == 0

def test_has_empty_dict(sample_entity_controller: EntityController):
    assert len(sample_entity_controller.entity_dict) == 0
    assert not sample_entity_controller.has(Soldier)

def test_has_e_empty_dict(sample_entity_controller: EntityController, sample_soldier: Soldier):
    assert not sample_entity_controller.has_e(sample_soldier)

def test_add_one_entity(sample_entity_controller: EntityController, sample_soldier: Soldier):
    sample_entity_controller.register_entity(sample_soldier)
    assert len(sample_entity_controller.entity_dict) == 1
    assert len(sample_entity_controller.entities(Soldier).sprites()) == 1

def test_one_entity_to_check(sample_entity_controller: EntityController, sample_soldier: Soldier):
    sample_entity_controller.register_entity(sample_soldier)
    assert sample_entity_controller.has(Soldier)
    assert sample_entity_controller.has_e(sample_soldier)
