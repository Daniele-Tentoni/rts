from random import randint

from pygame import K_DOWN, K_LEFT, K_RIGHT, K_UP, Surface
from pygame import display, font, mouse, draw
from pygame import (
  K_w, K_a, K_s, K_d,
  MOUSEBUTTONUP, MOUSEBUTTONDOWN,
)
from pygame.event import Event
from pygame.locals import (
  K_ESCAPE,
  QUIT,
)

from rts.config import *
from rts.models.game_entity import GameEntity
from rts.controllers.entity_controller import EntityController
from rts.controllers.event_controller import EventController
from rts.sprites.ruler import Ruler
from rts.sprites.soldier import Soldier
from rts.sprites.tower import Tower

class Game:
  running: bool
  routes: list[tuple[tuple[float, float], tuple[float, float]]]
  tower_traced: Tower

  # Reference to the controllers
  entity_controller: EntityController
  event_controller: EventController

  # Screen properties used during rendering
  screen: Surface
  sys_font: font.Font

  # Number of players in the game
  rulers_number: int

  # Constructor
  def __init__(self, screen: Surface, rulers_number: int = 2) -> None:
    """Init the game view.

    Init the game instance, adding rulers and their towers.

    Args:
      screen (pygame.Surface):
        screen where game is displayed.
      rulers_number (int):
        number of rulers in play.
    """

    self.running = False
    self.routes = list()
    self.tower_traced = None

    # Reference to the controllers
    self.entity_controller = EntityController()
    self.entity_controller.reset()
    self.event_controller = EventController()
    self.event_controller.reset()

    # Instance unique properties
    self.screen = screen
    self.sys_font = font.SysFont(font.get_default_font(), FONT_SIZE)
    self.rulers_number = rulers_number

    # Initialization of the main entities
    self.init_rulers()
    self.init_towers()

  # Generates the rulers of the game
  def init_rulers(self) -> None:
    """Init rulers in this game instance.

    Init rulers, showing who is controlled by current players and who is not.
    They will be marked differently. Number of rulers in game depends on the
    game mode and will be modified in the future.
    """

    # Creates a ruler for each player and adds it to the list
    for n in range(self.rulers_number):
      # Generates the position
      x: float = randint(0, SCREEN_WIDTH)
      y: float = randint(0, SCREEN_HEIGHT)

      # Creates the instance
      ruler = Ruler(GameEntity(x, y, RULER_COLOR, RULER_SIZE), 1)

      # Assigns the first ruler to the player by adding the movement events
      # TODO: Add arrows movement, maybe?
      if n == 0:
        self.event_controller.register_key_event(K_w, ruler.move_up)
        self.event_controller.register_key_event(K_a, ruler.move_left)
        self.event_controller.register_key_event(K_s, ruler.move_down)
        self.event_controller.register_key_event(K_d, ruler.move_right)
        self.event_controller.register_key_event(K_UP, ruler.move_up)
        self.event_controller.register_key_event(K_LEFT, ruler.move_left)
        self.event_controller.register_key_event(K_DOWN, ruler.move_down)
        self.event_controller.register_key_event(K_RIGHT, ruler.move_right)

      # if n > 0: # move other rulers from sockets events

      # Adds the instance to the list
      self.entity_controller.register_entity(ruler)

  # Generates the towers of the game
  # TODO: Select a random tower, assign it to a ruler and place it near tower.
  # TODO: All other tower will be marked as unclaimed.
  def init_towers(self) -> None:
    # Sets up the timer event associated to soldier generation
    add_soldiers = self.event_controller.register_time_event(1000)

    # Creates two towers for each player
    for n in range(PLAYERS_NUMBER * 2):
      # Generates the position
      x: float = SCREEN_WIDTH / 3 * (n + 1)
      y: float = SCREEN_HEIGHT / 2

      # Creates the instance and adds it to the list
      tower = Tower(
        e= GameEntity(x, y, TOWER_COLOR, TOWER_SIZE),
        level= 1,
        soldier_color= SOLDIER_COLOR,
        soldier_size= SOLDIER_SIZE,
        soldier_gen_ratio= 0.001)
      self.entity_controller.register_entity(tower)
      self.event_controller.register_time_callback(add_soldiers, tower.create_soldiers)

  # Keeps computing and showing frames until exit is requested
  def game_loop(self) -> None:

    # Game loop exit flag
    self.running = True

    # Exit event
    #TODO: Need to define event.type = QUIT
    def stop_loop():
      self.running = False

    self.event_controller.register_key_event(K_ESCAPE, stop_loop)
    self.event_controller.register_time_callback(QUIT, stop_loop)

    # Keeps looping until exit is required
    while self.running:
      # Screen cleaning
      self.screen.fill(SCREEN_COLOR)

      # System label rendering
      label = self.sys_font.render("To conquer enemy towers, send them soldiers from your towers.", 1, TEXT_COLOR)
      self.screen.blit(label, (80, 40))

      #TODO: Compute DELTA_TIME

      # Events manager
      self.event_controller.handle_events()
      '''
        elif self.has_to_un_trace(event):
          self.stop_trace()
          self.tower_traced = None
        elif self.has_to_trace(event):
          self.tower_traced = self.start_trace()
      '''

      # Towers update
      if self.entity_controller.has(Tower):
        towers = self.entity_controller.entity_dict[Tower]
        for tower in towers:
          tower.update()
          self.screen.blit(tower.surf, tower.rect)

      # Route updates
      if self.tower_traced is not None:
        tower_pos = self.tower_traced.rect.center
        mouse_pos = mouse.get_pos()
        draw.line(self.screen, TEXT_COLOR, tower_pos, mouse_pos)
        state_string = f"Tower click {self.tower_traced.rect.right}."
        state_label = self.sys_font.render(state_string, 1, TEXT_COLOR)
        self.screen.blit(state_label, (80, 80))

      for route in self.routes:
        draw.line(self.screen, TEXT_COLOR, route[0], route[1])

      # Soldiers updates
      if Soldier in self.entity_controller.entity_dict.keys():
        soldiers = self.entity_controller.entity_dict[Soldier]
        for soldier in soldiers:
          soldier.update()
          self.screen.blit(soldier.surf, soldier.rect)

      # Rulers update
      if Ruler in self.entity_controller.entity_dict.keys():
        rulers = self.entity_controller.entity_dict[Ruler]
        for ruler in rulers:
          ruler.update()
          self.screen.blit(ruler.surf, ruler.rect)

      # Renders the scene
      display.flip()

  def has_to_un_trace(self, event: Event) -> bool:
    return event.type == MOUSEBUTTONUP and mouse.get_pressed() == (0, 0, 0) and self.tower_traced is not None

  def has_to_trace(self, event: Event) -> bool:
    return event.type == MOUSEBUTTONDOWN and mouse.get_pressed() == (1, 0, 0) and self.tower_traced is None

  def start_trace(self) -> Tower:
    pos = mouse.get_pos()
    for tower in self.towers:
      if tower_clicked(tower, pos):
        return tower
    return None

  def stop_trace(self) -> None:
    pos = mouse.get_pos()
    remaining_towers = (t for t in self.towers if t is not self.tower_traced)
    for tower in remaining_towers:
      if tower_clicked(tower, pos):
        future_tuple = (self.tower_traced.rect.center, tower.rect.center)
        #TODO: Change the type to set instead of list? Performance improvement?
        if future_tuple not in self.routes:
          print("link")
          self.routes.append(future_tuple)

def tower_clicked(tower: Tower, mouse) -> bool:
  return tower.rect.right > mouse[0] > tower.rect.left and tower.rect.bottom > mouse[1] > tower.rect.top
