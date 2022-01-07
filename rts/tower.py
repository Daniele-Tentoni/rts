from typing import Sequence

from .constants import (
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
from pygame.sprite import Sprite

class Tower(Sprite):
  """
  Tower definition.

  It contains method to draw it and update his position. You can update his position without drawing it.
  """

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

  def update(self, pressed_keys: Sequence[bool]):
    """
    Move the tower object by pressed keys event.
    This only change coordinates of the object. Use draw to
    report it on the screen.

    Args:
        pressed_keys (Sequence[bool]): events sequence.
    """
    x, y = (0.0, 0.0) # Deltas
    factor = 5
    if pressed_keys[K_UP]:
      y = -0.2 * factor
    if pressed_keys[K_DOWN]:
      y = 0.2 * factor
    if pressed_keys[K_LEFT]:
      x = -0.2 * factor
    if pressed_keys[K_RIGHT]:
      x = 0.2 * factor

    self.rect.move_ip(x, y)

    # Keep player on the screen
    if self.rect.left < 0:
      self.rect.left = 0
    if self.rect.right > SCREEN_WIDTH:
      self.rect.right = SCREEN_WIDTH
    if self.rect.top <= 0:
      self.rect.top = 0
    if self.rect.bottom >= SCREEN_HEIGHT:
      self.rect.bottom = SCREEN_HEIGHT

  def draw(self, screen: Surface) -> None:
    """
    Draw on given screen the tower surface.

    Args:
        screen (Surface): Screen Surface.
    """
    screen.blit(self.surf, self.rect) # (self.x, self.y)
