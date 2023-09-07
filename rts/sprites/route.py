from typing import Tuple

from pygame import Surface
import pygame
from rts.config import TEXT_COLOR
from rts.controllers.entity_controller import EntityController
from rts.sprites.soldier import Soldier
from rts.sprites.tower import Tower


class Route:
    start: Tower
    end: Tower

    def __init__(self, start: Tower, end: Tower) -> None:
        self.start = start
        self.end = end

        self.color = TEXT_COLOR
        self.width = 2

    def update(self, delta: int, screen: Surface):
        self.rect = pygame.draw.line(
            screen,
            self.color,
            self.start.rect.center,
            self.end.rect.center,
            width=2,
        )
        # Per ogni soldato che appartiene ad una delle due torri
        soldiers = EntityController().entities(Soldier)
        for entity in soldiers:
            soldier: Soldier = entity
            if soldier.ownership == self.start:
                soldier.target = self.end
            if soldier.ownership == self.end:
                soldier.target = self.start
        # Lo avvicino alla rotta e poi lo mando verso l'altra torre

    def over(self, pos: Tuple[int, int], surf: Surface):
        if self.rect.collidepoint(pos):
            self.rect.width = 4
            self.color = "green" if self.start.ownership.id == 0 else "red"
        else:
            self.rect.width = 2
            self.color = TEXT_COLOR
