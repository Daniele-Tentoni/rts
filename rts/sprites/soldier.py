from cmath import atan, cos, sin
from random import randint

from controllers.time_controller import DELTA_TIME
from models.game_entity import GameEntity

class Soldier(GameEntity):
  # Position the soldier is binded to
  #TODO: Maybe change it to a particular entity?
  origin: tuple(float, float)
  origin_radius: float

  # Speed of the soldier
  speed: float

  # Constructor
  def __init__(self, e: GameEntity, origin: tuple(float, float),
    origin_radius: float, speed: float) -> None:
    """
    Create a new Soldier entity.

    Create a new Tower entity with a surface and a rectangle.

    Args:
        mother_tower (Tower): This is the mother tower, where the soldier has been generated.
    """

    # Base class initialization
    super(Soldier, self).__init__(e.x, e.y, e.color, e.size)

    # Instance unique properties
    self.origin = origin
    self.speed = speed

  # Updates the state of the instance
  def update(self) -> None:
    """
    Update the soldier location.

    If it get out of screen, the Sprite is removed from every Group to which
    belongs, removing the reference to it as well. This allow garbage collector
    to reclaim the memory as necessary.
    """

    # Updates the position of the instance
    self.update_position()

  # Moves the instance in a random way
  def update_position(self) -> None:
    # Generates the displacement
    delta_x = randint(-1, 1) * self.speed * DELTA_TIME
    delta_y = randint(-1, 1) * self.speed * DELTA_TIME

    # Updates the position of the instance
    self.x += delta_x
    self.y += delta_y

    # Moves the rectangle of the soldier
    self.update_rect()
  
  # Moves the rect of the ruler according to the current entity coordinates
  def update_rect(self) -> None:
    # Checks the position limit by looking at the center position only
    #TODO: Rectangle thickness is not checked, is it important?
    if self.x ** 2 + self.y ** 2 > self.origin_radius ** 2:
      # Moves the center radially towards the center
      #TODO: Verify if the atan is the correct function
      angle = atan(self.y / self.x)
      self.x = self.origin_radius * cos(angle)
      self.y = self.origin_radius * sin(angle)

    # Moves the rect of the instance
    self.rect.center = (self.x, self.y)