from typing import Tuple
from pygame import Surface
import pygame
import pygame.font as font
import pygame_gui

from rts.config import FONT_SIZE, TEXT_COLOR, LIMIT_PER_LEVEL
from rts.models.game_entity import GameEntity
from rts.sprites.soldier import Soldier
from rts.controllers.entity_controller import EntityController


class Tower(GameEntity):
    """
    Tower definition.

    It contains method to draw it and update its position. You can update its position without drawing it.
    """

    # Level of the tower
    level: int

    # Custom color and size for the tower
    soldier_color: tuple[int, int, int]
    soldier_size: tuple[float, float]
    # Soldier generation ratio
    soldier_gen_ratio: float
    # Number of soldiers waiting for creation
    soldier_gen_pool: float = 0

    # Soldiers number associated to the tower
    soldiers_number: int = 0
    # Soldiers number label
    soldiers_label: Surface

    s_gen_rect: pygame.Rect
    """Soldier generation Rect.

    Show the progress of the generation of the next soldier to spawn near the tower."""

    # Constructor
    def __init__(
        self,
        e: GameEntity,
        level: int,
        soldier_color: tuple[int, int, int],
        soldier_size: tuple[float, float],
        soldier_gen_ratio: float,
    ) -> None:
        """Creates a new Tower entity.

        Create a new Tower entity with a surface and a rectangle.
        Inside the tower is displayed the number of soldier defending it.
        """

        # Base class initialization
        super(Tower, self).__init__(e.x, e.y, e.color, e.size)

        # Instance unique properties
        self.soldier_color = soldier_color
        self.soldier_size = soldier_size
        self.level = level
        self.soldier_gen_ratio = soldier_gen_ratio
        self.tower_tooltip: pygame_gui.elements.UITooltip = None

    # Updates the state of the instance
    def update(self, delta: int) -> None:
        """Update tower and her soldiers.

        Update the tower and the label of soldier assigned to the tower.
        """

        # Updates the soldiers number label
        # TODO: Soldier number counting
        self._update_soldiers_pool(delta)
        self._update_soldiers_label()
        self._update_soldiers_rect()

    def _update_soldiers_pool(self, delta: int) -> None:
        """Adds soldiers to the pool if limit has not been reached."""
        if self._reached_max_soldiers():
            # Adds soldiers in the pool depending on the generation ratio
            self.soldier_gen_pool += self.soldier_gen_ratio * delta

    # Updates and renders the soldiers number label
    def _update_soldiers_label(self) -> None:
        """Update soldiers label inside tower.

        Update soldiers label content inside tower with the current length of
        soldiers sprite group. Remember to keep this updated.
        """

        # Setting up the label
        self.surf.fill(self.color)
        sys_font = font.SysFont(font.get_default_font(), FONT_SIZE)
        self.soldiers_label = sys_font.render(
            str(self.soldiers_number), True, TEXT_COLOR
        )
        width, height = self.rect.width, self.rect.height
        rect = self.soldiers_label.get_rect()
        rect.centerx = width / 2
        rect.centery = height / 2
        self.surf.blit(self.soldiers_label, rect)

    def _update_soldiers_rect(self) -> None:
        left = self.x + 15
        top = self.y + 15
        width = 10
        height = self.soldier_gen_pool * 25
        self.s_gen_rect = pygame.Rect(left, top, width, height)

    def update_tooltip(
        self, mouse_pos: Tuple[int, int], manager: pygame_gui.UIManager
    ) -> None:
        collision = self.s_gen_rect.collidepoint(mouse_pos[0], mouse_pos[1])
        if not collision and (
            self.tower_tooltip is not None and self.tower_tooltip.alive()
        ):
            self.tower_tooltip.kill()
        elif collision and (
            self.tower_tooltip is None or not self.tower_tooltip.alive()
        ):
            self.tower_tooltip = pygame_gui.elements.UITooltip(
                "Next soldier generation progress",
                [0, 16],
                manager,
            )
            pos = pygame.math.Vector2(
                (
                    self.s_gen_rect.left,
                    self.s_gen_rect.top,
                )
            )
            self.tower_tooltip.find_valid_position(pos)

    # Generates new soldiers depending on the pool number on the same position of the tower
    def create_soldiers(self, *args) -> None:
        """Spawn a new soldier.

        Spawn a soldier near the tower, given her center coordinates. Then, add the
        new sprite to soldier tower sprite group and return it.

        :return: New Soldier created
        :rtype: rts.sprites.soldier.Soldier
        """

        # Reference to the entity controller
        ent_cont = EntityController()

        # Generates one soldier at a time until limit gets reached or pool gets empty
        while self._reached_max_soldiers() and self.soldier_gen_pool >= 1:
            self.soldier_gen_pool -= 1
            self.soldiers_number += 1

            soldier = Soldier(
                e=GameEntity(
                    self.x, self.y, self.soldier_color, self.soldier_size
                ),
                origin=(self.x, self.y),
                origin_radius=25,
                speed=1,
            )
            ent_cont.register_entity(soldier)

    def _reached_max_soldiers(self):
        return self.soldiers_number < LIMIT_PER_LEVEL[self.level - 1]
