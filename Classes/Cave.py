import pygame
import random
from Assets import cave_texture
from Globals import win, Width, Height
from Classes.Object import Object

class Cave:

	def __init__(self, world, cave_x, cave_y, w, h):

		self.x = cave_x
		self.y = cave_y
		self.w = 128
		self.h = 128
		self.own_width = w
		self.own_height = h
		self.image = cave_texture
		self.objects = []
		self.seed = (int(self.x) * 888888 + int(self.y) * 425269) ^ 0x9e3779b9
		self.noise = world.chunk_manager.generator.get_cave_noise(self.seed)
		self.generate()

	def generate(self, world):

		# for _ in range(self.own_width // 100 + random.randint(-10, 10)):
		#	self.objects.append(Object("Stone", random.randint(self.own_width // 2 * -1, self.own_width // 2), random.randint(self.own_height // 2 * -1, self.own_height // 2), "Images/Items/Stone.png"))
			
		# for _ in range(self.own_width // 300 + random.randint(-10, 10)):
		#	self.objects.append(Object("Iron ore", random.randint(self.own_width // 2 * -1, self.own_width // 2), random.randint(self.own_height // 2 * -1, self.own_height // 2), "Images/Objects/Iron ore.png", (256, 256), special_flags=100, is_solid=True))

		# for _ in range(self.own_width // 300 + random.randint(-10, 10)):
		#	self.objects.append(Object("Gold ore", random.randint(self.own_width // 2 * -1, self.own_width // 2), random.randint(self.own_height // 2 * -1, self.own_height // 2), "Images/Objects/Gold ore.png", (256, 256), special_flags=100, is_solid=True))
		self.cave_map = world.chunk_manager.generator.generate_cave(self.noise, self.own_width, self.own_height)

	def main(self, player):

		if player.x - Width // 2 <= self.x <= player.x + Width // 2 and player.y - Height // 2 <= self.y + Height // 2:
			win.blit(self.image, (self.x - player.x + Width // 2 - self.w // 2, player.y - self.y + Height // 2 - self.h // 2))
		
	def get_in(self, player):

		global mouse_x, mouse_y
		mouse_x, mouse_y = pygame.mouse.get_pos()
		if self.x <= player.x <= self.x + 128 and self.y <= player.y <= self.y + 128 and self.x - player.x + Width // 2 - self.w // 2 <= mouse_x <= self.x - player.x + Width // 2 - self.w // 2 + 128 and player.y - self.y + Height // 2 - self.h // 2 <= mouse_y <= player.y - self.y + Height // 2 - self.h // 2 + 128 and pygame.mouse.get_pressed()[0]:
			return self
		else:
			return None

	def render(self, world_rect_to_screen):
		for Y in range(self.own_height // 64):
			for X in range(self.own_width // 64):
				if self.cave_map[Y][X]:
					pygame.draw.rect(win, (50, 50, 50), world_rect_to_screen(X * 64 - self.own_width // 2, Y * 64 - self.own_height // 2, 64, 64))
		
	def __getstate__(self):
		
		state = self.__dict__.copy()
		del state["image"]
		return state

	def __setstate__(self, state):
		
		self.__dict__.update(state)
		self.image = cave_texture
