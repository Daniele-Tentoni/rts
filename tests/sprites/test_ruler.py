"""Unit tests for ruler sprite.

Check if any movement for the ruler work as expected.
"""

import copy
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
import pytest

import rts.constants
from rts.sprites.ruler import Ruler

@pytest.fixture
def top_left_ruler() -> tuple[Ruler, pygame.rect.Rect]:
  ruler = Ruler(2, 2)
  rect = copy.deepcopy(ruler.rect)
  return (ruler, rect)

@pytest.fixture
def bottom_right_ruler() -> tuple[Ruler, pygame.rect.Rect]:
  x = rts.constants.SCREEN_WIDTH - rts.constants.RULER_WIDTH - 2
  y = rts.constants.SCREEN_HEIGHT - rts.constants.RULER_HEIGHT - 2
  ruler = Ruler(x, y)
  rect = copy.deepcopy(ruler.rect)
  return (ruler, rect)

@pytest.mark.parametrize(
  "moves, expected", 
  [
    (1, rts.constants.SCREEN_WIDTH - 1), 
    (2, rts.constants.SCREEN_WIDTH),
    (3, rts.constants.SCREEN_WIDTH),
  ]
)
@pytest.mark.parametrize("keys", [{ K_RIGHT: True }, { K_d: True }])
def test_right_horizontal_movement(
  bottom_right_ruler: tuple[Ruler, pygame.rect.Rect],
  moves: int,
  expected: int,
  keys: dict[int, bool],
) -> None:
  ruler, rect = bottom_right_ruler
  for x in range(0, moves):
    ruler.update(keys)
  assert expected == ruler.rect.right
  assert rect.top == ruler.rect.top

@pytest.mark.parametrize(
  "moves, expected", 
  [
    (1, 1), 
    (2, 0),
    (3, 0),
  ]
)
@pytest.mark.parametrize("keys", [{ K_LEFT: True }, { K_a: True }])
def test_left_horizontal_movement(
  top_left_ruler: tuple[Ruler, pygame.rect.Rect],
  moves: int,
  expected: int,
  keys: dict[int, bool],
) -> None:
  ruler, rect = top_left_ruler
  for x in range(0, moves):
    ruler.update(keys)
  assert expected == ruler.rect.left 
  assert rect.top == ruler.rect.top

@pytest.mark.parametrize(
  "moves, expected", 
  [
    (1, 1), 
    (2, 0),
    (3, 0),
  ]
)
@pytest.mark.parametrize("keys", [{ K_UP: True }, { K_w: True }])
def test_upper_vertical_movement(
  top_left_ruler: tuple[Ruler, pygame.rect.Rect],
  moves: int,
  expected: int,
  keys: dict[int, bool],
) -> None:
  ruler, rect = top_left_ruler
  for x in range(0, moves):
    ruler.update(keys)
  assert rect.left == ruler.rect.left
  assert expected == ruler.rect.top

@pytest.mark.parametrize(
  "moves, expected", 
  [
    (1, rts.constants.SCREEN_HEIGHT - 1), 
    (2, rts.constants.SCREEN_HEIGHT),
    (3, rts.constants.SCREEN_HEIGHT),
  ]
)
@pytest.mark.parametrize("keys", [{ K_DOWN: True }, { K_s: True }])
def test_bottom_movement(
  bottom_right_ruler: tuple[Ruler, pygame.rect.Rect],
  moves: int,
  expected: int,
  keys: dict[int, bool],
) -> None:
  ruler, rect = bottom_right_ruler
  for x in range(0, moves):
    ruler.update(keys)
  assert rect.left == ruler.rect.left
  assert expected == ruler.rect.bottom
