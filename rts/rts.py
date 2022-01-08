# Imports

import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT,
)
from pygame.event import Event
from pygame.sprite import Group
from pygame.font import SysFont

from rts.sprites.tower import Tower

from .constants import (
  GAME_NAME,
  TEXT_COLOR,
  TOWER_WIDTH,
  TOWER_HEIGHT,
  TOWER_COLOR,

  SCREEN_WIDTH,
  SCREEN_HEIGHT
)

# Globals

pygame.font.init()
sys_font = SysFont("Arial", 14)

towers: Group = Group()
soldiers: Group = Group()
all_sprites: Group = Group()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption(GAME_NAME)
label = sys_font.render("Send soldiers from your tower to enemies ones to conquer them.", 1, TEXT_COLOR)

# ADD SOLDIERS EVENT ID
ADDSOLDIERS = pygame.USEREVENT + 1

factor = 1.5
speed = 1.5

def quit_game(event: Event) -> bool:
  """
  Checks for the quit game condition.

  Args:
      event ([type]): event from pygame.

  Returns:
      bool: True if quit is required, false otherwise.
  """
  return event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE

def create_tower(towers: list[Tower]) -> None:
  towers.append(Tower(0, 0))

def game_cycle() -> bool:
  """Run a single game cycle.

  Run a single game cycle and return if the game as to be closed or not.

  Returns:
      bool: True if the game has to be closed, false otherwise.
  """
  running = True

  # Clean the screen
  screen.fill((21, 21, 21))

  screen.blit(label, (80, 40))

  # Did the user click the window close button?
  for event in pygame.event.get():
    if quit_game(event):
      running = False
    elif event.type == ADDSOLDIERS:
      add_soldiers_to_towers()

  pressed_keys = pygame.key.get_pressed()
  towers.update(pressed_keys)

  soldiers.update()

  # Draw all sprites
  for sprite in all_sprites:
    screen.blit(sprite.surf, sprite.rect)

  # Check if any enemies have collided with the player
  for tower in towers:
    if pygame.sprite.spritecollideany(tower, soldiers):
      # If so, then remove the player and stop the loop
      tower.kill()
      if len(towers) == 0:
        running = False

  # Flip the display
  pygame.display.flip()

  return running

def add_soldiers_to_towers() -> None:
  """Add soldiers to any tower.

  For any tower that can spawn soldiers, create one and spawn near it.

  A tower could spawn a soldier if it has not reached the maximum limit.
  """
  for tower in towers:
    soldier = tower.spawn_soldier()
    if soldier is not None:
      soldiers.add(soldier)
      all_sprites.add(soldier)

def init_game_view() -> None:
  """Init the game view.

  Init the game view, adding players and their towers. Create events to spawn soldiers in each tower.
  """
  # Init towers
  for t in range(0, 2):
    x: float = SCREEN_WIDTH / 3 * (t + 1)
    y: float = SCREEN_HEIGHT / 2
    tower = Tower(x, y)
    towers.add(tower)
    all_sprites.add(tower)

  pygame.time.set_timer(ADDSOLDIERS, 1000)

def main():
  pygame.init()

  init_game_view()

  running = True
  while running:
    # Continue to run the game until has to be closed.
    running = game_cycle()

  pygame.quit()
