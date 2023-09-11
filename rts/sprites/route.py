from typing import Tuple

from pygame import Rect, Surface
import pygame
from rts.config import TEXT_COLOR
from rts.controllers.entity_controller import EntityController
from rts.models.game_entity import GameEntity
from rts.sprites.soldier import Soldier
from rts.sprites.tower import Tower


class Route(GameEntity):
    start: Tower
    end: Tower

    def __init__(self, start: Tower, end: Tower) -> None:
        super(Route, self).__init__(0, 0, [0, 0, 0], [0, 0])
        self.start = start
        self.end = end

        self.color = TEXT_COLOR
        self.rect = Rect(-1, -1, 0, 0)
        self.width = 2

    def update(self, delta: int, screen: Surface):
        self.rect = pygame.draw.line(
            screen,
            self.color,
            self.start.rect.center,
            self.end.rect.center,
            width=self.width,
        )

        # Each soldier will have the other tower as a target
        soldiers = EntityController().entities(Soldier)
        for entity in soldiers:
            soldier: Soldier = entity
            if soldier.ownership == self.start:
                soldier.target = self.end
            elif soldier.ownership == self.end:
                soldier.target = self.start

    def over(self, pos: Tuple[int, int], surf: Surface = None):
        """
        Do things if the position given is over the route.
        This method has side effects inside, we should fix it.

        :param pos: Position of the object to check over the route
        :param surf: Screen surface where to draw new objects
        :return: True if is over, false otherwise
        """
        if self.rect.collidepoint(pos):
            self.width = 4
            self.color = "green" if self.start.ownership.id == 0 else "red"
            return True
        else:
            self.width = 2
            self.color = TEXT_COLOR
            return False
