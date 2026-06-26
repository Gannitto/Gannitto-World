import pygame
pygame.init()

image = pygame.image.load("C:/Users/HP/Downloads/1.png")
image2 = pygame.Surface((60, 80))
i = -1
ii = -1
for x in range(4, 600, 10):
    ii = -1
    i += 1
    for y in range(4, 800, 10):
        ii += 1
        image2.set_at((i, ii), image.get_at((x, y)))

image.pygame
pygame.image.save(image2, "C:/Users/HP/Downloads/2.png")
