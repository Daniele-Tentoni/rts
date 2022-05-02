import os
import pygame
import pygame_gui

from rts.config import (
    GAME_NAME,
    SCREEN_SIZE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
import rts.config

from rts.game import Game


def main():
    """Main function, entry point of the game.

    Init pygame library, game view and start the game cycle.
    """

    # Initializes all imported pygame modules
    passed, failed = pygame.init()
    pygame.font.init()

    # Stops any further operation if some initializations failed
    if failed > 0:
        print("Something went wrong during pygame init")
        exit(os.EX_DATAERR)

    # Initial setup of the game
    pygame.display.set_caption(GAME_NAME)
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    manager = pygame_gui.UIManager(SCREEN_SIZE)
    rts.config.parsed = rts.config._load_configs()
    game = Game(screen, manager)

    # Game loop
    game.game_loop()

    # Releases imported modules
    pygame.font.quit()
    pygame.quit()
    exit(os.EX_OK)
