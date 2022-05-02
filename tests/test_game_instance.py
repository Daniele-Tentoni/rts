import pygame
import pytest

from rts.controllers.entity_controller import EntityController
from rts.game import Game
from rts.models.game_entity import GameEntity
from rts.sprites.ruler import Ruler


@pytest.fixture
def sample_controller() -> EntityController:
    controller = EntityController()
    yield EntityController()
    del controller


def test_add_sprite_to_group(sample_controller: EntityController):
    """Test Add Sprite To Group in Game Instance.

    When invoking add sprite to group in a game instance, that sprite has to be
    added to GameInstance.all_sprites group too.

    Args:
      sample_game_instance (GameInstance): sample Game Instance.
    """
    test_entity: GameEntity = GameEntity(0, 0, [0, 0, 0], [0, 0])
    sample_controller.register_entity(test_entity)
    assert sample_controller.game_entities.has(test_entity)


def test_simple_init_rulers(sample_controller: EntityController):
    """Test Rulers in Game Instance without npc number.

    The number of rulers expected is 2: one player and one npc.

    Args:
        sample_game_instance (GameInstance): sample Game Instance.
    """
    pygame.init()
    pygame.font.init()
    game = Game(None, None)
    rulers = sample_controller.entity_dict[Ruler]
    assert len(rulers) == 2
    del game


supported_number_of_npc_at_once: int = 3


@pytest.mark.parametrize("npc", range(0, supported_number_of_npc_at_once))
def test_more_init_rulers(npc):
    """Test Rulers initialized by Game Instance giving npc number.

    Given npc number, we want n + 1 rulers in game instance.

    Test that we can support up to 4 players at once.
    """
    pygame.init()
    pygame.font.init()
    controller = EntityController()
    game = Game(None, None, 1 + npc)
    [print(f"C: {x}") for x in controller.entity_dict.keys()]
    assert len(controller.entity_dict[Ruler]) == npc + 1
    del controller
    del game
