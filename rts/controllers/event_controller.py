from typing import Callable, Dict, List, Tuple
from pygame import K_ESCAPE, QUIT, USEREVENT, key
from pygame.time import set_timer
from pygame.event import get as get_events

class EventControllerSingleton:
  _shared_state = {}
  def __init__(self):
    self.__dict__ = self._shared_state

class EventController(EventControllerSingleton):
  # Time events callbacks dictionary where the key is the event code
  time_events: Dict[int, List[Callable[[], None]]] = dict()

  # Key events callbacks dictionary where the key is the key code
  key_events: Dict[int, List[Callable[[], None]]] = dict()

  # Trigger events callbacks list where the first element of the tuple is the trigger condition
  trigger_event: List[Tuple[Callable[[], bool], Callable[[], None]]] = list()

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
      if event.type in self.time_events and (v := self.time_events[event.type]):
        self._handle_events(v)

    # Key events
    k_pressed = key.get_pressed()
    k_events = self.key_events.items()
    [self._handle_events(c) for k, c in k_events if k_pressed[k]]

    # Triggered events
    [callback() for condition, callback in self.trigger_event if condition()]

  def _handle_events(self, callbacks: List[Callable[[], None]]) -> None:
    for callback in callbacks:
      callback()

  # Adds a new event to timer schedule and return its code: max 7 events.
  def register_time_event(self, time_span: int) -> int:
    """Register a new time event.

    Register a new time event for pygame timer, giving it a time span.
    By pygame internal design, we can register up to 7 time events, so be
    careful!

    :param time_span: time span to trigger the timed event
    :type time_span: int
    :return: the event code registered
    :rtype: int
    """

    # Adds the event to schedule
    event_code = len(self.time_events) + USEREVENT + 1
    set_timer(event_code, time_span)

    # Prepares the callback list
    self.time_events[event_code] = list()

    return event_code

  # Removes the given event from timer schedule
  #TODO: Remove callbacks
  def remove_time_event(self, event_code: int) -> None:
    set_timer(event_code, 0)

  # Adds a new callback function to the given time event
  def register_time_callback(
    self,
    event_code: int,
    callback: Callable[[], None]
    ) -> None:
    if event_code not in self.time_events.keys():
      self.time_events[event_code] = list()

    self.time_events[event_code].append(callback)

  # Adds a new callback function to the given key event
  def register_key_event(self, key: int, callback: Callable[[], None]) -> None:
    # Creates the list if it does not exist
    if key not in self.key_events or self.key_events[key] is None:
      self.key_events[key] = list()

    self.key_events[key].append(callback)

  # Adds a new triggered event callback to the list
  def register_trigger_event(self, condition: Callable[[], bool], callback: Callable[[], None]):
    self.trigger_event.append((condition, callback))

# Checks whether or not a given key is pressed
def is_key_pressed(key, keys):
  return key in keys and keys[key]
