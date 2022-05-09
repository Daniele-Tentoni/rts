import pytest
import rts.state
from rts.state import (
    default,
    get as get_state,
    set as set_state,
)


@pytest.fixture(name="sample_state", autouse=True)
def sample_state_fixture(request: pytest.FixtureRequest):
    def clean_sets():
        rts.state.sets = default()

    request.addfinalizer(clean_sets)
    return rts.state.sets


@pytest.mark.parametrize("name", [("mouse_pos"), ("mouse_pressed")])
def test_init_some_values_false(name: str):
    with pytest.raises(Exception) as ex:
        get_state(name)
    assert str(ex.value) == "Not set for this frame"


def test_set():
    name = "mouse_pos"
    set1, val1 = rts.state.sets[name]
    assert set1 == False
    assert val1 == False
    set_state(name, (0, 0))
    set2, val2 = rts.state.sets.get(name)
    assert set2 == True
    assert val2 == (0, 0)


def test_get_before_set():
    name = "mouse_pos"
    with pytest.raises(Exception) as ex:
        get_state(name)
    assert str(ex.value) == "Not set for this frame"


def test_get_after_set():
    name = "mouse_pressed"
    value = (1, 0, 0)
    set_state(name, value)
    assert get_state(name) == value


def test_already_set():
    name = "screen_size"
    value = (100, 100)
    set_state(name, value)
    with pytest.raises(Exception) as ex:
        set_state(name, value)
    assert str(ex.value) == "Already set for this frame"


def test_reset():
    name = "mouse_pos"
    value = (0, 0)
    set_state(name, value)
    rts.state.reset()
    with pytest.raises(Exception) as ex:
        get_state(name)
    assert str(ex.value) == "Not set for this frame"
