import copy
import pygame
from pygame.constants import (
  K_a,
  K_d,
  K_s,
  K_w,
)
import pytest

from rts.sprites.ruler import Ruler

@pytest.fixture
def sample_ruler() -> tuple[Ruler, pygame.rect.Rect]:
  ruler = Ruler(1, 1)
  rect = copy.deepcopy(ruler.rect)
  return (ruler, rect)

def test__right_horizontal_movement(
  sample_ruler: tuple[Ruler, pygame.rect.Rect],
) -> None:
  ruler, rect = sample_ruler
  attr_dict: dict[int, bool] = { K_d: True }
  ruler.update(attr_dict)
  assert rect.left < ruler.rect.left
  assert rect.top == ruler.rect.top


def test_left_horizontal_movement(
  sample_ruler: tuple[Ruler, pygame.rect.Rect],
) -> None:
  ruler, rect = sample_ruler
  attr_dict: dict[int, bool] = { K_a: True }
  ruler.update(attr_dict)
  assert rect.left > ruler.rect.left
  assert rect.top == ruler.rect.top

def test_upper_vertical_movement(
  sample_ruler: tuple[Ruler, pygame.rect.Rect],
) -> None:
  ruler, rect = sample_ruler
  attr_dict: dict[int, bool] = { K_w: True }
  ruler.update(attr_dict)
  assert rect.left == ruler.rect.left
  assert rect.top > ruler.rect.top

def test_movement(
  sample_ruler: tuple[Ruler, pygame.rect.Rect],
) -> None:
  ruler, rect = sample_ruler
  attr_dict: dict[int, bool] = { K_s: True }
  ruler.update(attr_dict)
  assert rect.left == ruler.rect.left
  assert rect.top < ruler.rect.top