import random
from typing import Sequence

from rts.constants import (
  FONT_NAME,
  FONT_SIZE,
  TEXT_COLOR,
  TOWER_SIZE,
  TOWER_COLOR,
)

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

from pygame import Surface
import pygame.font
from pygame.sprite import Group, Sprite

# Array with soldiers limits per level for towers
# First one is the minimum, the second one is the maximum.
limits_per_level = [{ 'min': 0, 'max': 10 }]

class Tower(Sprite):
  """
  Tower definition.

  It contains method to draw it and update his position. You can update his position without drawing it.
  """
  starting_coordinates: tuple[float, float]
  level: int = 1
  soldiers: Group
  soldiers_label: Surface
  show_soldiers: bool
  soldiers_updated: bool

  def __init__(self, x: float, y: float) -> None:
    """Creates a new Tower entity.

    Create a new Tower entity with a surface and a rectangle.
    Inside the tower is displayed the number of soldier defending it.

    Args:
        x (float): initial position
        y (float): initial position
    """
    super(Tower, self).__init__()

    self.starting_coordinates = (x, y)
    self.surf = Surface(TOWER_SIZE)
    self.surf.fill(TOWER_COLOR)
    self.rect = self.surf.get_rect()
    self.rect.move_ip(self.starting_coordinates)

    self.soldiers = Group()
    self.show_soldiers = True # TODO: Let user toggle soldiers.
    self.soldiers_updated = True

  def update(self):
    """Update tower and her soldiers.

    Update the tower and the label of soldier assigned to the tower.
    """
    if self.show_soldiers:
      self.update_soldiers_label()

  def update_soldiers_label(self):
    """Update soldiers label inside tower.

    Update soldiers label content inside tower with the current length of
    soldiers sprite group. Remember to keep this updated.
    """
    self.surf.fill(TOWER_COLOR)
    sys_font = pygame.font.SysFont(pygame.font.get_default_font(), FONT_SIZE)
    self.soldiers_label = sys_font.render(
      str(len(self.soldiers)),
      True,
      TEXT_COLOR
    )
    textrect = self.soldiers_label.get_rect(center = self.surf.get_rect().center)
    self.surf.blit(self.soldiers_label, textrect)
    print(f"Update soldiers")

  def arrange_soldiers(self):
    import rts.sprites.soldier
    for soldier in self.soldiers:
      if isinstance(soldier, rts.sprites.soldier.Soldier):
        soldier.arrange()

  def spawn_soldier(self):
    """Spawn a soldier near the tower.

    Spawn a new soldier if is possible and return it. Otherwise return None.

    Returns:
      [rts.sprites.soldier.Soldier | None]: New Soldier created or None value
        if the soldier was not created, like when the soldier limit is reach.
    """
    max_soldiers = limits_per_level[self.level - 1]['max']
    if len(self.soldiers) < max_soldiers:
      return self.add_soldier()
    return None

  def add_soldier(self):
    """Spawn a new soldier.

    Spawn a soldier near the tower, given her center coordinates. Then, add the
    new sprite to soldier tower sprite group and return it.

    Returns:
      [rts.sprites.soldier.Soldier]: New Soldier created
    """
    import rts.sprites.soldier
    new_soldier = rts.sprites.soldier.Soldier(self)
    self.soldiers.add(new_soldier)
    self.soldiers_updated = True
    return new_soldier
