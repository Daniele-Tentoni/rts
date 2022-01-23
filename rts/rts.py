import pygame

from config import (
  GAME_NAME,
  SCREEN_WIDTH,
  SCREEN_HEIGHT,
)
from game import Game

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
    return

  # Initial setup of the game
  pygame.display.set_caption(GAME_NAME)
  screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
  game = Game(screen)

  # Game loop
  game.game_loop()

  # Releases imported modules
  pygame.font.quit()
  pygame.quit()
