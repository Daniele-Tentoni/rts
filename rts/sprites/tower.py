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
limits_per_level = [{ 'min': 0, 'max': 10 }]

class Tower(Sprite):
  """
  Tower definition.

  It contains method to draw it and update his position. You can update his position without drawing it.
  """
  level: int = 1
  soldiers: Group

  def __init__(self, x: float, y: float) -> None:
    """Creates a new Tower entity.

    Create a new Tower entity with a surface and a rectangle.

    Args:
        x (float): initial position
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
    import rts.sprites.soldier
    for soldier in self.soldiers:
      if isinstance(soldier, rts.sprites.soldier.Soldier):
        soldier.arrange()

  def spawn_soldier(self):
    """Spawn a soldier near the tower.

    Spawn a soldier near the tower, given her center coordinates. Then, add the
    new sprite to soldier tower sprite group and return it.

    Returns:
      [rts.sprites.soldier.Soldier | None]: New Soldier created or None value
        if the soldier was not created, like when the soldier limit is reach.
    """
    import rts.sprites.soldier

    max_soldiers = limits_per_level[self.level - 1]['max']
    if len(self.soldiers) < max_soldiers:
      new_soldier = rts.sprites.soldier.Soldier(self)
      self.soldiers.add(new_soldier)
      return new_soldier

    return None
