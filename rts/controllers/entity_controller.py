from typing import Dict, Type, TypeVar
from pygame.sprite import Group

from rts.models.game_entity import GameEntity

from threading import Lock


class MetaSingleton(type):
    """This is a thread-safe implementation of Singleton.

    Returns:
      Thread safe singleton.
    """

    _instances = {}
    _lock: Lock = Lock()
    """We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
  """

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class EntityController(metaclass=MetaSingleton):
    # Game entities groups
    game_entities: Group

    # Constructor
    def __init__(self):
        self.game_entities = Group()
        self.entity_dict: Dict[Type, Group] = dict()

    # Sets up the entities groups
    # TODO: Free old memory
    def reset(self) -> None:
        self.game_entities = Group()
        self.entity_dict.clear()

    T = TypeVar("T", bound=GameEntity)

    # Adds the given entity to the main list and to the corresponding sublist
    def register_entity(self, e: T) -> None:
        # First add to all game entities.
        self.game_entities.add(e)

        # Create Sprite group if not exists.
        if e.__class__ not in self.entity_dict.keys():
            self.entity_dict[e.__class__] = Group()

        # Finally add it to the group.
        self.entity_dict[e.__class__].add(e)

    def entities(self, t: Type):
        return self.entity_dict[t]

    def has(self, t: Type):
        return t in self.entity_dict.keys()

    def has_e(self, e: T):
        return self.has(e.__class__) and e in self.entity_dict[e.__class__]
