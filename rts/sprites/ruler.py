import pygame
from pygame.constants import (
  K_a,
  K_d,
  K_DOWN,
  K_LEFT,
  K_RIGHT,
  K_s,
  K_UP,
  K_w,
)
from typing import Sequence

import rts.constants

class Ruler(pygame.sprite.Sprite):
  """
  Ruler definition.

  A Ruler is the entity directly controller by the player.

  It contains method to draw it and update his position.

  Args:
    pygame (pygame.sprite.Sprite): Pygame Sprite.
  """

  def __init__(self, x: float, y: float) -> None:
    """
    Creates a new Ruler instance.

    Create a new Ruler instance with a surface and a rectangle.

    Args:
      x (float): initial horizontal position.
      y (float): initial vertical position.
    """
    super(Ruler, self).__init__()
    self.surf = pygame.Surface(rts.constants.RULER_SIZE)
    self.surf.fill(rts.constants.RULER_COLOR)
    self.rect = self.surf.get_rect()
    self.rect.move_ip(x, y)
    self.speed = 1

  def update(self, pressed_keys: Sequence[bool]):
    """
    Move the Ruler rectangle by pressed key event.

    Args:
      pressed_keys (Sequence[bool]): events sequence.
    """
    x, y = (0.0, 0.0)
    if K_UP in pressed_keys and pressed_keys[K_UP] or K_w in pressed_keys and pressed_keys[K_w]:
      y = -1 * self.speed
    if K_DOWN in pressed_keys and pressed_keys[K_DOWN] or K_s in pressed_keys and pressed_keys[K_s]:
      y = 1 * self.speed
    if K_LEFT in pressed_keys and pressed_keys[K_LEFT] or K_a in pressed_keys and pressed_keys[K_a]:
      x = -1 * self.speed
    if K_RIGHT in pressed_keys and pressed_keys[K_RIGHT] or K_d in pressed_keys and pressed_keys[K_d]:
      x = 1 * self.speed

    self.rect.move_ip(x, y)

    # Keep player on the screen
    if self.rect.left < 0:
      self.rect.left = 0
    if self.rect.right > rts.constants.SCREEN_WIDTH:
      self.rect.right = rts.constants.SCREEN_WIDTH
    if self.rect.top <= 0:
      self.rect.top = 0
    if self.rect.bottom >= rts.constants.SCREEN_HEIGHT:
      self.rect.bottom = rts.constants.SCREEN_HEIGHT

  def draw(self, screen: pygame.Surface) -> None:
    """
    Draw the Ruler on the given screen surface.

    Args:
      screen (pygame.Surface): Screen surface.
    """
    screen.blit(self.surf, self.rect)
