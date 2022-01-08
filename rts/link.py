from rts.tower import Tower
from .constants import (
  LINK_COLOR,
  LINK_HEIGHT,
  TOWER_COLOR
)

from pygame import Surface
from pygame.sprite import Sprite

class Link(Sprite):
  """
  Link between two towers.

  One tower linked to another send troupes to attack or defend it.

  Args:
      Sprite ([type]): [description]
  """

  def __init(self, fromm: Tower, to: Tower) -> None:
    """
    Creates a new Link instance.

    Draw a surface between from tower 'from' to 'to'.

    Args:
        fromm (Tower): [description]
        to (Tower): [description]
    """
    super(Link, self).__init__()
    self.surf = Surface((LINK_HEIGHT, LINK_HEIGHT))
    self.surf.fill(LINK_COLOR)
    self.rect = self.surf.get_rect()