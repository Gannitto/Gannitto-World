import pygame
import os
from random import randint
from Globals import path, FPS, Width, Height, win
from Functions import shadow

class Ron:

	def __init__(self, world_to_screen):
		self.x = 0
		self.y = 0
		self.home = (0, 0)
		self.direction = "Down"
		self.costum = 0
		self.window = [False, 0]
		self.images = {"Down": pygame.transform.scale(pygame.image.load(path + "Images/Players/Ron/Normal/Down/1.png"), (256, 256))}
		self.inventory = {"Bow": 0, "Arrow": 0, "Stick": 0, "Iron ingot": 0}
		self.speed = 50
		self.world_to_screen = world_to_screen

	def show(self):
		win.blit(shadow(self.images[self.direction], "Ron " + self.direction), self.world_to_screen(self.x, self.y, 256, 256))

	def walk(self, x: int, y: int):

		if self.home is None:

			if not (-256 < self.x - x < 256):
				if self.x < x:
					self.x += self.speed / FPS * 30
				elif x < self.x:
					self.x -= self.speed / FPS * 30
			
			if not (-256 < self.y - y < 256):
				if self.y < y:
					self.y += self.speed / FPS * 30
				elif y < self.y:
					self.y -= self.speed / FPS * 30

		else:

			if not (-256 < self.x - self.home[0] < 256):
				if self.x < self.home[0]:
					self.x += self.speed / FPS * 30
				elif self.home[0] < self.x:
					self.x -= self.speed / FPS * 30
			
			if not (-256 < self.y - self.home[1] < 256):
				if self.y < self.home[1]:
					self.y += self.speed / FPS * 30
				elif self.home[1] < self.y:
					self.y -= self.speed / FPS * 30

	def check_items(self, x, y, world):

		"""Проверяет лежащие предметы вокруг Рона"""

		if self.home is None:

			for item in world.visible_items:

				if x - 256 <= item.x <= x + 256 and y - 256 <= item.y <= y + 256 and item.name in ["Arrow", "Stick", "Iron ingot"]:
					
					if not (-32 < self.x - item.x < 32) and not (-32 < self.y - item.y < 32):
						
						if self.x < item.x:
							self.x += 30
						elif item.x < self.x:
							self.x -= 30

						if self.y < item.y:
							self.y += 30
						elif item.y < self.y:
							self.y -= 30

						break

					else:

						self.inventory[item.name] += 1
						world.chunk_manager.get_chunk_at(item.x, item.y).items.remove(item)
						break

	def check_mobs(self, world, Projectile, x, y):

		"""Проверяет мобов вокруг Рона"""
		
		for mob in world.mobs:

			if self.inventory["Arrow"] > 0 and self.x - Width // 2 <= mob.x <= self.x + Width // 2 and self.y - Height // 2 <= mob.y <= self.y + Height // 2 and mob.name == "Slime" and randint(1, FPS / 2) == 1:

				world.projectiles.append(Projectile(self.x, self.y, mob.x - x + Width // 2 - 64, y - mob.y + Height // 2 - 32, "Arrow"))
				break

	def get_start_items(self):

		"""Выдаёт Рону в инвентарь начальные предметы"""

		self.inventory["Bow"] = 1
		self.inventory["Arrow"] = 99

