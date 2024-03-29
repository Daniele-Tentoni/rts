from random import randint
from typing import Tuple
import pygame

import pygame_gui
from rts.controllers.entity_controller import EntityController

from rts.models.game_entity import GameEntity
from rts.sprites.tower import Tower


class Soldier(GameEntity):
    # Position the soldier is binded to
    # TODO: Maybe change it to a particular entity?
    origin: tuple[float, float]
    origin_radius: float

    # Speed of the soldier
    speed: float
    target: Tower

    selected: bool

    # Constructor
    def __init__(
        self,
        e: GameEntity,
        origin: tuple[float, float],
        origin_radius: float,
        owner: Tower,
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
        self.target = None

        self.ownership: Tower = owner

        self.tooltip: pygame_gui.elements.UITooltip = None

        self.initiative = 0
        self.initiative_step = 0.0011
        self.selected = False

    def die(self):
        """Call this to let this soldier die."""
        self.kill()
        self.ownership.soldier_died()

    # Updates the state of the instance
    def update(self, delta: int) -> None:
        """
        Update the soldier location.

        If it get out of screen, the Sprite is removed from every Group to which
        belongs, removing the reference to it as well. This allow garbage collector
        to reclaim the memory as necessary.
        """

        # Before check collision, ensure we are in the future correct position
        """self.initiative += self.initiative_step * delta
        if self.initiative > 1:
            
            self.initiative -= 1"""
        self.update_position(delta)

        # Moves the rectangle of the soldier
        self.update_rect()

        c = EntityController()
        list = pygame.sprite.spritecollide(self, c.game_entities, False)
        for sprite in list:
            # Check collision with other soldiers
            if isinstance(sprite, Soldier):
                # Some behaviour difference if they are enemies or not
                # If enemy, everyone has to die
                if sprite.ownership.ownership != self.ownership.ownership:
                    # Kill the enemy.
                    sprite.die()

                    # Kill the sprite itself.
                    self.die()
                    # Break to remove only one soldier each soldier collision.
                    break

            # Check collision with towers
            if isinstance(sprite, Tower):
                # Soldiers with a target must die only when colliding with the target tower
                if self.target == sprite:
                    print("E' il mio target!!!")
                    self.die()
                    sprite.die_random_soldier(self)
                    break

                # Soldiers without a target must die when they collide with an enemy tower
                if sprite.ownership != self.ownership.ownership:
                    print(f"Non e' il mio target {self.target} e {sprite}")
                    self.die()
                    break

                # TODO: If I hit a tower that is mine, I have to change my ownership to that tower.

    # Moves the instance in a random way
    def update_position(self, delta: int) -> None:
        if not self.target:
            # Generates the displacement
            delta_x = randint(-1, 1) * self.speed * delta
            delta_y = randint(-1, 1) * self.speed * delta
        else:
            to_x = -1 if self.target.rect.centerx < self.rect.centerx else 1
            to_y = -1 if self.target.rect.centery < self.rect.centery else 1

            delta_x = to_x * self.speed * delta
            delta_y = to_y * self.speed * delta

        # Updates the position of the instance
        self.x += delta_x / 20
        self.y += delta_y / 20

    # Moves the rect of the ruler according to the current entity coordinates
    def update_rect(self) -> None:
        # Checks the position limit by looking at the center position only
        # TODO: Rectangle thickness is not checked, is it important?
        #  500 ** 2 + 600 ** 2 > 10 ** 2
        # Moves the rect of the instance
        if not self.target:
            # Check that the new position if without target is inside tower area
            """if (self.x - self.origin[0]) ** 2 + (self.y - self.origin[1]) ** 2 > self.origin_radius ** 2:
            # Moves the center radially towards the center
            # TODO: Verify if the atan is the correct function
            angle = atan2(self.y, self.x).real
            self.x = self.origin_radius * cos(angle).real
            self.y = self.origin_radius * sin(angle).real
            """
            origin_x = self.ownership.rect.centerx
            origin_y = self.ownership.rect.centery
            if self.x > origin_x + self.origin_radius:
                self.x = origin_x + self.origin_radius
            if self.x < origin_x - self.origin_radius:
                self.x = origin_x - self.origin_radius
            if self.y < origin_y - self.origin_radius:
                self.y = origin_y - self.origin_radius
            if self.y > origin_y + self.origin_radius:
                self.y = origin_y + self.origin_radius

        self.rect.center = (self.x, self.y)
        should_enlarge = self.selected or self.ownership.selected
        size = [1.5 * x for x in self.size] if should_enlarge else self.size

        self.surf = pygame.Surface(size=size)
        self.surf.fill(self.color)

        # After update we can reset the target
        # If the target has to change, it will change by route update.
        # self.target = None
        # Removed due to issue with enemy tower collision

    def over(self, pos: Tuple[int, int], surface: pygame.Surface):
        pass

    def update_tooltip(
        self, mouse_pos: Tuple[int, int], manager: pygame_gui.UIManager
    ) -> None:
        collision = self.rect.collidepoint(mouse_pos[0], mouse_pos[1])
        if not collision and self.tooltip is not None and self.tooltip.alive():
            self.tooltip.kill()
        elif collision and (self.tooltip is None or not self.tooltip.alive()):
            self.tooltip = pygame_gui.elements.UITooltip(
                f"Ruler {self.ownership.ownership.x}",
                [0, 16],
                manager,
            )
            pos = pygame.math.Vector2(
                (
                    self.rect.left,
                    self.rect.top,
                )
            )
            self.tooltip.find_valid_position(pos)

    def change_ownership(self, owner: Tower):
        """
        This has to be called when the soldier has to change the ownership. Many operations have to be done in order to complete the process.
        """
        self.ownership = owner
        self.color = self.ownership.soldier_color
