import json
import os
import random
import sys

import pygame

from db import get_personal_best, get_top_10, save_game

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE
BASE_FPS = 8

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (205, 205, 205)
DARK_GRAY = (90, 90, 90)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 20, 60)
DARK_RED = (120, 0, 0)
BLUE = (30, 144, 255)
YELLOW = (240, 200, 40)
PURPLE = (155, 89, 182)
ORANGE = (230, 126, 34)

SETTINGS_FILE = "settings.json"


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, font):
        mouse_pos = pygame.mouse.get_pos()
        color = DARK_GRAY if self.rect.collidepoint(mouse_pos) else BLACK
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, GRAY, self.rect, 2, border_radius=8)
        text_img = font.render(self.text, True, WHITE)
        text_rect = text_img.get_rect(center=self.rect.center)
        screen.blit(text_img, text_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TSIS 4 Snake")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.big_font = pygame.font.SysFont("Arial", 42)

        self.settings = self.load_settings()
        self.username = "Player"
        self.personal_best = 0
        self.screen_name = "menu"
        self.running = True
        self.saved_after_game_over = False

        self.buttons = {}
        self.create_buttons()
        self.reset_game()

    def create_buttons(self):
        self.buttons["menu"] = [
            Button(200, 220, 200, 45, "Play"),
            Button(200, 280, 200, 45, "Leaderboard"),
            Button(200, 340, 200, 45, "Settings"),
            Button(200, 400, 200, 45, "Quit"),
        ]
        self.buttons["game_over"] = [
            Button(180, 370, 240, 45, "Retry"),
            Button(180, 430, 240, 45, "Main Menu"),
        ]
        self.buttons["leaderboard"] = [Button(200, 520, 200, 45, "Back")]
        self.buttons["settings"] = [
            Button(160, 180, 280, 45, "Toggle Grid"),
            Button(160, 240, 280, 45, "Toggle Sound"),
            Button(160, 300, 280, 45, "Change Snake Color"),
            Button(160, 420, 280, 45, "Save & Back"),
        ]

    def load_settings(self):
        default = {
            "snake_color": [0, 180, 0],
            "grid": True,
            "sound": True,
        }

        if not os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
                json.dump(default, file, indent=4)
            return default

        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            default.update(data)
            return default
        except Exception:
            return default

    def save_settings(self):
        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(self.settings, file, indent=4)

    def draw_text(self, text, font, color, x, y):
        img = font.render(str(text), True, color)
        self.screen.blit(img, (x, y))

    def draw_center_text(self, text, font, color, y):
        img = font.render(str(text), True, color)
        rect = img.get_rect(center=(WIDTH // 2, y))
        self.screen.blit(img, rect)

    def random_free_cell(self, forbidden):
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in forbidden:
                return pos

    def generate_food(self):
        forbidden = set(self.snake) | self.obstacles
        value = random.choice([1, 2, 3])
        color = RED if value == 1 else BLUE if value == 2 else ORANGE
        return {
            "position": self.random_free_cell(forbidden),
            "value": value,
            "color": color,
            "spawn_time": pygame.time.get_ticks(),
            "lifetime": 5000,
        }

    def generate_poison(self):
        forbidden = set(self.snake) | self.obstacles | {self.food["position"]}
        return {
            "position": self.random_free_cell(forbidden),
            "spawn_time": pygame.time.get_ticks(),
        }

    def generate_powerup(self):
        forbidden = set(self.snake) | self.obstacles | {self.food["position"], self.poison["position"]}
        kind = random.choice(["speed", "slow", "shield"])
        color = YELLOW if kind == "speed" else PURPLE if kind == "slow" else BLUE
        return {
            "position": self.random_free_cell(forbidden),
            "kind": kind,
            "color": color,
            "spawn_time": pygame.time.get_ticks(),
            "lifetime": 8000,
        }

    def generate_obstacles(self, count):
        obstacles = set()
        head = self.snake[0]

        while len(obstacles) < count:
            pos = (random.randint(2, COLS - 3), random.randint(2, ROWS - 3))
            distance = abs(pos[0] - head[0]) + abs(pos[1] - head[1])

            if pos not in self.snake and distance > 4:
                obstacles.add(pos)

        return obstacles

    def reset_game(self):
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self.next_direction = self.direction
        self.score = 0
        self.level = 1
        self.foods_eaten = 0
        self.base_speed = BASE_FPS
        self.speed = BASE_FPS
        self.obstacles = set()
        self.food = self.generate_food()
        self.poison = self.generate_poison()
        self.powerup = None
        self.last_powerup_spawn = pygame.time.get_ticks()
        self.active_powerup = None
        self.active_powerup_start = 0
        self.shield_active = False
        self.game_over = False
        self.saved_after_game_over = False

    def start_game(self):
        self.username = self.username.strip() or "Player"
        self.personal_best = get_personal_best(self.username)
        self.reset_game()
        self.screen_name = "game"

    def handle_collision(self):
        if self.shield_active:
            self.shield_active = False
            return False
        return True

    def update_powerup_effects(self):
        now = pygame.time.get_ticks()

        if self.active_powerup == "speed":
            self.speed = self.base_speed + 5
            if now - self.active_powerup_start >= 5000:
                self.active_powerup = None
                self.speed = self.base_speed

        elif self.active_powerup == "slow":
            self.speed = max(3, self.base_speed - 3)
            if now - self.active_powerup_start >= 5000:
                self.active_powerup = None
                self.speed = self.base_speed

    def update_game(self):
        now = pygame.time.get_ticks()
        self.update_powerup_effects()

        if now - self.food["spawn_time"] >= self.food["lifetime"]:
            self.food = self.generate_food()

        if self.powerup is None and now - self.last_powerup_spawn >= 6000:
            self.powerup = self.generate_powerup()
            self.last_powerup_spawn = now

        if self.powerup and now - self.powerup["spawn_time"] >= self.powerup["lifetime"]:
            self.powerup = None
            self.last_powerup_spawn = now

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        border_collision = new_head[0] < 0 or new_head[0] >= COLS or new_head[1] < 0 or new_head[1] >= ROWS
        self_collision = new_head in self.snake
        obstacle_collision = new_head in self.obstacles

        if border_collision or self_collision or obstacle_collision:
            if self.handle_collision():
                self.game_over = True
                self.screen_name = "game_over"
            return

        self.snake.insert(0, new_head)

        if new_head == self.food["position"]:
            self.score += self.food["value"]
            self.foods_eaten += 1
            self.food = self.generate_food()

            if self.foods_eaten % 4 == 0:
                self.level += 1
                self.base_speed += 2
                self.speed = self.base_speed

                if self.level >= 3:
                    self.obstacles = self.generate_obstacles(5 + self.level)
        else:
            self.snake.pop()

        if new_head == self.poison["position"]:
            if len(self.snake) > 2:
                self.snake = self.snake[:-2]
            else:
                self.snake = self.snake[:1]

            if len(self.snake) <= 1:
                self.game_over = True
                self.screen_name = "game_over"

            self.poison = self.generate_poison()

        if self.powerup and new_head == self.powerup["position"]:
            kind = self.powerup["kind"]

            if kind == "shield":
                self.shield_active = True
            else:
                self.active_powerup = kind
                self.active_powerup_start = pygame.time.get_ticks()

            self.powerup = None
            self.last_powerup_spawn = pygame.time.get_ticks()

    def save_result_once(self):
        if not self.saved_after_game_over:
            save_game(self.username, self.score, self.level)
            self.personal_best = max(self.personal_best, self.score)
            self.saved_after_game_over = True

    def draw_grid(self):
        if not self.settings.get("grid", True):
            return
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WIDTH, y))

    def draw_game(self):
        self.screen.fill(WHITE)
        self.draw_grid()

        for block in self.obstacles:
            x, y = block
            pygame.draw.rect(self.screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for index, segment in enumerate(self.snake):
            x, y = segment
            color = DARK_GREEN if index == 0 else tuple(self.settings["snake_color"])
            pygame.draw.rect(self.screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        fx, fy = self.food["position"]
        pygame.draw.rect(self.screen, self.food["color"], (fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        px, py = self.poison["position"]
        pygame.draw.rect(self.screen, DARK_RED, (px * CELL_SIZE, py * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        if self.powerup:
            ux, uy = self.powerup["position"]
            pygame.draw.rect(self.screen, self.powerup["color"], (ux * CELL_SIZE, uy * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        food_left = max(0, (self.food["lifetime"] - (pygame.time.get_ticks() - self.food["spawn_time"])) // 1000)

        self.draw_text(f"User: {self.username}", self.small_font, BLACK, 10, 8)
        self.draw_text(f"Score: {self.score}", self.small_font, BLACK, 10, 30)
        self.draw_text(f"Level: {self.level}", self.small_font, BLACK, 10, 52)
        self.draw_text(f"Best: {self.personal_best}", self.small_font, BLACK, 10, 74)
        self.draw_text(f"Food: +{self.food['value']} / {food_left}s", self.small_font, BLACK, 10, 96)

        if self.shield_active:
            self.draw_text("Shield: ON", self.small_font, BLUE, 460, 8)
        if self.active_powerup:
            self.draw_text(f"Power: {self.active_powerup}", self.small_font, PURPLE, 440, 30)

    def draw_menu(self):
        self.screen.fill(WHITE)
        self.draw_center_text("TSIS 4 Snake", self.big_font, BLACK, 90)
        self.draw_center_text("Enter username:", self.font, BLACK, 145)

        input_rect = pygame.Rect(170, 170, 260, 40)
        pygame.draw.rect(self.screen, WHITE, input_rect)
        pygame.draw.rect(self.screen, BLACK, input_rect, 2)
        self.draw_text(self.username, self.font, BLACK, 180, 176)

        for button in self.buttons["menu"]:
            button.draw(self.screen, self.font)

    def draw_game_over(self):
        self.save_result_once()
        self.screen.fill(WHITE)
        self.draw_center_text("GAME OVER", self.big_font, RED, 130)
        self.draw_center_text(f"Score: {self.score}", self.font, BLACK, 200)
        self.draw_center_text(f"Level reached: {self.level}", self.font, BLACK, 240)
        self.draw_center_text(f"Personal best: {self.personal_best}", self.font, BLACK, 280)

        for button in self.buttons["game_over"]:
            button.draw(self.screen, self.font)

    def draw_leaderboard(self):
        self.screen.fill(WHITE)
        self.draw_center_text("Leaderboard Top 10", self.big_font, BLACK, 50)
        rows = get_top_10()

        self.draw_text("#", self.small_font, BLACK, 30, 105)
        self.draw_text("Username", self.small_font, BLACK, 75, 105)
        self.draw_text("Score", self.small_font, BLACK, 250, 105)
        self.draw_text("Level", self.small_font, BLACK, 340, 105)
        self.draw_text("Date", self.small_font, BLACK, 430, 105)

        y = 140
        for i, row in enumerate(rows, start=1):
            username, score, level, played_at = row
            date_text = played_at.strftime("%Y-%m-%d") if played_at else "-"
            self.draw_text(i, self.small_font, BLACK, 30, y)
            self.draw_text(username[:12], self.small_font, BLACK, 75, y)
            self.draw_text(score, self.small_font, BLACK, 250, y)
            self.draw_text(level, self.small_font, BLACK, 340, y)
            self.draw_text(date_text, self.small_font, BLACK, 430, y)
            y += 32

        if not rows:
            self.draw_center_text("No database records yet", self.font, RED, 250)

        for button in self.buttons["leaderboard"]:
            button.draw(self.screen, self.font)

    def draw_settings(self):
        self.screen.fill(WHITE)
        self.draw_center_text("Settings", self.big_font, BLACK, 80)

        grid_text = "ON" if self.settings["grid"] else "OFF"
        sound_text = "ON" if self.settings["sound"] else "OFF"
        color_text = str(self.settings["snake_color"])

        self.draw_center_text(f"Grid: {grid_text}", self.font, BLACK, 140)
        self.draw_center_text(f"Sound: {sound_text}", self.font, BLACK, 360)
        self.draw_center_text(f"Snake color: {color_text}", self.small_font, BLACK, 390)

        preview = pygame.Rect(275, 345, 50, 25)
        pygame.draw.rect(self.screen, tuple(self.settings["snake_color"]), preview)
        pygame.draw.rect(self.screen, BLACK, preview, 2)

        for button in self.buttons["settings"]:
            button.draw(self.screen, self.font)

    def change_snake_color(self):
        colors = [
            [0, 180, 0],
            [30, 144, 255],
            [155, 89, 182],
            [230, 126, 34],
            [220, 20, 60],
        ]
        current = self.settings["snake_color"]
        index = colors.index(current) if current in colors else 0
        self.settings["snake_color"] = colors[(index + 1) % len(colors)]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.screen_name == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.start_game()
                    else:
                        if len(self.username) < 15 and event.unicode.isprintable():
                            if self.username == "Player":
                                self.username = ""
                            self.username += event.unicode

                for button in self.buttons["menu"]:
                    if button.clicked(event):
                        if button.text == "Play":
                            self.start_game()
                        elif button.text == "Leaderboard":
                            self.screen_name = "leaderboard"
                        elif button.text == "Settings":
                            self.screen_name = "settings"
                        elif button.text == "Quit":
                            self.running = False

            elif self.screen_name == "game":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != (0, 1):
                        self.next_direction = (0, -1)
                    elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                        self.next_direction = (0, 1)
                    elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                        self.next_direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                        self.next_direction = (1, 0)
                    elif event.key == pygame.K_ESCAPE:
                        self.screen_name = "menu"

            elif self.screen_name == "game_over":
                for button in self.buttons["game_over"]:
                    if button.clicked(event):
                        if button.text == "Retry":
                            self.start_game()
                        elif button.text == "Main Menu":
                            self.screen_name = "menu"

            elif self.screen_name == "leaderboard":
                for button in self.buttons["leaderboard"]:
                    if button.clicked(event):
                        self.screen_name = "menu"

            elif self.screen_name == "settings":
                for button in self.buttons["settings"]:
                    if button.clicked(event):
                        if button.text == "Toggle Grid":
                            self.settings["grid"] = not self.settings["grid"]
                        elif button.text == "Toggle Sound":
                            self.settings["sound"] = not self.settings["sound"]
                        elif button.text == "Change Snake Color":
                            self.change_snake_color()
                        elif button.text == "Save & Back":
                            self.save_settings()
                            self.screen_name = "menu"

    def draw_current_screen(self):
        if self.screen_name == "menu":
            self.draw_menu()
        elif self.screen_name == "game":
            self.draw_game()
        elif self.screen_name == "game_over":
            self.draw_game_over()
        elif self.screen_name == "leaderboard":
            self.draw_leaderboard()
        elif self.screen_name == "settings":
            self.draw_settings()

    def run(self):
        while self.running:
            self.clock.tick(self.speed if self.screen_name == "game" else 30)
            self.handle_events()

            if self.screen_name == "game" and not self.game_over:
                self.update_game()

            self.draw_current_screen()
            pygame.display.update()

        pygame.quit()
        sys.exit()