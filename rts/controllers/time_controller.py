from pygame import Rect
import pygame_gui
from rts.config import get_fps_label_visibility

from rts.controllers.meta_singleton import MetaSingleton


class TimeController(metaclass=MetaSingleton):
    clock_init: float
    """Clock accumulator, trigger when reach 1 second."""

    clock_init_step: float
    """How many times update fps counter."""

    def __init__(self, ui_manager: pygame_gui.UIManager):
        print(f"Visibility {get_fps_label_visibility()}")
        self.fps = 0
        fps_label_rel_rect = Rect(-20, -20, 100, 50)
        fps_label_rel_rect.bottomright = (-30, -20)
        self.fps_label = pygame_gui.elements.UILabel(
            relative_rect=fps_label_rel_rect,
            text=str(""),
            manager=ui_manager,
            anchors={
                "left": "right",
                "right": "right",
                "top": "bottom",
                "bottom": "bottom",
            },
            visible=get_fps_label_visibility(),
        )
        self.clock_init_step = 1.0
        self.clock_init = 0.0

    def reset(self) -> None:
        self.clock_init = 0.0
        self.clock_init_step = 0.0
        self.fps = 0

    def update(self, time_delta: int):
        self.clock_init += time_delta / 1000 * self.clock_init_step
        if self.clock_init >= 1:
            # Clock is computed once each second
            self.clock_init -= 1
            fps = 1000 / time_delta
            fps_string = f"FPS: {round(fps, 2)}"
            print(fps_string)
            if self.fps_label is not None:
                self.fps_label.set_text(fps_string)

        return self.clock_init
