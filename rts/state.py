from collections import defaultdict, namedtuple
from typing import Any

State = namedtuple("State", ["set", "val"], defaults=[False, False])


def default():
    """Return the default state dictionary"""
    return defaultdict(lambda: State())


sets: defaultdict[str, State] = default()


def set(name: str, value: Any):
    state = sets[name]
    if state and state.set:
        raise Exception("Already set for this frame")

    sets[name] = State(True, value)


def get(name: str):
    """Get a saved state

    :param name: Name of the state to retrieve
    :type name: str
    """
    state = sets[name]
    print(f"State {sets} / {bool(state)} / {not state.set}")
    if not state or not state.set:
        raise Exception("Not set for this frame")

    return state.val


def reset():
    for key in sets.keys():
        sets[key] = sets[key]._replace(set=False)
