import pygame

from collections import deque

WIDTH, HEIGHT = 800, 600

def flood_fill(surface, start_pos, fill_color):
    x, y = start_pos

    target_color = surface.get_at((x, y))

    if target_color == fill_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        x, y = queue.popleft()

        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            continue

        if surface.get_at((x, y)) != target_color:
            continue

        surface.set_at((x, y), fill_color)

        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))


def draw_shape(surface, mode, start, end, color, size):
    x1, y1 = start
    x2, y2 = end

    if mode == "line":
        pygame.draw.line(surface, color, start, end, size)

    elif mode == "rect":
        rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        pygame.draw.rect(surface, color, rect, size)

    elif mode == "circle":
        radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
        pygame.draw.circle(surface, color, start, radius, size)

    elif mode == "square":
        side = min(abs(x2 - x1), abs(y2 - y1))

        if x2 < x1:
            side = -side

        rect = pygame.Rect(x1, y1, side, side)
        pygame.draw.rect(surface, color, rect, size)

    elif mode == "right_triangle":
        points = [(x1, y1), (x2, y1), (x1, y2)]
        pygame.draw.polygon(surface, color, points, size)

    elif mode == "triangle":
        points = [
            (x1, y2),
            ((x1 + x2) // 2, y1),
            (x2, y2)
        ]
        pygame.draw.polygon(surface, color, points, size)

    elif mode == "rhombus":
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        points = [
            (cx, y1),
            (x2, cy),
            (cx, y2),
            (x1, cy)
        ]
        pygame.draw.polygon(surface, color, points, size)
