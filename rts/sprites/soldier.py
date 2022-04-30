from cmath import atan, cos, sin
from math import atan2
from random import randint

from rts.models.game_entity import GameEntity


class Soldier(GameEntity):
    # Position the soldier is binded to
    # TODO: Maybe change it to a particular entity?
    origin: tuple[float, float]
    origin_radius: float

    # Speed of the soldier
    speed: float

    # Constructor
    def __init__(
        self,
        e: GameEntity,
        origin: tuple[float, float],
        origin_radius: float,
        speed: float,
    ) -> None:
        """
        Create a new Soldier entity.

        Create a new Tower entity with a surface and a rectangle.
        """

        # Base class initialization
        diff_x = randint(-origin_radius, origin_radius)
        diff_y = randint(-origin_radius, origin_radius)
        def_x = e.x + diff_x
        def_y = e.y + diff_y
        super(Soldier, self).__init__(def_x, def_y, e.color, e.size)

        # Instance unique properties
        self.origin = origin
        self.origin_radius = origin_radius
        self.speed = speed

        self.initiative = 0
        self.initiative_step = 0.0011

    # Updates the state of the instance
    def update(self, delta: int) -> None:
        """
        Update the soldier location.

        If it get out of screen, the Sprite is removed from every Group to which
        belongs, removing the reference to it as well. This allow garbage collector
        to reclaim the memory as necessary.
        """

        # Updates the position of the instance
        self.initiative = self.initiative + self.initiative_step * delta
        if self.initiative > 1:
            self.update_position(delta)
            self.initiative = self.initiative - 1

    # Moves the instance in a random way
    def update_position(self, delta: int) -> None:
        # Generates the displacement
        delta_x = randint(-1, 1) * self.speed * delta
        delta_y = randint(-1, 1) * self.speed * delta

        # Updates the position of the instance
        self.x += delta_x
        self.y += delta_y

        # Moves the rectangle of the soldier
        self.update_rect()

    # Moves the rect of the ruler according to the current entity coordinates
    def update_rect(self) -> None:
        # Checks the position limit by looking at the center position only
        # TODO: Rectangle thickness is not checked, is it important?
        #  500 ** 2 + 600 ** 2 > 10 ** 2
        """if (self.x - self.origin[0]) ** 2 + (self.y - self.origin[1]) ** 2 > self.origin_radius ** 2:
        # Moves the center radially towards the center
        # TODO: Verify if the atan is the correct function
        angle = atan2(self.y, self.x).real
        self.x = self.origin_radius * cos(angle).real
        self.y = self.origin_radius * sin(angle).real"""
        if self.x > self.origin[0] + self.origin_radius:
            self.x = self.origin[0] + self.origin_radius
        if self.x < self.origin[0] - self.origin_radius:
            self.x = self.origin[0] - self.origin_radius
        if self.y < self.origin[1] - self.origin_radius:
            self.y = self.origin[1] - self.origin_radius
        if self.y > self.origin[1] + self.origin_radius:
            self.y = self.origin[1] + self.origin_radius

        # Moves the rect of the instance
        self.rect.center = (self.x, self.y)
