import pygame
import random
import math

# Инициализация Pygame
pygame.init()

# Размеры окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Белый квадрат")

# Размеры сетки
grid_size = 20
cols = width // grid_size
rows = height // grid_size

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Создание сетки
grid = [[0 for _ in range(cols)] for _ in range(rows)]

# Случайная позиция начального белого квадрата
start_x = random.randint(0, cols - 1)
start_y = random.randint(0, rows - 1)
grid[start_y][start_x] = 1

# Центр сетки
center_x = cols // 2
center_y = rows // 2

# Функция для расчёта расстояния
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Основной цикл
running = True
clock = pygame.time.Clock()
spread_speed = 1  # скорость заполнения (1 - медленно, 5 - быстро, например)

# Шрифт для отображения текста
font = pygame.font.SysFont(None, 24)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    
    # Обновление сетки
    new_grid = [row[:] for row in grid]
    # for y in range(rows):
    #     for x in range(cols):
    #         if grid[y][x] == 0:  # Если текущий квадрат чёрный
    #             min_dist = float('inf')
    #             for yy in range(rows):
    #                 for xx in range(cols):
    #                     if grid[yy][xx] == 1:
    #                         dist = distance(x, y, xx, yy)
    #                         if dist < min_dist:
    #                             min_dist = dist
                
    #             probability = min(1, spread_speed / max(1, min_dist))
    #             if random.random() < probability:
    #                 new_grid[y][x] = 1
    
    grid = new_grid

    # Рисование сетки
    for y in range(rows):
        for x in range(cols):
            color = WHITE if grid[y][x] == 1 else BLACK
            if x == center_x and y == center_y:
                color = RED  # Центр сетки выделяем красным цветом
            pygame.draw.rect(screen, color, (x * grid_size, y * grid_size, grid_size, grid_size))

    # Получение позиции курсора мыши
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_grid_x = mouse_x // grid_size
    mouse_grid_y = mouse_y // grid_size

    # Вычисление расстояния от центра до курсора мыши
    dist_to_mouse = distance(center_x, center_y, mouse_grid_x, mouse_grid_y)
    
    # Отображение расстояния на экране
    text = font.render(f'Расстояние до курсора: {dist_to_mouse:.2f}', True, WHITE)
    screen.blit(text, (10, 10))
    
    pygame.display.flip()
    clock.tick(30)  # FPS

pygame.quit()
