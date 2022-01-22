import pygame
import pygame.sprite
import pytest
from rts.config import PLAYERS_NUMBER, SCREEN_HEIGHT, SCREEN_WIDTH

from rts.rts import GameInstance
from rts.sprites.ruler import Ruler

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
    sample_game_instance (GameInstance): sample Game Instance.
  """
  test_sprite: pygame.sprite.Sprite = pygame.sprite.Sprite()
  test_group = pygame.sprite.Group()
  test_group.add(test_sprite)
  assert test_group.has(test_sprite)
  sample_game_instance.add_sprite_to(test_sprite, sample_game_instance.towers)
  assert sample_game_instance.all_sprites.has(test_sprite)

def test_simple_init_rulers(sample_game_instance: GameInstance):
  """Test Rulers in Game Instance without npc number.

  The number of rulers expected is 2: one player and one npc.

  Args:
      sample_game_instance (GameInstance): sample Game Instance.
  """
  assert isinstance(sample_game_instance.current_ruler, Ruler)
  assert sample_game_instance.npc == 1
  assert len(sample_game_instance.rulers) == 2

supported_number_of_npc_at_once: int = 3
@pytest.mark.parametrize("npc", range(0, supported_number_of_npc_at_once))
def test_more_init_rulers(npc):
  """Test Rulers initialized by Game Instance giving npc number.

  Given npc number, we want n + 1 rulers in game instance.

  Test that we can support up to 4 players at once.
  """
  instance = GameInstance(pygame.Surface((0, 0)), npc)
  assert isinstance(instance.current_ruler, Ruler)
  assert instance.npc == npc
  assert len(instance.rulers) == npc + 1

def test_arrange_soldiers(sample_game_instance: GameInstance):
  sample_game_instance.add_soldiers_to_towers()
  assert PLAYERS_NUMBER * 2 + 1 == len(sample_game_instance.towers)
  assert PLAYERS_NUMBER * 2 + 1 == len(sample_game_instance.soldiers)
  old_pos = [(x.rect.center) for x in sample_game_instance.soldiers]
  mid_pos = [(x.rect.center) for x in sample_game_instance.soldiers]
  for x in range(0, len(old_pos)):
    assert old_pos[x] == mid_pos[x]
  sample_game_instance.arrange_soldiers()
  new_pos = [(x.rect.center) for x in sample_game_instance.soldiers]
  for x in range(0, len(old_pos)):
    assert old_pos[x] != new_pos[x]

def test_spawn_tower_in_random_position(
  sample_game_instance: GameInstance
):
  """Towers has to spawn randomly inside the screen.

  Assert towers spawned inside the screen without overlapping.
  """
  ts = sample_game_instance.towers
  assert PLAYERS_NUMBER * 2 + 1 == len(ts)
  for t in ts:
    assert t.rect.bottom < SCREEN_HEIGHT
    assert t.rect.top > 0
    assert t.rect.right < SCREEN_WIDTH
    assert t.rect.left > 0
    assert pygame.sprite.spritecollideany(t, ts)
