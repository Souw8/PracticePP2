import pygame
import random
from persistence import save_score


pygame.init()

WIDTH = 600
HEIGHT = 800
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)
DARK_GRAY = (60, 60, 60)
RED = (220, 20, 60)
GREEN = (0, 180, 0)
BLUE = (40, 120, 220)
YELLOW = (240, 220, 0)
ORANGE = (255, 140, 0)

ROAD_LEFT = 80
ROAD_WIDTH = 440
ROAD_RIGHT = ROAD_LEFT + ROAD_WIDTH

font = pygame.font.SysFont("Arial", 26)
big_font = pygame.font.SysFont("Arial", 42)


class Player:
    def __init__(self, settings):
        self.width = 50
        self.height = 90
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 120
        self.base_speed = 6
        self.speed = self.base_speed

        if settings["car_color"] == "red":
            self.color = RED
        elif settings["car_color"] == "blue":
            self.color = BLUE
        else:
            self.color = GREEN

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        if self.x < ROAD_LEFT:
            self.x = ROAD_LEFT
        if self.x > ROAD_RIGHT - self.width:
            self.x = ROAD_RIGHT - self.width

        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)


class TrafficCar:
    def __init__(self, speed):
        self.width = 50
        self.height = 90
        self.base_speed = speed
        self.speed = speed
        self.respawn()

    def respawn(self):
        self.x = random.randint(ROAD_LEFT, ROAD_RIGHT - self.width)
        self.y = random.randint(-500, -100)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y += self.speed

        if self.y > HEIGHT:
            self.respawn()

        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, ORANGE, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)


class Coin:
    def __init__(self):
        self.size = 30
        self.speed = 5
        self.respawn()

    def respawn(self):
        self.x = random.randint(ROAD_LEFT, ROAD_RIGHT - self.size)
        self.y = random.randint(-400, -80)
        self.value = random.choice([20, 50, 100])
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def move(self):
        self.y += self.speed

        if self.y > HEIGHT:
            self.respawn()

        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        if self.value == 20:
            color = YELLOW
        elif self.value == 50:
            color = GREEN
        else:
            color = BLUE

        pygame.draw.circle(
            screen,
            color,
            (self.x + self.size // 2, self.y + self.size // 2),
            self.size // 2
        )

        value_text = pygame.font.SysFont("Arial", 16).render(str(self.value), True, BLACK)
        screen.blit(value_text, (self.x + 3, self.y + 7))


class Obstacle:
    def __init__(self):
        self.width = 65
        self.height = 40
        self.speed = 5
        self.respawn()

    def respawn(self):
        self.x = random.randint(ROAD_LEFT, ROAD_RIGHT - self.width)
        self.y = random.randint(-700, -150)
        self.type = random.choice(["barrier", "oil", "pothole"])
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y += self.speed

        if self.y > HEIGHT:
            self.respawn()

        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        if self.type == "barrier":
            color = RED
        elif self.type == "oil":
            color = BLACK
        else:
            color = DARK_GRAY

        pygame.draw.rect(screen, color, self.rect, border_radius=6)


class PowerUp:
    def __init__(self):
        self.size = 36
        self.speed = 5
        self.timeout = 5000
        self.types = ["nitro", "shield", "repair"]
        self.respawn()

    def respawn(self):
        self.type = random.choice(self.types)
        self.x = random.randint(ROAD_LEFT, ROAD_RIGHT - self.size)
        self.y = random.randint(-800, -150)
        self.spawn_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def move(self):
        self.y += self.speed
        now = pygame.time.get_ticks()

        if self.y > HEIGHT or now - self.spawn_time > self.timeout:
            self.respawn()

        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        if self.type == "nitro":
            color = BLUE
            text = "N"
        elif self.type == "shield":
            color = GREEN
            text = "S"
        else:
            color = YELLOW
            text = "R"

        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        label = font.render(text, True, BLACK)
        screen.blit(label, (self.x + 9, self.y + 3))


def ask_username(screen, clock):
    name = ""

    while True:
        screen.fill(WHITE)

        title = big_font.render("Enter your name", True, BLACK)
        name_text = font.render(name, True, BLACK)
        hint = font.render("Press ENTER to start", True, DARK_GRAY)

        screen.blit(title, (135, 230))
        pygame.draw.rect(screen, GRAY, (150, 320, 300, 55), border_radius=8)
        screen.blit(name_text, (165, 335))
        screen.blit(hint, (160, 410))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip() == "":
                        return "Player"
                    return name

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    if len(name) < 12:
                        name += event.unicode

        pygame.display.update()
        clock.tick(FPS)


def draw_road(screen, line_y):
    screen.fill(GRAY)

    pygame.draw.rect(screen, BLACK, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))

    pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 5)
    pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 5)

    for i in range(-40, HEIGHT, 80):
        pygame.draw.rect(screen, WHITE, (225, i + line_y, 10, 40))
        pygame.draw.rect(screen, WHITE, (375, i + line_y, 10, 40))


