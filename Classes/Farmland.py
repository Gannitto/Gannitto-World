import pygame
import random
from Assets import farmland_images, plant_images, seed_types
from Sound import play_sound
from Functions import destroy_object
from Globals import win, Settings
from Classes.Object import Object
from Classes.Particle import Particle

class Farmland:

	def __init__(self, X, Y):

		self.x = X
		self.y = Y

		self.neigbords = []
		self.rect = pygame.Rect(self.x - 64, self.y - 64, 128, 128)
		self.images = farmland_images
		self.image = self.images[0]
		self.plant = None
		self.plant_growth_stage = 0
		self.grow_timer = 0
		self.watered = False
		
	def main(self, release, dt, game, mouse_x, mouse_y):

		world_rect = game.world_rect_to_screen(self.x - 64, self.y + 64, 128, 128)
		if release and pygame.Rect(world_rect).collidepoint((mouse_x, mouse_y)):
			self.handle_click(game.world)
		win.blit(self.image, game.world_to_screen(self.x, self.y, 256, 256))
		if self.plant is not None:
			win.blit(plant_images[self.plant][self.plant_growth_stage], game.world_to_screen(self.x, self.y, 256, 256))
			if self.plant_growth_stage != 3:
				self.grow_timer -= dt
			if self.grow_timer <= 0:
				self.plant_growth_stage += 1
				self.grow_timer = random.randint(250, 350)
				if self.plant_growth_stage == 2 and not self.watered:
					self.plant_growth_stage = 3
		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), world_rect, 3)
		
	def handle_click(self, game):

		slot = game.inventory.whole_inventory[game.inventory.changed_slot]
		if self.plant is None:
			if slot is not None and slot.name in seed_types:
				self.plant = seed_types[slot.name]
				game.inventory.reduce(game.changed_slot)
				self.grow_timer = random.randint(250, 350)
		elif self.plant_growth_stage == 1:
			if slot is not None and slot.name == "Water bucket":
				game.inventory.reduce(game.inventory.changed_slot)
				game.inventory.increate("Water bucket")
				self.watered = True
				play_sound("Watering plants ", 2)
		elif self.plant_growth_stage == 2:
			destroy_object(plant_images[self.plant][self.plant_growth_stage], self.x - 64, self.y + 64, game.world, Particle)
			for _ in range(random.randint(1, 3)):
				rand_x, rand_y = self.x - 64 + random.randint(-64, 64), self.y + 64 + random.randint(-64, 64)
				game.world.chunk_manager.get_chunk_at(rand_x, rand_y).items.append(Object(self.plant, rand_x, rand_y, f"Images/Items/{self.plant}.png", pickable=True))
			self.plant = None
			self.plant_growth_stage = 0
			self.watered = False
		elif self.plant_growth_stage == 3:
			destroy_object(plant_images[self.plant][self.plant_growth_stage], self.x - 64, self.y + 64, game.world, Particle)
			self.plant = None
			self.plant_growth_stage = 0

		if slot is not None and slot.name == "Stone shovel":
			play_sound("Dirt")
			del game.world.chunk_manager.get_chunk_at(self.x, self.y).farmlands[(self.x, self.y)]
	
	def __getstate__(self):
		
		state = self.__dict__.copy()
		state["image"] = self.images.index(self.image)
		del state["images"]
		rect = state["rect"]
		state["rect"] = (rect[0], rect[1], rect[2], rect[3])
		return state

	def __setstate__(self, state):
		
		self.__dict__.update(state)
		self.images = farmland_images
		self.image = self.images[self.image]
		self.rect = pygame.Rect(state["rect"][0], state["rect"][1], state["rect"][2], state["rect"][3])
