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
from pygame.sprite import Group

from rts.soldier import Soldier

from .constants import (
  TOWER_WIDTH,
  TOWER_HEIGHT,
  TOWER_COLOR,

  SCREEN_WIDTH,
  SCREEN_HEIGHT
)

from .tower import Tower

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Real Time Strategy')

# ADD SOLDIERS EVENT ID
ADDSOLDIERS = pygame.USEREVENT + 1

factor = 1.5
speed = 1.5

def quit_game(event) -> bool:
  """
  Checks for the quit game condition.

  Args:
      event ([type]): event from pygame.

  Returns:
      bool: True if quit is required, false otherwise.
  """
  return event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE

towers: Group = Group()
soldiers: Group = Group()
all_sprites: Group = Group()

def create_tower(towers: list[Tower]):
  towers.append(Tower(0, 0))

def game_cycle() -> None:
  running = True

  # Clean the screen
  screen.fill((21, 21, 21))

  # Did the user click the window close button?
  for event in pygame.event.get():
    if quit_game(event):
      running = False
    elif event.type == ADDSOLDIERS:
      soldier = Soldier()
      soldiers.add(soldier)
      all_sprites.add(soldier)

  pressed_keys = pygame.key.get_pressed()
  towers.update(pressed_keys)
    # t.move(pressed_keys)

  soldiers.update()

  # Draw towers
  for sprite in all_sprites:
    screen.blit(sprite.surf, sprite.rect)

  # Flip the display
  pygame.display.flip()

  return running

def create_objects() -> None:
  # Init towers
  for t in range(0, 2):
    x: float = SCREEN_WIDTH / 3 * (t + 1)
    y: float = SCREEN_HEIGHT / 2
    tower = Tower(x, y)
    towers.add(tower)
    all_sprites.add(tower)

  pygame.time.set_timer(ADDSOLDIERS, 250)

def main():
  pygame.init()

  create_objects()

  running = True
  while running:
    running = game_cycle()

  pygame.quit()
