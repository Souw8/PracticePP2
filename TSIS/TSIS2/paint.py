import pygame
import sys
from datetime import datetime
from collections import deque
from tools import draw_shape,flood_fill

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2 Paint")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (0, 180, 0)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)
GRAY = (200, 200, 200)

current_color = BLACK
brush_size = 2

mode = "pencil"

drawing = False
start_pos = None
last_pos = None

text_active = False
text_pos = None
text_value = ""

font = pygame.font.SysFont("Arial", 28)
info_font = pygame.font.SysFont("Arial", 18)

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)



running = True

while running:
    screen.fill(GRAY)
    screen.blit(canvas, (0, 0))

    if drawing and mode in [
        "line", "rect", "circle", "square",
        "triangle", "right_triangle", "rhombus"
    ]:
        mouse_pos = pygame.mouse.get_pos()
        draw_shape(screen, mode, start_pos, mouse_pos, current_color, brush_size)

    # text preview
    if text_active:
        text_surface = font.render(text_value + "|", True, current_color)
        screen.blit(text_surface, text_pos)

    # info text
    info = f"Mode: {mode} | Brush: {brush_size}px | Color: {current_color}"
    info_surface = info_font.render(info, True, BLACK)
    screen.blit(info_surface, (10, 10))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # SAVE: Ctrl + S
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                filename = datetime.now().strftime("paint_%Y-%m-%d_%H-%M-%S.png")
                pygame.image.save(canvas, filename)
                print(f"Saved as {filename}")

            # text typing
            elif text_active:
                if event.key == pygame.K_RETURN:
                    final_text = font.render(text_value, True, current_color)
                    canvas.blit(final_text, text_pos)
                    text_active = False
                    text_value = ""

                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                    text_value = ""

                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]

                else:
                    text_value += event.unicode

            else:
                # COLORS
                if event.key == pygame.K_1:
                    brush_size = 2
                elif event.key == pygame.K_2:
                    brush_size = 5
                elif event.key == pygame.K_3:
                    brush_size = 10

                elif event.key == pygame.K_b:
                    current_color = BLACK
                elif event.key == pygame.K_r:
                    current_color = RED
                elif event.key == pygame.K_g:
                    current_color = GREEN
                elif event.key == pygame.K_u:
                    current_color = BLUE
                elif event.key == pygame.K_y:
                    current_color = YELLOW

                # MODES
                elif event.key == pygame.K_p:
                    mode = "pencil"
                elif event.key == pygame.K_l:
                    mode = "line"
                elif event.key == pygame.K_a:
                    mode = "rect"
                elif event.key == pygame.K_c:
                    mode = "circle"
                elif event.key == pygame.K_q:
                    mode = "square"
                elif event.key == pygame.K_t:
                    mode = "triangle"
                elif event.key == pygame.K_w:
                    mode = "right_triangle"
                elif event.key == pygame.K_h:
                    mode = "rhombus"
                elif event.key == pygame.K_e:
                    mode = "eraser"
                elif event.key == pygame.K_f:
                    mode = "fill"
                elif event.key == pygame.K_x:
                    mode = "text"

        if event.type == pygame.MOUSEBUTTONDOWN:

            if mode == "fill":
                flood_fill(canvas, event.pos, current_color)

            elif mode == "text":
                text_active = True
                text_pos = event.pos
                text_value = ""

            else:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

        if event.type == pygame.MOUSEMOTION and drawing:

            if mode == "pencil":
                pygame.draw.line(canvas, current_color, last_pos, event.pos, brush_size)
                last_pos = event.pos

            elif mode == "eraser":
                pygame.draw.line(canvas, WHITE, last_pos, event.pos, brush_size * 3)
                last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP and drawing:
            drawing = False
            end_pos = event.pos

            if mode in [
                "line", "rect", "circle", "square",
                "triangle", "right_triangle", "rhombus"
            ]:
                draw_shape(canvas, mode, start_pos, end_pos, current_color, brush_size)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()