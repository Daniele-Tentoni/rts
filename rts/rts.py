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

from .constants import (
  TOWER_WIDTH,
  TOWER_HEIGHT,
  TOWER_COLOR,

  SCREEN_WIDTH,
  SCREEN_HEIGHT
)

from .tower import Tower

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

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

towers: list[Tower] = list()

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
    # movement = move_towers(event)
    # if movement[0] is not 0 and movement[1] is not 0:
      # for t in towers:
        # print(f"TOWER {t.x} {t.y}")
        # t.move(movement[0] * speed, movement[1] * speed)

  pressed_keys = pygame.key.get_pressed()
  for t in towers:
    t.move(pressed_keys)

  # Draw towers
  for t in towers:
    t.draw(screen)

  # Flip the display
  pygame.display.flip()

  return running

def main():
  pygame.init()

  # Init towers
  for t in range(0, 2):
    x: float = SCREEN_WIDTH / 3 * (t + 1)
    y: float = SCREEN_HEIGHT / 2
    towers.append(Tower(x, y))

  running = True
  while running:
    running = game_cycle()

  pygame.quit()
