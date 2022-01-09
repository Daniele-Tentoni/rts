import pygame.sprite
import pytest
import rts.rts

@pytest.fixture
def sample_game_instance() -> rts.rts.GameInstance:
  return rts.rts.GameInstance()

def test_add_sprite_to_group(sample_game_instance: rts.rts.GameInstance):
  """Test Add Sprite To Group in Game Instance.

  When invoking add sprite to group in a game instance, that sprite has to be
  added to GameInstance.all_sprites group too.

  Args:
    sample_game_instance (rts.rts.GameInstance): sample GameInstance.
  """
  test_sprite: pygame.sprite.Sprite = pygame.sprite.Sprite()
  sample_game_instance.add_sprite_to(test_sprite, sample_game_instance.towers)
  assert sample_game_instance.all_sprites.has(test_sprite)