def get_difficulty_values(settings):
    difficulty = settings["difficulty"]

    if difficulty == "easy":
        return 1, 5
    elif difficulty == "hard":
        return 3, 7
    else:
        return 2, 6


def run_game(screen, clock, settings):
    username = ask_username(screen, clock)

    if username is None:
        return "quit"

    traffic_count, traffic_speed = get_difficulty_values(settings)

    player = Player(settings)
    traffic_cars = [TrafficCar(traffic_speed) for _ in range(traffic_count)]
    coins = Coin()
    obstacles = [Obstacle()]
    powerup = PowerUp()

    coins_collected = 0
    distance = 0
    bonus_score = 0
    score = 0

    line_y = 0
    line_speed = 7

    active_power = None
    power_start_time = 0
    power_duration = 4000
    shield_active = False
    nitro_active = False

    game_over = False
    saved = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "play"
                if event.key == pygame.K_m:
                    return "menu"

        if not game_over:
            keys = pygame.key.get_pressed()
            player.move(keys)

            distance += 1
            score = coins_collected + distance // 10 + bonus_score

            line_y += line_speed
            if line_y >= 40:
                line_y = 0

            if distance > 1500 and len(traffic_cars) < traffic_count + 1:
                traffic_cars.append(TrafficCar(traffic_speed + 1))

            if distance > 3000 and len(obstacles) < 2:
                obstacles.append(Obstacle())

            if distance > 5000 and len(obstacles) < 3:
                obstacles.append(Obstacle())

            coins.move()
            powerup.move()

            for traffic in traffic_cars:
                traffic.speed = traffic.base_speed + distance // 2500
                traffic.move()

                if player.rect.colliderect(traffic.rect):
                    if shield_active:
                        shield_active = False
                        active_power = None
                        traffic.respawn()
                    else:
                        game_over = True

            for obstacle in obstacles:
                obstacle.speed = 5 + distance // 3000
                obstacle.move()

                if player.rect.colliderect(obstacle.rect):
                    if obstacle.type == "oil":
                        player.speed = max(3, player.speed - 1)
                        obstacle.respawn()

                    elif shield_active:
                        shield_active = False
                        active_power = None
                        obstacle.respawn()

                    else:
                        game_over = True

            if player.rect.colliderect(coins.rect):
                coins_collected += coins.value
                coins.respawn()

            if player.rect.colliderect(powerup.rect):
                if active_power is None:
                    active_power = powerup.type
                    power_start_time = pygame.time.get_ticks()

                    if active_power == "nitro":
                        nitro_active = True
                        player.speed += 3
                        bonus_score += 50

                    elif active_power == "shield":
                        shield_active = True
                        bonus_score += 30

                    elif active_power == "repair":
                        if obstacles:
                            obstacles[0].respawn()
                        bonus_score += 20
                        active_power = None

                    powerup.respawn()

            if active_power == "nitro":
                now = pygame.time.get_ticks()

                if now - power_start_time > power_duration:
                    if nitro_active:
                        player.speed -= 3
                        nitro_active = False

                    active_power = None

            draw_road(screen, line_y)

            coins.draw(screen)
            powerup.draw(screen)

            for obstacle in obstacles:
                obstacle.draw(screen)

            for traffic in traffic_cars:
                traffic.draw(screen)

            player.draw(screen)

            coins_text = font.render(f"Coins: {coins_collected}", True, WHITE)
            distance_text = font.render(f"Distance: {distance}", True, WHITE)
            score_text = font.render(f"Score: {score}", True, WHITE)
            power_text = font.render(f"Power: {active_power}", True, WHITE)

            screen.blit(coins_text, (20, 20))
            screen.blit(distance_text, (20, 50))
            screen.blit(score_text, (20, 80))
            screen.blit(power_text, (20, 110))

        else:
            if not saved:
                save_score(username, score, distance)
                saved = True

            screen.fill(WHITE)

            title = big_font.render("GAME OVER", True, RED)
            score_text = font.render(f"Score: {score}", True, BLACK)
            coins_text = font.render(f"Coins: {coins_collected}", True, BLACK)
            distance_text = font.render(f"Distance: {distance}", True, BLACK)
            retry_text = font.render("Press R to Retry", True, BLACK)
            menu_text = font.render("Press M for Main Menu", True, BLACK)

            screen.blit(title, (175, 220))
            screen.blit(score_text, (210, 300))
            screen.blit(coins_text, (210, 340))
            screen.blit(distance_text, (210, 380))
            screen.blit(retry_text, (190, 450))
            screen.blit(menu_text, (160, 490))

        pygame.display.update()
        clock.tick(FPS)