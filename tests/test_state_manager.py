from random import sample
import pytest
from rts.controllers.state_controller import State, StateController


def test_default_state():
    print(f"{State._field_defaults}")
    assert State() == (False, False)
    assert State().set == False
    assert State().val == False
    assert State(True) == (True, False)
    assert State(val=1) == (False, 1)
    assert State(True, "a") == (True, "a")


@pytest.fixture(name="sample_state_controller")
def sample_state_controller() -> StateController:
    c = StateController()
    yield StateController()
    del c


@pytest.mark.parametrize("name", [("mouse_pos"), ("mouse_pressed")])
def test_init_some_values_false(
    name: str, sample_state_controller: StateController
):
    with pytest.raises(Exception) as ex:
        sample_state_controller.get(name)
    assert str(ex.value) == "Not set for this frame"


def test_set(sample_state_controller: StateController):
    name = "mouse_pos"
    set1, val1 = sample_state_controller.sets[name]
    assert set1 == False
    assert val1 == False
    sample_state_controller.set(name, (0, 0))
    set2, val2 = sample_state_controller.sets.get(name)
    assert set2 == True
    assert val2 == (0, 0)


def test_get_before_set(sample_state_controller: StateController):
    name = "mouse_pos"
    with pytest.raises(Exception) as ex:
        sample_state_controller.get(name)
    assert str(ex.value) == "Not set for this frame"


def test_get_after_set(sample_state_controller: StateController):
    name = "mouse_pressed"
    value = (1, 0, 0)
    sample_state_controller.set(name, value)
    assert sample_state_controller.get(name) == value


def test_already_set(sample_state_controller: StateController):
    name = "screen_size"
    value = (100, 100)
    sample_state_controller.set(name, value)
    with pytest.raises(Exception) as ex:
        sample_state_controller.set(name, value)
    assert str(ex.value) == "Already set for this frame"


def test_reset(sample_state_controller: StateController):
    name = "mouse_pos"
    value = (0, 0)
    sample_state_controller.set(name, value)
    sample_state_controller.reset()
    with pytest.raises(Exception) as ex:
        sample_state_controller.get(name)
    assert str(ex.value) == "Not set for this frame"
