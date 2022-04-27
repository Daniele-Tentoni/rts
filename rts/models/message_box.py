from typing import Tuple
from pygame import Rect, Surface
from pygame import font
import pygame

from rts.config import FONT_SIZE, SCREEN_COLOR, TEXT_COLOR, TOWER_COLOR
from rts.models.game_entity import GameEntity

class MessageBox(GameEntity):
  def __init__(self):
    super(MessageBox, self).__init__(60, 40, SCREEN_COLOR, [200, 100])
    self.messages: list[str] = list()
    self.micro_number = 0
    self.chunk_size = 35
    self.padding: int = 5

  def append(self, message: str) -> None:
    if len(message) > self.chunk_size:
      chunks = (len(message) // self.chunk_size) + 1
      self.micro_number = self.micro_number + chunks
    else:
      self.micro_number = self.micro_number + 1
    self.messages.append(message)

  def has_messages(self) -> bool:
    return len(self.messages) > 0

  def reset(self) -> None:
    self.messages.clear()
    self.micro_number = 0

  def update(self) -> None:
    sys_font = font.SysFont(font.get_default_font(), FONT_SIZE)

    def make_label(message, y) -> Surface:
      surf = sys_font.render(str(message), True, TEXT_COLOR)
      rect = surf.get_rect()
      rect.move_ip(self.padding, y)
      return [surf, rect]

    next_y = self.padding * 2
    labels: list[Tuple[Surface, Rect]] = list()
    for message in self.messages:
      if len(message) > self.chunk_size:
        for j in range(0, len(message), self.chunk_size):
          micro = message[j:j+self.chunk_size]
          lbl = make_label(micro, next_y)
          next_y = next_y + FONT_SIZE
          labels.append(lbl)
      else:
        lbl = make_label(message, next_y)
        labels.append(lbl)
        next_y = next_y + FONT_SIZE

      # Add padding between messages
      next_y = next_y + self.padding

    # Build definitive surface
    self.surf = Surface([250, next_y])
    self.surf.fill(TOWER_COLOR)
    self.rect = self.surf.get_rect()
    self.rect.move_ip(self.x, self.y)
    [self.surf.blit(l, r) for l, r in labels]
