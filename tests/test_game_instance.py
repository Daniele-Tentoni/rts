import pygame
import pygame.sprite
import pytest

from rts.rts import GameInstance

@pytest.fixture
def sample_game_instance() -> GameInstance:
  pygame.init()
  pygame.font.init()
  return GameInstance(pygame.Surface((1, 1)))

def test_add_sprite_to_group(sample_game_instance: GameInstance):
  """Test Add Sprite To Group in Game Instance.

  When invoking add sprite to group in a game instance, that sprite has to be
  added to GameInstance.all_sprites group too.

  Args:
    sample_game_instance (GameInstance): sample GameInstance.
  """
  test_sprite: pygame.sprite.Sprite = pygame.sprite.Sprite()
  test_group = pygame.sprite.Group()
  test_group.add(test_sprite)
  assert test_group.has(test_sprite)
  sample_game_instance.add_sprite_to(test_sprite, sample_game_instance.towers)
  assert sample_game_instance.all_sprites.has(test_sprite)