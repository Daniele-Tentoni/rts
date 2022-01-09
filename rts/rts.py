# Imports

import random
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

import rts.sprites.tower
import rts.sprites.ruler

from .constants import (
  GAME_NAME,
  PLAYERS_NUMBER,
  SCREEN_COLOR,
  SCREEN_WIDTH,
  SCREEN_HEIGHT,
  TEXT_COLOR,
)

# Globals

pygame.font.init()
sys_font = SysFont("Arial", 14)

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption(GAME_NAME)
label = sys_font.render("Send soldiers from your tower to enemies ones to conquer them.", 1, TEXT_COLOR)

# ADD SOLDIERS EVENT ID
ADDSOLDIERS = pygame.USEREVENT + 1

factor = 1.5
speed = 1.5

class GameInstance:
  current_ruler: rts.sprites.ruler.Ruler
  rulers: Group
  towers: Group
  soldiers: Group
  all_sprites: Group

  def __init__(self) -> None:
    """Init the game view.

    Init the game instance, adding rulers and their towers. Create events to
    spawn soldiers in each tower.
    """
    self.all_sprites = Group()
    self.rulers = Group()
    self.soldiers = Group()
    self.towers = Group()
    self.init_rulers()
    self.init_towers()
    pygame.time.set_timer(ADDSOLDIERS, 1000)

  def init_rulers(self) -> None:
    """Init rulers in this game instance.

    Init rulers, showing who is controlled by current players and who is not.
    They will be marked differently. Number of rulers in game depends on the
    game mode and will be modified in the future.
    """
    # Create ruler for current player
    self.current_ruler = rts.sprites.ruler.Ruler(
      random.randint(0, SCREEN_WIDTH),
      random.randint(0, SCREEN_HEIGHT)
      )
    self.rulers.add(self.current_ruler)
    self.all_sprites.add(self.current_ruler)

    # Create ruler for each enemy player
    for n in range(0, PLAYERS_NUMBER - 1):
      new_ruler = rts.sprites.ruler.Ruler(
        random.randint(0, SCREEN_WIDTH),
        random.randint(0, SCREEN_HEIGHT)
        )
      self.rulers.add(new_ruler)
      self.all_sprites.add(new_ruler)

  def init_towers(self) -> None:
    # Init towers
    for t in range(0, PLAYERS_NUMBER * 2):
      x: float = SCREEN_WIDTH / 3 * (t + 1)
      y: float = SCREEN_HEIGHT / 2
      tower = rts.sprites.tower.Tower(x, y)
      self.add_sprite_to(tower, self.towers)

    # TODO: Select a random tower, assign it to a ruler and place it near tower.
    # TODO: All other tower will be marked as unclaimed.

  def add_soldiers_to_towers(self) -> None:
    """Add soldiers to any tower.

    For any tower that can spawn soldiers, create one and spawn near it.

    A tower could spawn a soldier if it has not reached the maximum limit.
    """
    for tower in self.towers:
      if isinstance(tower, rts.sprites.tower.Tower):
        soldier = tower.spawn_soldier()
        if soldier is not None:
          self.add_sprite_to(soldier, self.soldiers)
          screen.blit(soldier.surf, soldier.rect)
          print(f"sprites have {len(self.all_sprites)}")

  def game_cycle(self) -> bool:
    """Run a single game cycle.

    Run a single game cycle and return if the game as to be closed or not.

    Returns:
        bool: True if the game has to be closed, false otherwise.
    """
    running = True

    # Clean the screen
    screen.fill(SCREEN_COLOR)

    screen.blit(label, (80, 40))
    soldiers_label = sys_font.render(f"Soldiers spawn {self.soldiers}.", 1, TEXT_COLOR)
    screen.blit(soldiers_label, (80, 80))

    # Did the user click the window close button?
    for event in pygame.event.get():
      if quit_game(event):
        running = False
      elif event.type == ADDSOLDIERS:
        self.add_soldiers_to_towers()

    pressed_keys = pygame.key.get_pressed()
    self.current_ruler.update(pressed_keys)
    self.towers.update()

    self.soldiers.update()

    # Draw all sprites
    for sprite in self.all_sprites:
      # if isinstance(sprite, Soldier):
        # print(f"Soldier {sprite.rect}")
      screen.blit(sprite.surf, sprite.rect)

    for soldier in self.soldiers:
      screen.blit(soldier.surf, soldier.rect)

    # Check if any enemies have collided with the player
    # for tower in self.towers:
      # if pygame.sprite.spritecollideany(tower, self.soldiers):
        # If so, then remove the player and stop the loop
        # tower.kill()
        # if len(self.towers) == 0:
          # running = False

    # Flip the display
    pygame.display.flip()

    return running

  def add_sprite_to(
    self,
    sprite: pygame.sprite.Sprite,
    group: pygame.sprite.Group,
    ):
    group.add(sprite)
    self.all_sprites.add(sprite)

def quit_game(event: Event) -> bool:
  """
  Checks for the quit game condition.

  Args:
      event ([type]): event from pygame.

  Returns:
      bool: True if quit is required, false otherwise.
  """
  return event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE

def main():
  """Main function, entry point of the game.

  Init pygame library, game view and start the game cycle.
  """
  pygame.init()

  instance = GameInstance()

  running = True
  while running:
    # Continue to run the game until has to be closed.
    running = instance.game_cycle()

  pygame.quit()
