from pygame.sprite import Sprite
from pygame.surface import Surface


class GameEntity(Sprite):
    # Entity coordinates
    x: float
    y: float

    # Entity aesthetics
    color: tuple[int, int, int]
    size: tuple[float, float]

    selected: bool
    """
    Gets or sets if the entity is selected or not.
    You can select an entity by moving mouse over it or over the owner.
    """

    # Constructor
    def __init__(
        self,
        x: float,
        y: float,
        color: tuple[int, int, int],
        size: tuple[float, float],
    ):
        # Base class initialization
        super(GameEntity, self).__init__()

        # Copy of the values
        self.x = x
        self.y = y
        self.color = color
        self.size = size

        # Aesthetics
        self.surf = Surface(self.size)
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()
        self.rect.move_ip(self.x, self.y)

        self.selected = False
