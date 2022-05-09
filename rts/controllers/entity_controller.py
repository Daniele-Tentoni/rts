from typing import Dict, Type, TypeVar
from pygame.sprite import Group
from rts.controllers.meta_singleton import MetaSingleton

from rts.models.game_entity import GameEntity


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
