from typing import Callable, Dict, List, Tuple
from pygame import USEREVENT, key
from pygame.time import set_timer
from pygame.event import get as get_events

class EventControllerSingleton:
  _shared_state = {}
  def __init__(self):
    self.__dict__ = self._shared_state

class EventController(EventControllerSingleton):
  # Counts the number of registered time events
  time_event_counter: int = 0
  # Time events callbacks dictionary where the key is the event code
  time_events: Dict[int, List(Callable[[], None])] = dict()

  # Key events callbacks dictionary where the key is the key code
  key_events: Dict[int, List(Callable[[], None])] = dict()

  # Trigger events callbacks list where the first element of the tuple is the trigger condition
  trigger_event: List(Tuple(Callable[[], bool], Callable[[], None])) = list()

  # Constructor
  def __init__(self):
    EventControllerSingleton.__init__(self)

  # Resets the instance by removing all events and all callbacks
  #TODO: Cancel registered events and free memory from callbacks
  def reset(self):
    self.time_event_counter = 0
    self.time_events = dict()
    self.key_events = dict()
    self.trigger_event = list()

  # Goes through all registered events and runs their callbacks if conditions are met
  def handle_events(self):
    # Time events
    for event in get_events():
      if self.time_events[event.type - USEREVENT - 1] is not None:
        for callback in self.time_events[event.type - USEREVENT - 1]:
          callback()
    
    # Key events
    for key, callbacks in self.key_events:
      if is_key_pressed(key):
        for callback in callbacks:
          callback()
    
    # Triggered events
    for event in self.trigger_event:
      condition, callback = event

      if condition():
        callback()

  # Adds a new event to timer schedule and return its code
  def register_time_event(self, time_span: int) -> int:
    # Adds the event to schedule
    self.time_event_counter += 1
    set_timer(self.time_event_counter + USEREVENT, time_span)

    # Prepares the callback list
    self.time_events[self.time_event_counter - 1] = ()

    return self.time_event_counter + USEREVENT

  # Removes the given envet from timer schedule
  #TODO: Remove callbacks
  def remove_time_event(self, event_code: int) -> None:
    set_timer(event_code, 0)

  # Adds a new callback function to the given time event
  def register_time_callback(self, event_code: int, callback: Callable[[], None]) -> None:
    self.time_events[event_code].add(callback)
  
  # Adds a new callback function to the given key event
  def register_key_event(self, key: int, callback: Callable[[], None]) -> None:
    # Creates the list if it does not exist
    if self.key_events[key] is None:
        self.key_events[key] = ()
    
    self.key_events[key].add(callback)
  
  # Adds a new triggered event callback to the list
  def register_trigger_event(self, condition: Callable[[], bool], callback: Callable[[], None]):
    self.trigger_event.add((condition, callback))

# Checks whether or not a given key is pressed
def is_key_pressed(k):
  pressed_keys = key.get_pressed()

  if k in pressed_keys and pressed_keys[k]:
    return True
  else:
    return False