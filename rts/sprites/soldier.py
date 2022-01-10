import random

from pygame import Surface
import pygame.sprite

from rts.constants import (
  SOLDIER_COLOR,
  SOLDIER_RADIUS_AROUND_TOWER,
  SOLDIER_SIZE,
)

import rts.sprites.tower

class Soldier(pygame.sprite.Sprite):

  mother_tower: rts.sprites.tower.Tower

  def __init__(self, mother_tower: rts.sprites.tower.Tower) -> None:
    """
    Create a new Soldier entity.

    Create a new Tower entity with a surface and a rectangle.

    Args:
        mother_tower (Tower): This is the mother tower, where the soldier has been generated.
    """
    if not mother_tower:
      raise ValueError('mother_tower argument must be valued')

    super(Soldier, self).__init__()

    # Sprite stuff.
    self.surf = Surface(SOLDIER_SIZE)
    self.surf.fill(SOLDIER_COLOR)

    base_x = mother_tower.rect.centerx
    base_y = mother_tower.rect.centery
    random_x = random.randint(base_x + 10, base_x + 50)
    random_y = random.randint(base_y + 10, base_y + 50)
    self.rect = self.surf.get_rect(center = (random_x, random_y))

    self.speed = 0.5

    self.mother_tower = mother_tower

  def update(self):
    """
    Update the soldier location.

    If it get out of screen, the Sprite is removed from every Group to which
    belongs, removing the reference to it as well. This allow garbage collector
    to reclaim the memory as necessary.
    """
    # self.rect.move_ip(-self.speed / 2, 0)
    if self.rect.right < 0:
      print(f"killed")
      self.kill() # Remove from screen and memory.

  def arrange(self):
    random_x = random.randint(-1, 1) * self.speed
    random_y = random.randint(-1, 1) * self.speed
    self.rect.move_ip((random_x, random_y))

    if self.rect.left < self.mother_tower.rect.left + SOLDIER_RADIUS_AROUND_TOWER:
      self.rect.left = self.mother_tower.rect.left + SOLDIER_RADIUS_AROUND_TOWER
    if self.rect.right > self.mother_tower.rect.right + SOLDIER_RADIUS_AROUND_TOWER:
      self.rect.right = self.mother_tower.rect.right + SOLDIER_RADIUS_AROUND_TOWER
    if self.rect.top < self.mother_tower.rect.top + SOLDIER_RADIUS_AROUND_TOWER:
      self.rect.top = self.mother_tower.rect.top + SOLDIER_RADIUS_AROUND_TOWER
    if self.rect.bottom > self.mother_tower.rect.bottom + SOLDIER_RADIUS_AROUND_TOWER:
      self.rect.bottom = self.mother_tower.rect.bottom + SOLDIER_RADIUS_AROUND_TOWER

    # TODO: resolve any possible collision with other soldiers and tower
