import os
import pygame
import pygame_gui

import rts.config
import rts.game


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
    pygame.display.set_caption(rts.config.GAME_NAME)
    screen = pygame.display.set_mode(rts.config.SCREEN_SIZE)
    manager = pygame_gui.UIManager(rts.config.SCREEN_SIZE)
    rts.config.parsed = rts.config._load_configs()
    instance = rts.game.Game(screen, manager)

    # Game loop
    instance.game_loop()

    # Releases imported modules
    pygame.font.quit()
    pygame.quit()
    exit(os.EX_OK)
