import pygame
import sys
from Chunks import Chunk, ChunkManager
import numpy

chunk_manager = ChunkManager()

pygame.init()
biomes = {
		"Forest": pygame.transform.scale(pygame.image.load("./Images/Bioms/Forest.png"), (4, 4)),
		"Desert": pygame.transform.scale(pygame.image.load("./Images/Bioms/Desert.png"), (4, 4)),
		"Field": pygame.transform.scale(pygame.image.load("./Images/Bioms/Field.png"), (4, 4)),
		"Taiga": pygame.transform.scale(pygame.image.load("./Images/Bioms/Taiga.png"), (4, 4)),
		"Swamp": pygame.transform.scale(pygame.image.load("./Images/Bioms/Swamp.png"), (4, 4))
}

win = pygame.display.set_mode((1000, 1000))
width, height = 240, 240
arr = numpy.empty((width, height), dtype="U10")
arr[:] = ""

for x in range(width):
	for y in range(height):
		chunk = Chunk(x, y)
		chunk_manager.generate_chunk(chunk)
		arr[y, x] = chunk.biome

world = pygame.Surface((width * 4, height * 4))
for x in range(width):
	for y in range(height):
		world.blit(biomes[arr[y, x]], (x * 4, y * 4))

# pygame.image.save(world, "world.png")

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	win.fill((0, 0, 0))
	win.blit(world, (0, 0))
	pygame.display.update()
