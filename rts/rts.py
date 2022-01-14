# Imports

import random
import pygame
import pygame.font

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

import rts.sprites.tower
import rts.sprites.ruler

from .constants import (
  FONT_NAME,
  FONT_SIZE,
  GAME_NAME,
  PLAYERS_NUMBER,
  SCREEN_COLOR,
  SCREEN_WIDTH,
  SCREEN_HEIGHT,
  TEXT_COLOR,
)

# ADD SOLDIERS EVENT ID
ADDSOLDIERS = pygame.USEREVENT + 1
UPDATESOLDIERS = ADDSOLDIERS + 1

factor = 1.5
speed = 1.5

class GameInstance:
  all_sprites: Group
  current_ruler: rts.sprites.ruler.Ruler
  rulers: Group
  screen: pygame.Surface
  soldiers: Group
  sys_font: pygame.font.Font
  tower_traced: rts.sprites.tower.Tower
  towers: Group

  def __init__(self, screen: pygame.Surface, npc: int = 1) -> None:
    """Init the game view.

    Init the game instance, adding rulers and their towers. Create events to
    spawn soldiers in each tower.

    Creating game instance without giving the number of non playable characters
    to the constructor means that we want to generate a game with only 2
    players: one for the current user, one for the computer.

    Args:
      screen (pygame.Surface): screen where game is displayed.
      npc (int): number of non playable characters.
    """
    self.all_sprites = Group()
    self.npc = npc
    self.rulers = Group()
    self.screen = screen
    self.soldiers = Group()
    self.sys_font = pygame.font.SysFont(pygame.font.get_default_font(), FONT_SIZE)
    self.tower_traced = None
    self.towers = Group()

    self.init_rulers()
    self.init_towers()
    pygame.time.set_timer(ADDSOLDIERS, 1000)
    pygame.time.set_timer(UPDATESOLDIERS, 100)

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
    for n in range(0, self.npc):
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
          self.screen.blit(soldier.surf, soldier.rect)

  def arrange_soldiers(self) -> None:
    for tower in self.towers:
      if isinstance(tower, rts.sprites.tower.Tower):
        tower.arrange_soldiers()

  def game_cycle(self) -> bool:
    """Run a single game cycle.

    Run a single game cycle and return if the game as to be closed or not.

    Returns:
        bool: True if the game has to be closed, false otherwise.
    """
    running = True

    # 1. Screen cleaning
    self.screen.fill(SCREEN_COLOR)

    # 2. System label writing
    label = self.sys_font.render("Send soldiers from your tower to enemies ones to conquer them.", 1, TEXT_COLOR)
    self.screen.blit(label, (80, 40))

    # 3. Events managing
    for event in pygame.event.get():
      if quit_game(event):
        running = False
      elif event.type == ADDSOLDIERS:
        self.add_soldiers_to_towers()
      elif event.type == UPDATESOLDIERS:
        self.arrange_soldiers()
      elif self.has_to_un_trace(event):
        self.stop_trace()
        self.tower_traced = None
      elif self.has_to_trace(event):
        self.tower_traced = self.start_trace()

    # 4. Ruler updates
    pressed_keys = pygame.key.get_pressed()
    self.current_ruler.update(pressed_keys)

    # 5. Tower updates
    self.towers.update()

    # 5b. Route updates
    if self.tower_traced is not None:
      tower_pos = self.tower_traced.rect.center
      mouse_pos = pygame.mouse.get_pos()
      pygame.draw.line(self.screen, TEXT_COLOR, tower_pos, mouse_pos)
      state_string = f"Tower click {self.tower_traced.rect.right}."
      state_label = self.sys_font.render(state_string, 1, TEXT_COLOR)
      self.screen.blit(state_label, (80, 80))

    # 6. Other soldiers updates
    self.soldiers.update()

    # 7. Blit all
    for sprite in self.all_sprites:
      self.screen.blit(sprite.surf, sprite.rect)

    # for soldier in self.soldiers:
      # screen.blit(soldier.surf, soldier.rect)

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

  def has_to_un_trace(self, event: pygame.event.Event) -> bool:
    return event.type == pygame.MOUSEBUTTONUP and pygame.mouse.get_pressed() == (0, 0, 0) and self.tower_traced is not None

  def has_to_trace(self, event: pygame.event.Event) -> bool:
    return event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed() == (1, 0, 0) and self.tower_traced is None

  def start_trace(self) -> rts.sprites.tower.Tower:
    pos = pygame.mouse.get_pos()
    for tower in self.towers:
      if tower.rect.right > pos[0] > tower.rect.left and tower.rect.bottom > pos[1] > tower.rect.top:
        return tower
    return None

  def stop_trace(self) -> None:
    pass

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
  pygame.font.init()

  pygame.display.set_caption(GAME_NAME)
  screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
  instance = GameInstance(screen)

  running = True
  while running:
    # Continue to run the game until has to be closed.
    running = instance.game_cycle()

  pygame.font.quit()
  pygame.quit()
