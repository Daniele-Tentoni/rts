import random

from pygame import Surface
from pygame.sprite import Sprite

from .constants import (
  LINK_COLOR,
  LINK_SIZE,
  SCREEN_WIDTH,
  SCREEN_HEIGHT
)

class Soldier(Sprite):
  def __init__(self) -> None:
    super(Soldier, self).__init__()
    self.surf = Surface(LINK_SIZE)
    self.surf.fill(LINK_COLOR)
    self.rect = self.surf.get_rect(
      center = (
        random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), # Start outside the screen.
        random.randint(0 + 5, SCREEN_HEIGHT - 5) # Start inside the screen.
      )
    )
    self.speed = random.randint(1, 5)

  def update(self):
    """
    Update the soldier location.

    If it get out of screen, the Sprite is removed from every Group to which
    belongs, removing the reference to it as well. This allow garbage collector
    to reclaim the memory as necessary.
    """
    self.rect.move_ip(-self.speed, 0)
    if self.rect.right < 0:
      self.kill() # Remove from screen and memory.
