"""This module helps you to manage many event types, from the registration
to the invocation.
"""

from typing import Callable, Dict, List, Tuple
from pygame import USEREVENT, key
from pygame.time import set_timer
from pygame.event import get as get_events, Event
from pygame_gui import UIManager

from rts.controllers.meta_singleton import MetaSingleton


class EventController(metaclass=MetaSingleton):
    """Controller to manage registration and invocation of events

    This will handle for you the storage and the management of events from the
    game. You can register:
    * key events: when user press down a key and don't release it
    * time span events: after a defined time span, pygame fire an event
    * triggered events: each loop check some conditions are verified

    Use registration function for the right event and handle them using the
    handle_events function.

    .. note::
        This is a singleton, don't expect many instances of it.
    """

    # Time events callbacks dictionary where the key is the event code
    time_events: Dict[int, List[Callable[[Event], None]]]

    # Key events callbacks dictionary where the key is the key code
    key_events: Dict[int, List[Callable[[], None]]] = dict()

    # Trigger events callbacks list where the first element of the tuple is the trigger condition
    trigger_event: List[Tuple[Callable[[], bool], Callable[[], None]]] = list()

    # Constructor
    def __init__(self):
        self.time_events = {}

    # Resets the instance by removing all events and all callbacks
    # TODO: Cancel registered events and free memory from callbacks
    def reset(self):
        self.time_callbacks: Dict[int, int] = dict()
        self.time_event_counter = 0
        self.time_events = dict()
        self.key_events = dict()
        self.trigger_event = list()

    def handle_events(self, manager: UIManager):
        """Goes through all registered events and runs their callbacks if conditions are met

        This method require a manager as input since the UIManager from pygame_gui
        could have events that need to be handled.

        :param manager: UIManager from pygame_gui
        :type manager: pygame_gui.UIManager

        :Example:

        self.event_controller.handle_events(self.manager)

        .. note::
            Invoking this method more than one time in the same game_loop will fire a second time key events and triggered ones, but not pygame events!
        """
        # Time events

        # TODO: Refactor it!
        # Each triggered event must take an event as input and check if the
        # callback has a true result to trigger it.
        for event in get_events():
            # If event is managed by pygame_ui, skip to next event.
            try:
                if manager.process_events(event):
                    continue
            except AttributeError as attr_err:
                if hasattr(event, "ui_element"):
                    print(
                        f"Event {event} from {event.ui_element} was rejected due to {attr_err}"
                    )

            if event.type in self.time_events and (
                v := self.time_events[event.type]
            ):
                self._handle_events(v, event)

        # Key events
        k_pressed = key.get_pressed()
        k_events = self.key_events.items()
        [self._handle_events(c) for k, c in k_events if k_pressed[k]]

        # Triggered events
        [
            callback()
            for condition, callback in self.trigger_event
            if condition()
        ]

    def _handle_events(
        self,
        callbacks: List[Callable[[Event], None]],
        *args,
    ) -> None:
        for callback in callbacks:
            event = args[0] if len(args) > 0 else None
            callback(event)

    def register_time_event(self, time_span: int) -> int:
        """Register a new time event.

        Register a new time event for pygame timer, giving it a time span.

        :param time_span: time span to trigger the timed event
        :type time_span: int
        :return: the event code registered
        :rtype: int

        .. warning::
            By pygame internal design, we can register up to 7 time events, so be
            careful!
        """
        if len(self.time_callbacks) == 7:
            raise Exception("Too many time callbacks")

        if time_span not in self.time_callbacks.keys():
            self.time_callbacks[time_span] = (
                len(self.time_callbacks) + USEREVENT + 1
            )

        # Adds the event to schedule
        event_code = self.time_callbacks[time_span]
        set_timer(event_code, time_span)

        # Prepares the callback list
        self.time_events[event_code] = list()

        return event_code

    # Removes the given event from timer schedule
    # TODO: Remove callbacks
    def remove_time_event(self, event_code: int) -> None:
        set_timer(event_code, 0)

    # Adds a new callback function to the given time event
    def register_time_callback(
        self, event_code: int, callback: Callable[[], None]
    ) -> None:
        if event_code not in self.time_events.keys():
            self.time_events[event_code] = list()

        self.time_events[event_code].append(callback)

    # Adds a new callback function to the given key event
    def register_key_event(
        self, key: int, callback: Callable[[], None]
    ) -> None:
        # Creates the list if it does not exist
        if key not in self.key_events or self.key_events[key] is None:
            self.key_events[key] = list()

        self.key_events[key].append(callback)

    # Adds a new triggered event callback to the list
    def register_trigger_event(
        self, condition: Callable[[Event], bool], callback: Callable[[], None]
    ) -> None:
        self.trigger_event.append((condition, callback))


# Checks whether or not a given key is pressed
def is_key_pressed(key, keys):
    return key in keys and keys[key]
