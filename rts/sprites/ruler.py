from pygame import Surface, key

import rts.config
from rts.models.game_entity import GameEntity


class Ruler(GameEntity):
    """
    Ruler definition.

    A Ruler is the entity directly controller by the player.

    It contains method to draw it and update his position.
    """

    # Constructor
    def __init__(self, e: GameEntity, speed: float) -> None:
        """
        Creates a new Ruler instance.

        Create a new Ruler instance with a surface and a rectangle. If given
        starting position make sprite exceed the screen, it will move in.
        """

        # Base class initialization
        super(Ruler, self).__init__(e.x, e.y, e.color, e.size)

        # Instance unique properties
        self.speed = speed

    # Updates the state of the instance
    def update(self, delta: int) -> None:
        """
        Move the Ruler rectangle by pressed key event.
        """

        # Updates the position of the instance
        self.delta = delta
        self.update_position()

    # Moves the instance depending on the keys pressed
    def update_position(self) -> None:

        # Moves the rect of the ruler
        self.rect.left = self.x
        self.rect.top = self.y

        # Keeps the rectangle within screen limits
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > rts.config.SCREEN_WIDTH:
            self.rect.right = rts.config.SCREEN_WIDTH

        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= rts.config.SCREEN_HEIGHT:
            self.rect.bottom = rts.config.SCREEN_HEIGHT

    # Draws the rect associated to the instance
    def draw(self, screen: Surface) -> None:
        """
        Draw the Ruler on the given screen surface.

        Args:
          screen (pygame.Surface): Screen surface.
        """

        # Superposition of the rectangle on the given surface
        screen.blit(self.surf, self.rect)

    # Right movement
    def move_right(self, *args) -> None:
        self.x += self.delta * self.speed

    # Left movement
    def move_left(self, *args) -> None:
        self.x += -self.delta * self.speed

    # Upwards movement
    def move_up(self, *args) -> None:
        self.y += -self.delta * self.speed

    # Downwards movement
    def move_down(self, *args) -> None:
        self.y += self.delta * self.speed
