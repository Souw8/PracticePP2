import pygame
import sys

from ui import main_menu, leaderboard_screen, settings_screen
from racer import run_game
from persistence import load_settings


pygame.init()

WIDTH = 600
HEIGHT = 800
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3 Racer")

clock = pygame.time.Clock()


def main():
    settings = load_settings()
    current_screen = "menu"

    while True:
        if current_screen == "menu":
            current_screen = main_menu(screen, clock)

        elif current_screen == "play":
            current_screen = run_game(screen, clock, settings)

        elif current_screen == "leaderboard":
            current_screen = leaderboard_screen(screen, clock)

        elif current_screen == "settings":
            current_screen, settings = settings_screen(screen, clock, settings)

        elif current_screen == "quit":
            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()