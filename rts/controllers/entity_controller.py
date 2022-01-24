from pygame.sprite import Group

from rts.models.game_entity import GameEntity
from rts.sprites.ruler import Ruler
from rts.sprites.soldier import Soldier
from rts.sprites.tower import Tower

class EntityControllerSingleton:
  _shared_state = {}
  def __init__(self):
    self.__dict__ = self._shared_state

class EntityController(EntityControllerSingleton):
  # Game entities groups
  game_entities: Group
  # Separated game entities depending on their class
  #TODO: Is this really needed when we can search using instance type?
  rulers: Group
  soldiers: Group
  towers: Group

  # Constructor
  def __init__(self):
    EntityControllerSingleton.__init__(self)

  # Sets up the entities groups
  #TODO: Free old memory
  def reset(self) -> None:
    self.game_entities = Group()

    self.rulers = Group()
    self.soldiers = Group()
    self.towers = Group()

  # Adds the given entity to the main list and to the corresponding sublist
  def register_entity(self, e: GameEntity) -> None:
    self.game_entities.add(e)

    if isinstance(e, Ruler):
      self.rulers.add(e)
    elif isinstance(e, Soldier):
      self.soldiers.add(e)
    elif isinstance(e, Tower):
      self.towers.add(e)
