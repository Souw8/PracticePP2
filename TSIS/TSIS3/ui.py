import pygame
from persistence import load_leaderboard, save_settings



pygame.init()
WIDTH = 600
HEIGHT = 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)
DARK_GRAY = (80, 80, 80)
RED = (220, 20, 60)
GREEN = (0, 180, 0)
BLUE = (40, 120, 220)


font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 44)


def draw_button(screen, text, x, y, w, h):
    mouse_pos = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, w, h)

    if rect.collidepoint(mouse_pos):
        color = DARK_GRAY
    else:
        color = GRAY

    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=10)

    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

    return rect


def main_menu(screen, clock):
    while True:
        screen.fill(WHITE)

        title = big_font.render("RACER TSIS 3", True, BLACK)
        screen.blit(title, (150, 120))

        play_button = draw_button(screen, "Play", 200, 240, 200, 60)
        leaderboard_button = draw_button(screen, "Leaderboard", 200, 320, 200, 60)
        settings_button = draw_button(screen, "Settings", 200, 400, 200, 60)
        quit_button = draw_button(screen, "Quit", 200, 480, 200, 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return "play"

                if leaderboard_button.collidepoint(event.pos):
                    return "leaderboard"

                if settings_button.collidepoint(event.pos):
                    return "settings"

                if quit_button.collidepoint(event.pos):
                    return "quit"

        pygame.display.update()
        clock.tick(60)


def leaderboard_screen(screen, clock):
    while True:
        screen.fill(WHITE)

        title = big_font.render("Leaderboard", True, BLACK)
        screen.blit(title, (160, 60))

        leaderboard = load_leaderboard()

        y = 140

        if len(leaderboard) == 0:
            empty_text = font.render("No scores yet", True, BLACK)
            screen.blit(empty_text, (210, 240))
        else:
            for index, item in enumerate(leaderboard):
                line = f"{index + 1}. {item['name']} | Score: {item['score']} | Dist: {item['distance']}"
                text = font.render(line, True, BLACK)
                screen.blit(text, (60, y))
                y += 45

        back_button = draw_button(screen, "Back", 200, 700, 200, 55)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return "menu"

        pygame.display.update()
        clock.tick(60)


def settings_screen(screen, clock, settings):
    car_colors = ["red", "blue", "green"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        screen.fill(WHITE)

        title = big_font.render("Settings", True, BLACK)
        screen.blit(title, (200, 70))

        sound_text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
        color_text = f"Car color: {settings['car_color']}"
        difficulty_text = f"Difficulty: {settings['difficulty']}"

        sound_button = draw_button(screen, sound_text, 150, 200, 300, 60)
        color_button = draw_button(screen, color_text, 150, 290, 300, 60)
        difficulty_button = draw_button(screen, difficulty_text, 150, 380, 300, 60)
        back_button = draw_button(screen, "Save and Back", 150, 520, 300, 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                return "quit", settings

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_button.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]

                if color_button.collidepoint(event.pos):
                    current_index = car_colors.index(settings["car_color"])
                    next_index = (current_index + 1) % len(car_colors)
                    settings["car_color"] = car_colors[next_index]

                if difficulty_button.collidepoint(event.pos):
                    current_index = difficulties.index(settings["difficulty"])
                    next_index = (current_index + 1) % len(difficulties)
                    settings["difficulty"] = difficulties[next_index]

                if back_button.collidepoint(event.pos):
                    save_settings(settings)
                    return "menu", settings

        pygame.display.update()
        clock.tick(60)