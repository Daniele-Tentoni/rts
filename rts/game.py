from random import randint

from pygame import K_DOWN, K_LEFT, K_RIGHT, K_UP, Rect, Surface
from pygame import display, font, mouse, draw
from pygame import (
    K_w,
    K_a,
    K_s,
    K_d,
    MOUSEBUTTONUP,
    MOUSEBUTTONDOWN,
)
import pygame
from pygame.event import Event
from pygame.locals import (
    K_ESCAPE,
    QUIT,
)

import pygame_gui
from pygame_gui import UIManager

from rts.config import *
from rts.models.game_entity import GameEntity
from rts.controllers.entity_controller import EntityController
from rts.controllers.event_controller import EventController
from rts.models.message_box import MessageBox
from rts.sprites.ruler import Ruler
from rts.sprites.soldier import Soldier
from rts.sprites.tower import Tower


class Game:
    running: bool
    clock_init_step: float
    """How many times update fps counter."""

    routes: list[tuple[tuple[float, float], tuple[float, float]]]
    tower_traced: Tower

    # Reference to the controllers
    entity_controller: EntityController
    event_controller: EventController

    message_box: MessageBox

    # Screen properties used during rendering
    screen: Surface
    sys_font: font.Font

    # Number of players in the game
    rulers_number: int

    # Constructor
    def __init__(
        self,
        screen: Surface,
        manager: UIManager,
        rulers_number: int = 2,
    ) -> None:
        """Init the game view.

        Init the game instance, adding rulers and their towers.

        :param screen: screen where game is displayed
        :paramtype screen: pygame.Surface
        :param manager: ui components manager
        :paramtype manager: pygame_gui.UIManager
        :param rulers_number: number of rulers in play
        :paramtype rulers_number: int
        """

        self.running = False
        self.routes = list()
        self.tower_traced = None

        # Reference to the controllers, ensuring they are clean.
        self.entity_controller = EntityController()
        self.entity_controller.reset()
        self.event_controller = EventController()
        self.event_controller.reset()

        # Instance unique properties
        self.screen = screen
        self.manager = manager
        self.sys_font = font.SysFont(font.get_default_font(), FONT_SIZE)
        self.rulers_number = rulers_number

        # Initialization of the main entities
        self.init_rulers()
        self.init_towers()

        self.clock_init_step = 1

    # Generates the rulers of the game
    def init_rulers(self) -> None:
        """Init rulers in this game instance.

        Init rulers, showing who is controlled by current players and who is not.
        They will be marked differently. Number of rulers in game depends on the
        game mode and will be modified in the future.
        """

        # Creates a ruler for each player and adds it to the list
        for n in range(self.rulers_number):
            # Generates the position
            x: float = randint(0, SCREEN_WIDTH)
            y: float = randint(0, SCREEN_HEIGHT)

            # Creates the instance
            ruler = Ruler(
                e=GameEntity(x, y, RULER_COLOR, RULER_SIZE), speed=0.1
            )

            # Assigns the first ruler to the player by adding the movement events
            # TODO: Add arrows movement, maybe?
            if n == 0:
                self.event_controller.register_key_event(K_w, ruler.move_up)
                self.event_controller.register_key_event(K_a, ruler.move_left)
                self.event_controller.register_key_event(K_s, ruler.move_down)
                self.event_controller.register_key_event(K_d, ruler.move_right)
                self.event_controller.register_key_event(K_UP, ruler.move_up)
                self.event_controller.register_key_event(
                    K_LEFT, ruler.move_left
                )
                self.event_controller.register_key_event(
                    K_DOWN, ruler.move_down
                )
                self.event_controller.register_key_event(
                    K_RIGHT, ruler.move_right
                )

            # if n > 0: # move other rulers from sockets events

            # Adds the instance to the list
            self.entity_controller.register_entity(ruler)

    # Generates the towers of the game
    # TODO: Select a random tower, assign it to a ruler and place it near tower.
    # TODO: All other tower will be marked as unclaimed.
    def init_towers(self) -> None:
        # Sets up the timer event associated to soldier generation
        add_soldiers = self.event_controller.register_time_event(1000)

        # Creates two towers for each player
        for n in range(PLAYERS_NUMBER * 2):
            # Generates the position
            x: float = SCREEN_WIDTH / 3 * (n + 1)
            y: float = SCREEN_HEIGHT / 2

            # Creates the instance and adds it to the list
            tower = Tower(
                e=GameEntity(x, y, TOWER_COLOR, TOWER_SIZE),
                level=1,
                soldier_color=SOLDIER_COLOR,
                soldier_size=SOLDIER_SIZE,
                soldier_gen_ratio=0.001,
            )
            self.entity_controller.register_entity(tower)
            self.event_controller.register_time_callback(
                add_soldiers,
                tower.create_soldiers,
            )

    # Keeps computing and showing frames until exit is requested
    def game_loop(self) -> None:
        # Take current clock as first thing
        clock = pygame.time.Clock()

        # Game loop exit flag
        self.running = True

        # Exit event
        def stop_loop(*args):
            self.running = False

        self.event_controller.register_key_event(K_ESCAPE, stop_loop)
        self.event_controller.register_time_callback(QUIT, stop_loop)

        self.hello_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 275), (100, 50)),
            text="Say Hello",
            manager=self.manager,
            tool_tip_text="Click to say Hello!",
        )
        self.tower_tooltip = None

        def print_hello_def(event: Event) -> None:
            """Example of button click event handler.

            :param event: event that has triggered this handler
            :paramtype event: pygame.event.Event
            """
            if (
                hasattr(event, "ui_element")
                and event.ui_element == self.hello_button
            ):
                # This setting has to be moved in the settings window
                set_fps_label_visibility(not bool(get_fps_label_visibility()))
                print("Hello World!")

        self.event_controller.register_time_callback(
            pygame_gui.UI_BUTTON_PRESSED, print_hello_def
        )

        self.txt = pygame_gui.elements.UITextBox(
            "To conquer enemy towers, send them soldiers from your towers.",
            relative_rect=pygame.Rect((40, 275), (200, 100)),
            manager=self.manager,
        )
        self.fps = 0
        fps_label_rel_rect = Rect(-20, -20, 100, 50)
        fps_label_rel_rect.bottomright = (-30, -20)
        self.fps_label = pygame_gui.elements.UILabel(
            relative_rect=fps_label_rel_rect,
            text=str(self.fps),
            manager=self.manager,
            anchors={
                "left": "right",
                "right": "right",
                "top": "bottom",
                "bottom": "bottom",
            },
            visible=get_fps_label_visibility(),
        )

        self.new_player_message = pygame_gui.windows.UIMessageWindow(
            rect=Rect(20, 20, 250, 160),
            html_message="Welcome to RTS",
            manager=self.manager,
            window_title="Welcome",
        )

        clock = pygame.time.Clock()
        clock_init = 0.0
        # Keeps looping until exit is required
        while self.running:
            # Calculate the current delta_time from last frame
            # This function return the number of milliseconds from previous call
            time_delta = clock.tick(60)
            clock_init += time_delta / 1000 * self.clock_init_step
            if clock_init > 1:
                # Clock is computed once each second
                clock_init -= 1
                self.fps = 1000 / time_delta
                fps_string = f"FPS: {round(self.fps, 2)}"
                print(fps_string)
                self.fps_label.set_text(fps_string)

            # Screen cleaning
            self.screen.fill(SCREEN_COLOR)

            # Events manager
            self.event_controller.handle_events(self.manager)
            """
        elif self.has_to_un_trace(event):
          self.stop_trace()
          self.tower_traced = None
        elif self.has_to_trace(event):
          self.tower_traced = self.start_trace()
      """

            mouse_pos = mouse.get_pos()

            # Towers update
            if self.entity_controller.has(Tower):
                towers = self.entity_controller.entity_dict[Tower]
                towers.update(delta=time_delta)
                for tower in towers:
                    self.screen.blit(tower.surf, tower.rect)
                    pygame.draw.rect(
                        self.screen,
                        TEXT_COLOR,
                        tower.s_gen_rect,
                        border_radius=2,
                    )
                    tower.update_tooltip(mouse_pos, self.manager)

            # Route updates
            if self.tower_traced is not None:
                tower_pos = self.tower_traced.rect.center
                draw.line(self.screen, TEXT_COLOR, tower_pos, mouse_pos)
                state_string = f"Tower click {self.tower_traced.rect.right}."
                state_label = self.sys_font.render(state_string, 1, TEXT_COLOR)
                self.screen.blit(state_label, (80, 80))

            for route in self.routes:
                draw.line(self.screen, TEXT_COLOR, route[0], route[1], width=2)

            # Soldiers updates
            if Soldier in self.entity_controller.entity_dict.keys():
                soldiers = self.entity_controller.entity_dict[Soldier]
                soldiers.update(time_delta)
                for soldier in soldiers:
                    self.screen.blit(soldier.surf, soldier.rect)

            # Rulers update
            if Ruler in self.entity_controller.entity_dict.keys():
                rulers = self.entity_controller.entity_dict[Ruler]
                rulers.update(delta=time_delta)
                for ruler in rulers:
                    self.screen.blit(ruler.surf, ruler.rect)

            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            # Renders the scene
            display.flip()

    def has_to_un_trace(self, event: Event) -> bool:
        return (
            event.type == MOUSEBUTTONUP
            and mouse.get_pressed() == (0, 0, 0)
            and self.tower_traced is not None
        )

    def has_to_trace(self, event: Event) -> bool:
        return (
            event.type == MOUSEBUTTONDOWN
            and mouse.get_pressed() == (1, 0, 0)
            and self.tower_traced is None
        )

    def start_trace(self) -> Tower:
        pos = mouse.get_pos()
        for tower in self.towers:
            if tower_clicked(tower, pos):
                return tower
        return None

    def stop_trace(self) -> None:
        pos = mouse.get_pos()
        remaining_towers = (
            t for t in self.towers if t is not self.tower_traced
        )
        for tower in remaining_towers:
            if tower_clicked(tower, pos):
                future_tuple = (
                    self.tower_traced.rect.center,
                    tower.rect.center,
                )
                # TODO: Change the type to set instead of list? Performance improvement?
                if future_tuple not in self.routes:
                    print("link")
                    self.routes.append(future_tuple)


def tower_clicked(tower: Tower, mouse) -> bool:
    return (
        tower.rect.right > mouse[0] > tower.rect.left
        and tower.rect.bottom > mouse[1] > tower.rect.top
    )
