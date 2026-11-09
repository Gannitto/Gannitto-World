import pygame
import math
import random
import time
from Cache import load
from Assets import explosion_texture
from Globals import Width, Height, path, Settings, win
from Classes.Particle import Particle

class Projectile:

	def __init__(self, X: int, Y: int, mouse_x, mouse_y, type: str):
		
		"""
		Снаряд, который непрерывно летит в заданном направлении
		X - Координата x
		Y - Координата y
		mouse_x - x мыши
		mouse_y - y мыши
		type - Тип патрона, например стрела
		"""

		self.x = X
		self.y = Y

		self.angle = math.atan2(Height / 2 - mouse_y, Width / 2 - mouse_x)
		self.x_vel = math.cos(self.angle) * 100
		self.y_vel = math.sin(self.angle) * 100
		self.image = pygame.transform.rotate(load(path + "Images/Items/" + type + ".png", 64), math.atan2(mouse_x - Width / 2, mouse_y - Height / 2) * 180 / math.pi + 180)
		self.end_time = int(time.time()) + 3

	def main(self, game):

		"""Показывает снаряд"""

		self.x -= int(self.x_vel)
		self.y += int(self.y_vel)
		
		win.blit(self.image, game.world_to_screen(self.x, self.y, 64, 64))

		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), game.world_rect_to_screen(self.x, self.y, 64, 64), 3)
		if time.time() >= self.end_time:
			game.world.projectiles.remove(self)

class ExplodingProjectile:

	def __init__(self, X: int, Y: int, mouse_x: int, mouse_y: int, type: str, target_pos: tuple):
		
		"""
		Снаряд, который летит до заданной точки и потом взрывается
		X - Координата x
		Y - Координата y
		mouse_x - x мыши
		mouse_y - y мыши
		type - Тип патрона, например граната
		"""

		self.x = X
		self.y = Y
		self.start_x = X
		self.start_y = Y

		self.angle = math.atan2(Height / 2 - mouse_y, Width / 2 - mouse_x)
		self.x_vel = math.cos(self.angle) * 50
		self.y_vel = math.sin(self.angle) * 50
		self.image = pygame.transform.rotate(load(path + "Images/Items/" + type + ".png", 64), math.atan2(mouse_x - Width / 2, mouse_y - Height / 2) * 180 / math.pi + 180)
		self.dist_x = abs(target_pos[0] - self.x)
		self.dist_y = abs(target_pos[1] - self.y)

	def main(self, game):

		"""Показывает снаряд"""

		self.x -= int(self.x_vel)
		self.y += int(self.y_vel)
		
		rect = self.image.get_rect()
		rect_rotated = pygame.transform.rotate(self.image, -10)
		rect_copy = rect.copy()
		rect_copy.center = rect_rotated.get_rect().center
		
		win.blit(rect_rotated.subsurface(rect_copy).copy(), game.world_to_screen(self.x, self.y, 64, 64))

		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), game.world_rect_to_screen(self.x, self.y, 64, 64), 3)
		if abs(self.x - self.start_x) > self.dist_x or abs(self.y - self.start_y) > self.dist_y:
			radius = 20
			for _ in range(150):
				angle = random.uniform(0, 2 * math.pi)
				radius -= 0.1
				game.world.particles.append(Particle(self.x, self.y, explosion_texture.copy(), x_bias=radius * math.cos(angle), y_bias=radius * math.sin(angle), increased_transparency=30, end_time=0.3))
			game.world.projectiles.remove(self)

