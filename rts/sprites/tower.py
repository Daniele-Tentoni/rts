import random
from typing import Sequence

from rts.constants import (
  TOWER_SIZE,
  TOWER_COLOR,

  SCREEN_WIDTH,
  SCREEN_HEIGHT
)

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

from pygame import Surface
from pygame.sprite import Group, Sprite

# Array with soldiers limits per level for towers
# First one is the minimum, the second one is the maximum.
limits_per_level = [(0, 10)]

class Tower(Sprite):
  """
  Tower definition.

  It contains method to draw it and update his position. You can update his position without drawing it.
  """
  level: int = 1
  soldiers: Group

  def __init__(self, x: float, y: float) -> None:
    """Creates a new Tower instance.

    Create a new Tower instance with a surface and a rectangle.

    Args:
        x (float): initial position.
        y (float): initial position
    """
    super(Tower, self).__init__()
    self.surf = Surface(TOWER_SIZE)
    self.surf.fill(TOWER_COLOR)
    self.rect = self.surf.get_rect()
    self.rect.move_ip(x, y)
    self.soldiers = Group()

  def update(self):
    """
    Update the position of each soldier assigned to the tower.
    """
    for soldier in self.soldiers:
      random_x = random.randint(
        self.rect.centerx + 10,
        self.rect.centerx + 50
      )
      random_y = random.randint(
        self.rect.centery + 10,
        self.rect.centery + 50
      )
      soldier.rect.move_ip(random_x, random_y)

  def draw(self, screen: Surface) -> None:
    """
    Draw on given screen the tower surface.

    Args:
        screen (Surface): Screen Surface.
    """
    screen.blit(self.surf, self.rect) # (self.x, self.y)

  def spawn_soldier(self):
    import rts.sprites.soldier

    if len(self.soldiers) < limits_per_level[self.level - 1][1]:
      new_soldier = rts.sprites.soldier.Soldier(self)
      self.soldiers.add(new_soldier)
      return new_soldier

    return None
