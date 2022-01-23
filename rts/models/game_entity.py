from pygame.sprite import Sprite
from pygame.surface import Surface

class GameEntity(Sprite):
    # Entity coordinates
    x, y = tuple(float, float)

    # Entity aesthetics
    color: tuple(int, int, int)
    size: tuple(float, float)

    # Constructor
    def __init__(self, x: float, y: float, color: tuple(int, int, int), size: tuple(float, float)):
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