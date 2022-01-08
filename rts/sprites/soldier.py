import random

from pygame import Surface
from pygame.sprite import Sprite

from rts.constants import (
  LINK_COLOR,
  LINK_SIZE,
  SCREEN_WIDTH,
  SCREEN_HEIGHT
)

import rts.sprites.tower

class Soldier(Sprite):

  mother_tower: rts.sprites.tower.Tower

  def __init__(self, mother_tower: rts.sprites.tower.Tower) -> None:
    """
    Create a new Soldier entity.

    Args:
        mother_tower (Tower): This is the mother tower, where the soldier has been generated.
    """
    if not mother_tower:
      raise ValueError('mother_tower argument must be valued')

    super(Soldier, self).__init__()

    self.tower = mother_tower

    # Sprite stuff.
    self.surf = Surface(LINK_SIZE)
    self.surf.fill(LINK_COLOR)

    random_x = random.randint(
      self.tower.rect.centerx + 10,
      self.tower.rect.centerx + 50
      )
    random_y = random.randint(
      self.tower.rect.centery + 10,
      self.tower.rect.centery + 50
      )
    self.rect = self.surf.get_rect(center = (random_x, random_y))
    self.speed = random.randint(1, 3)

  def update(self):
    """
    Update the soldier location.

    If it get out of screen, the Sprite is removed from every Group to which
    belongs, removing the reference to it as well. This allow garbage collector
    to reclaim the memory as necessary.
    """
    # self.rect.move_ip(-self.speed / 2, 0)
    if self.rect.right < 0:
      self.kill() # Remove from screen and memory.
