import pygame
import os
from random import randint
from Globals import path, Width, Height, win
from Functions import shadow

class Ron:

	def __init__(self, world_to_screen, Projectile, player):

		self.x = 0
		self.y = 0
		self.home = (0, 0)
		self.direction = "Down"
		self.costum = 0
		self.window = [False, 0]
		self.images = {"Down": pygame.transform.scale(pygame.image.load(path + "Images/Players/Ron/Normal/Down/1.png"), (256, 256))}
		self.inventory = {"Bow": 0, "Arrow": 0, "Stick": 0, "Iron ingot": 0}
		self.speed = 50
		self.INTERACTION_RADIUS = 400
		self.PICKUP_RADIUS = 32
		self.PLAYER_RADIUS = 512
		self.world_to_screen = world_to_screen
		self.Projectile = Projectile
		self.player = player

	def show(self):
		win.blit(shadow(self.images[self.direction], "Ron " + self.direction), self.world_to_screen(self.x, self.y, 256, 256))

	def move_towards_player(self, dt):
		"""Обобщенный метод движения к цели"""
		dx = self.player.x - self.x
		dy = self.player.y - self.y
		distance = (dx**2 + dy**2)**0.5
		
		if distance > self.PLAYER_RADIUS:
			step = self.speed / dt * 30
			if abs(dx) > self.PLAYER_RADIUS:
				self.x += step if dx > 0 else -step
			if abs(dy) > self.PLAYER_RADIUS:
				self.y += step if dy > 0 else -step
			return True
		return False

	def move_towards_item(self, target_x, target_y, dt):
		"""Обобщенный метод движения к цели"""
		dx = target_x - self.x
		dy = target_y - self.y
		distance = (dx**2 + dy**2)**0.5
		
		if distance > self.PICKUP_RADIUS:
			step = self.speed / dt * 30
			if abs(dx) > self.PICKUP_RADIUS:
				self.x += step if dx > 0 else -step
			if abs(dy) > self.PICKUP_RADIUS:
				self.y += step if dy > 0 else -step
			return True
		return False

	def check_items(self, world, dt):
		"""Проверяет и подбирает предметы вокруг Рона"""
		target = self.home if self.home is not None else None

		for item in world.visible_items[:]:  # Копия списка для безопасного удаления
			if item.name not in ("Arrow", "Stick", "Iron ingot"):
				continue
				
			dx = abs(self.x - item.x)
			dy = abs(self.y - item.y)
			
			# Если предмет в радиусе подбора
			if dx <= self.PICKUP_RADIUS and dy <= self.PICKUP_RADIUS:
				self._pickup_item(item, world)
				return True
			
			# Если предмет в радиусе взаимодействия
			if dx <= self.INTERACTION_RADIUS and dy <= self.INTERACTION_RADIUS:
						
				if self.home is None:
					dx_to_player = self.player.x - item.x
					dy_to_player = self.player.y - item.y
					distance_to_player = (dx_to_player**2 + dy_to_player**2)**0.5
				if self.home or distance_to_player <= self.PLAYER_RADIUS:
					self.move_towards_item(item.x, item.y, dt)
					return True
		
		return False

	def _pickup_item(self, item, world):
		"""Подбирает предмет"""
		self.inventory[item.name] += 1
		chunk = world.chunk_manager.get_chunk_at(item.x, item.y)
		if chunk and item in chunk.items:
			chunk.items.remove(item)
	
	def check_mobs(self, world, dt):
		"""Проверяет мобов и атакует при возможности"""
		if self.inventory["Arrow"] <= 0:
			return
		if randint(1, int(dt * 10000)) != 1:  # Шанс атаки
			return
		
		for mob in world.mobs:
			if not ((abs(self.x - mob.x) <= Width // 2 and abs(self.y - mob.y) <= Height // 2)):
				continue
				
			if mob.name in ("Slime", "Spider"):
				world.projectiles.append(self.Projectile(self.x, self.y, mob.x - self.x + Width // 2 - 64, self.y - mob.y + Height // 2 - 32, "Arrow"))
				return
	
	def update(self, world, dt):
	
		if self.home is None:
			self.move_towards_player(dt)
		self.check_items(world, dt)
		self.check_mobs(world, dt)
		self.show()

	def get_start_items(self):

		"""Выдаёт Рону в инвентарь начальные предметы"""

		self.inventory["Bow"] = 1
		self.inventory["Arrow"] = 99

