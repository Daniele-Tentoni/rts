from collections import defaultdict, namedtuple
from typing import Any, Dict
from rts.controllers.meta_singleton import MetaSingleton

State = namedtuple("State", ["set", "val"], defaults=[False, False])


class StateController(metaclass=MetaSingleton):
    def __init__(self):
        self.sets: defaultdict[str, State] = defaultdict(lambda: State())

    def set(self, name: str, value: Any):
        state = self.sets[name]
        if state and state.set:
            raise Exception("Already set for this frame")

        self.sets[name] = State(True, value)

    def get(self, name: str):
        state = self.sets[name]
        print(f"State {self.sets}, {state}")
        if not state or not state.set:
            raise Exception("Not set for this frame")

        return state.val

    def reset(self):
        for key in self.sets.keys():
            self.sets[key] = self.sets[key]._replace(set=False)
