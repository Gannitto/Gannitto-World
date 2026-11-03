import pygame
import subprocess
import pyperclip
from pathlib import Path
import time
import random
import math
from itertools import product
import socket
import sys
import os
import Backrooms
from Ron import Ron
import Saver
from Multiplayer import NetworkManager
from Functions import *
from Build import build, check_build_objects, draw_select_image, draw_select_image_arbitrarily
from Chunks import ChunkManager
from Inventory import inventory
from Translator import translator
from Cache import load
from UISystem import UISystem
from TimeSystem import TimeSystem
from Commands import command_system
from Sound import play_sound, set_sound_volume, music_channel
from InputSystem import input_system
from Assets import *
from Globals import *
from Classes import Player, World, Object, Particle, Slime, Spider, Butterfly
from Light import create_light_circle, create_light_circle_with_falloff, remove_light_circle

pygame.init()

"""
Чтобы найти что-то на карте кода, просто вбейте в поиск

Карта кода:

Классы
Загрузка команд
Кнопки в меню
Загрузка данных мира
Основной цикл игры
	Отображение объектов
	Отображение мобов
	Анимация игрока
	Рон
	Механика использования еды и некоторых предметов через пробел
	Отрисовка погоды
	Отображение частиц
	Механика освещения
	Механика анимации слотов
	Меню на клавише TAB
	Отображение инвентаря
	Отображение полосы здоровья
	Механика мультиплеера
Меню редактирования мира
Меню миров
Меню

	########					########	 ###	  ###		   ########
   ##########				  #########		 ###	  ###		 ######### 
   #		####			 ###			 ###	  ###		###		   
   #############			  ########		 ###	  ###		 ########  
   #############			   ########		 ###	  ###		  ######## 
   #############					 ###	 ###	  ###				###
   ####   ####				 ##########		 ############		########## 
   ####   ####				#########		   ########		   #########   

"""

translator.load_language(Settings["Languages"][0])
t = translator.get

def get_build_number():
	try:
		build_num = int(subprocess.check_output(("git", "rev-list", "--count", "HEAD"), text=True).strip())
	except:
		build_num = "Error"
	return build_num

def save(darken:bool=True, save_world_settings:bool=False):

	"""
	Сохраняет игру
	darken - Затемнять ли экран
	save_world_settings - Сохранять ли настройки мира
	"""

	global player
	Saver.save_objects(path + "Saves/Settings/Statistics.save", statistics)
	
	if world_name is not None:
		
		if multiplayer:
			pass
			# TODO сохранение данных о других игроках
		else:
			
			Saver.save_objects(path + "Saves/Worlds/" + world_name + "/Mobs.save", world.mobs)
			Saver.save_objects(path + "Saves/Worlds/" + world_name + "/Info.save", [player.x, player.y, Backrooms.InBackrooms, Backrooms.Level, world.current_cave, player.speed, player.HP, start_time, ron.x, ron.y, ron.home, ron.inventory, world.chunk_manager.generator.seed, time_system.current_time])
			Saver.save_objects(path + "Saves/Worlds/" + world_name + "/Inventory.save", inventory.whole_inventory)
			Saver.save_objects(path + "Saves/Worlds/" + world_name + "/Resources.save", inventory.resources)
			Saver.save_objects(path + "Saves/Worlds/" + world_name + "/Effects.save", player.effects)

			new_particles = []
			particle_count = 1
			for particle in new_particles:
				if particle.save_particle:
					pygame.image.save(particle.image, path + "Saves/Worlds/" + world_name +"/Images/Particle " + str(particle_count) + ".png")
					particle.image_path = path + "Saves/Worlds/Images/Particle " + str(particle_count) + ".png"
					particle_count += 1
					new_particles.append(particle)
			Saver.save_objects(path + "Saves/Worlds/" + world_name + "/Particles.save", new_particles)
			world.chunk_manager.save_all_loaded_chunks()
				
	if darken and Settings["Display"][9]:
		win_darken(win)
		
	if save_world_settings: Saver.save_objects(path + "Saves/Worlds/" + world_name + "/Settings.save", [game.difficulty, player.god_mode])

# Применение настроек TODO

statistics[0] += 1

pygame.display.set_icon(pygame.image.load(path + "Images/Icon.png"))
pygame.display.set_caption("Gannitto World")



# Классы

player = Player()
world_to_screen = lambda X, Y, W, H, player=player: (X - player.x + Width // 2 - W // 2, player.y - Y + Height // 2 - H // 2)
world_rect_to_screen = lambda X, Y, W, H, player=player: (X - player.x + Width // 2 - W // 2, player.y - Y + Height // 2 - H // 2, W, H)
world = World(world_rect_to_screen)
time_system = TimeSystem()

class Peer(Player):

	def __init__(self, id: str, address: tuple, name: str, last_seen: float, X: int = 0, Y: int = 0, view_distance: int = 1):
		super().__init__()
		self.address = address
		self.name = name
		self.last_seen = last_seen
		self.x = X
		self.y = Y
		self.view_distance = view_distance
	
	def render(self, screen):
		"""Отрисовывает игрока на экране"""
		frames = self.animations[self.direction]
		screen.blit(shadow(self.image, f"Player {self.direction} {self.frame_index % len(frames)}"), world_to_screen(self.x, self.y, 256, 256))
		if self.changed_item is not None and self.direction != "Up":
			changed_item_x = 0
			changed_item_y = 0
			match self.direction:
				case "Down":
					changed_item_x = -80
					changed_item_y = 0
				case "Left":
					changed_item_x = -84
					changed_item_y = 0
				case "Right":
					changed_item_x = -20
					changed_item_y = 0
			win.blit(inventory.resources[self.changed_item].image, world_to_screen(self.x + changed_item_x + 128, self.y + changed_item_y - 128, 256, 256))
		text_x, text_y = world_to_screen(self.x + 128, self.y + 32, 256, 256)
		text(self.name, text_x, text_y, (255, 255, 255), alignment=True)
		
		if Settings["Display"][3]:
			self.rect = pygame.Rect(self.x - 25, self.y - 112, 50, 224)
			pygame.draw.rect(screen, (0, 255, 0), world_rect_to_screen(self.x, self.y, 256, 256), 2)
			pygame.draw.rect(win, (0, 0, 0), (self.rect[0] - self.x + Width // 2, self.y - self.rect[1] - self.rect[3] + Height // 2, self.rect[2], self.rect[3]), 3)

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

	def main(self):

		"""Показывает снаряд"""

		self.x -= int(self.x_vel)
		self.y += int(self.y_vel)
		
		win.blit(self.image, world_to_screen(self.x, self.y, 64, 64))

		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), world_rect_to_screen(self.x, self.y, 64, 64), 3)
		if time.time() >= self.end_time:
			world.projectiles.remove(self)

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

	def main(self):

		"""Показывает снаряд"""

		self.x -= int(self.x_vel)
		self.y += int(self.y_vel)
		
		rect = self.image.get_rect()
		rect_rotated = pygame.transform.rotate(self.image, -10)
		rect_copy = rect.copy()
		rect_copy.center = rect_rotated.get_rect().center
		self.image = rect_rotated.subsurface(rect_copy).copy()

		win.blit(self.image, world_to_screen(self.x, self.y, 64, 64))

		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), world_rect_to_screen(self.x, self.y, 64, 64), 3)
		if abs(self.x - self.start_x) > self.dist_x or abs(self.y - self.start_y) > self.dist_y:
			radius = 20
			for _ in range(150):
				angle = random.uniform(0, 2 * math.pi)
				radius -= 0.1
				world.particles.append(Particle(self.x, self.y, explosion_texture.copy(), x_bias=radius * math.cos(angle), y_bias=radius * math.sin(angle), increased_transparency=30, end_time=0.3))
			world.projectiles.remove(self)

ron = Ron(world_to_screen, Projectile, player)

class Button:

	def __init__(self, X: int, Y: int, image1: pygame.Surface, image2: pygame.Surface, surface=win, alignment=False, sound=True, cooldown=0.15, info=None, action=None):

		"""
		Кнопка.
		Аргементы:
		x - Координата x, на которой появится кнопка
		y - Координата y, на которой появится кнопка
		image1 - Изображение кнопки
		image2 - Изображение кнопки, когда на неё навели
		surface - Плоскость, на которой появится кнопка
		aligment - Выравнивание кнопки по центру своих координат
		sound - Будет ли раздаваться звук при нажатии на кнопку, или нет
		cooldown - Задержка в секундах между срабатываниями (защита от спама)
		info - Текст всплывающей подсказки
		action - Функция, которая выполняется после нажатия
		"""

		self.w = image1.get_width()
		self.h = image2.get_height()

		self.x = X
		self.y = Y

		self.image = image1
		self.image1 = image1
		self.image2 = image2

		self.surface = surface
		self.alignment = alignment

		self.sound = sound
		self.cooldown = cooldown

		self.info = info
		self.hold = 0
		self.info_y = 0
		self.info_speed = 3
		self.info_forward = True
		self.info_back = False

		self.action = action

		self.is_pressed = False
		self.is_activated = False
		self.last_trigger_time = 0
	
	def main(self, action=None):

		"""Главная функция кнопки, которая её показывает и работает с её механикой"""

		mouse_x, mouse_y = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		current_time = pygame.time.get_ticks()
		
		if self.info_back:

			if self.info_y <= 0:
				self.info_back = False
				self.info_y = 0
				self.info_speed = 3
				self.info_forward = True
			else:
				self.info_speed += 2
				self.info_y -= self.info_speed

		elif self.hold > 20:

			if self.info_y < 60:
				self.info_speed += 7
				self.info_y += self.info_speed

			elif self.info_y < 100 and self.info_forward:
				self.info_speed -= 4
				self.info_y += self.info_speed

			elif 100 < self.info_y < 130:
				self.info_y -= self.info_speed // 4
				self.info_forward = False

		if self.info is not None and self.info_y != 0:

			if self.alignment:
				pygame.draw.rect(self.surface, menu_color_medium, (self.x - textInfo.size(self.info)[0] // 2 - 5, self.y - self.h / 2 - self.info_y - 5, textInfo.size(self.info)[0] + 10, 28))
				self.surface.blit(textInfo.render(self.info, True, menu_color_medium, menu_color_light), (self.x - textInfo.size(self.info)[0] // 2, self.y - self.h / 2 - self.info_y))
			else:
				pygame.draw.rect(self.surface, menu_color_medium, (self.x - self.w // 2 - textInfo.size(self.info)[0] // 2 - 5, self.y - self.h / 2 - self.info_y - 5, textInfo.size(self.info)[0] + 10, 28))
				self.surface.blit(textInfo.render(self.info, True, menu_color_medium, menu_color_light), (self.x - self.w // 2 - textInfo.size(self.info)[0] // 2, self.y - self.info_y))

		hovered = self.alignment and (self.x - self.w / 2 < mouse_x < self.x + self.w / 2 and self.y - self.h / 2 < mouse_y < self.y + self.h / 2) or not self.alignment and (self.x < mouse_x < self.x + self.w and self.y < mouse_y < self.y + self.h)
		if hovered:

			self.image = self.image2
			self.hold += 1

			#if self.info_back:   # Очень необычная механика

			#	self.info_speed += 2
			#	self.info_y -= self.info_speed

			#elif self.hold > 50:

			#	if self.info_y < 50:
			#		self.info_speed += 4
			#		self.info_y += self.info_speed

			#	elif self.info_y >= 50 and self.info_forward:
			#		self.info_speed -= 5
			#		self.info_y += self.info_speed

			#	elif 27 < self.info_y < 30:
			#		self.info_y -= self.info_speed // 3
			#		self.info_forward = False
			
			#if self.alignment:
			#	self.surface.blit(bigTextInfo.render(self.info, True, (139, 105, 180)), (self.x - bigTextInfo.size(self.info)[0] // 2, self.y - self.h / 2 - self.info_y))
			#else:
			#	self.surface.blit(bigTextInfo.render(self.info, True, (139, 105, 180)), (self.x - self.w // 2 - bigTextInfo.size(self.info)[0] // 2, self.y - self.info_y))

		else:

			self.image = self.image1
			self.hold = 0
			if self.info_y > 0: self.info_back = True

		if hovered and click[0]:
			self.is_pressed = True
		else:
			if not click[0]:
				if self.is_pressed and hovered:
					if current_time - self.last_trigger_time > self.cooldown * 1000:
						if self.sound:
							play_sound("Button click")
						self.last_trigger_time = current_time
						self.is_activated = True

						if self.action is not None:
							self.action()
						if action is not None:
							action()
		
		if not click[0]:
			self.is_pressed = False
		
		if self.alignment:
			self.surface.blit(self.image, (self.x - self.w / 2, self.y - self.h / 2))
		else:
			self.surface.blit(self.image, (self.x, self.y))

	def get_pressed(self) -> bool:

		"Проверяет, нажата ли кнопка. Устаревший метод, оставлен для совместимости"

		mouse_x, mouse_y = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		if self.alignment and (self.x - self.w / 2 < mouse_x < self.x + self.w / 2 and self.y - self.h / 2 < mouse_y < self.y + self.h / 2) or not self.alignment and (self.x < mouse_x < self.x + self.w and self.y < mouse_y < self.y + self.h):
			self.image = self.image2
			if click[0]:
				return True
		else:
			self.image = self.image1
			return False

class BackroomsPortal:

	def __init__(self, X: int, Y: int):

		self.image = 0
		self.rect = Backrooms_portal_images[0].get_rect()
		self.x = X
		self.y = Y

	def main(self):

		win.blit(Backrooms_portal_images[self.image], (self.x - player.x + Width // 2 - 128, player.y - self.y + Height // 2 - 128))

		self.image += 1
		if self.image == 10:
			self.image = 0

		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), (self.x - player.x + Width // 2 - 128, player.y - self.y + Height // 2 - 128, 256, 256), 3)

class Wire:

	def __init__(self, in_motherboard):

		self.in_motherboard = in_motherboard
		if self.in_motherboard is None:
			self.x = (player.x + mouse_x - Width // 2) // 64
			self.y = (player.y - mouse_y + Height // 2) // 64
		else:
			self.x = (mouse_x - Width // 2 - 300) // 18.75
			self.y = (mouse_y + Width // 2 - 300) // 18.75
		self.condition = "Off"
		self.image = wire_images[0]
		self.neigbords = []
		self.neigbords_on = 0
		self.neigbords_none = 0
		self.num = len(world.mechanisms)
	
	def main(self):

		self.neigbords = []
		self.neigbords_on = 0
		self.neigbords_none = 0

		if self.in_motherboard is None:
			for mechanism in world.mechanisms:
				if mechanism.__class__ in (Wire, Lever, Motherboard):
					if ((mechanism.x == self.x and mechanism.y in (self.y + 1, self.y - 1)) or (mechanism.x in (self.x - 1, self.x + 1) and mechanism.y == self.y)) and mechanism.num != self.num:

						self.neigbords.append(mechanism)
						if mechanism.__class__ == Motherboard:

							if mechanism.left_condition == "On" and mechanism.x >= self.x:
								self.neigbords_on += 1
							if mechanism.left_condition is None and mechanism.x >= self.x:
								self.neigbords_none += 1
						else:

							if mechanism.condition == "On":
								self.neigbords_on += 1
							elif mechanism.condition is None:
								self.neigbords_none += 1

				elif mechanism.__class__ == Random_box:

					if mechanism.x - self.x in (1, -1) and mechanism.y == self.y and mechanism.num != self.num:

						self.neigbords.append(mechanism)

						if mechanism.condition == "On":
							self.neigbords_on += 1
						elif mechanism.condition is None:
							self.condition = None

		else:

			for mechanism in in_motherboard.objects:

				if mechanism.__class__ in (Wire, Lever, Motherboard):
					if ((mechanism.x == self.x and mechanism.y in (self.y + 1, self.y - 1)) or (mechanism.x in (self.x - 1, self.x + 1) and mechanism.y == self.y)) and mechanism.num != self.num:
						self.neigbords.append(mechanism)
						if mechanism.condition == "On":
							self.neigbords_on += 1
						elif mechanism.condition is None:
							self.neigbords_none += 1

				elif mechanism.__class__ == Random_box:

					if mechanism.x - self.x in (1, -1) and mechanism.y == self.y and mechanism.num != self.num:
						self.neigbords.append(mechanism)
						if mechanism.condition == "On":
							self.neigbords_on += 1
						elif mechanism.condition is None:
							self.condition = None

		if len(self.neigbords) == 1:

			if self.neigbords[0].x == self.x:
				self.image = wire_images[1]
			else:
				self.image = wire_images[0]

		elif len(self.neigbords) == 2:

			if self.neigbords[0].x == self.x == self.neigbords[1].x:
				self.image = wire_images[1]
			elif self.neigbords[0].y == self.y == self.neigbords[1].y:
				self.image = wire_images[0]
			elif (self.neigbords[0].x == self.x - 1 and self.neigbords[1].y == self.y + 1) or (self.neigbords[1].x == self.x - 1 and self.neigbords[0].y == self.y + 1):
				self.image = wire_images[2]
			elif (self.neigbords[0].x == self.x + 1 and self.neigbords[1].y == self.y + 1) or (self.neigbords[1].x == self.x + 1 and self.neigbords[0].y == self.y + 1):
				self.image = wire_images[3]
			elif (self.neigbords[0].x == self.x + 1 and self.neigbords[1].y == self.y - 1) or (self.neigbords[1].x == self.x + 1 and self.neigbords[0].y == self.y - 1):
				self.image = wire_images[4]
			elif (self.neigbords[0].x == self.x - 1 and self.neigbords[1].y == self.y - 1) or (self.neigbords[1].x == self.x - 1 and self.neigbords[0].y == self.y - 1):
				self.image = wire_images[5]

		elif len(self.neigbords) == 3:

			if self.neigbords[0].y != self.y + 1 and self.neigbords[1].y != self.y + 1 and self.neigbords[2].y != self.y + 1:
				self.image = wire_images[6]
			if self.neigbords[0].y != self.y - 1 and self.neigbords[1].y != self.y - 1 and self.neigbords[2].y != self.y - 1:
				self.image = wire_images[7]
			if self.neigbords[0].x != self.x + 1 and self.neigbords[1].x != self.x + 1 and self.neigbords[2].x != self.x + 1:
				self.image = wire_images[8]
			if self.neigbords[0].x != self.x - 1 and self.neigbords[1].x != self.x - 1 and self.neigbords[2].x != self.x - 1:
				self.image = wire_images[9]

		if len(self.neigbords) == 4:
			self.image = wire_images[10]

		if self.neigbords_on != 0 and self.condition == "Off":
			self.condition = "On"
		if self.condition is None:
			self.condition = "Off"
		elif self.neigbords_none != 0:
			self.condition = None
		
		if self.in_motherboard is None:

			win.blit(textInfo.render(self.condition, True, (0, 0, 0)), (self.x * 64 + Width // 2 - player.x, player.y - self.y * 64 + Height // 2 - 16))
			win.blit(self.image, (self.x * 64 + Width // 2 - player.x, player.y - self.y * 64 + Height // 2 - 16))

class Lever:

	def __init__(self, in_motherboard):

		self.in_motherboard = in_motherboard
		self.x = (player.x + mouse_x - Width // 2) // 64
		self.y = (player.y - mouse_y + Height // 2) // 64
		self.condition = False
		self.image1 = pygame.transform.scale(pygame.image.load(path + "Images/Objects/Lever 1.png"), (64, 64))
		self.image2 = pygame.transform.scale(pygame.image.load(path + "Images/Objects/Lever 2.png"), (64, 64))
		self.image = self.image1
		self.neigbords = []
		self.num = len(world.mechanisms)

	def main(self):

		global click, mouse_x, mouse_y

		click = pygame.mouse.get_pressed()
		mouse_x, mouse_y = pygame.mouse.get_pos()
		self.neigbords = []

		for mechanism in world.mechanisms:

			if mechanism.__class__ == Wire:
				if ((mechanism.x == self.x and mechanism.y in (self.y + 1, self.y - 1)) or (mechanism.x in (self.x - 1, self.x + 1) and mechanism.y == self.y)) and mechanism.num != self.num:
					self.neigbords.append(mechanism)

			elif mechanism.__class__ == Random_box:
				if mechanism.x - self.x in (1, -1) and mechanism.y == self.y and mechanism.num != self.num:
					self.neigbords.append(mechanism)

		if click[0] and self.x * 64 + Width // 2 - player.x <= mouse_x <= self.x * 64 + Width // 2 - player.x + 64 and player.y - self.y * 64 + Height // 2 - 16 <= mouse_y <= player.y - self.y * 64 + Height // 2 - 16 + 64:

			if self.image == self.image1:
				self.image = self.image2
				self.condition = "On"
			else:
				self.image = self.image1
				self.condition = None

		win.blit(self.image, (self.x * 64 + Width // 2 - player.x, player.y - self.y * 64 + Height // 2 - 16))

class Wall:

	def __init__(self, wall_type: str, X, Y, is_door: bool=False):

		self.x = X
		self.y = Y

		self.wall_type = wall_type
		self.neigbords = []
		self.is_door = is_door
		self.open = False
		self.rect = pygame.Rect(self.x - 24, self.y - 128, 48, 256)
		self.images = wall_images[self.wall_type]

		self.image = self.images[0]
		self.update_neigboors()

	def update_neigboors(self):

		self.neigbords = []
		for wall in ((self.x - 256, self.y), (self.x + 256, self.y), (self.x, self.y - 256), (self.x, self.y + 256)):
			chunk = world.chunk_manager.get_chunk_at(*wall)
			if chunk is not None and wall in chunk.walls:
				self.neigbords.append(wall)

		if self.is_door:

			if len(self.neigbords) == 0:
				if self.open:
					self.image = self.images[2]
				else:
					self.image = self.images[0]

			if len(self.neigbords) == 1:

				if self.neigbords[0][0] == self.x:
					if self.open:
						self.image = self.images[3]
					else:
						self.image = self.images[1]
				else:
					if self.open:
						self.image = self.images[2]
					else:
						self.image = self.images[0]

			elif len(self.neigbords) == 2:

				if self.neigbords[0][0] == self.x == self.neigbords[1][0]:
					if self.open:
						self.image = self.images[3]
					else:
						self.image = self.images[1]
				elif self.neigbords[0][1] == self.y == self.neigbords[1][1]:
					if self.open:
						self.image = self.images[2]
					else:
						self.image = self.images[0]

		else:

			if len(self.neigbords) == 1:

				if self.neigbords[0][0] < self.x:
					self.image = self.images[3]
					self.rect = pygame.Rect(self.x - 128, self.y - 128, 152, 256)
				elif self.neigbords[0][0] > self.x:
					self.image = self.images[4]
					self.rect = pygame.Rect(self.x - 24, self.y - 128, 152, 256)
				else:
					self.image = self.images[2]
					self.rect = pygame.Rect(self.x - 24, self.y - 128, 48, 256)

			elif len(self.neigbords) == 2:

				if self.neigbords[0][0] == self.x == self.neigbords[1][0]:
					self.image = self.images[2]
					self.rect = pygame.Rect(self.x - 24, self.y - 128, 48, 256)
				elif self.neigbords[0][1] == self.y == self.neigbords[1][1]:
					self.image = self.images[1]
					self.rect = pygame.Rect(self.x - 128, self.y - 128, 256, 256)
				elif (self.neigbords[0][0] == self.x - 256 and self.neigbords[1][1] == self.y + 256) or (self.neigbords[1][0] == self.x - 256 and self.neigbords[0][1] == self.y + 256):
					self.image = self.images[5]
					self.rect = pygame.Rect(self.x - 128, self.y - 128, 152, 256)
				elif (self.neigbords[0][0] == self.x + 256 and self.neigbords[1][1] == self.y + 256) or (self.neigbords[1][0] == self.x + 256 and self.neigbords[0][1] == self.y + 256):
					self.image = self.images[6]
					self.rect = pygame.Rect(self.x - 24, self.y - 128, 152, 256)
				elif (self.neigbords[0][0] == self.x + 256 and self.neigbords[1][1] == self.y - 256) or (self.neigbords[1][0] == self.x + 256 and self.neigbords[0][1] == self.y - 256):
					self.image = self.images[7]
					self.rect = pygame.Rect(self.x - 24, self.y - 128, 152, 256)
				elif (self.neigbords[0][0] == self.x - 256 and self.neigbords[1][1] == self.y - 256) or (self.neigbords[1][0] == self.x - 256 and self.neigbords[0][1] == self.y - 256):
					self.image = self.images[8]
					self.rect = pygame.Rect(self.x - 128, self.y - 128, 152, 256)

			elif len(self.neigbords) == 3:

				if self.neigbords[0][1] != self.y + 256 and self.neigbords[1][1] != self.y + 256 and self.neigbords[2][1] != self.y + 256:
					self.image = self.images[9]
					self.rect = pygame.Rect(self.x - 128, self.y - 128, 256, 256)
				if self.neigbords[0][1] != self.y - 256 and self.neigbords[1][1] != self.y - 256 and self.neigbords[2][1] != self.y - 256:
					self.image = self.images[10]
					self.rect = pygame.Rect(self.x - 128, self.y - 128, 256, 256)
				if self.neigbords[0][0] != self.x + 256 and self.neigbords[1][0] != self.x + 256 and self.neigbords[2][0] != self.x + 256:
					self.image = self.images[11]
					self.rect = pygame.Rect(self.x - 128, self.y - 128, 152, 256)
				if self.neigbords[0][0] != self.x - 256 and self.neigbords[1][0] != self.x - 256 and self.neigbords[2][0] != self.x - 256:
					self.image = self.images[12]
					self.rect = pygame.Rect(self.x - 24, self.y - 128, 152, 256)

			elif len(self.neigbords) == 4:
				self.image = self.images[12]
				self.rect = pygame.Rect(self.x - 128, self.y - 128, 256, 256)
		
	def main(self, release):
		screen_x, screen_y = world_to_screen(self.x, self.y, 256, 256)
		if self.is_door and release and screen_x <= mouse_x <= screen_x + 256 and screen_y <= mouse_y <= screen_y + 256:
			self.open = not self.open
			self.update_neigboors()
			if multiplayer:
				game_events.append({"event_type": "wall_interaction", "wall_pos": (self.x, self.y)})
		win.blit(self.image, world_to_screen(self.x, self.y, 256, 256))
		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), world_rect_to_screen(self.rect[0] + self.rect[2] // 2, self.rect[1] + self.rect[3] // 2, self.rect[2], self.rect[3]), 3)
		
	def __getstate__(self):
		
		state = self.__dict__.copy()
		state["image"] = self.images.index(self.image)
		del state["images"]
		rect = state["rect"]
		state["rect"] = (rect[0], rect[1], rect[2], rect[3])
		return state

	def __setstate__(self, state):
		
		self.__dict__.update(state)
		self.images = wall_images[self.wall_type]
		self.image = self.images[self.image]

		self.rect = pygame.Rect(state["rect"][0], state["rect"][1], state["rect"][2], state["rect"][3])

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
		
	def main(self, release, dt):

		world_rect = world_rect_to_screen(self.x - 64, self.y + 64, 128, 128)
		if release and pygame.Rect(world_rect).collidepoint((mouse_x, mouse_y)):
			self.handle_click()
		win.blit(self.image, world_to_screen(self.x, self.y, 256, 256))
		if self.plant is not None:
			win.blit(plant_images[self.plant][self.plant_growth_stage], world_to_screen(self.x, self.y, 256, 256))
			if self.plant_growth_stage != 3:
				self.grow_timer -= dt
			if self.grow_timer <= 0:
				self.plant_growth_stage += 1
				self.grow_timer = random.randint(250, 350)
				if self.plant_growth_stage == 2 and not self.watered:
					self.plant_growth_stage = 3
		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), world_rect, 3)
		
	def handle_click(self):

		slot = inventory.whole_inventory[changed_slot]
		if self.plant is None:
			if slot is not None and slot.name in seed_types:
				self.plant = seed_types[slot.name]
				inventory.reduce(changed_slot)
				self.grow_timer = random.randint(250, 350)
		elif self.plant_growth_stage == 1:
			if slot is not None and slot.name == "Water bucket":
				inventory.reduce(changed_slot)
				inventory.increate("Water bucket")
				self.watered = True
				play_sound("Watering plants ", 2)
		elif self.plant_growth_stage == 2:
			destroy_object(plant_images[self.plant][self.plant_growth_stage], self.x - 64, self.y + 64, world, Particle)
			for _ in range(random.randint(1, 3)):
				rand_x, rand_y = self.x - 64 + random.randint(-64, 64), self.y + 64 + random.randint(-64, 64)
				world.chunk_manager.get_chunk_at(rand_x, rand_y).items.append(Object(self.plant, rand_x, rand_y, f"Images/Items/{self.plant}.png", pickable=True))
			self.plant = None
			self.plant_growth_stage = 0
			self.watered = False
		elif self.plant_growth_stage == 3:
			destroy_object(plant_images[self.plant][self.plant_growth_stage], self.x - 64, self.y + 64, world, Particle)
			self.plant = None
			self.plant_growth_stage = 0

		if slot is not None and slot.name == "Stone shovel":
			play_sound("Dirt")
			del world.chunk_manager.get_chunk_at(self.x, self.y).farmlands[(self.x, self.y)]
	
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

class Random_box:

	def __init__(self, in_motherboard):
		
		self.x = (player.x + mouse_x - Width // 2) // 64
		self.y = (player.y - mouse_y + Height // 2) // 64

		self.on = False
		self.image = random_box_images[0]
		self.neigbords = []
		self.neigbords_on = 0
		self.num = len(world.mechanisms)
		self.in_motherboard = in_motherboard
	
	def main(self):

		self.neigbords = []
		self.neigbords_on = 0

		for mechanism in world.mechanisms:

			if mechanism.y == self.y and mechanism.x - self.x in (1, -1) and mechanism.num != self.num:

				self.neigbords.append(mechanism)
				if mechanism.on:
					self.neigbords_on += 1
		
		if len(self.neigbords) == 1:

			if self.neigbords[0].x == self.x - 1:
				self.image = random_box_images[1]
			else:
				self.image = random_box_images[2]

		elif len(self.neigbords) == 2:
			self.image = random_box_images[3]

		else:
			self.image = random_box_images[0]
		
		win.blit(self.image, (self.x * 64 + Width // 2 - player.x, player.y - self.y * 64 + Height // 2 - 16))

class LogicGate:

	def __init__(self, in_motherboard):

		self.x = (player.x + mouse_x - Width // 2) // 64
		self.y = (player.y - mouse_y + Height // 2) // 64

		self.image = wire_images[10]
		self.neigbords = []
		self.neigbords_on = 0
		self.num = len(world.mechanisms)
		self.in_motherboard = in_motherboard
	
	def main(self):

		self.neigbords = []
		self.neigbords_on = 0

		for mechanism in world.mechanisms:

			if mechanism.__class__ in (Wire, Lever):

				if ((mechanism.x == self.x and mechanism.y in (self.y + 1, self.y - 1)) or (mechanism.x in (self.x - 1, self.x + 1) and mechanism.y == self.y)) and mechanism.num != self.num:
					self.neigbords.append(mechanism)
					if mechanism.condition == "On":
						self.neigbords_on += 1

			elif mechanism.__class__ == Random_box:

				if mechanism.x - self.x in (1, -1) and mechanism.y == self.y and mechanism.num != self.num:
					self.neigbords.append(mechanism)
					if mechanism.condition == "On":
						self.neigbords_on += 1

		if len(self.neigbords) == 1:

			if self.neigbords[0].x == self.x:
				self.image = wire_images[1]
			else:
				self.image = wire_images[0]

		elif len(self.neigbords) == 2:
			if self.neigbords[0].x == self.x == self.neigbords[1].x:
				self.image = wire_images[1]
			elif self.neigbords[0].y == self.y == self.neigbords[1].y:
				self.image = wire_images[0]
			elif (self.neigbords[0].x == self.x - 1 and self.neigbords[1].y == self.y + 1) or (self.neigbords[1].x == self.x - 1 and self.neigbords[0].y == self.y + 1):
				self.image = wire_images[2]
			elif (self.neigbords[0].x == self.x + 1 and self.neigbords[1].y == self.y + 1) or (self.neigbords[1].x == self.x + 1 and self.neigbords[0].y == self.y + 1):
				self.image = wire_images[3]
			elif (self.neigbords[0].x == self.x + 1 and self.neigbords[1].y == self.y - 1) or (self.neigbords[1].x == self.x + 1 and self.neigbords[0].y == self.y - 1):
				self.image = wire_images[4]
			elif (self.neigbords[0].x == self.x - 1 and self.neigbords[1].y == self.y - 1) or (self.neigbords[1].x == self.x - 1 and self.neigbords[0].y == self.y - 1):
				self.image = wire_images[5]

		elif len(self.neigbords) == 3:
			if self.neigbords[0].y != self.y + 1 and self.neigbords[1].y != self.y + 1 and self.neigbords[2].y != self.y + 1:
				self.image = wire_images[6]
			if self.neigbords[0].y != self.y - 1 and self.neigbords[1].y != self.y - 1 and self.neigbords[2].y != self.y - 1:
				self.image = wire_images[7]
			if self.neigbords[0].x != self.x + 1 and self.neigbords[1].x != self.x + 1 and self.neigbords[2].x != self.x + 1:
				self.image = wire_images[8]
			if self.neigbords[0].x != self.x - 1 and self.neigbords[1].x != self.x - 1 and self.neigbords[2].x != self.x - 1:
				self.image = wire_images[9]

		if len(self.neigbords) == 4:
			self.image = wire_images[10]

		if self.neigbords_on != 0 and self.condition == "Off":
			self.condition = "On"
		if self.condition is None:
			self.condition = "Off"
		elif self.neigbords_none != 0:
			self.condition = None
		
		if not self.in_motherboard:
			win.blit(self.image, (self.x * 64 + Width // 2 - player.x, player.y - self.y * 64 + Height // 2 - 16))

class Motherboard:

	def __init__(self, in_motherboard):

		self.x = (player.x + mouse_x - Width // 2) // 64
		self.y = (player.y - mouse_y + Height // 2) // 64

		self.condition = "Off"
		self.image = pygame.transform.scale(pygame.image.load(path + "Images/Objects/Motherboard.png"), (64, 64))
		self.neigbords = []
		self.neigbords_on = 0
		self.neigbords_none = 0
		self.num = len(world.mechanisms)
		self.in_motherboard = in_motherboard
		self.objects = [None] * 1024
		self.objects_left = []
		self.objects_left_xy = []
		self.left_condition = "Off"
		self.objects_right = []
		self.objects_right_xy = []
		self.right_condition = "Off"
		self.objects_up = []
		self.objects_up_xy = []
		self.up_condition = "Off"
		self.objects_down = []
		self.objects_down_xy = []
		self.down_condition = "Off"
	
	def main(self):

		self.neigbords = []
		self.neigbords_on = 0
		self.neigbords_none = 0

		self.objects_left = []
		self.objects_left_xy = []
		self.objects_right = []
		self.objects_right_xy = []
		self.objects_up = []
		self.objects_up_xy = []
		self.objects_down = []
		self.objects_down_xy = []

		for mechanism in world.mechanisms:

			if mechanism.__class__ in (Wire, Lever, Motherboard):

				if ((mechanism.x == self.x and mechanism.y in (self.y + 1, self.y - 1)) or (mechanism.x in (self.x - 1, self.x + 1) and mechanism.y == self.y)) and mechanism.num != self.num:
					self.neigbords.append(mechanism)
					if mechanism.condition == "On" and mechanism.x <= self.x and self.left_condition == "Off":
						self.left_condition = "On"
					elif mechanism.condition is None and mechanism.x <= self.x:
						self.left_condition = None

			elif mechanism.__class__ == Random_box:

				if mechanism.x - self.x in (1, -1) and mechanism.y == self.y and mechanism.num != self.num:
					self.neigbords.append(mechanism)
					if mechanism.condition == "On":
						self.neigbords_on += 1
					elif mechanism.condition is None:
						self.condition = None

		for i in self.objects:

			if i is not None:

				if i.x + 32 == 0:

					self.objects_left.append(i.condition)
					self.objects_left_xy.append(i)
				
				elif i.x == -1:
					self.objects_right.append(i.condition)
					self.objects_right_xy.append(i)

				if i.y == 21:

					self.objects_up.append(i.condition)
					self.objects_up_xy.append(i)

				elif i.y == 52:

					self.objects_down.append(i.condition)
					self.objects_down_xy.append(i)
					
		if (any(self.objects_left) and self.left_condition == "Off") or self.left_condition == "On":

			self.left_condition = "On"

			for i in self.objects_left_xy:
				if self.objects[self.objects.index(i)].condition == "Off":
					self.objects[self.objects.index(i)].condition = "On"

		if self.left_condition is None:
			self.left_condition = "Off"

		elif None in self.objects_left:
			self.left_condition = None
			for i in self.objects_left_xy:
				self.objects[self.objects.index(i)].condition = None
		
		self.get_pressed()

		if not self.in_motherboard:
			win.blit(self.image, (self.x * 64 + Width // 2 - player.x, player.y - self.y * 64 + Height // 2 - 16))

	def get_pressed(self):
		global in_motherboard, mouse_x, mouse_y, click
		mouse_x, mouse_y = pygame.mouse.get_pos()
		if self.in_motherboard is None:
			if self.x * 64 + Width // 2 - player.x <= mouse_x <= self.x * 64 + Width // 2 - player.x + 64 and player.y - self.y * 64 + Height // 2 - 16 <= mouse_y <= player.y - self.y * 64 + Height // 2 - 16 + 64 and in_motherboard is None and click[0]:
				in_motherboard = self

class GameState:

	def __init__(self):

		self.difficulty = "norm"
		self.weather = "Clear"
		self.shadow_surface = pygame.Surface((Width, Height), pygame.SRCALPHA)
		self.shadow_surface.fill((0, 0, 0, 90))

game = GameState()

class Cave:

	def __init__(self, cave_x, cave_y, w, h):

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

	def generate(self):

		# for _ in range(self.own_width // 100 + random.randint(-10, 10)):
		#	self.objects.append(Object("Stone", random.randint(self.own_width // 2 * -1, self.own_width // 2), random.randint(self.own_height // 2 * -1, self.own_height // 2), "Images/Items/Stone.png"))
			
		# for _ in range(self.own_width // 300 + random.randint(-10, 10)):
		#	self.objects.append(Object("Iron ore", random.randint(self.own_width // 2 * -1, self.own_width // 2), random.randint(self.own_height // 2 * -1, self.own_height // 2), "Images/Objects/Iron ore.png", (256, 256), special_flags=100, is_solid=True))

		# for _ in range(self.own_width // 300 + random.randint(-10, 10)):
		#	self.objects.append(Object("Gold ore", random.randint(self.own_width // 2 * -1, self.own_width // 2), random.randint(self.own_height // 2 * -1, self.own_height // 2), "Images/Objects/Gold ore.png", (256, 256), special_flags=100, is_solid=True))
		self.cave_map = world.chunk_manager.generator.generate_cave(self.noise, self.own_width, self.own_height)

	def main(self):

		if player.x - Width // 2 <= self.x <= player.x + Width // 2 and player.y - Height // 2 <= self.y + Height // 2:
			win.blit(self.image, (self.x - player.x + Width // 2 - self.w // 2, player.y - self.y + Height // 2 - self.h // 2))
		
	def get_in(self):

		global mouse_x, mouse_y
		mouse_x, mouse_y = pygame.mouse.get_pos()
		if self.x <= player.x <= self.x + 128 and self.y <= player.y <= self.y + 128 and self.x - player.x + Width // 2 - self.w // 2 <= mouse_x <= self.x - player.x + Width // 2 - self.w // 2 + 128 and player.y - self.y + Height // 2 - self.h // 2 <= mouse_y <= player.y - self.y + Height // 2 - self.h // 2 + 128 and pygame.mouse.get_pressed()[0]:
			return self
		else:
			return None

	def render(self):
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

class Portal:

	def __init__(self):

		self.x = (player.x + mouse_x - Width // 2) // 128
		self.y = (player.y + mouse_y - Height // 2) // 256
		a = False
		for object in world.visible_objects:
			if object.__class__ == Portal and (self.x, self.y) != (object.x, object.y):
				a = True
		if a:
			self.image = Portal_2
		else:
			self.image = Portal_1

	def main(self):

		global player

		for object in world.visible_objects:
			if object.__class__ == Portal and (self.x, self.y) != (object.x, object.y):
				if self.x * 128 <= player.x <= self.x * 128 + 128 and self.y * 256 - 256 <= player.y <= self.y * 256:
					player.x = object.x * 128
					player.y = object.y * 256 - 257
		
		win.blit(self.image, (self.x * 128 + Width // 2 - player.x, player.y - self.y * 256 + Height // 2))

ui_system = UISystem()

def create_throw_particle(item_image, item_name):
	
	# Векторы направления
	dir_map = {
		"Down": (0, -1), "Up": (0, 1),
		"Left": (-1, 0), "Right": (1, 0),
		"Up-right": (1, 1), "Up-left": (-1, 1),
		"Down-right": (1, -1), "Down-left": (-1, -1)
	}
	
	dx, dy = dir_map.get(player.direction, (0, 1))
	norm = math.sqrt(dx*dx + dy*dy)
	if norm > 0:
		dx, dy = dx/norm, dy/norm
	
	# Скорость
	vx = dx * 2000
	vy = dy * 2000
	
	# Состояние для физики
	physics_state = {"vx": vx, "vy": vy, "start_x": player.x, "start_y": player.y}
	
	def tick_command(p):
		dt = p.dt
		p.x += physics_state["vx"] * dt
		p.y += physics_state["vy"] * dt
		physics_state["vx"] *= 0.0001 ** dt
		physics_state["vy"] *= 0.0001 ** dt
	
	def del_condition(p):
		# return abs(p.x - physics_state["start_x"]) > 200 or abs(p.y - physics_state["start_y"]) > 200
		return abs(physics_state["vx"]) < 64 and abs(physics_state["vy"]) < 64
	
	def end_command(p):
		chunk = world.chunk_manager.get_chunk_at(p.x, p.y)
		obj = Object(p.special_flags, p.x, p.y, f"Images/Items/{p.special_flags}.png", pickable=True)
		chunk.items.append(obj)
		if multiplayer:
			game_events.append({
				"event_type": "item_added",
				"item": obj.__getstate__()
			})
	
	return Particle(
		player.x, player.y,
		item_image,
		x_bias=0, y_bias=0,
		end_time=None,
		end_command=end_command,
		special_flags=item_name,
		tick_command=tick_command,
		del_self_condition=del_condition
	)

# Загрузка команд

def tp(x, y, player=player):
	"""Телепортация игрока на указанные координаты"""
	player.x = x
	player.y = y
	if multiplayer:
		game_events.append({"event_type": "player_tp", "x": player.x, "y": player.y, "direction": player.direction})
		net.peers[net.player_id].x = player.x
		net.peers[net.player_id].y = player.y
		net.peers[net.player_id].direction = player.direction

def chat_message(message: str, send_to_peers: bool = False):
	"""Отправляет сообщение в чат"""
	global chat_tick
	chat.append(message)
	main_chat.append(message)
	chat_tick = len(message) // 1.5 * FPS
	if multiplayer and send_to_peers:
		game_events.append({"event_type": "chat_message", "message_text": message})

def command_help(command: str=""):
	if command == "":
		chat_message("Команды можно использовать, если у вас включён режим бога или вы взломали код вселенной. Для ознакомления со списком команд введите /command_list")
	elif command in command_system.commands:
		chat_message(command_system.commands[command][1])
	else:
		chat_message("Нет такой команды: " + command)

def command_list():
	for command in command_system.commands.keys():
		chat_message(command)

def kukusiki_hack():
	hack_list = ("рожи дыбильные", "лысый кал", "хитрожопые скоты", "спина и дождь", "маслодонное кино", "помидорный чай", "пьяный хлеб", "флюрография гуся")
	chat_message("Смори, Ришный Мцэць взломал код вселенной и скинул нам этот шифрованный список:")
	for i in hack_list:
		chat_message(i)

command_system.commands = {

		"help": (command_help, "Выдаёт справку\n/help КОМАНДА"),
		"command_list": (command_list, "Выдаёт список команд\n/command_list"),
		"kukusiki_hack": (kukusiki_hack, "Раскрывает код вселенной\n/kukusiki_hack"),
		"tp": (tp, "Телепортация игрока на указанные координаты\n tp X Y"),
		"give": (inventory.increate, "Выдача предмета в инвентарь\n give ПРЕДМЕТ КОЛИЧЕСТВО=1"),
		"get_brightness": (time_system.get_brightness, "Получение текущей яркости днейвного цикла\n/get_brightness"),
		"get_time_of_day": (time_system.get_time_of_day, "Получение текущего времени в 24-часовом формате\n/get_time_of_day"),
		"set_time_speed": (time_system.set_time_speed, "Изменить скорость времени\n/time_scale МНОЖИТЕЛЬ"),
		"reset_to_day": (time_system.reset_to_day, "Обнулить время до дня\n/reset_to_day"),
		"skip_time": (time_system.skip_time, "Перемотать время вперёд\n/skip_time СЕКУНДЫ"),
		"chat_message": (chat_message, "Вывести сообщение в чат\n/chat_message ТЕКСТ")

		}

# def show_bar(times):
#	import matplotlib.pyplot as plt
#	categories = range(len(times))
#	values = []
#	for i in times:
#		values.append(sum(i) / len(i))

#	plt.bar(categories, values, color="orange")
#	plt.title("Время на обработку")
#	plt.xlabel('Часть кода')
#	plt.ylabel('Время')
#	plt.show()
#	plt.savefig("aboba.png")

# time_values = []
# time_index = 0

# def add_time(t):
#	global time_index
#	if len(time_values) <= time_index:
#		time_values.append([])
#	time_values[time_index].append(t)
#	time_index += 1
# def reset_time():
#	global time_index
#	time_index = 0

# Кнопки в меню

def settings():

	global does_lighten

	does_lighten = False
	def page_back():
		global page
		page = max(1, page - 1)
	def next_page():
		global page
		page += 1 
	back_button = Button(-20, -20, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back.png"), (128, 128)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back 2.png"), (128, 128)))

	help_button = Button(10, 117, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Help.png"), (132, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Help 2.png"), (132, 64)))
	display_button = Button(10, 192, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Display.png"), (222, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Display 2.png"), (222, 64)))
	languages_button = Button(10, 267, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Languages.png"), (272, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Languages 2.png"), (272, 64)))
	user_button = Button(10, 342, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/User.png"), (132, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/User 2.png"), (132, 64)))
	sound_button = Button(10, 417, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Sound.png"), (160, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Sound 2.png"), (160, 64)))
	statistics_button = Button(10, 492, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Statistics.png"), (300, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Statistics 2.png"), (300, 64)))
	keys_button = Button(10, 567, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Keys.png"), (132, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Keys 2.png"), (132, 64)))
	game_button = Button(10, 642, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Game.png"), (132, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Game 2.png"), (132, 64)))
	
	english_button = Button(385, 198, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/English.png"), (220, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/English 2.png"), (220, 64)))
	russian_button = Button(385, 267, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Russian.png"), (220, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Russian 2.png"), (220, 64)))
	kazach_button = Button(385, 336, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Kazach.png"), (188, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Kazach 2.png"), (188, 64)))

	page_back_button = Button(361, Height - 138, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back.png"), (128, 128)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back 2.png"), (128, 128)), action=page_back)
	page_next_button = Button(Width - 138, Height - 138, pygame.transform.flip(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back.png"), (128, 128)), True, False), pygame.transform.flip(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back 2.png"), (128, 128)), True, False), action=next_page)

	bigTextInfo = pygame.font.Font(path + "Font.ttf", 36)
	
	def show_reset_settings():
		
		global Settings

		if Width - 30 - bigTextInfo.size(t("Reset settings"))[0] < mouse_x < Width - 30 and 30 < mouse_y < 60:
			win.blit(bigTextInfo.render(t("Reset settings"), True, menu_color_dark), (Width - 30 - bigTextInfo.size(t("Reset settings"))[0], 30))
			if pygame.mouse.get_pressed()[0]:
					
				Settings = default_settings
		else:
			win.blit(bigTextInfo.render(t("Reset settings"), True, menu_color_medium), (Width - 30 - bigTextInfo.size(t("Reset settings"))[0], 30))

	def help():

		global win, screenmode, mouse_x, mouse_y, does_lighten, page, alt_pressed
		
		while True:

			mouse_x, mouse_y = pygame.mouse.get_pos()
			dt = clock.tick(MAX_FPS) / 1000.0

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					save()
					sys.exit()
				if event.type == pygame.KEYUP:
					if event.key == hot_keys["Show keys"]:
						alt_pressed = not alt_pressed

				if event.type == pygame.KEYUP:
					if event.key == hot_keys["Change screen"]:
						if screenmode == "FULLSCREEN":
							win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
							screenmode = "RESIZABLE"
						else:
							win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
							screenmode = "FULLSCREEN"

					if event.key == hot_keys["Close"]:
						Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
						win_darken(win)
						menu()

			win.fill(menu_color_light)
			pygame.draw.rect(win, menu_color_medium, (-8, 100, 373, Height), 8)
			pygame.draw.line(win, menu_color_medium, (307, 103), (Width, 103), 8)
			back_button.main()
			show_reset_settings()
			
			if back_button.get_pressed():
				Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
				win_darken(win)
				menu()
				
			page_back_button.main()
			page_next_button.main()
			page = min(page, 2)

			win.blit(bigTextInfo.render(str(page), True, menu_color_medium), ((Width - 415) // 2 + 391, Height - 96))
			win.blit(load(path + "Images/Buttons/Help 2.png", 132, 64), (10, 117))
			display_button.main(display)
			languages_button.main(Languages)
			user_button.main(User)
			sound_button.main(Sound)
			statistics_button.main(Statistics)
			keys_button.main(Keys)
			game_button.main(Game)

			if page == 1:
				
				win.blit(bigTextInfo.render(t("Start game"), True, menu_color_medium), (385, 123))
				win.blit(textInfo.render(t(" • To move, you can use the arrows or A, S, W and D"), True, menu_color_medium), (385, 209)) # между строками 86 пикселей
				win.blit(arrow_up, (459, 239))
				win.blit(arrow_left, (385, 313))
				win.blit(arrow_down, (459, 313))
				win.blit(arrow_right, (533, 313))
				pygame.draw.rect(win, menu_color_medium, (701, 239, 64, 64), 6)
				pygame.draw.rect(win, menu_color_medium, (627, 313, 64, 64), 6)
				pygame.draw.rect(win, menu_color_medium, (701, 313, 64, 64), 6)
				pygame.draw.rect(win, menu_color_medium, (775, 313, 64, 64), 6)
				win.blit(bigTextInfo.render("W", True, menu_color_medium), (710, 247))
				win.blit(bigTextInfo.render("A", True, menu_color_medium), (640, 321))
				win.blit(bigTextInfo.render("S", True, menu_color_medium), (716, 321))
				win.blit(bigTextInfo.render("D", True, menu_color_medium), (790, 321))
				win.blit(textInfo.render(t("  Also, you can put an item on the ground by pressing E, and to get it, just click"), True, menu_color_medium), (385, 381)) # между строками 30 пикселей
				win.blit(textInfo.render(t("on it!"), True, menu_color_medium), (385, 411))
				win.blit(textInfo.render(languages(" • Если вы хотите узнать свой координаты, или что-нибудь ещё, нажмите F2", " • If you want to know you coordinate, or anything more, press F2", "• Координаттарды немесе басқа кез келген нәрсені білгіңіз келсе, F2 пернесін басыңыз"), True, menu_color_medium), (385, 441))
				win.blit(textInfo.render(languages("для открытия меню.", "to open the menu", "мәзірді ашу үшін"), True, menu_color_medium), (385, 471))
				win.blit(textInfo.render(languages(" • При нажатии на I откроется весь инвентарь, чтобы его закрыть, нажмите", " • Clicking on I will open the entire inventory, to close it, click again.", "• Мен түймешігін бассаңыз, бүкіл тізімді ашамын, оны жабу үшін қайтадан басыңыз"), True, menu_color_medium), (385, 501))
				win.blit(textInfo.render(languages("ещё раз", None, None), True, menu_color_medium), (385, 531))
				win.blit(textInfo.render(languages(" • В верхнем правом углу есть пункт, в котором можно узнать информацию", " • In the upper right corner there is an item where you can find out", " • Жоғарғы оң жақ бұрышта ақпаратты табуға болатын элемент бар"), True, menu_color_medium), (385, 561))
				win.blit(textInfo.render(languages("об объекте, на который вы навели.", "information about the object you hovered over", "меңзерді апарған нысан туралы."), True, menu_color_medium), (385, 591))
				
			elif page == 2:
				
				win.blit(bigTextInfo.render(languages("Крафт", "Craft", "Қолөнер"), True, menu_color_medium), (385, 123))
				win.blit(textInfo.render(languages("   Наверняка, тебе было интересно, что это за слоты под инвентарём. Это", "    Forsnre, you were interesting about the cells under the inventory. This is", "Әлбетте, сіз бұл слоттардың түгендеу астында не бар екенін сұрадыңыз. Бұл"), True, menu_color_medium), (385, 209))
				win.blit(textInfo.render(languages("система крафта", "crafting system", "Қолөнер жүйесі"), True, menu_color_medium), (385, 239))
				win.blit(Changed_inventory_slot, (385, 269))
				win.blit(Changed_inventory_slot, (465, 269))
				win.blit(Inventory_slot, (545, 269))
				win.blit(textInfo.render(languages("   На первый взгляд, всё как-то уныло, но на самом деле, крафтить весело!", "  At first glance, everything is somehow dull, but in fact, crafting is fun!", "Бір қарағанда, бәрі қандай да бір түсініксіз, бірақ шын мәнінде қолөнер қызықты!"), True, menu_color_medium), (385, 359))
				win.blit(textInfo.render(languages("Первый слот обозначает объект, который нужен для крафта, например стол.", "The first slot denotes an object that is needed for crafting, such as a table.", "Бірінші ұяшық кесте сияқты өңдеуге қажет нысанды білдіреді"), True, menu_color_medium), (385, 389))
				win.blit(textInfo.render(languages("Второй слот - инструмент, который тебе нужен, например молоток. Дальше", "The second slot is the tool you need, like a hammer. Еhen there are 7 slots", "Екінші ұяшық - балға сияқты сізге қажет құрал. Әрі қарай"), True, menu_color_medium), (385, 419))
				win.blit(textInfo.render(languages("идут 7 слотов для предметов. Если положить предмет в первый, то", "for items. If you put an item in the first one, then the second one is", "7 элемент ұясы бар. Егер объектіні біріншіге қойсақ, онда"), True, menu_color_medium), (385, 449))
				win.blit(textInfo.render(languages("разблокируется второй, потом третий, и так далее.", "unlocked, then the third, and so on.", "екіншісі құлыптан босатылады, содан кейін үшінші және т.б."), True, menu_color_medium), (385, 479))
				win.blit(Changed_inventory_slot, (385, 509))
				win.blit(load(path + "Images/Items/Furnace.png", 64), (385, 509))
				win.blit(Changed_inventory_slot, (465, 509))
				win.blit(Inventory_slot, (545, 509))
				win.blit(load(path + "Images/Items/Clay.png", 64), (545, 509))
				win.blit(Inventory_slot, (625, 509))
				win.blit(Changed_inventory_slot, (1185, 509))
				win.blit(load(path + "Images/Items/Brick.png", 64), (1185, 509))
				win.blit(textInfo.render(languages("   Если положить определённую комбинацию предметов, то можно будет", "	 If you put a certain combination of items, then you can", "Егер сіз элементтердің белгілі бір комбинациясын қойсаңыз, онда сіз жасай аласыз"), True, menu_color_medium), (385, 599))
				win.blit(textInfo.render(languages("получить что-либо. Например, если поставить печь и положить глину в ячейки", "get something. For example, if you put a furnace and put clay in the cells of", "бірдеңе алу. Мысалы, пешті қойып, ұяшықтарға балшық салсаңыз"), True, menu_color_medium), (385, 629))
				win.blit(textInfo.render(languages("крафта, то можно будет получить кирпич, а чтобы его получить, нажми.", "crafting, you can get a brick, and to get it, click.", "қолөнер, сіз кірпіш алуға болады, және оны алу үшін басыңыз."), True, menu_color_medium), (385, 659))
			

			if alt_pressed:
				
				draw_key("ESC", 44, 108)
				draw_key("<-", 425, Height - 168)
				draw_key("->", Width - 74, Height - 168)

			animate_click(dt, mouse_x, mouse_y)

			win_fill(alpha=100 - Settings["Display"][0])   # Если в настройках установлена яркость ниже 100, то экран становится темнее
			
			if not does_lighten:
				win_lighten(win)
				does_lighten = True

			pygame.display.update()

	def display():

		global win, screenmode, Settings, alt_pressed, MAX_FPS

		bias = 0
		max_bias = -ui_system._set_positions(bias, "Display", True)
		max_bias = (max_bias + Height - 103) * max_bias > Height - 103

		while True:
			
			click = pygame.mouse.get_pressed()
			mouse_x, mouse_y = pygame.mouse.get_pos()
			release = False
			events = pygame.event.get()
			dt = clock.tick(MAX_FPS) / 1000.0
			
			for event in events:
				if event.type == pygame.QUIT:
					Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
					save()
					sys.exit()
				
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					release = True
				
				elif event.type == pygame.KEYUP:
					if event.key == hot_keys["Show keys"]:
						alt_pressed = not alt_pressed
					if event.key == hot_keys["Close"]:
						Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
						win_darken(win)
						menu()
					if event.key == hot_keys["Change screen"]:
						if screenmode == "FULLSCREEN":
							win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
							screenmode = "RESIZABLE"
						else:
							win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
							screenmode = "FULLSCREEN"

				elif event.type == pygame.MOUSEWHEEL:
					bias = max((min(bias + event.y * Settings["Game"][2], 0)), max_bias)
					ui_system._set_positions(bias, "Display")
			
			# Очистка экрана
			win.fill(menu_color_light)
			
			# Обработка UI
			ui_system.handle_events(events, mouse_x, mouse_y, release, "Display")
			ui_system.draw("Display", bias, max_bias)
			
			help_button.main(help)
			win.blit(load(path + "Images/Buttons/Display 2.png", 222, 64), (10, 192))
			languages_button.main(Languages)
			user_button.main(User)
			sound_button.main(Sound)
			statistics_button.main(Statistics)
			keys_button.main(Keys)
			game_button.main(Game)
			back_button.main()
			show_reset_settings()
			
			if alt_pressed:
				draw_key("ESC", 44, 108)

			if back_button.get_pressed():
				Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
				win_darken(win)
				menu()
				
			# Анимация и эффекты
			animate_click(dt, mouse_x, mouse_y)
			win_fill(alpha=100 - Settings["Display"][0])
			
			pygame.display.update()

	def Languages():

		global win, screenmode, does_lighten, page, alt_pressed
		
		while True:
			
			mouse_x, mouse_y = pygame.mouse.get_pos()
			dt = clock.tick(MAX_FPS) / 1000.0

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					save()
					sys.exit()
				if event.type == pygame.KEYUP:
					if event.key == hot_keys["Show keys"]:
						alt_pressed = not alt_pressed
					if event.key == hot_keys["Close"]:
						Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
						win_darken(win)
						menu()

					if event.key == pygame.K_1:
						Settings["Languages"][0] = "English"
						translator.load_language("English")
						for element_list in ui_system.elements.values():
							for element in element_list:
								element.label_width = element.font.size(t(element.label))[0] + 10
								element.rect = pygame.Rect(element.x + element.label_width, element.y, element.width, element.height)

					if event.key == pygame.K_2:
						Settings["Languages"][0] = "Russian"
						translator.load_language("Russian")
						for element_list in ui_system.elements.values():
							for element in element_list:
								element.label_width = element.font.size(t(element.label))[0] + 10
								element.rect = pygame.Rect(element.x + element.label_width, element.y, element.width, element.height)

					if event.key == pygame.K_3:
						Settings["Languages"][0] = "Kazach"
						translator.load_language("Karach")
						for element_list in ui_system.elements.values():
							for element in element_list:
								element.label_width = element.font.size(t(element.label))[0] + 10
								element.rect = pygame.Rect(element.x + element.label_width, element.y, element.width, element.height)

					if event.key == hot_keys["Change screen"]:
						if screenmode == "FULLSCREEN":
							win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
							screenmode = "RESIZABLE"
						else:
							win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
							screenmode = "FULLSCREEN"

			win.fill(menu_color_light)
			pygame.draw.rect(win, menu_color_medium, (-8, 100, 373, Height), 8)
			pygame.draw.line(win, menu_color_medium, (307, 103), (Width, 103), 8)
			back_button.main()
			if back_button.get_pressed():
				Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
				win_darken(win)
				menu()
			show_reset_settings()
			
			page_back_button.main()
			page_next_button.main()
			page = min(page, 1)

			win.blit(bigTextInfo.render(t("You can choose one of these"), True, menu_color_medium), (385, 123))
			win.blit(bigTextInfo.render(t("languages:"), True, menu_color_medium), (385, 153))

			english_button.main()
			if english_button.get_pressed():
				Settings["Languages"][0] = "English"
				translator.load_language("English")
				for element_list in ui_system.elements.values():
					for element in element_list:
						element.label_width = element.font.size(t(element.label))[0] + 10
						element.rect = pygame.Rect(element.x + element.label_width, element.y, element.width, element.height)

			russian_button.main()
			if russian_button.get_pressed():
				Settings["Languages"][0] = "Russian"
				translator.load_language("Russian")
				for element_list in ui_system.elements.values():
					for element in element_list:
						element.label_width = element.font.size(t(element.label))[0] + 10
						element.rect = pygame.Rect(element.x + element.label_width, element.y, element.width, element.height)

			kazach_button.main()
			if kazach_button.get_pressed():
				Settings["Languages"][0] = "Kazach"
				translator.load_language("Kazach")
				for element_list in ui_system.elements.values():
					for element in element_list:
						element.label_width = element.font.size(t(element.label))[0] + 10
						element.rect = pygame.Rect(element.x + element.label_width, element.y, element.width, element.height)

			win.blit(bigTextInfo.render(str(page), True, menu_color_medium), ((Width - 415) // 2 + 391, Height - 96))
			help_button.main(help)
			display_button.main(display)
			win.blit(load(path + "Images/Buttons/Languages 2.png", 272, 64), (10, 267))
			user_button.main(User)
			sound_button.main(Sound)
			statistics_button.main(Statistics)
			keys_button.main(Keys)
			game_button.main(Game)
			
			if alt_pressed:
				
				draw_key("ESC", 44, 108)
				draw_key("<-", 425, Height - 168)
				draw_key("->", Width - 74, Height - 168)

			animate_click(dt, mouse_x, mouse_y)
			win_fill(alpha=100 - Settings["Display"][0])   # Если в настройках установлена яркость ниже 100, то экран становится темнее

			if not does_lighten:
				win_lighten(win)
				does_lighten = True

			pygame.display.update()

	def User():

		global win, screenmode, Settings, alt_pressed, MAX_FPS

		bias = 0
		max_bias = -ui_system._set_positions(bias, "User", True)
		max_bias = (max_bias + Height - 103) * max_bias > Height - 103

		while True:
			
			click = pygame.mouse.get_pressed()
			mouse_x, mouse_y = pygame.mouse.get_pos()
			release = False
			dt = clock.tick(MAX_FPS) / 1000.0
			
			events = pygame.event.get()
			
			for event in events:
				if event.type == pygame.QUIT:
					Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
					save()
					sys.exit()
				
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					release = True
				
				elif event.type == pygame.KEYUP:
					if event.key == hot_keys["Show keys"]:
						alt_pressed = not alt_pressed
					if event.key == hot_keys["Close"]:
						Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
						win_darken(win)
						menu()
					if event.key == hot_keys["Change screen"]:
						if screenmode == "FULLSCREEN":
							win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
							screenmode = "RESIZABLE"
						else:
							win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
							screenmode = "FULLSCREEN"

				elif event.type == pygame.MOUSEWHEEL:
					bias = max((min(bias + event.y * Settings["Game"][2], 0)), max_bias)
					ui_system._set_positions(bias, "User")
			
			# Очистка экрана
			win.fill(menu_color_light)
			
			# Обработка UI
			ui_system.handle_events(events, mouse_x, mouse_y, release, "User")
			ui_system.draw("User", bias, max_bias)
			
			help_button.main(help)
			display_button.main(display)
			languages_button.main(Languages)
			win.blit(load(path + "Images/Buttons/User 2.png", 132, 64), (10, 342))
			sound_button.main(Sound)
			statistics_button.main(Statistics)
			keys_button.main(Keys)
			game_button.main(Game)
			back_button.main()
			show_reset_settings()
			
			if alt_pressed:
				draw_key("ESC", 44, 108)

			if back_button.get_pressed():
				Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
				win_darken(win)
				menu()
				
			# Анимация и эффекты
			animate_click(dt, mouse_x, mouse_y)
			win_fill(alpha=100 - Settings["Display"][0])
			
			pygame.display.update()

	def Sound():

		global win, screenmode, Settings, alt_pressed, MAX_FPS

		bias = 0
		max_bias = -ui_system._set_positions(bias, "Sound", True)
		max_bias = (max_bias + Height - 103) * max_bias > Height - 103

		while True:
			
			click = pygame.mouse.get_pressed()
			mouse_x, mouse_y = pygame.mouse.get_pos()
			release = False
			dt = clock.tick(MAX_FPS) / 1000.0
			
			events = pygame.event.get()
			
			for event in events:
				if event.type == pygame.QUIT:
					Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
					save()
					sys.exit()
				
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					release = True
				
				elif event.type == pygame.KEYUP:
					if event.key == hot_keys["Show keys"]:
						alt_pressed = not alt_pressed
					if event.key == hot_keys["Close"]:
						Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
						win_darken(win)
						menu()
					if event.key == hot_keys["Change screen"]:
						if screenmode == "FULLSCREEN":
							win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
							screenmode = "RESIZABLE"
						else:
							win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
							screenmode = "FULLSCREEN"

					if event.key == pygame.K_RETURN:

						music_channel.set_volume(Settings["Sound"][0], Settings["Sound"][0] / 100)
						set_sound_volume(Settings["Sound"][1] / 100)

				elif event.type == pygame.MOUSEWHEEL:
					bias = max((min(bias + event.y * Settings["Game"][2], 0)), max_bias)
					ui_system._set_positions(bias, "Sound")
			
			# Очистка экрана
			win.fill(menu_color_light)
			
			# Обработка UI
			ui_system.handle_events(events, mouse_x, mouse_y, release, "Sound")
			ui_system.draw("Sound", bias, max_bias)
			
			help_button.main(help)
			display_button.main(display)
			languages_button.main(Languages)
			user_button.main(User)
			win.blit(load(path + "Images/Buttons/Sound 2.png", 160, 64), (10, 417))
			statistics_button.main(Statistics)
			keys_button.main(Keys)
			game_button.main(Game)
			back_button.main()
			show_reset_settings()
			
			if alt_pressed:
				draw_key("ESC", 44, 108)

			if back_button.get_pressed():
				Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
				win_darken(win)
				menu()
				
			# Анимация и эффекты
			animate_click(dt, mouse_x, mouse_y)
			win_fill(alpha=100 - Settings["Display"][0])
			
			pygame.display.update()

	def Statistics():

		global win, screenmode, Settings, alt_pressed, MAX_FPS

		bias = 0
		max_bias = -ui_system._set_positions(bias, "Statistics", True)
		max_bias = (max_bias + Height - 103) * max_bias > Height - 103

		while True:
			
			click = pygame.mouse.get_pressed()
			mouse_x, mouse_y = pygame.mouse.get_pos()
			release = False
			dt = clock.tick(MAX_FPS) / 1000.0
			
			events = pygame.event.get()
			
			for event in events:
				if event.type == pygame.QUIT:
					Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
					save()
					sys.exit()
				
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					release = True
				
				elif event.type == pygame.KEYUP:
					if event.key == hot_keys["Show keys"]:
						alt_pressed = not alt_pressed
					if event.key == hot_keys["Close"]:
						Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
						win_darken(win)
						menu()
					if event.key == hot_keys["Change screen"]:
						if screenmode == "FULLSCREEN":
							win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
							screenmode = "RESIZABLE"
						else:
							win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
							screenmode = "FULLSCREEN"

				elif event.type == pygame.MOUSEWHEEL:
					bias = max((min(bias + event.y * Settings["Game"][2], 0)), max_bias)
					ui_system._set_positions(bias, "Statistics")
			
			# Очистка экрана
			win.fill(menu_color_light)
			
			# Обработка UI
			ui_system.draw("Statistics", bias, max_bias)
			
			help_button.main(help)
			display_button.main(display)
			languages_button.main(Languages)
			user_button.main(User)
			sound_button.main(Sound)
			win.blit(load(path + "Images/Buttons/Statistics 2.png", 300, 64), (10, 492))
			keys_button.main(Keys)
			game_button.main(Game)
			back_button.main()
			show_reset_settings()
			
			if alt_pressed:
				draw_key("ESC", 44, 108)

			if back_button.get_pressed():
				Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
				win_darken(win)
				menu()
				
			# Анимация и эффекты
			animate_click(dt, mouse_x, mouse_y)
			win_fill(alpha=100 - Settings["Display"][0])
			
			pygame.display.update()

	def Keys():

		global win, screenmode, Settings, click, mouse_x, mouse_y, does_lighten, page, alt_pressed, hot_keys
		
		changed_key = ""
		looked_key = None
		key_values = ({
				"esc": pygame.K_ESCAPE,
				"f1": pygame.K_F1,
				"f2": pygame.K_F2,
				"f3": pygame.K_F3,
				"f4": pygame.K_F4,
				"f4": pygame.K_F5,
				"f5": pygame.K_F5,
				"f6": pygame.K_F6,
				"f7": pygame.K_F7,
				"f8": pygame.K_F8,
				"f9": pygame.K_F9,
				"f10": pygame.K_F10,
				"f11": pygame.K_F11,
				"f12": pygame.K_F12,
				"prt sc": pygame.K_PRINTSCREEN,
				"off": pygame.K_o,
				"delete": pygame.K_DELETE
			},
			{
				"`": pygame.K_BACKQUOTE,
				"1": pygame.K_1,
				"2": pygame.K_2,
				"3": pygame.K_3,
				"4": pygame.K_4,
				"5": pygame.K_5,
				"6": pygame.K_6,
				"7": pygame.K_7,
				"8": pygame.K_8,
				"9": pygame.K_9,
				"0": pygame.K_0,
				"-": pygame.K_MINUS,
				"=": pygame.K_EQUALS,
				"← backspace": pygame.K_BACKSPACE,
				"home": pygame.K_HOME
			},
			{
				"tab ⥂": pygame.K_TAB,
				"Q": pygame.K_q,
				"W": pygame.K_w,
				"E": pygame.K_e,
				"R": pygame.K_r,
				"T": pygame.K_t,
				"Y": pygame.K_y,
				"U": pygame.K_u,
				"I": pygame.K_i,
				"O": pygame.K_o,
				"P": pygame.K_p,
				"[": pygame.K_LEFTBRACKET,
				"]": pygame.K_RIGHTBRACKET,
				"\\": pygame.K_BACKSLASH,
				"pg up": pygame.K_PAGEUP,
			},
			{
				"caps lock": pygame.K_CAPSLOCK,
				"A": pygame.K_a,
				"S": pygame.K_s,
				"D": pygame.K_d,
				"F": pygame.K_f,
				"G": pygame.K_g,
				"H": pygame.K_h,
				"J": pygame.K_j,
				"K": pygame.K_k,
				"L": pygame.K_l,
				";": pygame.K_SEMICOLON,
				"'": pygame.K_QUOTE,
				"↵ enter": pygame.K_RETURN,
				"pg dn": pygame.K_PAGEDOWN
			},
			{
				"shift ↑": pygame.K_LSHIFT,
				"Z": pygame.K_z,
				"X": pygame.K_x,
				"C": pygame.K_c,
				"V": pygame.K_v,
				"B": pygame.K_b,
				"N": pygame.K_n,
				"M": pygame.K_m,
				",": pygame.K_COMMA,
				".": pygame.K_PERIOD,
				"/": pygame.K_SLASH,
				"↑ shift": pygame.K_RSHIFT,
				"↑": pygame.K_UP,
				"end": pygame.K_END
			},
			{
				"ctrl": pygame.K_LCTRL,
				"fn": pygame.K_o,
				"super": pygame.K_LSUPER,
				"alt": pygame.K_LALT,
				" ": pygame.K_SPACE,
				"alt ": pygame.K_RALT,
				"ctrl ": pygame.K_RCTRL,
				"←": pygame.K_LEFT,
				"↓": pygame.K_DOWN,
				"→": pygame.K_RIGHT
			}
			)
		key_values_combined = {}
		for key in key_values:
			key_values_combined.update(key)

		key_sizes = (
			(40,) * 16,
			(40,) * 13 + (90,) + (40,),
			(60,) + (40,) * 12 + (70,) + (40,),
			(70,) + (40,) * 11 + (110,) + (40,),
			(90,) + (40,) * 10 + (90,) + (40,) * 2,
			(40,) * 4 + (340,) + (40,) * 50
			)
		check_keys = lambda key: key_values_combined[key] in hot_keys.values() # Эта lambda-функция выясняет, является ли данная клавиша одной из горячих клавиш игры
		check_blocked_keys = lambda key: key in ("prt sc", "super", "off")

		while True:

			changed_key = ""
			click = pygame.mouse.get_pressed()
			mouse_x, mouse_y = pygame.mouse.get_pos()
			release = False
			dt = clock.tick(MAX_FPS) / 1000.0
			
			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					Saver.save_objects(path + "Saves/Settings/Hot keys.save", hot_keys)
					save()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					release = True
				if event.type == pygame.KEYUP:
					if event.key == hot_keys["Show keys"]:
						alt_pressed = not alt_pressed
					if event.key == hot_keys["Close"]:
						if looked_key is not None:
							looked_key = None
						else:
							Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
							Saver.save_objects(path + "Saves/Settings/Hot keys.save", hot_keys)
							win_darken(win)
							menu()

					if event.key == hot_keys["Change screen"]:
						if screenmode == "FULLSCREEN":
							win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
							screenmode = "RESIZABLE"
						else:
							win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
							screenmode = "FULLSCREEN"

			back_button.main()
			if back_button.get_pressed():
				if looked_key is not None:
					looked_key = None
				else:
					Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
					Saver.save_objects(path + "Saves/Settings/Hot keys.save", hot_keys)
					win_darken(win)
					menu()
				
			win.fill(menu_color_light)
			pygame.draw.rect(win, menu_color_medium, (-8, 100, 373, Height), 8)
			pygame.draw.line(win, menu_color_medium, (307, 103), (Width, 103), 8)
			back_button.main()
			show_reset_settings()
			help_button.main(help)
			display_button.main(display)
			languages_button.main(Languages)
			user_button.main(User)
			sound_button.main(Sound)
			statistics_button.main(Statistics)
			win.blit(load(path + "Images/Buttons/Keys 2.png", 132, 64), (10, 567))
			game_button.main(Game)
			
			littleTextInfo = pygame.font.Font(path + "Font.ttf", 8)
			key_color = menu_color_medium
			X = 385
			Y = 123
			close_key = ""

			for line_num, line in enumerate(key_values):
				for key_x, key in enumerate(line):
					key_size = key_sizes[line_num][key_x]
					key_rect = pygame.Rect(X, Y, key_size, 40)
					key_color = menu_color_medium
					if check_keys(key): key_color = menu_color_dark
					if key == looked_key: key_color = menu_color_medium
					if check_blocked_keys(key): key_color = (255, 255, 255)
					if key_values_combined[key] == hot_keys["Close"]: close_key = key
					if key_rect.collidepoint((mouse_x, mouse_y)): changed_key = key
					
					pygame.draw.rect(win, key_color, (X, Y, key_size, 40), 6 if changed_key == key else 3)
					win.blit(littleTextInfo.render(key, True, key_color), (X + 5, Y + 7))
					X += key_size + 10
				X = 385
				Y += 50
			
			text(t("Hotkeys are highlighted in dark blue"), 385, 440, menu_color_dark)
			text(t("Locked keys are highlighted in white"), 385, 470, (255, 255, 255))
			text(t("To change the hot key, click on it"), 385, 500, menu_color_medium)

			if Width - 30 - textInfo.size(t("Reset key settings"))[0] < mouse_x < Width - 30 and 420 < mouse_y < 450:
				win.blit(textInfo.render(t("Reset key settings"), True, menu_color_dark), (Width - 30 - textInfo.size(t("Reset key settings"))[0], 420))
				if click[0]:
					hot_keys = default_hot_keys
			else:
				win.blit(textInfo.render(t("Reset key settings"), True, menu_color_medium), (Width - 30 - textInfo.size(t("Reset key settings"))[0], 420))

			pygame.draw.rect(win, menu_color_medium, (385, 530, Width - 500, 150))
			pygame.draw.rect(win, menu_color_dark, (385, 530, Width - 500, 150), 5)
			text(changed_key if looked_key is None else f"Выбрана клавиша {looked_key}.\nНажмите {close_key}, чтобы отменить, либо выберите клавишу, которую Вы хотите назначить вместо неё.", 400, 545, menu_color_dark)
			
			changed_key_key = ""
			if changed_key == "":
				changed_key_value = None
			else:
				changed_key_value = key_values_combined[changed_key]

			if changed_key_value is None:
				win.blit(textInfo.render(changed_key_key, True, menu_color_dark), (400, 575))
			else:
				for key, val in hot_keys.items():
					if val == changed_key_value:
						text("\n" + key, 400, 575, menu_color_dark)
						break

			if changed_key != "" and release:
				
				if looked_key is None:
					if changed_key != "" and check_keys(changed_key) and not check_blocked_keys(key):
						looked_key = changed_key
				elif changed_key != looked_key and looked_key is not None and not check_blocked_keys(changed_key) and not check_keys(changed_key):
					for key, val in hot_keys.items():
						if val == key_values_combined[looked_key]:
							hot_keys[key] = changed_key_value
							break
					looked_key = None

			if alt_pressed:
				draw_key("ESC", 44, 108)

			animate_click(dt, mouse_x, mouse_y)

			win_fill(alpha=100 - Settings["Display"][0])   # Если в настройках установлена яркость ниже 100, то экран становится темнее
			
			if not does_lighten:
				win_lighten(win)
				does_lighten = True

			pygame.display.update()

	def Game():

		global win, screenmode, Settings, alt_pressed, MAX_FPS

		bias = 0
		max_bias = -ui_system._set_positions(bias, "Game", True)
		max_bias = (max_bias + Height - 103) * max_bias > Height - 103

		while True:
			
			click = pygame.mouse.get_pressed()
			mouse_x, mouse_y = pygame.mouse.get_pos()
			release = False
			dt = clock.tick(MAX_FPS) / 1000.0
			
			events = pygame.event.get()
			
			for event in events:
				if event.type == pygame.QUIT:
					Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
					save()
					sys.exit()
				
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					release = True
				
				elif event.type == pygame.KEYUP:
					if event.key == hot_keys["Show keys"]:
						alt_pressed = not alt_pressed
					if event.key == hot_keys["Close"]:
						Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
						win_darken(win)
						menu()
					if event.key == hot_keys["Change screen"]:
						if screenmode == "FULLSCREEN":
							win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
							screenmode = "RESIZABLE"
						else:
							win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
							screenmode = "FULLSCREEN"

				elif event.type == pygame.MOUSEWHEEL:
					bias = max((min(bias + event.y * Settings["Game"][2], 0)), max_bias)
					ui_system._set_positions(bias, "Game")
			
			# Очистка экрана
			win.fill(menu_color_light)
			
			# Обработка UI
			ui_system.handle_events(events, mouse_x, mouse_y, release, "Game")
			ui_system.draw("Game", bias, max_bias)
			
			help_button.main(help)
			display_button.main(display)
			languages_button.main(Languages)
			user_button.main(User)
			sound_button.main(Sound)
			statistics_button.main(Statistics)
			keys_button.main(Keys)
			win.blit(load(path + "Images/Buttons/Game 2.png", 132, 64), (10, 642))
			back_button.main()
			show_reset_settings()
			
			if alt_pressed:
				draw_key("ESC", 44, 108)

			if back_button.get_pressed():
				Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)
				win_darken(win)
				menu()
				
			# Анимация и эффекты
			animate_click(dt, mouse_x, mouse_y)
			win_fill(alpha=100 - Settings["Display"][0])
			
			pygame.display.update()
	
	win_darken(win)
	help()

def change_a_character():

	global does_lighten

	does_lighten = False

	back_button = Button(-20, -20, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back.png"), (128, 128)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back 2.png"), (128, 128)))
	character_button = Button(10, 120, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Character.png"), (272, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Character 2.png"), (272, 64)))
	pets_button = Button(10, 192, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Pets.png"), (132, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Pets 2.png"), (132, 64)))
	page_back_button = Button(361, Height - 138, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back.png"), (128, 128)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back 2.png"), (128, 128)))
	page_next_button = Button(Width - 138, Height - 138, pygame.transform.flip(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back.png"), (128, 128)), True, False), pygame.transform.flip(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back 2.png"), (128, 128)), True, False))

	bigTextInfo = pygame.font.Font(path + "Font.ttf", 36)
	
	win_darken(win)

	def characters():

		global win, screenmode, does_lighten, page, alt_pressed
		
		class Character():

			def __init__(self, name: str, info: str, images_list: list):
				self.name = name
				self.info = info
				self.images_list = images_list
				self.image_num = 0
		
		characters_list = [
			Character("Hiro", "123", [
				player.animations["Down"][0],
				player.animations["Down-left"][0],
				player.animations["Left"][0],
				player.animations["Up-left"][0],
				player.animations["Up"][0],
				player.animations["Up-right"][0],
				player.animations["Right"][0],
				player.animations["Down-right"][0],
			])
		]

		changed_character = characters_list[0]
		changed_character_num = 0

		while True:

			mouse_x, mouse_y = pygame.mouse.get_pos()
			dt = clock.tick(MAX_FPS) / 1000.0

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					save()
					sys.exit()
				if event.type == pygame.KEYUP:
					if event.key == hot_keys["Show keys"]:
						alt_pressed = not alt_pressed
					if event.key == hot_keys["Close"]:
						win_darken(win)
						menu()
					if event.key == pygame.K_1:
						changed_character_num = 0
					if event.key == pygame.K_2:
						changed_character_num = 1
					if event.key == pygame.K_LEFT and page > 1:
						page -= 1
					if event.key == pygame.K_RIGHT and page < 3:
						page += 1
					if event.key == hot_keys["Change screen"]:
						if screenmode == "FULLSCREEN":
							win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
							screenmode = "RESIZABLE"
						else:
							win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
							screenmode = "FULLSCREEN"
			
			win.fill()

			pygame.draw.rect(win, menu_color_medium, (-8, 100, 315, Height), 8)
			pygame.draw.rect(win, menu_color_medium, (315, 100, Width - 325, 100), 8)
			pygame.draw.rect(win, menu_color_medium, (316 + changed_character_num * 300, 210, 256, 256), 8)
			pygame.draw.rect(win, menu_color_medium, (316, 476, 256, Height - 604), 8)
			pygame.draw.rect(win, menu_color_medium, ((Width - 415) // 2 + 230, 476, 256, Height - 604), 8)
			pygame.draw.rect(win, menu_color_medium, (Width - 266, 476, 256, Height - 604), 8)

			win.blit(textInfo.render(t("Name") + ":", True, menu_color_medium), (335, 120))
			win.blit(bigTextInfo.render(changed_character.name, True, menu_color_medium), (335, 140))
			pygame.draw.line(win, menu_color_medium, (325 + len(changed_character.name) * 30, 100), (325 + len(changed_character.name) * 30, 198), 8)
			win.blit(textInfo.render(t("Info") + ":", True, menu_color_medium), (Width - len(changed_character.info) * 30 - 28, 120))
			win.blit(bigTextInfo.render(changed_character.info, True, menu_color_medium), (Width - len(changed_character.info) * 30 - 28, 140))
			back_button.main()
			
			if back_button.get_pressed():
				win_darken(win)
				menu()
			win.blit(load(path + "Images/Buttons/Character 2.png", 278, 64), (10, 120))
			pets_button.main(pets)
			
			page_back_button.main()
			if page_back_button.get_pressed() and page > 1: page -= 1
			page_next_button.main()
			
			if page_next_button.get_pressed() and page < 3: page += 1
			win.blit(bigTextInfo.render(str(page), True, menu_color_medium), ((Width - 415) // 2 + 340, Height - 96))

			for index, character in enumerate(characters_list):
				
				character.image_num += 1
				if character.image_num == 40:
					character.image_num = 0
				if index // 3 == page - 1:
					win.blit(character.images_list[character.image_num // 5], (316, 216))
					
			if alt_pressed:
				
				draw_key("ESC", 44, 108)
				draw_key("<-", 425, Height - 168)
				draw_key("->", Width - 74, Height - 168)

			animate_click(dt, mouse_x, mouse_y)

			win_fill(alpha=100 - Settings["Display"][0])
			
			if not does_lighten:
				win_lighten(win)
				does_lighten = True

			pygame.display.update()
	
	def pets():

		global win, screenmode, does_lighten
		
		while True:
			
			mouse_x, mouse_y = pygame.mouse.get_pos()
			dt = clock.tick(MAX_FPS) / 1000.0

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					save()
					sys.exit()
				if event.type == pygame.KEYUP:
					if event.key == hot_keys["Change screen"]:
						if screenmode == "FULLSCREEN":
							win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
							screenmode = "RESIZABLE"
						else:
							win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
							screenmode = "FULLSCREEN"
					if event.key == hot_keys["Close"]:
						win_darken(win)
						menu()


			win.fill(menu_color_light)

			pygame.draw.rect(win, menu_color_medium, (-8, 100, 315, Height), 8)
			pygame.draw.rect(win, menu_color_medium, (315, 100, Width - 325, 100), 8)

			back_button.main()

			if back_button.get_pressed():
				win_darken(win)
				menu()

			character_button.main(characters)

			win.blit(load(path + "Images/Buttons/Pets 2.png", 132, 64), (10, 192))

			animate_click(dt, mouse_x, mouse_y)

			win_fill(alpha=100 - Settings["Display"][0])
			
			if not does_lighten:
				win_lighten(win)
				does_lighten = True
			
			pygame.display.update()

	characters()

hot_keys = Saver.load_objects(path + "Saves/Settings/Hot keys.save")
objects_templates = {
		"Table": Object("Table", 0, 0, "Images/Objects/Table.png", (256, 256), is_solid=True, breakable_by_hammer=True),
		"Wall table": Object("Wall table", 0, 0, "Images/Objects/Wall table.png", (256, 256), special_flags=1, is_solid=True, breakable_by_hammer=True),
		"Furnace": Object("Furnace", 0, 0, "Images/Items/Furnace.png", (256, 256), special_flags=1, is_solid=True, breakable_by_hammer=True),
		"Punch": Object("Punch", 0, 0, "Images/Objects/Punch 1.png", (256, 256), is_solid=True, breakable_by_hammer=True)
		}

# Основной цикл игры

def start_game():
	
	global win, changed_slot, menu_open, multiplayer_menu_open, screenmode, inventory_open, hold_left, backrooms, text_color, bullet_num, craft_items_list, craft_amounts_list, craft_images_list, screenshot_num, mouse_x, mouse_y, item_settings_open, chat_tick, chat, main_chat, chat_open, craft_list_open, craft_list_page, craft_list_offset, craft_list_max_offset, click, in_motherboard, world_name, color, multiplayer, animation, start_time, new_particles, game, alt_pressed, player, world, FPS, MAX_FPS, screen_rect, time_index, game_events, show_cursor, cursor_timer

	night_playing = False
	bigTextInfo = pygame.font.Font(path + "Font.ttf", 36)
	aaa = 0
	AA = 0
	use_item_pressed = False
	start_time = time.time()

	tile_size = 256
	Width, Height = pygame.display.get_surface().get_size()
	tiles_x = (Width // tile_size) + 3
	tiles_y = (Height // tile_size) + 3
	dx = 0
	dy = 0
	release = False
	craft_list_max_offset = (len(inventory.recipes) + 1) * -80 + Height

	new_particles = []

	if Settings["Game"][1]:
		up_b = Button(Width - 148, Height - 148, arrow_up, arrow_up, sound=False, cooldown=0)
		left_b = Button(Width - 222, Height - 74, arrow_left, arrow_left, sound=False, cooldown=0)
		down_b = Button(Width - 148, Height - 74, arrow_down, arrow_down, sound=False, cooldown=0)
		right_b = Button(Width - 74, Height - 74, arrow_right, arrow_right, sound=False, cooldown=0)

	
	craft_list_back_button = Button(114, Height - 176, bigTextInfo.render("<", True, (0, 150, 0)), bigTextInfo.render("<", True, (0, 100, 0)))
	craft_list_next_button = Button(Width - 144, Height - 176, bigTextInfo.render(">", True, (0, 150, 0)), bigTextInfo.render(">", True, (0, 100, 0)))

	# Загрузка данных мира
	if not multiplayer or multiplayer_role == "Host":
		world.chunk_manager.save_directory = path + "Saves/Worlds/" + world_name + "/Chunks/"

		if os.path.exists(path + "Saves/Worlds/" + world_name):
			
			world.mobs = Saver.load_objects(path + "Saves/Worlds/" + world_name + "/Mobs.save")
			player.x, player.y, Backrooms.InBackrooms, Backrooms.Level, world.current_cave, player.speed, player.HP, start_time, ron.x, ron.y, ron.home, ron.inventory, world.chunk_manager.generator.seed, time_system.current_time = Saver.load_objects(path + "Saves/Worlds/" + world_name + "/Info.save")
			world.chunk_manager.update_seed()
			game.difficulty, player.god_mode = Saver.load_objects(path + "Saves/Worlds/" + world_name + "/Settings.save")
			inventory.whole_inventory = Saver.load_objects(path + "Saves/Worlds/" + world_name + "/Inventory.save")
			player.effects = Saver.load_objects(path + "Saves/Worlds/" + world_name + "/Effects.save")

			if multiplayer:
				net.peers[net.player_id].x = player.x
				net.peers[net.player_id].y = player.y
				net.peers[net.player_id].direction = player.direction
			
		else:

			os.mkdir(path + "Saves/Worlds/" + world_name)
			os.mkdir(path + "Saves/Worlds/" + world_name + "/Images")

			save(False, True)
		
		# Старая система плагинов, которая уже толком не работает. От неё нужно отказываться в пользу модов (которые ещё не созданы)
		plugins = []
		for _, _, files in os.walk(os.path.dirname(path) + "/Plugins/"):
			plugins = files
			break
		
		for plugin in plugins:

			for i in Saver.load_objects(path + "" + plugin):

				match i[0]:

					case "Item":
						
						from Inventory import Resource
						try:
							inventory.resources[i[1]] = Resource(i[1], i[2], [i[3], i[4]], [i[5], i[6]], i[7])
						except FileNotFoundError:
							inventory.resources[i[1]] = Resource(i[1], path + "Images/No-file texture.png", [i[3], i[4]], [i[5], i[6]], i[7])

					case "Recipe":

						from Inventory import Recipe
						a = []
						for ii in i[2]: a.append(str(ii))
						inventory.recipes.append(Recipe(i[1], a, i[3], i[4], i[5], i[6]))
						del Recipe
			
					case "Object":

						try:
							a = Object(i[1], i[3], i[4], i[2], (load(i[2]).get_width(), load(i[2]).get_height()), special_flags=i[5], add_path=False)
						except FileNotFoundError:
							a = Object(i[1], i[3], i[4], "Images/No-file texture.png", special_flags=i[5])
						b = True
						for object in world.visible_objects:
							if a == object:
								b = False
						if b and world_name == i[6]:
							world.visible_objects.append(a)

					case "Command":

						if i[2] == "1":
							try:
								eval(i[1])
							except:
								pass
	
	while True:

		mouse_x, mouse_y = pygame.mouse.get_pos()
		mouse_object = None
		click = pygame.mouse.get_pressed()
		Width, Height = pygame.display.get_surface().get_size()
		release = False
		use_item_pressed = False
		dx = 0
		dy = 0
		screen_rect = pygame.Rect((player.x - Width / 2, player.y + Height / 2, Width, Height))
		player.hovered_object = None
		player.breaking_object = None

		FPS = int(clock.get_fps())
		dt = clock.tick(MAX_FPS) / 1000.0
		time_system.update(dt)
		player.changed_item = inventory.whole_inventory[changed_slot]
		if multiplayer:
			game_events.clear()
		events = pygame.event.get()
		for event in events:
			
			if event.type == pygame.QUIT:
				statistics[1] += (time.time() - start_time) / 3600
				if multiplayer:
					net.disconnect()
				save()
				sys.exit()

			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					release = True
			
			elif event.type == pygame.MOUSEWHEEL and not any((item_settings_open, ron.window[0], in_motherboard)):
				if craft_list_open:
					craft_list_offset = max((min(craft_list_offset + event.y * Settings["Game"][2], 0)), craft_list_max_offset)
				else:
					changed_slot += event.y
					if changed_slot > 9: changed_slot = 0
					if changed_slot < 0: changed_slot = 9

			if event.type == pygame.KEYUP:
				if chat_open:
					if event.key == hot_keys["Close"]:
						chat_open = False
						input_system.stop_input()
				else:
					if event.key == hot_keys["Show keys"]:
						alt_pressed = not alt_pressed
					if event.key == hot_keys["Use item"]:
						use_item_pressed = True
					if event.key == hot_keys["Multiplayer menu"]:
						multiplayer_menu_open = True
					if event.key == hot_keys["Set Ron home"]:
						ron.home = [player.x, player.y]
					if event.key == hot_keys["Menu"]:
						menu_open = not menu_open
					if event.key == hot_keys["Open chat"]:
						chat_open = True
						input_system.start_input("Chat", 20, Height - 40, (255, 255, 255))
					if event.key == hot_keys["Execute command"]:
						chat_open = True
						input_system.start_input("Chat", 20, Height - 40, (255, 255, 255), input_text="/")

					if event.key == hot_keys["Close"]:
	
						if item_settings_open:
							item_settings_open = False
						elif ron.window[0]:
							ron.window[0] = False
						elif in_motherboard is not None:
							in_motherboard = None
						elif craft_list_open:
							craft_list_open = False
						elif inventory_open:
							inventory_open = False
						else:
							music_channel.stop()
							statistics[1] += (time.time() - start_time) / 3600
							save()
							world.chunk_manager.chunks = {}
							world.mobs = []
							player.effects = []
							particles = []
							chat = []
							main_chat = []
							chat_tick = 0
							inventory.whole_inventory = [None] * 30
							world_name = None
							if multiplayer:
								net.disconnect()
							menu()

					if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0, ):
						last_changed_slot = changed_slot
						changed_slot = int(event.unicode) - 1 + 10 * (event.key == pygame.K_0)
						player.changed_item = inventory.whole_inventory[changed_slot]
						if player.changed_item is not None:
							player.changed_item = player.changed_item.name

					if event.key == pygame.K_o and Settings["User"][1]:
						world.mobs.append(Spider(player.x, player.y))
						# create_light_circle(world.chunk_manager, player.x, player.y, 10, 15)
						# world.chunk_manager.chunks[(0, 0)].shadow_map.update({(0, 0): 0, (1, 0): 1, (2, 0): 2, (3, 0): 3, (4, 0): 4, (5, 0): 5, (6, 0): 6, (7, 0): 7, (8, 0): 8, (9, 0): 9, (10, 0): 10, (11, 0): 11, (12, 0): 12, (13, 0): 13, (14, 0): 14, (15, 0): 15})
						# world.chunk_manager.chunks[(0, 0)].light_map.update({(0, 1): 0, (1, 1): 1, (2, 1): 2, (3, 1): 3, (4, 1): 4, (5, 1): 5, (6, 1): 6, (7, 1): 7, (8, 1): 8, (9, 1): 9, (10, 1): 10, (11, 1): 11, (12, 1): 12, (13, 1): 13, (14, 1): 14, (15, 1): 15})


					if event.key == hot_keys["Help"]:
						music_channel.stop()
						statistics[1] += (time.time() - start_time) / 3600
						save(False)
						settings()

					if event.key == hot_keys["Inventory"]:
						inventory_open = not inventory_open
						if not inventory_open:
							if craft_items_list != [None] * 7:
								for item_index, item in enumerate(craft_items_list):
									if item is not None:
										inventory.increate(item, craft_amounts_list[item_index])
							craft_items_list = [None] * 7
							craft_amounts_list = [None] * 7
							craft_images_list = [None] * 7

					if event.key == hot_keys["Throw away the item"] and inventory.whole_inventory[changed_slot] is not None:
						
						if Backrooms.InBackrooms:
							backrooms_objects.append(Object(inventory.whole_inventory[changed_slot].name, player.x, player.y, "Images/Items/" + inventory.whole_inventory[changed_slot].name + ".png", special_flags="Item"))
						else:
							world.particles.append(create_throw_particle(inventory.whole_inventory[changed_slot].image, inventory.whole_inventory[changed_slot].name))
						
						inventory.reduce(changed_slot)

					if event.key == hot_keys["Change screen"]:
						if screenmode == "FULLSCREEN":
							win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
							screenmode = "RESIZABLE"
						else:
							win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
							screenmode = "FULLSCREEN"
		
		if inventory_open:
			if click[0] and not hold_left:
				inventory.set_start_cell(mouse_x, mouse_y)
				hold_left = True
			if hold_left and not click[0]:
				craft_items_list, craft_amounts_list, craft_images_list = inventory.set_end_cell(mouse_x, mouse_y, craft_items_list, craft_amounts_list, craft_images_list)
				hold_left = False

		keys = pygame.key.get_pressed()

		if not chat_open:

			if keys[hot_keys["Move left"]]: dx = -1
			if keys[hot_keys["Move right"]]: dx = 1
			if keys[hot_keys["Move down"]]: dy = -1
			if keys[hot_keys["Move up"]]: dy = 1

			if abs(dx) == abs(dy) == 1:
				dx *= 0.7
				dy *= 0.7

		# Если есть движение - двигаем игрока
		if dx != 0 or dy != 0:
			player.move(dx, dy, dt, check_collision, world)
			game_events.append({"event_type": "player_moved", "x": player.x, "y": player.y, "direction": player.direction})
			if multiplayer:
				net.peers[net.player_id].x = player.x
				net.peers[net.player_id].y = player.y
				net.peers[net.player_id].direction = player.direction
		else:
			if player.is_moving:
				game_events.append({"event_type": "player_stopped", "x": player.x, "y": player.y})
			player.stop()
		
		# Обновляем анимацию
		player.update_animation(dt)

		win.fill((0, 0, 0))

		if Width // 2 - 100 <= mouse_x <= Width // 2 + 100 and Height // 2 - 100 <= mouse_y <= Height // 2 + 100 and not any((item_settings_open, ron.window[0], in_motherboard, craft_list_open)):
			mouse_object = t("It's you")

		if not Backrooms.InBackrooms:
			
			current_chunk = world.chunk_manager.get_chunk_at(player.x, player.y)
			if current_chunk is not None:
				current_biome = current_chunk.biome
			else:
				current_biome = None
			world.render_loaded_chunks(player)
			if time_system.day_phase == "Night" and not night_playing:
				music_channel.stop()
				music_channel.play(pygame.mixer.Sound(path + "Soundtracks/Night " + str(random.randint(1, 2)) + ".mp3"))
				night_playing = True

			elif not music_channel.get_busy() or (night_playing and time_system.day_phase != "Night"):

				night_playing = False
				music_channel.stop()

				match current_biome:

					case "Forest" | "Field":
						music_channel.queue(pygame.mixer.Sound(path + "Soundtracks/Forest " + str(random.randint(1, 3)) + ".mp3"))
						
					case "Desert":
						music_channel.queue(pygame.mixer.Sound(path + "Soundtracks/Desert " + str(random.randint(1, 2)) + ".mp3"))
						
					case "Swamp":
						music_channel.queue(pygame.mixer.Sound(path + "Soundtracks/Swamp " + str(random.randint(1, 2)) + ".mp3"))
						
					case "Taiga":
						music_channel.queue(pygame.mixer.Sound(path + "Soundtracks/Taiga " + str(random.randint(1, 1)) + ".mp3"))

			if player.animation_timer == 0 and (player.frame_index % 6 == 2 or player.frame_index % 6 == 5):

				if world.current_cave is not None:
					play_sound("Cave walking", 3)

				elif current_biome in ("Forest", "Field"):
					play_sound("Grass walking", 3)

				elif current_biome == "Desert":
					play_sound("Sand walking", 3)

				elif current_biome == "Taiga":
					play_sound("Snow walking", 3)

				elif current_biome == "Swamp":
					play_sound("Swamp walking", 3)

		else:

			for i, ii in product(range(-6, 6), range(-3, 3)):
				win.blit(textures["Backrooms " + str(Backrooms.Level)], (Width - player.x % 256 + i * 256, player.y % 256 + ii * 256))
		
		for mechanism in world.mechanisms:
			mechanism.main()
		
		for farmland in world.visible_farmlands.values():
			farmland.main(release, dt)

		if not Backrooms.InBackrooms and world.current_cave is None:

			if False: # TODO тут сделать переход в закулисье
				Backrooms.InBackrooms = True
				color = colors["Backrooms"]
				text_color = colors["Backrooms2"]
				i = -1

				for object in Backrooms.objects:
					i += 1
					backrooms_objects.append(Object(object, Backrooms.objects_x[i], Backrooms.objects_y[i], "Images/Items/" + inventory.resources[object].name + ".png", special_flags="Item"))

				x = 0
				y = 0

				play_sound("1", loops=-1)
				pygame.mixer.music.set_volume(0.5)

				aaa = 100
				AA = 0

		elif Backrooms.InBackrooms:
			
			if int(player.x / 2000) != Backrooms.room_x:
				Backrooms.get_rooms(int(player.x / 2000), int(player.y / 2000))
			if int(player.y / 2000) != Backrooms.room_y:
				Backrooms.get_rooms(int(player.x / 2000), int(player.y / 2000))

			Backrooms.room_x = int(player.x / 2000)
			Backrooms.room_y = int(player.y / 2000)

			match Backrooms.Level:
				case 0:
					win.fill((120, 100, 40))
				case 0.2:
					win.fill((170, 60, 50))
				case 1:
					win.fill((100, 100, 100))
				case 2:
					win.fill((50, 50, 50))

			for room in Backrooms.rooms:
				room.main(player.x, player.y)

			if random.randint(1, 1000) == 1:
				play_sound("Random sound 1")
			
			match Backrooms.Level:

				case 0:

					wall_color = (180, 159, 50)
					next_levels = [0.2, 1]

				case 0.2:

					wall_color = (200, 180, 70)
					next_levels = [0, 1]

				case 1:

					wall_color = (50, 50, 50)
					next_levels = [2]

				case 2:

					wall_color = (50, 50, 50)

			a, b, c, d = True, True, True, True

			for i in range(Width // 2 - 80, Width // 2 + 80):

				if win.get_at((i, Height // 2 + 127)) == wall_color:
					a = False

				if win.get_at((Width // 2 - 100, i)) == wall_color:
					b = False

			for i in range(Height // 2 - 100, Height // 2 + 100):

				if win.get_at((Width // 2 - 100, i)) == wall_color:
					c = False

				if win.get_at((Width // 2 + 107, i)) == wall_color:
					d = False

			aa = 0

			for i in (a, b, c, d):
				if not i:
					aa += 1

			if aa == 4:
				Backrooms.get_rooms(player.x // 2000, player.y // 2000)

			if aa == 3 and keys[hot_keys["Noclip in backrooms"]] and random.randint(1, 30) == 30:

				AA = 100
				Backrooms.Level = random.choice(next_levels)

				player.x = 0
				player.y = 0

				Backrooms.get_rooms(0, 0)
				win.fill((0, 0, 0))

			if aaa > 0:
				win.blit(pygame.transform.scale(win, (Width - aaa * 2, Height - aaa * 2)), (aaa, aaa))

			aaa = 0
			if random.randint(1, 300) == 50:
				aaa = 50

			if AA > 0:
				win.blit(pygame.transform.scale(win, (Width - AA * 2, Height - AA * 2)), (AA, AA))
				AA -= 3
		
		if not Backrooms.InBackrooms:

			if world.current_cave is not None and -64 <= player.x <= 64 and -64 <= player.y <= 64 and release:

				player.x = world.current_cave.x
				player.y = world.current_cave.y - 128

				world.current_cave = None
			
			if world.current_cave is None:

				for cave in world.visible_caves:

					cave.main()
					get_in = cave.get_in()
					if get_in is not None:
						world.current_cave = get_in
						player.x = 0
						player.y = -128

			if world.current_cave is not None:
				
				win.fill((50, 50, 50))
				
				pygame.draw.rect(win, (100, 100, 100), (world.current_cave.own_width // 2 * -1 - player.x + Width // 2, player.y - world.current_cave.own_height // 2 + Height // 2, world.current_cave.own_width, world.current_cave.own_height))
				world.current_cave.render()
				win.blit(cave_texture, (0 - player.x + Width // 2 - world.current_cave.w // 2, player.y - 0 + Height // 2 - world.current_cave.h // 2))

				for object in world.current_cave.objects:

					object.main(player)

					if object.__class__ == Object:

						if object.x - player.x + Width // 2 - object.w // 2 <= mouse_x <= object.x - player.x + Width // 2 + object.w // 2 and player.y - object.y + Height // 2 - object.h // 2 <= mouse_y <= player.y - object.y + Height // 2 + object.h // 2:

							if object.name == "Iron ore" and click[0] and inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name in ("Stone pickaxe"):

								object.special_flags -= 1
								object.image = pygame.transform.scale(object.image, (32, 32))

								for _ in range(random.randint(20, 25)):

									a = random.randint(0, 31)
									b = random.randint(0, 31)

									if object.image.get_at((a, b)).a != 0:
										c = random.randint(10, 20)
										c = pygame.Surface((a, a))
										c.fill(object.image.get_at((a, b)))
										object.image.set_at((a, b), (0, 0, 0, 99))
										if random.randint(1, 5) == 1:
											world.particles.append(Particle(object.x + (a - 16) * 8, object.y + (b - 16) * 8, c, 5, -16, 10, end_time=0.5))

								object.image.set_alpha(object.image.get_alpha() - 1)
								object.image = pygame.transform.scale(object.image, (256, 256))

								if random.randint(1, 15) == 1:
									play_sound("Stone breaking", 2)

								if object.special_flags == -1:
									world.current_cave.objects.remove(object)
									for i in range(random.randint(1, 3)):
										world.current_cave.objects.append(Object("Iron ore", random.randint(object.x - 128, object.x + 128), random.randint(object.y - 128, object.y + 128), "Images/Items/Iron ore.png", special_flags="Item"))
									break

							if object.name == "Gold ore" and click[0] and inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name in ("Stone pickaxe"):

								object.special_flags -= 1
								object.image = pygame.transform.scale(object.image, (32, 32))

								for _ in range(random.randint(20, 25)):

									a = random.randint(0, 31)
									b = random.randint(0, 31)
									if object.image.get_at((a, b)).a != 0:
										c = random.randint(10, 20)
										c = pygame.Surface((a, a))
										c.fill(object.image.get_at((a, b)))
										object.image.set_at((a, b), (0, 0, 0, 99))
										if random.randint(1, 5) == 1:
											world.particles.append(Particle(object.x + (a - 16) * 8, object.y + (b - 16) * 8, c, 5, -16, 10, end_time=0.5))

								object.image.set_alpha(object.image.get_alpha() - 1)
								object.image = pygame.transform.scale(object.image, (256, 256))

								if random.randint(1, 15) == 1:
									play_sound("Stone breaking", 2)

								if object.special_flags == -1:
									world.current_cave.objects.remove(object)
									for _ in range(random.randint(1, 3)):
										world.current_cave.objects.append(Object("Gold ore", random.randint(object.x - 128, object.x + 128), random.randint(object.y - 128, object.y + 128), "Images/Items/Gold ore.png", special_flags="Item"))
									break

						if object.name == "Pot":
							if object.get_right_pressed(mouse_x, mouse_y, player) and inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].type == "Flower":
								world.chunk_manager.get_chunk_at(object.x, object.y).items.append(Object(inventory.whole_inventory[changed_slot].name, object.x, object.y + 36, 64, 64, inventory.whole_inventory[changed_slot].image))
								inventory.reduce(changed_slot)
				
			else:

				# Обновление мира
				world.update(player, multiplayer, multiplayer_role, net) #TODO оптимизировать

				# Отображение объектов

				for object in world.visible_objects:

					object.main(player, world, dt, world_to_screen, multiplayer, game_events, Particle)

					if object.get_left_pressed(mouse_x, mouse_y, player):

						if object.name == "Pond":
							if object.special_flags[0] != 0 and inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name == "Bucket":

								inventory.reduce(changed_slot)

								inventory.increate("Water bucket")
								object.special_flags[0] -= 1
			
							if object.special_flags[1] != 0 and inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name == "Stone shovel" and object.get_left_pressed(mouse_x, mouse_y, player) and random.randint(1, 30) == 1:
								rand_x, rand_y = object.x +random.randint(-128, 128), object.y + random.randint(-128, 128)
								world.chunk_manager.get_chunk_at(rand_x, rand_y).items.append(Object("Clay", rand_x, rand_y, "Images/Items/Clay.png", pickable=True))
								object.special_flags[1] -= 1

						mouse_object = object.name

						if object.name == "Pot":

							if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].type == "Flower":
								world.chunk_manager.get_chunk_at(object.x, object.y + 36).items.append(Object(inventory.whole_inventory[changed_slot].name, object.x, object.y + 36, 64, 64, inventory.whole_inventory[changed_slot].image))
								inventory.reduce(changed_slot)

					if object.name == "Dandelion" and time.time() - object.start_time > 1200:

						object.start_time = time.time()
						
						try:
							object.image_path = path + "Images/Objects/Dandelion " + str(int(object.image_path[-5]) + 1) + ".png"
							object.image = load(object.image_path, 64)
						except:
							world.chunk_manager.get_chunk_at(object.x, object.y).objects.remove(object)

						if object.image_path[-5] == "5":

							for _ in range(5):

								if random.randint(1, 5) == 1:
									world.particles.append(Particle(object.x, object.y, load(path + "Images/Items/Dandelion seed.png", 32), random.randint(-30, 30), random.randint(-30, 30), end_time=5, end_command=lambda particle: (world.chunk_manager.get_chunk_at(particle.x, particle.y).items.append(Object("Dandelion", particle.x, particle.y, "Images/Objects/Dandelion 1.png")))))
								else:
									world.particles.append(Particle(object.x, object.y, load(path + "Images/Items/Dandelion seed.png", 32), random.randint(-30, 30), random.randint(-30, 30), end_time=5))

					if object.name == "Punch" and False:

						if object.get_left_pressed(mouse_x, mouse_y, player) and inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name in ("Mushroom", "Red mushroom", "Thread", "Poppy", "Purple tulip", "Orange tulip", "Black tulip", "Red tulip", "Yellow tulip", "Dandelion", "Cotton grass", "Onion"):
							if object.special_flags < 11:
								object.special_flags += 1
								if object.special_flags > 6:
									object.image = load(path + "Images/Objects/Punch " + str(object.special_flags - 5) + ".png")
							else:
								object.special_flags = 1
								world.chunk_manager.get_chunk_at(object.x, object.y).items.append(Object("Punch", object.x, object.y, "Images/Items/Powder.png"))

				if player.breaking_object is None and player.started_break:
					player.started_break = False
					if multiplayer:
						game_events.append({"event_type": "object_stopped_breaking", "x": player.breaking_object_info[0], "y": player.breaking_object_info[1], "name": player.breaking_object_info[2]})
					player.breaking_object_info = None

				# Отображение предметов
				if inventory.whole_inventory[changed_slot] is None:
					last_changed_item = None
				else:
					last_changed_item = inventory.whole_inventory[changed_slot].name

				for item in world.visible_items:
					item.main(player, world, dt, world_to_screen, multiplayer, game_events, Particle)
					try_pick = True
					if item.pickable and Settings["Game"][0] and player.x - 150 < item.x < player.x + 150 and player.y - 150 < item.y < player.y + 150:
						world.particles.append(Particle(item.x, item.y, item.image, lambda particle: round(((player.x - particle.x) // 2) / 10 * 5), lambda particle: round(((player.y - particle.y) // 2) / 10 * 5), track_ticks=True, del_self_condition=lambda particle: abs(particle.x - player.x) < 30 and abs(particle.y - player.y) < 30, end_command=lambda particle: (inventory.increate(item.name), play_sound("Pick an item"))))
						if multiplayer:
							game_events.append({"event_type": "item_removed", "x": item.x, "y": item.y, "name": item.name})

						world.chunk_manager.get_chunk_at(item.x, item.y).items.remove(item)
						try_pick = False

					if try_pick and item.x - player.x + Width // 2 - item.image.get_width() // 2 <= mouse_x <= item.x - player.x + Width // 2 + item.image.get_width() // 2 and player.y - item.y + Height // 2 - item.image.get_height() // 2 <= mouse_y <= player.y - item.y + Height // 2 + item.image.get_height() // 2:
						mouse_object = t("Click to pick the ") + t("Item name " + item.name)
						
						if click[0]:
							world.particles.append(Particle(item.x, item.y, item.image, lambda particle: round(((player.x - particle.x) // 2) / 10 * 5), lambda particle: round(((player.y - particle.y) // 2) / 10 * 5), track_ticks=True, del_self_condition=lambda particle: abs(particle.x - player.x) < 30 and abs(particle.y - player.y) < 30, end_command=lambda particle: (inventory.increate(particle.special_flags), play_sound("Pick an item")), special_flags=item.name))
									
							if multiplayer:
								game_events.append({"event_type": "item_removed", "x": item.x, "y": item.y, "name": item.name})
							world.chunk_manager.get_chunk_at(item.x, item.y).items.remove(item)
						elif item.pickable and click[2] and inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name in ("Blue slime", "Pink slime"):
							item.pickable = False
							inventory.reduce(changed_slot)

		elif len(Backrooms.objects) != 1:

			for object in backrooms_objects:

				object.main()

				if click[0] and object.x - player.x + Width // 2 - object.w // 2 <= mouse_x <= object.x - player.x + Width // 2 + object.w // 2 and player.y - object.y + Height // 2 - object.h // 2 <= mouse_y <= player.y - object.y + Height // 2 + object.h // 2:

					mouse_object = object.name

					if object.name == "Pot":

						if object.get_right_pressed(mouse_x, mouse_y, player) and inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].type == "Flower":
							world.chunk_manager.get_chunk_at(object.x, object.y).items.append(Object(inventory.whole_inventory[changed_slot].name, object.x, object.y + 36, 64, 64, inventory.whole_inventory[changed_slot].image))
							inventory.reduce(changed_slot)

						if not object.x - 60 < object.special_flags[0] < object.x + 60:
							if object.x < object.special_flags[0]:
								object.x += 30
								i = object.image.get_rect()
								key = pygame.transform.rotate(object.image, -10)
								ii = i.copy()
								ii.center = key.get_rect().center
								object.image = key.subsurface(ii).copy()
							else:
								object.x -= 30
								i = object.image.get_rect()
								key = pygame.transform.rotate(object.image, 10)
								ii = i.copy()
								ii.center = key.get_rect().center
								object.image = key.subsurface(ii).copy()

						if not object.y - 60 < object.special_flags[1] < object.y + 60:
							if object.y < object.special_flags[1]:
								object.y += 30
							else:
								object.y -= 30
		
		if not Backrooms.InBackrooms and world.current_cave is None and len(world.mobs) < 5:

			if time_system.day_phase == "Night":
				if random.randint(1, int(dt * 50000000)) == 1:
					world.mobs.append(Spider(player.x + random.randint(-Width, Width), player.y + random.randint(-Height, Height)))
			else:
				if random.randint(1, int(dt * 10000000)) == 1:
					world.mobs.append(Slime(player.x + random.randint(-Width, Width), player.y + random.randint(-Height, Height)))

		for projectile in world.projectiles:
			projectile.main()

		for wall in world.visible_walls.values():
			wall.main(release)
		
		if not Backrooms.InBackrooms and world.current_cave is None:

			# Отображение мобов
			for mob in world.mobs:

				mob.update(player, world, dt)
				mob.draw(player)

				if world.projectiles != []:

					if mob.name == "Slime": mob_rect = pygame.Rect((mob.x, mob.y - 64, 128, 128))
					else: mob_rect = pygame.Rect((mob.x, mob.y - 128, 256, 256))

					if check_projectiles_collision(mob_rect, world):

						mob.HP -= 15

						if mob.name == "Slime":
							temp = mob.animation_frames[int(mob.animation_timer) % 5].copy().convert_alpha()
						if mob.name == "Spider":
							temp = mob.animation_images[mob.direction].copy().convert_alpha()

						for a, b in product(range(128 if mob.name == "Slime" else 256), range(128 if mob.name == "Slime" else 256)):
							if temp.get_at((a, b)).a != 0:
								temp.set_at((a, b), (200, 0, 0, 80))

						world.particles.append(Particle(mob.x + random.randint(-64, 64), mob.y + random.randint(-64, 64), text("-15", 0, 0, (180, 10, 10), max_width=44, max_height=50, return_surface=True), y_bias=3, increased_transparency=30, end_time=0.5))

						if mob.name == "Slime":
							win.blit(temp, (mob.x - player.x + Width // 2 - 64, player.y - mob.y + Height // 2 - 64))
						else:
							win.blit(temp, (mob.x - player.x + Width // 2 - 128, player.y - mob.y + Height // 2 - 128))

						win.blit(text(str(mob.HP), 0, 0, (180, 10, 10), return_surface=True), (mob.x + 58 - player.x + Width // 2 - 64, player.y - mob.y + Height // 2 - 32))

				if mob.HP < 1:

					if mob.name == "Slime":

						for _ in range(random.randint(1, 3)):
							rand_x, rand_y = mob.x + random.randint(-30, 30), mob.y + random.randint(-30, 30)
							world.chunk_manager.get_chunk_at(rand_x, rand_y).items.append(Object("Blue slime" if mob.slime_type == 1 else "Pink slime", rand_x, rand_y, f"Images/Items/{'Blue' if mob.slime_type == 1 else 'Pink'} slime.png", pickable=True))
						world.mobs.remove(mob)

					elif mob.name == "Spider":
						rand_x, rand_y = mob.x + random.randint(-30, 30), mob.y + random.randint(-30, 30)
						world.chunk_manager.get_chunk_at(rand_x, rand_y).items.append(Object("Thread", mob.x + random.randint(-30, 30), mob.y + random.randint(-30, 30), "Images/Items/Thread.png", pickable=True))
						world.mobs.remove(mob)

		# Отрисовка игрока
		
		player.render(win)

		if multiplayer:
			with net.lock:
				peers_copy = dict(net.peers.items())  # Создаем копию
			for pid, peer in peers_copy.items():
				if pid != net.player_id:
					if pid in net.server_events:
						for event in net.server_events[pid]:
							match event["event_type"]:
								case "player_moved":
									peer.x = event["x"]
									peer.y = event["y"]
									peer.direction = event["direction"]
									peer.is_moving = True
								case "player_tp":
									peer.x = event["x"]
									peer.y = event["y"]
									peer.direction = event["direction"]
								case "changed_item":
									peer.changed_item = event["changed_item"]
								case "player_stopped":
									peer.stop()
								case "object_started_breaking":
									peer.breaking_object_info = (event["x"], event["y"], event["name"])
								case "object_stopped_breaking":
									peer.breaking_object_info = None

							net.server_events[pid].remove(event)
					peer.render(win)
					peer.update_animation(dt)
					if peer.breaking_object_info is not None:
						for object in world.visible_objects:
							if (object.x, object.y, object.name) == (*peer.breaking_object_info,):
								object.image = crack_surface(world, Particle, object, (object.max_break - object.breaked) // object.max_break, 8)
								break

		# Анимации Хиро

		if animation[0] is None:
			
			if random.randint(1, 300) == 1:
				animation = ["Close eyes", 0, 16]

		elif animation[1] <= animation[2]:
			animation[1] += 1
		else:
			animation = [None, 0]

		changed_item_x = 0
		changed_item_y = 0

		match player.direction:

			case "Down":

				match player.costum:
					# 97, 209
					case 0 | 1 | 3 | 4 | 6 | 7:

						changed_item_x = Width // 2 - 80
						changed_item_y = Height // 2

						match animation[0]:

							case "Close eyes":

								if animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 32, 8, animation[1] * 2))
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 32, 8, animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 32, 8, (8 - animation[1] + 8) * 2))
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 32, 8, (8 - animation[1] + 8) * 2))

						match player.costum:

							case 1 | 3:
								
								a = pygame.Surface((16, 24))
								a.fill((0, 0, 0))
								a.set_alpha(90)
								world.particles.append(Particle(player.x + 16, player.y + 96, a, end_time=3))

							case 4 | 6:

								a = pygame.Surface((16, 24))
								a.fill((0, 0, 0))
								a.set_alpha(90)
								world.particles.append(Particle(player.x - 32, player.y + 96, a, end_time=3))

					case 2:

						changed_item_x = Width // 2 - 74
						changed_item_y = Height // 2 - 16

						match animation[0]:

							case "Close eyes":

								if animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, animation[1] * 2))
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, (8 - animation[1] + 8) * 2))
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, (8 - animation[1] + 8) * 2))

					case 5:

						changed_item_x = Width // 2 - 94
						changed_item_y = Height // 2 - 16

						match animation[0]:

							case "Close eyes":

								if animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, animation[1] * 2))
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, (8 - animation[1] + 8) * 2))
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, (8 - animation[1] + 8) * 2))

			case "Left":

				match player.costum:

					case 0 | 1 | 3 | 4 | 6 | 7:

						changed_item_x = Width // 2 - 84
						changed_item_y = Height // 2 - 16

						match animation[0]:

							case "Close eyes":

								if animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 32, 8, animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 32, 8, (8 - animation[1] + 8) * 2))

					case 2:

						changed_item_x = Width // 2 - 104
						changed_item_y = Height // 2

						match animation[0]:

							case "Close eyes":

								if animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, (8 - animation[1] + 8) * 2))

					case 5:

						changed_item_x = Width // 2 - 70
						changed_item_y = Height // 2

						match animation[0]:

							case "Close eyes":

								if animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, (8 - animation[1] + 8) * 2))

			case "Right":

				match player.costum:

					case 0 | 1 | 3 | 4:

						changed_item_x = Width // 2 - 20
						changed_item_y = Height // 2

						match animation[0]:

							case "Close eyes":

								if animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 32, 8, animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 32, 8, (8 - animation[1] + 8) * 2))

					case 2:

						changed_item_x = Width // 2 - 32
						changed_item_y = Height // 2

						match animation[0]:

							case "Close eyes":

								if animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, (8 - animation[1] + 8) * 2))

					case 5 | 6 | 7:

						changed_item_x = Width // 2 - 16
						changed_item_y = Height // 2 + 16

						match animation[0]:

							case "Close eyes":

								if animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, (8 - animation[1] + 8) * 2))

		if inventory.whole_inventory[changed_slot] is not None and player.direction != "Up" and not (changed_item_x == changed_item_y == 0):
			win.blit(inventory.whole_inventory[changed_slot].image, (changed_item_x, changed_item_y))

		# Рон
		old_ron_pos = ron.x, ron.y
		ron.update(world, dt, not multiplayer or multiplayer_role == "Host")
		if multiplayer and multiplayer_role == "Host" and old_ron_pos != (ron.x, ron.y):
			game_events.append({"event_type": "ron_moved", "x": ron.x, "y": ron.y, "direction": ron.direction})

		# Механика использования еды и некоторых предметов через пробел

		for i in range(Settings["Display"][2]):
			win.blit(pygame.transform.scale(win, (Width - i * 2, Height - i * 2)), (i, i))

		if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name in ("Gun", "Bow") and Settings["Game"][1]:
			win.blit(Inventory_slot, (Width - 370, Height - 74))
			win.blit(inventory.whole_inventory[changed_slot].image, (Width - 370, Height - 74))
		
		if (inventory.whole_inventory[changed_slot] is not None and (use_item_pressed or (click[0] and Settings["Game"][1]))) and not chat_open:

			match inventory.whole_inventory[changed_slot].name:

				case "Gun":

					for item_index, slot in enumerate(inventory.whole_inventory):
						if slot is not None and slot.name == "Bullet":
							inventory.reduce(item_index)
							world.projectiles.append(Projectile(player.x, player.y, mouse_x, mouse_y, "Bullet"))
							if multiplayer:
								game_events.append({"event_type": "projectile_added", "x": player.x, "y": player.y, "mouse_x": mouse_x, "mouse_y": mouse_y, "projectile_type": "Bullet"})
							bullet_num += 1
							break
					else:
						text(t("You don't have bullets to shoot"), Width // 2, Height // 2, (200, 30, 30), alignment=True)

				case "Bow":

					for item_index, slot in enumerate(inventory.whole_inventory):
						if slot is not None and slot.name == "Arrow":
							inventory.reduce(item_index)
							world.projectiles.append(Projectile(player.x, player.y, mouse_x, mouse_y, "Arrow"))
							if multiplayer:
								game_events.append({"event_type": "projectile_added", "x": player.x, "y": player.y, "mouse_x": mouse_x, "mouse_y": mouse_y, "projectile_type": "Arrow"})
							bullet_num += 1
							break
					else:
						text(t("You don't have arrows to shoot"), Width // 2, Height // 2, (200, 30, 30), alignment=True)

				case "Beer":

					player.effects.append(["Drunk", 180])
					inventory.reduce(changed_slot)

				case "Grenade":

					world.projectiles.append(ExplodingProjectile(player.x, player.y, mouse_x, mouse_y, "Grenade", (player.x + mouse_x - Width // 2, player.y - mouse_y + Height // 2)))

					inventory.reduce(changed_slot)
						
			if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].type == "Food":
				
				player.HP += inventory.whole_inventory[changed_slot].special_info
				inventory.reduce(changed_slot)
				
		

		if keys[hot_keys["Screenshot"]] and keys[hot_keys["Show keys"]]:
			
			pygame.image.save(win, str(Path.home()) + "/Your Screenshot " + time.asctime().replace(":", " ") + ".png")
			chat_message(t("Game: Your screenshot is in ") + str(Path.home()) + "/Your Screenshot " + time.asctime().replace(":", " ") + ".png")
			
			for _ in range(3):
				win.fill((200, 255, 200))
				clock.tick(MAX_FPS)
				pygame.display.update()
			time.sleep(0.1)

		# Отрисовка погоды
		
		if random.randint(1, 18000) == 1: game.weather = random.choice(("Clear", "Rain"))

		match game.weather:
			
			case "Rain":
				offset = random.randint(-10, 10)
				for _ in range(15):
					world.particles.append(Particle(random.randint(1, Width), -50, drop_texture,  x_bias=random.randint(-5, 5) + offset, y_bias=random.randint(30, 40), display_mode=lambda X, Y, w, h: (X, Y), end_y=Height, end_zone=30))

		# Отображение частиц

		for particle in world.particles:

			particle.main(dt, world)
			
			if (particle.end_time is not None and time.time() - particle.start_time >= particle.end_time) or (particle.del_self_condition is not None and particle.del_self_condition(particle)):
				if particle.end_command is not None:
					particle.end_command(particle)

				world.particles.remove(particle)

		for particle in new_particles:
			world.particles.append(particle)

		new_particles.clear()

		# Механика освещения

		# 1 слой - естественный свет
		if world.current_cave is None:
			current_brightness = time_system.get_brightness()
			light_level = max((1 - current_brightness) * 200, 0)
		else:
			light_level = 180

		game.shadow_surface = pygame.Surface((Width, Height), pygame.SRCALPHA)
		try:
			game.shadow_surface.fill((0, 0, 0, light_level))
		except:pass
		# 2 слой - тени
		# 3 слой - искусственное освещение
		world.chunk_manager.show_light_and_dark(light_level, player, game.shadow_surface) #TODO оптимизировать
		if player.hovered_object is not None:
			draw_select_image_arbitrarily(player.hovered_object.x, player.hovered_object.y, player.hovered_object.w, player.hovered_object.h, world_to_screen, world_rect_to_screen)
			mouse_object = player.hovered_object.name


		# Механика анимации слотов
		if Settings["Display"][5]:
			for yy, xx in product(range(0, 3), range(0, 10)):
				
				cell_x = 10 + xx * 80
				cell_y = 10 + yy * 80
			
				if cell_x <= mouse_x <= cell_x + 64 and cell_y <= mouse_y <= cell_y + 64:
					if slot_animations[yy * 10 + xx][0]:
						if slot_animations[yy * 10 + xx][1] < dt * 150:
							slot_animations[yy * 10 + xx][1] += 1
							slot_animations[yy * 10 + xx][2] -= 3
							slot_animations[yy * 10 + xx][2] = abs(slot_animations[yy * 10 + xx][2])
					else:
						slot_animations[yy * 10 + xx] = [True, 0, 10]
					
				elif slot_animations[yy * 10 + xx][0]:
					slot_animations[yy * 10 + xx][0] = False
					slot_animations[yy * 10 + xx][1] = 0
				elif slot_animations[yy * 10 + xx][1] < dt * 250:
					slot_animations[yy * 10 + xx][1] += 1	

		# Меню на клавише TAB

		if keys[hot_keys["TAB menu"]] and not chat_open:

			radius = 0	 # Расстояние, на котором кнопки находятся относительно центра экрана
			display_speed = 7	# Скорость отдаления кнопок от центра экрана
			a = True
			b = False 
			time_on_button = 0	 # Время, которое прошло спустя тот момент, когда пользователь навёл курсором мыши на одну из кнопок
			win_copy = win.copy()
			while True:
				
				if b:

					display_speed += 4
					radius -= display_speed
					if display_speed > 45:
						break

				else:

					if radius < 200:
						display_speed += 4
						radius += display_speed

					elif radius < 270 and a:
						display_speed -= 5
						radius += display_speed

					elif 270 < radius < 300:
						radius -= display_speed // 3
						a = False

				mouse_x, mouse_y = pygame.mouse.get_pos()
				click = pygame.mouse.get_pressed()
				release = False

				for event in pygame.event.get():

					if event.type == pygame.QUIT:
						save()
						sys.exit()

					if event.type == pygame.MOUSEBUTTONUP:
						release = True

					if event.type == pygame.KEYUP:
						if event.key == hot_keys["Close"]:
							b = True
							display_speed = 7

				win.blit(win_copy, (0, 0))
				
				# Дальше идёт отображение всех кнопок по супер сложной формуле, я уже сам хз как это работает
					
				if Width // 2 + radius - 32 < mouse_x < Width // 2 + radius + 32 and Height // 2 - 32 < mouse_y < Height // 2 + 32:
					if special_slot_animations["Craft list slot"][0]:
						if special_slot_animations["Craft list slot"][1] < FPS / 6:
							special_slot_animations["Craft list slot"][1] += 1
							special_slot_animations["Craft list slot"][2] -= 3
							special_slot_animations["Craft list slot"][2] = abs(special_slot_animations["Craft list slot"][2])
					else:
						special_slot_animations["Craft list slot"] = [True, 0, 10]
					
					if release:
						inventory_open = True
						craft_list_open = True
						b = True
						display_speed = 7
					
				elif special_slot_animations["Craft list slot"][0]:
					special_slot_animations["Craft list slot"][0] = False
					special_slot_animations["Craft list slot"][1] = 0
				elif special_slot_animations["Craft list slot"][1] < FPS / 4:
					special_slot_animations["Craft list slot"][1] += 1	 
				if special_slot_animations["Craft list slot"][0] and Settings["Display"][5]:
					try:win.blit(pygame.transform.scale(Craft_list_slot2, (64 - special_slot_animations["Craft list slot"][2], 64 - special_slot_animations["Craft list slot"][2])), (Width // 2 + radius - 32, Height // 2 - 32))
					except: win.blit(Craft_list_slot2, (Width // 2 + radius - 32, Height // 2 - 32))
				
				else:
					win.blit(Craft_list_slot1, (Width // 2 + radius - 32, Height // 2 - 32))

				text(t("Craft list"), Width // 2 + radius, Height // 2 + 40, alignment=True)
				


				if Width // 2 + math.cos((2 * math.pi) / 6) * radius - 32 < mouse_x < Width // 2 + math.cos((2 * math.pi) / 6) * radius + 32 and Height // 2 + math.sin((2 * math.pi) / 6) * radius - 32 < mouse_y < Height // 2 + math.sin((2 * math.pi) / 6) * radius + 32:
					if special_slot_animations["Game menu slot"][0]:
						if special_slot_animations["Game menu slot"][1] < FPS / 6:
							special_slot_animations["Game menu slot"][1] += 1
							special_slot_animations["Game menu slot"][2] -= 3
							special_slot_animations["Game menu slot"][2] = abs(special_slot_animations["Game menu slot"][2])
					else:
						special_slot_animations["Game menu slot"] = [True, 0, 10]
					
					if click[0]:
						save(False)
						if multiplayer:
							net.disconnect()
						menu()
					
				elif special_slot_animations["Game menu slot"][0]:
					special_slot_animations["Game menu slot"][0] = False
					special_slot_animations["Game menu slot"][1] = 0
				elif special_slot_animations["Game menu slot"][1] < FPS / 4:
					special_slot_animations["Game menu slot"][1] += 1

				if special_slot_animations["Game menu slot"][0] and Settings["Display"][5]:
					try:win.blit(pygame.transform.scale(Game_menu_slot2, (64 - special_slot_animations["Game menu slot"][2], 64 - special_slot_animations["Game menu slot"][2])), (Width // 2 + math.cos((2 * math.pi) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi) / 6) * radius - 32))
					except: win.blit(Game_menu_slot2, (Width // 2 + math.cos((2 * math.pi) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi) / 6) * radius - 32))
				
				else:
					win.blit(Game_menu_slot1, (Width // 2 + math.cos((2 * math.pi) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi) / 6) * radius - 32))

				text(t("Game menu"), Width // 2 + math.cos((2 * math.pi) / 6) * radius, Height // 2 + math.sin((2 * math.pi) / 6) * radius + 40, alignment=True)
				

				
				if Width // 2 + math.cos((2 * math.pi * 2) / 6) * radius - 32 < mouse_x < Width // 2 + math.cos((2 * math.pi * 2) / 6) * radius + 32 and Height // 2 + math.sin((2 * math.pi * 2) / 6) * radius - 32 < mouse_y < Height // 2 + math.sin((2 * math.pi * 2) / 6) * radius + 32:
					if special_slot_animations["Menu slot"][0]:
						if special_slot_animations["Menu slot"][1] < FPS / 6:
							special_slot_animations["Menu slot"][1] += 1
							special_slot_animations["Menu slot"][2] -= 3
							special_slot_animations["Menu slot"][2] = abs(special_slot_animations["Menu slot"][2])
					else:
						special_slot_animations["Menu slot"] = [True, 0, 10]
					
					if click[0]:
						multiplayer_menu_open = True
						b = True
						display_speed = 7

				elif special_slot_animations["Menu slot"][0]:
					special_slot_animations["Menu slot"][0] = False
					special_slot_animations["Menu slot"][1] = 0
				elif special_slot_animations["Menu slot"][1] < FPS / 4:
					special_slot_animations["Menu slot"][1] += 1   

				if special_slot_animations["Menu slot"][0] and Settings["Display"][5]:
					try:win.blit(pygame.transform.scale(Menu_slot2, (64 - special_slot_animations["Menu slot"][2], 64 - special_slot_animations["Menu slot"][2])), (Width // 2 + math.cos((2 * math.pi * 2) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi) / 6) * radius - 32))
					except: win.blit(Menu_slot2, (Width // 2 + math.cos((2 * math.pi * 2) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 2) / 6) * radius - 32))
				
				else:
					win.blit(Menu_slot1, (Width // 2 + math.cos((2 * math.pi * 2) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 2) / 6) * radius - 32))

				text(t("Extra info menu"), Width // 2 + math.cos((2 * math.pi * 2) / 6) * radius, Height // 2 + math.sin((2 * math.pi * 2) / 6) * radius + 40, alignment=True)
				


				if Width // 2 + math.cos((2 * math.pi * 3) / 6) * radius - 32 < mouse_x < Width // 2 + math.cos((2 * math.pi * 3) / 6) * radius + 32 and Height // 2 + math.sin((2 * math.pi * 3) / 6) * radius - 32 < mouse_y < Height // 2 + math.sin((2 * math.pi * 3) / 6) * radius + 32:
					if special_slot_animations["Multiplayer slot"][0]:
						if special_slot_animations["Multiplayer slot"][1] < FPS / 6:
							special_slot_animations["Multiplayer slot"][1] += 1
							special_slot_animations["Multiplayer slot"][2] -= 3
							special_slot_animations["Multiplayer slot"][2] = abs(special_slot_animations["Multiplayer slot"][2])
					else:
						special_slot_animations["Multiplayer slot"] = [True, 0, 10]
					
					if click[0]:
						multiplayer_menu_open = True
						b = True
						display_speed = 7

				elif special_slot_animations["Multiplayer slot"][0]:
					special_slot_animations["Multiplayer slot"][0] = False
					special_slot_animations["Multiplayer slot"][1] = 0
				elif special_slot_animations["Multiplayer slot"][1] < FPS / 4:
					special_slot_animations["Multiplayer slot"][1] += 1   

				if special_slot_animations["Multiplayer slot"][0] and Settings["Display"][5]:
					try:win.blit(pygame.transform.scale(Multiplayer_slot2, (64 - special_slot_animations["Multiplayer slot"][2], 64 - special_slot_animations["Multiplayer slot"][2])), (Width // 2 + math.cos((2 * math.pi * 3) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 3) / 6) * radius - 32))
					except: win.blit(Multiplayer_slot2, (Width // 2 + math.cos((2 * math.pi * 3) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 3) / 6) * radius - 32))
				
				else:
					win.blit(Multiplayer_slot1, (Width // 2 + math.cos((2 * math.pi * 3) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 3) / 6) * radius - 32))

				text(t("Multiplayer menu"), Width // 2 + math.cos((2 * math.pi * 3) / 6) * radius, Height // 2 + math.sin((2 * math.pi * 3) / 6) * radius + 40, alignment=True)
				

				
				if Width // 2 + math.cos((2 * math.pi * 4) / 6) * radius - 32 < mouse_x < Width // 2 + math.cos((2 * math.pi * 4) / 6) * radius + 32 and Height // 2 + math.sin((2 * math.pi * 4) / 6) * radius - 32 < mouse_y < Height // 2 + math.sin((2 * math.pi * 4) / 6) * radius + 32:
					if special_slot_animations["Close slot"][0]:
						if special_slot_animations["Close slot"][1] < FPS / 6:
							special_slot_animations["Close slot"][1] += 1
							special_slot_animations["Close slot"][2] -= 3
							special_slot_animations["Close slot"][2] = abs(special_slot_animations["Close slot"][2])
					else:
						special_slot_animations["Close slot"] = [True, 0, 10]
					
					if click[0]:
						b = True
						display_speed = 7

				elif special_slot_animations["Close slot"][0]:
					special_slot_animations["Close slot"][0] = False
					special_slot_animations["Close slot"][1] = 0
				elif special_slot_animations["Close slot"][1] < FPS / 4:
					special_slot_animations["Close slot"][1] += 1	

				if special_slot_animations["Close slot"][0] and Settings["Display"][5]:
					try:win.blit(pygame.transform.scale(Close_slot2, (64 - special_slot_animations["Close slot"][2], 64 - special_slot_animations["Close slot"][2])), (Width // 2 + math.cos((2 * math.pi * 4) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 4) / 6) * radius - 32))
					except: win.blit(Close_slot2, (Width // 2 + math.cos((2 * math.pi * 4) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 4) / 6) * radius - 32))
				
				else:
					win.blit(Close_slot1, (Width // 2 + math.cos((2 * math.pi * 4) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 4) / 6) * radius - 32))

				text(t("Close"), Width // 2 + math.cos((2 * math.pi * 4) / 6) * radius, Height // 2 + math.sin((2 * math.pi * 4) / 6) * radius + 40, alignment=True)



				if Width // 2 + math.cos((2 * math.pi * 5) / 6) * radius - 32 < mouse_x < Width // 2 + math.cos((2 * math.pi * 5) / 6) * radius + 32 and Height // 2 + math.sin((2 * math.pi * 5) / 6) * radius - 32 < mouse_y < Height // 2 + math.sin((2 * math.pi * 5) / 6) * radius + 32:
					if special_slot_animations["Reference slot"][0]:
						if special_slot_animations["Reference slot"][1] < FPS / 6:
							special_slot_animations["Reference slot"][1] += 1
							special_slot_animations["Reference slot"][2] -= 3
							special_slot_animations["Reference slot"][2] = abs(special_slot_animations["Reference slot"][2])
					else:
						special_slot_animations["Reference slot"] = [True, 0, 10]
					
					if click[0]:
						save(False)
						settings()

				elif special_slot_animations["Reference slot"][0]:
					special_slot_animations["Reference slot"][0] = False
					special_slot_animations["Reference slot"][1] = 0
				elif special_slot_animations["Reference slot"][1] < FPS / 4:
					special_slot_animations["Reference slot"][1] += 1	

				if special_slot_animations["Reference slot"][0] and Settings["Display"][5]:
					try:win.blit(pygame.transform.scale(Reference_slot2, (64 - special_slot_animations["Reference slot"][2], 64 - special_slot_animations["Reference slot"][2])), (Width // 2 + math.cos((2 * math.pi * 5) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 4) / 6) * radius - 32))
					except: win.blit(Reference_slot2, (Width // 2 + math.cos((2 * math.pi * 5) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 5) / 6) * radius - 32))
				
				else:
					win.blit(Reference_slot1, (Width // 2 + math.cos((2 * math.pi * 5) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 5) / 6) * radius - 32))

				text(t("Reference"), Width // 2 + math.cos((2 * math.pi * 5) / 6) * radius, Height // 2 + math.sin((2 * math.pi * 5) / 6) * radius + 40, alignment=True)

				pygame.display.update()
				clock.tick(MAX_FPS)

		if Settings["Game"][1]:

			up_b.main()
			left_b.main()
			down_b.main()
			right_b.main()
			if inventory_open:
				win.blit(load(path + "Images/Slots/Open inventory slot.png", 64), (890, 10))
				if 890 <= mouse_x <= 954 and 10 <= mouse_y <= 74 and click[0]:
					inventory_open = False
			else:
				win.blit(load(path + "Images/Slots/Open inventory slot.png", 64), (810, 10))
				if 810 <= mouse_x <= 874 and 10 <= mouse_y <= 74 and click[0]:
					inventory_open = True
		
		if player.HP_animation_tick > 0 and not player.god_mode:
			
			player.HP_animation_tick += 1
			
			if player.HP_animation_tick < 6:
				win_fill((200, 0, 0), player.HP_animation_tick * 20)
				win.blit(pygame.transform.scale(win, (Width + player.HP_animation_tick * 2, Height + player.HP_animation_tick * 2)), (-player.HP_animation_tick, -player.HP_animation_tick))
			else:
				win_fill((200, 0, 0), (player.HP_animation_tick - 10 - player.HP_animation_tick - 10) * 20)

			if player.HP_animation_tick == 21:
				player.HP_animation_tick = 0

		# Отображение инвентаря
		if inventory_open:

			if 10 < mouse_x < 794 and 10 < mouse_y < 314:
				mouse_object = t("Inventory (I)")

			slot_x = 10
			slot_y = 10

			for slot in range(30):
				
				if slot == changed_slot: win.blit(Changed_inventory_slot, (slot_x, slot_y))
				else:
					
					if slot_animations[slot][0]:
						try:win.blit(pygame.transform.scale(Inventory_slot, (64 - slot_animations[slot][2], 64 - slot_animations[slot][2])), (slot_x, slot_y))
						except: win.blit(pygame.transform.scale(Inventory_slot, (64, 64)), (slot_x, slot_y))

					else:
						win.blit(pygame.transform.scale(Inventory_slot, (64, 64)), (slot_x, slot_y))
						
				slot_x += 80
				if slot_x == 810:
					slot_x = 10
					slot_y += 80
			
			win.blit(Object_inventory_slot, (10, 250))
			
			# TODO перенести это в функцию main у объекта
			min_dist = 512
			need_object = None
			for object in world.visible_objects:
				if object.name in ("Table", "Wall table", "Furnace"):
					distance = math.dist((player.x, player.y), (object.x, object.y))
					if distance < min_dist:
						need_object = object.name
						min_dist = distance

			if need_object is not None:
				win.blit(inventory.resources[need_object].image, (10, 250))

			win.blit(Tool_inventory_slot, (90, 250))

			item_to_get = inventory.check_recipies(need_object, craft_items_list, craft_amounts_list)
			
			if item_to_get is not None:

				win.blit(Changed_inventory_slot, (730, 250))
				win.blit(inventory.resources[item_to_get[0]].image, (730, 250))

				if item_to_get[2] is not None:
					win.blit(inventory.resources[item_to_get[2]].image, (10, 250))
				if item_to_get[3] is not None:
					win.blit(inventory.resources[item_to_get[3]].image, (90, 250))
				if 730 <= mouse_x <= 810 and 250 <= mouse_y <= 330 and release:
					inventory.increate(item_to_get[0], item_to_get[1])
					craft_items_list = [None] * 7
					craft_amounts_list = [None] * 7
					craft_images_list = [None] * 7
			
			# Разделение предметов
			if 810 <= mouse_x <= 874 and 10 <= mouse_y <= 74:
				if special_slot_animations["Split items slot"][0]:
					if special_slot_animations["Split items slot"][1] < FPS / 6:
						special_slot_animations["Split items slot"][1] += 1
						special_slot_animations["Split items slot"][2] -= 3
						special_slot_animations["Split items slot"][2] = abs(special_slot_animations["Split items slot"][2])
				else:
					special_slot_animations["Split items slot"] = [True, 0, 10]
				
				if release:
					inventory.Split_items = not inventory.Split_items
				
			elif special_slot_animations["Split items slot"][0]:
				special_slot_animations["Split items slot"][0] = False
				special_slot_animations["Split items slot"][1] = 0
			elif special_slot_animations["Split items slot"][1] < FPS / 4:
				special_slot_animations["Split items slot"][1] += 1   

			if special_slot_animations["Split items slot"][0] or inventory.Split_items:
				try:
					if Settings["Display"][5]: win.blit(pygame.transform.scale(Split_items2, (64 - special_slot_animations["Split items slot"][2], 64 - special_slot_animations["Split items slot"][2])), (810, 10))
					else: win.blit(pygame.transform.scale(Split_items2, (64, 64)), (810, 10))
				except: win.blit(pygame.transform.scale(Split_items2, (64, 64)), (810, 10))
				mouse_object = t("Split items")
			
			else:
				win.blit(pygame.transform.scale(Split_items1, (64, 64)), (810, 10))
			
			# Сжатие инвентаря
			
			if 810 <= mouse_x <= 874 and 170 <= mouse_y <= 234:
				if special_slot_animations["Compact inventory slot"][0]:
					if special_slot_animations["Compact inventory slot"][1] < FPS / 6:
						special_slot_animations["Compact inventory slot"][1] += 1
						special_slot_animations["Compact inventory slot"][2] -= 3
						special_slot_animations["Compact inventory slot"][2] = abs(special_slot_animations["Compact inventory slot"][2])
				else:
					special_slot_animations["Compact inventory slot"] = [True, 0, 10]
				
				if release:
					inventory.compact_inventory()
				
			elif special_slot_animations["Compact inventory slot"][0]:
				special_slot_animations["Compact inventory slot"][0] = False
				special_slot_animations["Compact inventory slot"][1] = 0
			elif special_slot_animations["Compact inventory slot"][1] < FPS / 4:
				special_slot_animations["Compact inventory slot"][1] += 1	

			if special_slot_animations["Compact inventory slot"][0]:
				try:
					if Settings["Display"][5]: win.blit(pygame.transform.scale(Compact_inventory2, (64 - special_slot_animations["Compact inventory slot"][2], 64 - special_slot_animations["Compact inventory slot"][2])), (810, 170))
					else: win.blit(pygame.transform.scale(Compact_inventory2, (64, 64)), (810, 170))
				except: win.blit(pygame.transform.scale(Compact_inventory2, (64, 64)), (810, 170))
				mouse_object = t("Compact inventory")
			
			else:
				win.blit(pygame.transform.scale(Compact_inventory1, (64, 64)), (810, 170))

			inventory.draw_whole(craft_images_list, craft_amounts_list, Inventory_slot)
			
			if craft_list_open:

				win.blit(Changed_craft_list_inventory_slot, (810, 90))
				win_fill(rect=(970, 0, Width - 970, Height))
					
				for cell_y, recipe in enumerate(inventory.recipes):
					cell_y += 1
					cell_x = -1
					for ii in recipe.ingredients:
						if ii is None:
							break
						else:
							cell_x += 1
							win.blit(Inventory_slot, (970 + cell_x * 80, 10 + craft_list_offset + cell_y * 80))
							win.blit(inventory.resources[ii].image, (970 + cell_x * 80, 10 + craft_list_offset + cell_y * 80))
							win.blit(textInfo.render(str(recipe.ingredients_amounts[cell_x]), True, (0, 150, 0)), (980 + cell_x * 80, 52 + craft_list_offset + cell_y * 80))
					if recipe.need_object is not None:
						cell_x = 8
						win.blit(Changed_inventory_slot, (990 + cell_x * 80, 10 + craft_list_offset + cell_y * 80))
						win.blit(inventory.resources[recipe.need_object].image, (990 + cell_x * 80, 10 + craft_list_offset + cell_y * 80))
					if recipe.need_tool is not None:
						cell_x = 9
						win.blit(Changed_inventory_slot, (990 + cell_x * 80, 10 + craft_list_offset + cell_y * 80))
						win.blit(inventory.resources[recipe.need_tool].image, (990 + cell_x * 80, 10 + craft_list_offset + cell_y * 80))
					cell_x = 10
					win.blit(Changed_inventory_slot, (990 + cell_x * 80, 10 + craft_list_offset + cell_y * 80))
					win.blit(inventory.resources[recipe.result].image, (990 + cell_x * 80, 10 + craft_list_offset + cell_y * 80))
					win.blit(textInfo.render(str(recipe.result_amount), True, (0, 150, 0)), (1000 + cell_x * 80, 52 + craft_list_offset + cell_y * 80))

				if 810 <= mouse_x <= 874 and 90 <= mouse_y <= 154 and release:
					craft_list_open = False
						
			else:
				
				if 810 <= mouse_x <= 874 and 90 <= mouse_y <= 154:
					if special_slot_animations["Craft list slot"][0]:
						if special_slot_animations["Craft list slot"][1] < FPS / 6:
							special_slot_animations["Craft list slot"][1] += 1
							special_slot_animations["Craft list slot"][2] -= 3
							special_slot_animations["Craft list slot"][2] = abs(special_slot_animations["Craft list slot"][2])
					else:
						special_slot_animations["Craft list slot"] = [True, 0, 10]
					
					if release:
						craft_list_open = True
					
				elif special_slot_animations["Craft list slot"][0]:
					special_slot_animations["Craft list slot"][0] = False
					special_slot_animations["Craft list slot"][1] = 0
				elif special_slot_animations["Craft list slot"][1] < FPS / 4:
					special_slot_animations["Craft list slot"][1] += 1	 

				if special_slot_animations["Craft list slot"][0] and Settings["Display"][5]:
					try:win.blit(pygame.transform.scale(Changed_craft_list_inventory_slot, (64 - special_slot_animations["Craft list slot"][2], 64 - special_slot_animations["Craft list slot"][2])), (810, 90))
					except: win.blit(pygame.transform.scale(Changed_craft_list_inventory_slot, (64, 64)), (810, 90))
					mouse_object = t("Craft list")
			
				else:
					win.blit(pygame.transform.scale(Craft_list_inventory_slot, (64, 64)), (810, 90))

			if alt_pressed:
				draw_key(" I ", 42, 344)

			if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name == "Wrench":

				if 900 <= mouse_x <= 964 and 10 <= mouse_y <= 74:
					win.blit(Changed_inventory_slot, (900, 10))
					if release: item_settings_open = True
				else:
					win.blit(Inventory_slot, (900, 10))
		else:
			
			if 10 < mouse_x < 794 and 10 < mouse_y < 74:
				mouse_object = t("Inventory (I)")

			for slot_x in range(10):
				if slot_x == changed_slot: win.blit(Changed_inventory_slot, (slot_x * 80 + 10, 10))
				else: win.blit(Inventory_slot, (slot_x * 80 + 10, 10))

			inventory.draw_panel()
			
			if alt_pressed:
				draw_key(" I ", 42, 104)

		# Отображение полосы здоровья

		if not player.god_mode:
			
			for heart_x in range(player.HP // 10):
				win.blit(Heart, (Width - 50 - heart_x * 40, 10))

			if Width - 10 - player.HP // 10 * 40 < mouse_x < Width - 10 and 40 < mouse_y < 104:
				mouse_object = t("Health bar")

			player.HP_TICK += 1
			if player.HP_TICK == 300:
				player.HP_TICK = 0
				if player.HP < 100:
					player.HP += 10

			if player.HP > 100:
				player.HP = 100

			if player.HP < 1:
				for item in inventory.whole_inventory:
					if item is not None:
						for _ in range(item.amount):
							rand_x, rand_y = player.x + random.randint(-300, 300), player.y + random.randint(-300, 300)
							world.chunk_manager.get_chunk_at(rand_x, rand_y).items.append(Object(item.name, rand_x, rand_y, item.image_path, add_path=False, pickable=True))
				inventory.whole_inventory = [None] * 30
				player.HP = 100
				player.x = 0
				player.y = 0

		for effect_y, effect in enumerate(player.effects):

			win.blit(textInfo.render(effect[0], True, text_color, (0, 0, 0, 0.5)), (Width - 30 - textInfo.size(effect[0])[0], effect_y * 60 + 100))
			win.blit(textInfo.render(str(int(effect[1])), True, text_color, (0, 0, 0, 0.5)), (Width - 30 - textInfo.size(str(int(effect[1])))[0], effect_y * 60 + 130))

			match effect[0]:
				case "Drunk":
					d = pygame.Surface((Width, Height))
					d.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
					d.set_alpha(90)
					win.blit(d, (0, 0))

					for _ in range(10000):
						win.set_at((random.randint(0, Width), random.randint(0, Height)), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
						
					win.blit(win, (random.randint(-10, 10), random.randint(-10, 10)))

			effect[1] -= dt
			if effect[1] <= 0:
				player.effects.remove(effect)
		
		if item_settings_open:

			if inventory.whole_inventory[changed_slot].name == "Wrench":

				win_fill()

				pygame.draw.rect(win, text_color, (100, 100, Width - 200, Height - 200))
				pygame.draw.rect(win, (0, 150, 0), (100, 100, Width - 200, Height - 200), 10)
				win.blit(pygame.transform.scale2x(inventory.whole_inventory[changed_slot].image), (Width // 2 - 64, 130))
				pygame.draw.line(win, (0, 150, 0), (150, 308), (Width - 150, 308), 10)
				win.blit(textInfo.render(t("Only wire"), True, (0, 150, 0)), (130, 348))
				win.blit(textInfo.render(t("All mechanisms"), True, (0, 150, 0)), (Width // 2 - textInfo.size(t("All mechanisms"))[0] // 2, 348))
				win.blit(textInfo.render(t("All mechanisms except wire"), True, (0, 150, 0)), (Width - 150 - textInfo.size(t("All mechanisms except wire"))[0], 378))

				if inventory.whole_inventory[changed_slot].settings == ["Only wire"]:
					pygame.draw.rect(win, (0, 150, 0), (120, 278, 60, 60), 30)
					pygame.draw.circle(win, (0, 150, 0), (Width // 2, 308), 30)
					pygame.draw.circle(win, (0, 150, 0), (Width - 150, 308), 30)
				if inventory.whole_inventory[changed_slot].settings == []:
					pygame.draw.circle(win, (0, 150, 0), (150, 308), 30)
					pygame.draw.rect(win, (0, 150, 0), (Width // 2 - 30, 278, 60, 60), 30)
					pygame.draw.circle(win, (0, 150, 0), (Width - 150, 308), 30)
				if inventory.whole_inventory[changed_slot].settings == ["All mechanisms, but wire"]:
					pygame.draw.circle(win, (0, 150, 0), (150, 308), 30)
					pygame.draw.circle(win, (0, 150, 0), (Width // 2, 308), 30)
					pygame.draw.rect(win, (0, 150, 0), (Width - 180, 278, 60, 60), 30)

				if 120 <= mouse_x <= 180 and 278 <= mouse_y <= 338 and release:
					inventory.whole_inventory[changed_slot].settings = ["Only wire"]
				if Width // 2 - 30 <= mouse_x <= Width // 2 + 30 and 278 <= mouse_y <= 338 and release:
					inventory.whole_inventory[changed_slot].settings = []
				if Width - 180 <= mouse_x <= Width - 120 and 278 <= mouse_y <= 338 and release:
					inventory.whole_inventory[changed_slot].settings = ["All mechanisms, but wire"]
					
				
				win.blit(bigTextInfo.render("x", True, (0, 150, 0)), (Width - 160, 130))
				
				if alt_pressed:
					draw_key("ESC", Width - 160, 170)
					
				if Width - 160 <= mouse_x <= Width - 130 and 130 <= mouse_y <= 160:
					win.blit(bigTextInfo.render("x", True, (0, 100, 0)), (Width - 160, 130))
					if release:
						item_settings_open = False
		
		if inventory.whole_inventory[changed_slot] is not None:
			text(t("Item name " + inventory.whole_inventory[changed_slot].name), 10, 320 if inventory_open else 80)

		if ron.x - player.x + Width // 2 - 128 <= mouse_x <= ron.x - player.x + Width // 2 + 128 and player.y - ron.y + Height // 2 - 128 <= mouse_y <= player.y - ron.y + Height // 2 + 128 and release and (not multiplayer or multiplayer_role == "Host"):
			ron.window[0] = True

		if ron.window[0]:
			
			win_fill()

			pygame.draw.rect(win, text_color, (100, 100, Width - 200, Height - 200))
			pygame.draw.rect(win, (0, 150, 0), (100, 100, Width - 200, Height - 200), 10)

			win.blit(bigTextInfo.render(t("Set a home point"), True, (0, 150, 0)), (200, 150))
			
			if 200 <= mouse_x <= 200 + bigTextInfo.size(t("Set a home point"))[0] and 150 <= mouse_y <= 180:
				
				win.blit(bigTextInfo.render(t("Set a home point"), True, (0, 100, 0)), (200, 150))
				
				if release:
					ron.home = [player.x, player.y]

			if ron.home is not None:
				win.blit(bigTextInfo.render(t("Current home point: ") + str(ron.home[0] // 50) + "; " + str(ron.home[1] // 50), True, (0, 150, 0)), (200, 200))

			win.blit(bigTextInfo.render(t("Call"), True, (0, 150, 0)), (200, 250))
			
			if 200 <= mouse_x <= 200 + bigTextInfo.size(t("Call"))[0] and 250 <= mouse_y <= 280:
				
				win.blit(bigTextInfo.render(t("Call"), True, (0, 100, 0)), (200, 250))
				if release:
					ron.home = None
					
			win.blit(bigTextInfo.render("x", True, (0, 150, 0)), (Width - 160, 130))
			
			if alt_pressed:
				draw_key("ESC", Width - 160, 170)
				
			if Width - 160 <= mouse_x <= Width - 130 and 130 <= mouse_y <= 160:
				win.blit(bigTextInfo.render("x", True, (0, 100, 0)), (Width - 160, 130))
				if release:
					ron.window[0] = False
					
		if in_motherboard is not None:

			win_fill()

			pygame.draw.rect(win, text_color, (Width // 2 - 300, Height // 2 - 300, 600, 600))
			pygame.draw.rect(win, (0, 150, 0), (Width // 2 - 300, Height // 2 - 300, 600, 600), 10)
			
			a = -1
			b = 0

			for i in in_motherboard.objects:
				a += 1
				if a == 32:
					a = 0
					b += 1
				if i is None:
					pygame.draw.rect(win, (0, 150, 0), (Width // 2 - 300 + a * 18.75, Height // 2 - 300 + b * 18.75, 18.75, 18.75), 2)
				else:
					i.main()
					if i.condition == "On":
						pygame.draw.rect(win, (180, 0, 0), (Width // 2 - 300 + a * 18.75, Height // 2 - 300 + b * 18.75, 18.75, 18.75))
					if i.condition == "Off":
						pygame.draw.rect(win, (180, 100, 100), (Width // 2 - 300 + a * 18.75, Height // 2 - 300 + b * 18.75, 18.75, 18.75))
			
			win.blit(bigTextInfo.render("x", True, (0, 150, 0)), (Width - 160, 130))
			
			if alt_pressed:
				draw_key("ESC", Width - 160, 170)
				
			if Width - 160 <= mouse_x <= Width - 130 and 130 <= mouse_y <= 160:
				win.blit(bigTextInfo.render("x", True, (0, 100, 0)), (Width - 160, 130))
				if release:
					in_motherboard = None

		if menu_open:

			text(f"""X {player.x // 50}
Y {player.y // 50}
Ron X {ron.x // 50}
Ron Y {ron.y // 50}
FPS {FPS}""" + (f"""
You are in backrooms lol
Level {Backrooms.Level}""" if Backrooms.InBackrooms else ""), 10, 400 if inventory_open else 300)
		
		if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name == "Wire":

			if in_motherboard is None:
				pos = (player.x + mouse_x - Width // 2) // 64 * 64 + 32, (player.y - mouse_y + Height // 2) // 64 * 64 + 32
				draw_select_image(64, 64, player, mouse_x, mouse_y)


				a = True
				if click[0]:
					for mechanism in world.mechanisms:
						if mechanism.x == (player.x + mouse_x - Width // 2) // 64 and mechanism.y == (player.y - mouse_y + Height // 2) // 64:
							a = False
							break
				
					if a:
						inventory.reduce(changed_slot)
						world.mechanisms.append(Wire(None))
			else:
				a = True
				if click[0]:
					for mechanism in in_motherboard.objects:
						if mechanism is not None and mechanism.x == (mouse_x - Width // 2 - 300) // 18.75 and mechanism.y == (mouse_y + Width // 2 - 300) // 18.75:
							a = False
							break
				
					if a and Width // 2 - 300 <= mouse_x <= Width // 2 + 300 and  Height // 2 - 310 <= mouse_y < Height // 2 + 290:
						inventory.reduce(changed_slot)
						in_motherboard.objects[(mouse_x - Width // 2 - 300) // 19 + ((mouse_y + Width // 2 - 300) // 19 - 19) * 32] = (Wire(in_motherboard))

		if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name == "Lever":

			pos = (player.x + mouse_x - Width // 2) // 64 * 64 + 32, (player.y - mouse_y + Height // 2) // 64 * 64 + 32
			draw_select_image(64, 64, player, mouse_x, mouse_y)

			a = True
			if click[0]:
				for mechanism in world.mechanisms:
					if mechanism.x == (player.x + mouse_x - Width // 2) // 64 and mechanism.y == (player.y - mouse_y + Height // 2) // 64:
						a = False
				
				if a:
					inventory.reduce(changed_slot)
					world.mechanisms.append(Lever(None))

		if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name == "Wrench":

			pos = (player.x + mouse_x - Width // 2) // 64 * 64 + 32, (player.y - mouse_y + Height // 2) // 64 * 64 + 32
			draw_select_image(64, 64, player, mouse_x, mouse_y)
			if click[0]:
				for mechanism in world.mechanisms:
					if mechanism.x == (player.x + mouse_x - Width // 2) // 64 and mechanism.y == (player.y - mouse_y + Height // 2) // 64:
						if (inventory.whole_inventory[changed_slot].settings == ["Only wire"] and mechanism.__class__ == Wire) or inventory.whole_inventory[changed_slot].settings == [] or (inventory.whole_inventory[changed_slot].settings == ["All mechanisms, but wire"] and mechanism.__class__ != Wire):
							world.mechanisms.remove(mechanism)
						break

		if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name == "Random box":

			pos = (player.x + mouse_x - Width // 2) // 64 * 64 + 32, (player.y - mouse_y + Height // 2) // 64 * 64 + 32
			draw_select_image(64, 64, player, mouse_x, mouse_y)
			a = True

			if click[0]:

				for mechanism in world.mechanisms:
					if mechanism.x == (player.x + mouse_x - Width // 2) // 64 and mechanism.y == (player.y - mouse_y + Height // 2) // 64:
						a = False
				
				if a:
					inventory.reduce(changed_slot)
					world.mechanisms.append(Random_box(None))

		if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name == "Motherboard":

			pos = (player.x + mouse_x - Width // 2) // 64 * 64 + 32, (player.y - mouse_y + Height // 2) // 64 * 64 + 32
			draw_select_image(64, 64, player, mouse_x, mouse_y)

			a = True
			if click[0]:
				for mechanism in world.mechanisms:
					if mechanism.x == (player.x + mouse_x - Width // 2) // 64 and mechanism.y == (player.y - mouse_y + Height // 2) // 64:
						a = False
				
				if a:
					inventory.reduce(changed_slot)
					world.mechanisms.append(Motherboard(None))
		if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name == "Portal gun":

			draw_select_image(128, 256, player, mouse_x, mouse_y)

			if click[0]:

				a = 0
				if not check_collision(pygame.Rect((player.x + mouse_x - Width // 2) // 256 * 256 + 128, (player.y - mouse_y + Height // 2) // 256 * 256 + 128, 256, 256), world, False):
					world.chunk_manager.get_chunk_at((player.x + mouse_x - Width // 2) // 128, (player.y + mouse_y - Height // 2) // 256).objects.append(Portal())
		build_tuple = (changed_slot, player, world, inventory.whole_inventory)
		new_object = check_build_objects(objects_templates, build_tuple)

		if multiplayer and new_object is not None:
			game_events.append({"event_type": "object_added", "object": new_object.__getstate__()})

		if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name == "Stone hoe":
			
			farmland_pos = (player.x + mouse_x - Width // 2) // 128 * 128 + 128, (player.y - mouse_y + Height // 2) // 128 * 128
			draw_select_image(128, 128, player, mouse_x, mouse_y)

			if click[0] and farmland_pos not in world.visible_farmlands and not check_collision(pygame.Rect(farmland_pos[0] - 128, farmland_pos[1], 128, 128), world, False):
				world.chunk_manager.get_chunk_at(*farmland_pos).farmlands[farmland_pos] = Farmland(farmland_pos[0], farmland_pos[1])
				game_events.append({"event_type": "farmland_added", "farmland_pos": farmland_pos})

				play_sound("Dirt")
				# for farmland in (((farmland_pos[0] - 128, farmland_pos[1]), (farmland_pos[0] + 128, farmland_pos[1]), (farmland_pos[0], farmland_pos[1] - 128), (farmland_pos[0], farmland_pos[1] + 128))):
				#	if farmland in world.visible_farmlands:
				#		world.visible_farmlands[farmland].update_neigboors()

		if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name in wall_types:
			
			wall_pos = (player.x + mouse_x - Width // 2) // 256 * 256 + 128, (player.y - mouse_y + Height // 2) // 256 * 256 + 128
			draw_select_image(256, 256, player, mouse_x, mouse_y)

			if click[0] and wall_pos not in world.visible_walls and not check_collision(pygame.Rect(wall_pos[0], wall_pos[1], 256, 256), world, False, False):
				world.chunk_manager.get_chunk_at(*wall_pos).walls[wall_pos] = Wall(inventory.whole_inventory[changed_slot].name, wall_pos[0], wall_pos[1])
				for wall in (((wall_pos[0] - 256, wall_pos[1]), (wall_pos[0] + 256, wall_pos[1]), (wall_pos[0], wall_pos[1] - 256), (wall_pos[0], wall_pos[1] + 256))):
					if wall in world.visible_walls:
						world.visible_walls[wall].update_neigboors()
				if multiplayer:
					game_events.append({"event_type": "wall_added", "wall": world.chunk_manager.get_chunk_at(*wall_pos).walls[wall_pos].__getstate__()})
				inventory.reduce(changed_slot)

		if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name in door_types:

			wall_pos = (player.x + mouse_x - Width // 2) // 256 * 256 + 128, (player.y - mouse_y + Height // 2) // 256 * 256 + 128
			draw_select_image(256, 256, player, mouse_x, mouse_y)

			if click[0] and wall_pos not in world.visible_walls and not check_collision(pygame.Rect(wall_pos[0], wall_pos[1], 256, 256), world, False, False):
				world.chunk_manager.get_chunk_at(*wall_pos).walls[wall_pos] = Wall(inventory.whole_inventory[changed_slot].name, wall_pos[0], wall_pos[1], True)
				for wall in (((wall_pos[0] - 256, wall_pos[1]), (wall_pos[0] + 256, wall_pos[1]), (wall_pos[0], wall_pos[1] - 256), (wall_pos[0], wall_pos[1] + 256))):
					if wall in world.visible_walls:
						world.visible_walls[wall].update_neigboors()
				if multiplayer:
					game_events.append({"event_type": "wall_added", "wall": world.chunk_manager.get_chunk_at(*wall_pos).walls[wall_pos].__getstate__()})
				inventory.reduce(changed_slot)

		if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name == "Stone hammer":

			break_pos = (player.x + mouse_x - Width // 2) // 256 * 256 + 128, (player.y - mouse_y + Height // 2) // 256 * 256 + 128
			draw_select_image(256, 256, player, mouse_x, mouse_y)

			if click[0]:
				if break_pos in world.visible_walls:
					inventory.increate(world.chunk_manager.get_chunk_at(*break_pos).walls[break_pos].wall_type)
					destroy_object(world.visible_walls[break_pos].image, world.visible_walls[break_pos].x, world.visible_walls[break_pos].y, world, Particle)
					game_events.append({"event_type": "wall_removed", "break_pos": break_pos})
					world.chunk_manager.get_chunk_at(*break_pos).walls.pop(break_pos, None)
					for wall in ((break_pos[0] - 256, break_pos[1]), (break_pos[0] + 256, break_pos[1]), (break_pos[0], break_pos[1] - 256), (break_pos[0], break_pos[1] + 256)):
						if wall in world.chunk_manager.get_chunk_at(*wall).walls:
							world.chunk_manager.get_chunk_at(*wall).walls[wall].update_neigboors()

				for object in world.visible_objects:
					if object.breakable_by_hammer and (object.x, object.y) == break_pos:
						inventory.increate(object.name)
						destroy_object(object.image, object.x, object.y, world, Particle)
						game_events.append({"event_type": "object_removed", "x": object.x, "y": object.y, "name": object.name})
						world.chunk_manager.get_chunk_at(object.x, object.y).objects.remove(object)
						break

		if mouse_object is not None and Settings["Display"][8]:
			# text(mouse_object, Width - textInfo.size(mouse_object)[0] - 10, 10)
			win.blit(textInfo.render(mouse_object, True, text_color), (Width - textInfo.size(mouse_object)[0] - 10, 10))
		
		if chat_open:
			win_fill()
			win_fill(rect=(10, Height - 50, Width - 20, 40))
			if not input_system.inputting:

				chat_open = False
				if input_system.last_text[0:2] == "/!" and Settings["User"][1]:
					try:
						eval(input_system.last_text[2:])
						# Команды через eval - опасная штука, так что они доступны только в режиме разработчика
					except Exception as e:
						chat_message(languages("<<< Команда " + Settings["User"][0] + f" получила ошибку {e}" + ". >>>", "<<< " + Settings["User"][0] + f"'s command got an {e}" + "error. >>>", ""))
					else:
						chat_message(languages("<<< Команда " + Settings["User"][0] + " была успешно исполнена. >>>", "<<< " + Settings["User"][0] + "'s command was successfully executed. >>>", ""))
				elif input_system.last_text != "" and input_system.last_text[0] == "/":
					chat_message(command_system.execute(input_system.last_text))
				elif input_system.last_text != "":
					if multiplayer:
						message_text = f"{net.peers[net.player_id].name}: {input_system.last_text}"
					else:
						message_text = f"{Settings['User'][0]}: {input_system.last_text}"
					chat_message(message_text, True)
		
		if len(chat) != 0:

			if chat_tick == 0:
				chat.remove(chat[0])
				try:
					chat_tick = len(chat[0]) // 1.5 * FPS
				except: pass
			
		reversed_chat = main_chat.copy() if chat_open else chat.copy()
		reversed_chat.reverse()
		message_y = 80
		for message in reversed_chat:
			message_y += get_text_height(message)
			text(message, 10, Height - message_y)
		
		chat_tick = max(0, chat_tick - 1)
		
		if multiplayer_menu_open:
			
			enable_multiplayer = Button(Width // 2, Height // 2 - 30, bigTextInfo.render(t("Enable multiplayer"), True, menu_color_medium), bigTextInfo.render(t("Enable multiplayer"), True, menu_color_dark), alignment=True, info=t("Your IP-address - ") + socket.gethostbyname(socket.gethostname()))
			enter_another_game = Button(Width // 2, Height // 2 + 30, bigTextInfo.render(t("Enter another game"), True, menu_color_medium), bigTextInfo.render(t("Enter another game"), True, menu_color_dark), alignment=True)
			
			pygame.image.save(win, path + "Saves/Cache/Win.png")
			win_darken(win)
			a, b = True, None
			animation_showed = False
			release = False

			while multiplayer_menu_open:

				mouse_x, mouse_y = pygame.mouse.get_pos()
				click = pygame.mouse.get_pressed()
				release = False

				for event in pygame.event.get():

					if event.type == pygame.QUIT:
						save()
						sys.exit()

					elif event.type == pygame.MOUSEBUTTONUP:
						if event.button == 1:
							release = True

					elif event.type == pygame.KEYDOWN and event.key == hot_keys["Close"]:
						multiplayer_menu_open = False						

				win.fill(menu_color_light)

				if mouse_x <= 128 and mouse_y <= 128:
					win.blit(load(path + "Images/Buttons/Back 2.png", 128), (0, 0))
					if release:
						multiplayer_menu_open = False
						
				else:
					win.blit(load(path + "Images/Buttons/Back.png", 128), (0, 0))

				pygame.draw.rect(win, menu_color_dark, (0, 0, Width, Height), 10)
				pygame.draw.rect(win, menu_color_medium, (10, 10, Width - 20, Height - 20), 10)
				
				enable_multiplayer.main()
				enter_another_game.main()

				if enable_multiplayer.get_pressed():
					b = 1
					multiplayer_menu_open = False

				elif enter_another_game.get_pressed():
					b = 2
					multiplayer_menu_open = False
				if not animation_showed:
					win_lighten(win)
					animation_showed = True
				pygame.display.update()
				clock.tick(MAX_FPS)

			win_darken(win)
			win_lighten(win, pygame.image.load(path + "Saves/Cache/Win.png"))

			if b is not None:
				
				if b == 1:

					input_text = ""
					i = Button(Width // 2, Height // 2, textInfo.render("Next", True, text_color), textInfo.render("Next", True, (0, 0, 0)), alignment=True)

					while a:

						for event in pygame.event.get():
							if event.type == pygame.QUIT:
								save()
								sys.exit()

						win.fill(color)
						win.blit(textInfo.render("Your server's host is " + socket.gethostbyname(socket.gethostname()), True, text_color), ((Width - textInfo.size("Your server's host is " + socket.gethostbyname(socket.gethostname()))[0]) // 2, Height // 2 - 30))
						i.main()
						if i.get_pressed():
							a = False

						pygame.display.update()
						clock.tick(MAX_FPS)

					save(False)

				else:

					input_text = ""
					a = True

					while a:

						for event in pygame.event.get():
							if event.type == pygame.QUIT:
								save()
								sys.exit()
			
							elif event.type == pygame.KEYDOWN:
								if event.key == pygame.K_RETURN:
									a = False
								elif event.key == pygame.K_BACKSPACE:
									input_text = input_text[:-1]
								elif len(input_text) <= 500:
									input_text += event.unicode

						win.fill(menu_color_light)
						pygame.draw.rect(win, menu_color_dark, (0, 0, Width, Height), 10)
						pygame.draw.rect(win, menu_color_medium, (10, 10, Width - 20, Height - 20), 10)

						win.blit(textInfo.render("Enter server host", True, menu_color_medium), ((Width - textInfo.size("Enter server host")[0]) // 2, Height // 2 - 30))
						win.blit(textInfo.render(input_text, True, menu_color_medium), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2))

						pygame.display.update()
						clock.tick(MAX_FPS)

					save(False)

					# try:
						
					#	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					#	sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
					#	sock.connect((input_text, 10000))
						
					# except:
						
					#	a = Button(Width // 2, Height // 2 + 20, bigTextInfo.render(i("Next"), True, menu_color_medium), bigTextInfo.render(t("Next"), True, menu_color_dark), alignment=True)

					#	while True:
						
					#		for event in pygame.event.get():
					#			if event.type == pygame.QUIT:
					#				save()
					#				sys.exit()
						   
									
					#		win.fill(menu_color_light)
					#		pygame.draw.rect(win, menu_color_dark, (0, 0, Width, Height), 10)
					#		pygame.draw.rect(win, menu_color_medium, (10, 10, Width - 20, Height - 20), 10)
							
					#		win.blit(textInfo.render(t("Connection error"), True, menu_color_medium), ((Width - textInfo.size(t("Connection error"))[0]) // 2, Height // 2 - 20))

					#		a.main()
					#		if a.get_pressed():
					#			break
							
					#		pygame.display.update()
					#		clock.tick(MAX_FPS)
				
		if inventory.whole_inventory[inventory.start_cell] is not None and inventory.start_cell > -1 and hold_left:

			item_text = t("Item info " + inventory.whole_inventory[inventory.start_cell].name) + "\n" + t("Item purpose " + inventory.whole_inventory[inventory.start_cell].name)
			
			text_height = get_text_height(item_text) + 40
			if inventory.whole_inventory[inventory.start_cell].type == "Food":
				text_height += 84
			
			for yy, xx in product(range(0, 3), range(0, 10)):
				cell_x = 10 + xx * 80
				cell_y = 10 + yy * 80
				if cell_x <= mouse_x <= cell_x + 64 and cell_y <= mouse_y <= cell_y + 64:
					win_fill(rect=(cell_x, cell_y, 64, 64))
					break

			pygame.draw.rect(win, text_color, (mouse_x, mouse_y, Width // 3 + 40, text_height))
			pygame.draw.rect(win, (0, 150, 0), (mouse_x, mouse_y, Width // 3 + 40, text_height), 3)
			text(item_text, mouse_x + 20, mouse_y + 20, color=(0, 150, 0), max_width=Width // 3)
			
			if inventory.whole_inventory[inventory.start_cell].type == "Food":
				win.blit(Heart, (mouse_x + 20, mouse_y + text_height - 84))
				win.blit(textInfo.render(str(inventory.whole_inventory[inventory.start_cell].special_info), True, text_color), (mouse_x + 52 - textInfo.size(str(inventory.whole_inventory[inventory.start_cell].special_info))[0] // 2, mouse_y + text_height - 59))
			
			win.blit(inventory.whole_inventory[inventory.start_cell].image, (mouse_x - 32, mouse_y - 32))
		
		# Механика мультиплеера

		if multiplayer:

			if inventory.check_new_items(changed_slot):
				if inventory.whole_inventory[changed_slot] is None:
					player.changed_item = None
				else:
					player.changed_item = inventory.whole_inventory[changed_slot].name
				game_events.append({"event_type": "changed_item", "changed_item": player.changed_item})
			if len(game_events) != 0:
				net.send_events(tuple(game_events))
			for event in net.server_events["Game"]:
				remove_event = True

				match event["event_type"]:

					case "object_added":
						object = event["object"]
						chunk = world.chunk_manager.get_chunk_at(object["x"], object["y"])
						if chunk is not None:
							object["scale"] = tuple(object["scale"])
							chunk.objects.append(Object(object["name"], object["x"], object["y"], object["image_path"], object["scale"], None, object["special_flags"], object["add_path"], object["start_time"], object["is_solid"], object["rect"], object["is_solid"], object["breakable"], object["max_break"], object["breakable_by_hammer"], object["drop_items"]))
							chunk.objects[-1].__setstate__(object)

					case "object_removed":
						for object in world.visible_objects:
							if (object.x, object.y, object.name) == (event["x"], event["y"], event["name"]):
								destroy_object(object.image, object.x, object.y, world, Particle)
								world.chunk_manager.get_chunk_at(object.x, object.y).objects.remove(object)
								break

					case "item_added":
						item = event["item"]
						chunk = world.chunk_manager.get_chunk_at(item["x"], item["y"])
						if chunk is not None:
							item["scale"] = tuple(item["scale"])
							chunk.items.append(Object(item["name"], item["x"], item["y"], item["image_path"], item["scale"], None, item["special_flags"], item["add_path"], item["start_time"], item["is_solid"], item["rect"], item["is_solid"], item["breakable"], item["max_break"], item["breakable_by_hammer"], item["drop_items"]))
							chunk.items[-1].__setstate__(item)

					case "item_removed":
						for item in world.visible_items:
							if (item.x, item.y, item.name) == (event["x"], event["y"], event["name"]):
								world.chunk_manager.get_chunk_at(item.x, item.y).items.remove(item)
								break

					case "wall_added":
						wall = event["wall"]
						chunk = world.chunk_manager.get_chunk_at(wall["x"], wall["y"])
						if chunk is not None:
							wall_pos = (wall["x"], wall["y"])
							chunk.walls[wall_pos] = Wall(wall["wall_type"], wall["x"], wall["y"], wall["is_door"])
							chunk.walls[wall_pos].__setstate__(wall)
							for wall in (((wall_pos[0] - 256, wall_pos[1]), (wall_pos[0] + 256, wall_pos[1]), (wall_pos[0], wall_pos[1] - 256), (wall_pos[0], wall_pos[1] + 256))):
								if wall in world.visible_walls:
									world.visible_walls[wall].update_neigboors()

					case "wall_removed":
						break_pos = tuple(event["break_pos"])
						chunk = world.chunk_manager.get_chunk_at(*break_pos)
						if chunk is not None and break_pos in chunk.walls:
							del chunk.walls[break_pos]
							for wall in (((break_pos[0] - 256, break_pos[1]), (break_pos[0] + 256, break_pos[1]), (break_pos[0], break_pos[1] - 256), (break_pos[0], break_pos[1] + 256))):
								if wall in world.visible_walls:
									world.visible_walls[wall].update_neigboors()

					case "wall_interaction":
						wall_pos = tuple(event["wall_pos"])
						chunk = world.chunk_manager.get_chunk_at(*wall_pos)
						if chunk is not None and wall_pos in chunk.walls:
							chunk.walls[wall_pos].open = not chunk.walls[wall_pos].open
							chunk.walls[wall_pos].update_neigboors()

					case "farmland_added":
						farmland_pos = tuple(event["farmland_pos"])
						chunk = world.chunk_manager.get_chunk_at(*farmland_pos)
						if chunk is not None:
							chunk.farmlands[farmland_pos] = Farmland(*farmland_pos)
							play_sound("Dirt")

					case "projectile_added":
						world.projectiles.append(Projectile(event["x"], event["y"], event["mouse_x"], event["mouse_y"], event["projectile_type"]))

					case "chat_message":
						chat_message(event["message_text"])

					case _:
						remove_event = False

				if remove_event:
					net.server_events["Game"].remove(event)

			if multiplayer_role == "Host":
				for event in net.server_events["Game"]:
					match event["event_type"]:
						case "peer_joined":
							net._send_packet({"type": "server_event", "player_id": "Game", "event_type": "world_info", "world_info": (
								0, 0, False, 0, None, player.speed, player.HP, start_time, ron.x, ron.y, ron.home, ron.inventory, world.chunk_manager.generator.seed, time_system.current_time, game.difficulty
								)}, event["address"])
						case "get_chunk":
							chunk_key = tuple(event["chunk_key"])
							if chunk_key in world.chunk_manager.chunks:
								chunk = world.chunk_manager.chunks[chunk_key]
							else:
								chunk = world.chunk_manager._load_chunk_from_disk(*chunk_key)
								if chunk is None:
									world.chunk_manager.chunks[chunk_key] = world.chunk_manager.Chunk(*chunk_key)
									chunk = world.chunk_manager.chunks[chunk_key]
									world.chunk_manager.generate_chunk(chunk)
									chunk.is_loaded = True
							state = chunk.__getstate__()
							state["mobs"] = []
							state["particles"] = []
							state["caves"] = []

							new_objects = [object.__getstate__() for object in state["objects"]]
							state["objects"] = new_objects
							new_items = [item.__getstate__() for item in state["items"]]
							state["items"] = new_items
							new_walls = [wall.__getstate__() for _, wall in state["walls"].items()]
							state["walls"] = new_walls
							new_farmlands = [farmland.__getstate__() for _, farmland in state["farmlands"].items()]
							state["farmlands"] = new_farmlands
							if event["player_id"] in net.peers:
								net._send_packet({"type": "server_event", "event_type": "chunk", "player_id": "Game", "chunk_key": chunk_key, "chunk_state": state}, net.peers[event["player_id"]].address)

					net.server_events["Game"].remove(event)
			else:
				if time.time() - net.last_heartbeat > 3:
					net.send_heartbeat()
				for event in net.server_events["Game"]:
					match event["event_type"]:
						case "world_info":
							player.x, player.y, Backrooms.InBackrooms, Backrooms.Level, world.current_cave, player.speed, player.HP, start_time, ron.x, ron.y, ron.home, ron.inventory, world.chunk_manager.generator.seed, time_system.current_time, game.difficulty = event["world_info"]
							world.chunk_manager.update_seed()

						case "ron_moved":
							ron.x = event["x"]
							ron.y = event["y"]
							ron.direction = event["direction"]

						case "chunk":
							chunk_key = tuple(event["chunk_key"])
							world.chunk_manager.chunks[chunk_key] = world.chunk_manager.Chunk(*chunk_key)
							chunk = world.chunk_manager.chunks[chunk_key]
							chunk.__setstate__(event["chunk_state"])
							chunk.is_loaded = True

							new_objects = []
							for object in chunk.objects:
								object["scale"] = tuple(object["scale"])
								new_objects.append(Object(object["name"], object["x"], object["y"], object["image_path"], object["scale"], None, object["special_flags"], object["add_path"], object["start_time"], object["is_solid"], object["rect"], object["is_solid"], object["breakable"], object["max_break"], object["breakable_by_hammer"], object["drop_items"]))
								new_objects[-1].__setstate__(object)
							chunk.objects = new_objects
							
							new_items = []
							for item in chunk.items:
								item["scale"] = tuple(item["scale"])
								new_items = [Object(item["name"], item["x"], item["y"], item["image_path"], item["scale"], None, item["special_flags"], item["add_path"], item["start_time"], item["is_solid"], item["rect"], item["is_solid"], item["breakable"], item["max_break"], item["breakable_by_hammer"], item["drop_items"]) for item in chunk.items]
								new_items[-1].__setstate__(item)
							chunk.items = new_items
							
							new_walls = {}
							for wall in chunk.walls:
								new_walls[(wall["x"], wall["y"])] = Wall(wall["wall_type"], wall["x"], wall["y"])
								new_walls[(wall["x"], wall["y"])].__setstate__(wall)
							chunk.walls = new_walls

							new_farmlands = {}
							for farmland in chunk.farmlands:
								new_farmlands[(farmland["x"], farmland["y"])] = Farmland(farmland["x"], farmland["y"])
								new_farmlands[(farmland["x"], farmland["y"])].__setstate__(farmland)
							chunk.farmlands = new_farmlands
							world.chunk_manager.chunks_to_get.remove(chunk_key)

					net.server_events["Game"].remove(event)

		if keys[hot_keys["Screenshot"]] and not keys[hot_keys["Show keys"]]:
			
			pygame.image.save(win, str(Path.home()) + "/Your Screenshot " + str(time.asctime().replace(":", " ")) + ".png")
	
			for _ in range(3):
				win.fill((200, 255, 200))
				clock.tick(MAX_FPS)
				pygame.display.update()
			time.sleep(0.1)
			
		if keys[hot_keys["Plugin manager"]] and not chat_open:
			
			win = pygame.display.set_mode((0, 0), pygame.RESIZABLE)

			win.fill(menu_color_light)
			pygame.draw.rect(win, menu_color_dark, (0, 0, Width, Height), 10)
			pygame.draw.rect(win, menu_color_medium, (10, 10, Width - 20, Height - 20), 10)

			win.blit(textInfo.render(t("The gameplay will continue, when you close the plugin creator"), True, menu_color_medium), ((Width - textInfo.size(t("The gameplay will continue, when you close the plugin creator"))[0]) // 2, Height // 2 - 32))
			pygame.display.update()
			os.system("python " + path + "Plugin_creater.py")
		
		input_system.handle_input(events)
		animate_click(dt, mouse_x, mouse_y)
		win_fill((200, 0, 0), 100 - Settings["Display"][0])

		pygame.display.update()



# Меню редактирования мира

def edit_world():
	
	global world_name, game, player, alt_pressed, does_lighten

	create_world = False
	release = False
	does_lighten = False

	try:
		game.difficulty, player.god_mode = Saver.load_objects(path + "Saves/Worlds/" + world_name + "/Settings.save")
	except:
		game.difficulty = "norm"
		player.god_mode = False
		create_world = True
	Settings["Edit world"][0] = world_name
	Settings["Edit world"][1] = player.god_mode

	input_text = ""
	world_name_input = False
	seed_input = False

	easy_but = Button(50, 200, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Easy.png"), (132, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Easy 2.png"), (132, 64)))
	norm_but = Button(50, 270, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Norm.png"), (132, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Norm 2.png"), (132, 64)))
	hard_but = Button(50, 340, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Hard.png"), (132, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Hard 2.png"), (132, 64)))
	skull_but = Button(50, 410, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Skull.png"), (132, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Skull 2.png"), (132, 64)))

	if create_world:
		world.chunk_manager.generator.seed = random.randint(0, 2**31 - 1)
		world.chunk_manager.update_seed()
	while True:
		
		mouse_x, mouse_y = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		keys = pygame.key.get_pressed()
		release = False
		events = pygame.event.get()

		for event in events:

			if event.type == pygame.QUIT:
				if not create_world:
					if world_name != Settings["Edit world"][0]:
						os.rename(path + "Saves/Worlds/" + world_name, path + "Worlds/" + Settings["Edit world"][0])
					world_name = Settings["Edit world"][0]
					player.god_mode = Settings["Edit world"][1]
					Saver.save_objects(path + "Saves/Worlds/" + world_name + "/Settings.save", [game.difficulty, player.god_mode])
				win_darken(win)
				sys.exit()
				
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					release = True

			elif event.type == pygame.KEYDOWN and (world_name_input or seed_input):
				if event.key == pygame.K_RETURN or len(input_text) == 50:
					if seed_input:
						if input_text != "":
							world.chunk_manager.generator.seed = int(input_text)
							world.chunk_manager.update_seed()
						seed_input = False
					input_text = ""
				elif event.key == pygame.K_BACKSPACE:
					input_text = input_text[:-1]
				elif not seed_input or event.unicode in "0123456789":
					input_text += event.unicode
			
			if event.type == pygame.KEYUP:
				
				if event.key == hot_keys["Close"] and not create_world:
					if world_name != Settings["Edit world"][0]:
						os.rename(path + "Saves/Worlds/" + world_name, path + "Worlds/" + Settings["Edit world"][0])
					world_name = Settings["Edit world"][0]
					player.god_mode = Settings["Edit world"][1]
					Saver.save_objects(path + "Saves/Worlds/" + world_name + "/Settings.save", [game.difficulty, player.god_mode])
					worlds()
				
				if event.key == hot_keys["Show keys"]:
					alt_pressed = not alt_pressed
		
		win.fill(menu_color_light)
		ui_system.handle_events(events, mouse_x, mouse_y, release, "World settings")
		ui_system.draw("World settings", show_settings_lines=False)

		win.blit(bigTextInfo.render("x", True, menu_color_medium), (Width - 50, 15))
		
		if Width - 50 < mouse_x < Width - 20 and 15 < mouse_y < 45:
			
			win.blit(bigTextInfo.render("x", True, menu_color_dark), (Width - 50, 15))
			
			if pygame.mouse.get_pressed()[0]:
				
				if not create_world:
					os.rename(path + "Saves/Worlds/" + world_name, path + "Worlds/" + Settings["Edit world"][0])
					world_name = Settings["Edit world"][0]
					player.god_mode = Settings["Edit world"][1]
					Saver.save_objects(path + "Saves/Worlds/" + world_name + "/Settings.save", [game.difficulty, player.god_mode])
				worlds()

		win.blit(bigTextInfo.render(t("Game difficulty:"), True, menu_color_medium), (50, 150))

		easy_but.main()
		if easy_but.get_pressed():
			game.difficulty = "easy"
		
		norm_but.main()
		if norm_but.get_pressed():
			game.difficulty = "norm"
		
		hard_but.main()
		if hard_but.get_pressed():
			game.difficulty = "hard"
		
		skull_but.main()
		if skull_but.get_pressed():
			game.difficulty = "skull"

		win.blit(load(path + "Images/Modes/" + game.difficulty + ".png", 548, 274), (232, 200))
		
		match game.difficulty:
			
			case "easy":
				win.blit(load(path + "Images/Buttons/Easy 2.png", 132, 64), (50, 200))
				
			case "norm":
				win.blit(load(path + "Images/Buttons/Norm 2.png", 132, 64), (50, 270))
				
			case "hard":
				win.blit(load(path + "Images/Buttons/Hard 2.png", 132, 64), (50, 340))
				
			case "skull":
				win.blit(load(path + "Images/Buttons/Skull 2.png", 132, 64), (50, 410))

		if create_world:
			
		
			if bigTextInfo.size(t("World seed"))[0] + 100 <= mouse_x <= bigTextInfo.size(t("World seed"))[0] + 900 and 590 <= mouse_y <= 661 and release:
				seed_input = True
			win.blit(bigTextInfo.render(t("World seed"), True, menu_color_medium), (50, 600))
			pygame.draw.rect(win, menu_color_medium, (bigTextInfo.size(t("World seed"))[0] + 100, 590, 800, 71), 5)
			if seed_input:
				win.blit(bigTextInfo.render(input_text, True, menu_color_medium), (bigTextInfo.size(t("World seed"))[0] + 120, 600))
			else:
				win.blit(bigTextInfo.render(str(world.chunk_manager.generator.seed), True, menu_color_medium), (bigTextInfo.size(t("World seed"))[0] + 120, 600))
			win.blit(bigTextInfo.render(t("Create world"), True, menu_color_medium), (Width - bigTextInfo.size(t("Create world"))[0] - 50, 150))
			
			if Width - bigTextInfo.size(t("Create world"))[0] - 50 < mouse_x < Width - 50 and 150 < mouse_y < 180:
				
				win.blit(bigTextInfo.render(t("Create world"), True, menu_color_dark), (Width - bigTextInfo.size(t("Create world"))[0] - 50, 150))
				if release:
					world_name = Settings["Edit world"][0]
					player.god_mode = Settings["Edit world"][1]
					win_darken(win)
					start_game()
		else:
			
			win.blit(bigTextInfo.render(t("Delete world"), True, menu_color_medium), (50, 660))

			if 50 < mouse_x < 50 + bigTextInfo.size(t("Delete world"))[0] and 660 < mouse_y < 690:
		   
				win.blit(bigTextInfo.render(t("Delete world"), True, menu_color_dark), (50, 660))
			
				if release:
				
					win_fill()
					a = win.copy()
				
					yes_button = Button(Width // 2 - 150, Height // 2, bigTextInfo.render(t("Yes"), True, menu_color_medium), bigTextInfo.render(t("Yes"), True, menu_color_dark), alignment=True)
					no_button = Button(Width // 2 + 150, Height // 2, bigTextInfo.render(t("No"), True, menu_color_medium), bigTextInfo.render(t("No"), True, menu_color_dark), alignment=True)

					while True:
					
						for event in pygame.event.get():
							if event.type == pygame.QUIT:
								win_darken(win)
								sys.exit()
							
						mouse_x, mouse_y = pygame.mouse.get_pos()
						click = pygame.mouse.get_pressed()
						keys = pygame.key.get_pressed()
					
						win.blit(a, (0, 0))
					
						pygame.draw.rect(win, menu_color_light, (Width // 2 - 300, Height // 2 - 150, 600, 300))
						pygame.draw.rect(win, menu_color_medium, (Width // 2 - 300, Height // 2 - 150, 600, 300), 5)
					
						win.blit(textInfo.render(t("Are you sure want to delete this world?"), True, menu_color_medium), ((Width - textInfo.size(t("Are you sure want to delete this world?"))[0]) // 2, Height // 2 - 100))

						yes_button.main()
						if yes_button.get_pressed():   # Удалить выбранный мир
							import shutil
							shutil.rmtree(path + "Saves/Worlds/" + world_name)
							del shutil
							win_darken(win)
							worlds()
						
						no_button.main()
						if no_button.get_pressed() or keys[hot_keys["Close"]]:
							break
					
						win_fill(alpha=100 - Settings["Display"][0])   # Если в настройках установлена яркость ниже 100, то экран становится темнее
					
						pygame.display.update()
						clock.tick(30)
					
			win.blit(bigTextInfo.render(t("Copy world"), True, menu_color_medium), (50, 600))

			if 50 < mouse_x < 50 + bigTextInfo.size(t("Copy world"))[0] and 600 < mouse_y < 630:
				win.blit(bigTextInfo.render(t("Copy world"), True, menu_color_dark), (50, 600))
				if release:
					import shutil
					shutil.copytree(path + "Saves/Worlds/" + world_name, path + "Worlds/" + world_name + t(" - copy"))
					del shutil
					win_darken(win)
					if create_world:
						start_game()
					else:
						worlds()
						
		if alt_pressed:
			draw_key("ESC", Width - 50, 55)
			
		win_fill(alpha=100 - Settings["Display"][0])   # Если в настройках установлена яркость ниже 100, то экран становится темнее
		
		if not create_world:
			Saver.save_objects(path + "Saves/Worlds/" + world_name + "/Settings.save", [game.difficulty, player.god_mode])

		if not does_lighten:
			win_lighten(win)
			does_lighten = True
		
		pygame.display.update()
		clock.tick(30)

def multiplayer_settings_menu():
	
	global alt_pressed, does_lighten, multiplayer_role, net

	back_button = Button(-20, -20, load(path + "Images/Buttons/Back.png", 128), load(path + "Images/Buttons/Back 2.png", 128))
	host_button = Button(Width // 4, 50, textInfo.render("Хост (в твой мир заходят игроки)", True, menu_color_medium), textInfo.render("Хост (в твой мир заходят игроки)", True, menu_color_dark), alignment=True)
	client_button = Button(Width * 3 // 4, 50, textInfo.render("Клиент (ты заходишь в мир хоста)", True, menu_color_medium), textInfo.render("Клиент (ты заходишь в мир хоста)", True, menu_color_dark), alignment=True)
	start_game_button = Button(Width - 10 - bigTextInfo.size("Начать игру")[0], 150, bigTextInfo.render("Начать игру", True, menu_color_medium), bigTextInfo.render("Начать игру", True, menu_color_dark), alignment=True)

	create_world = False
	release = False
	does_lighten = False
	max_bias = -ui_system._set_positions(0, "Multiplayer settings menu", True)
	max_bias = (max_bias + Height - 103) * max_bias > Height - 103

	while True:
		
		mouse_x, mouse_y = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		keys = pygame.key.get_pressed()
		release = False
		events = pygame.event.get()
		dt = clock.tick(MAX_FPS) / 1000.0

		for event in events:

			if event.type == pygame.QUIT:
				win_darken(win)
				sys.exit()
				
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					release = True
			
			if event.type == pygame.KEYUP:
				
				if event.key == hot_keys["Show keys"]:
					alt_pressed = not alt_pressed
				if event.key == hot_keys["Close"]:
					win_darken(win)
					worlds()
		
		win.fill(menu_color_light)

		pygame.draw.rect(win, menu_color_light, (0, 0, Width, 103))
		pygame.draw.line(win, menu_color_medium, (0, 103), (Width, 103), 8)
		pygame.draw.line(win, menu_color_medium, (Width // 2, 0), (Width // 2, 103), 8)
		ui_system.handle_events(events, mouse_x, mouse_y, release, "Multiplayer settings menu")
		ui_system.draw("Multiplayer settings menu",show_settings_lines=False)
		back_button.main()
		if back_button.get_pressed():
			win_darken(win)
			worlds()

		if multiplayer_role == "Client":
			host_button.main()
			if host_button.get_pressed():
				multiplayer_role = "Host"
			win.blit(textInfo.render("Клиент (ты заходишь в мир хоста)", True, menu_color_dark), (Width * 3 // 4 - textInfo.size("Клиент (ты заходишь в мир хоста)")[0] // 2, 50 - textInfo.size("Клиент (ты заходишь в мир хоста)")[1] // 2))
		else:
			win.blit(textInfo.render("Хост (в твой мир заходят игроки)", True, menu_color_dark), (Width // 4 - textInfo.size("Хост (в твой мир заходят игроки)")[0] // 2, 50 - textInfo.size("Хост (в твой мир заходят игроки)")[1] // 2))
			client_button.main()
			if client_button.get_pressed():
				multiplayer_role = "Client"
		start_game_button.main()

		if start_game_button.get_pressed():
			net = NetworkManager(Peer, chat_message, world.chunk_manager.view_distance)
			if multiplayer_role == "Host":
				if Settings["Multiplayer"][0]:
					net.start_host(Settings["Multiplayer"][1], Settings["Multiplayer"][2])
				else:
					net.start_local_host(Settings["Multiplayer"][1])
			else:
				if not os.path.exists(path + "Saves/Cache/Multiplayer"):
					os.mkdir(path + "Saves/Cache/Multiplayer")
				world.chunk_manager.save_directory = path + "Saves/Cache/Multiplayer/"
				if Settings["Multiplayer"][0]:
					net.connect_to_host(Settings["Multiplayer"][3], Settings["Multiplayer"][4])
				else:
					net.connect_to_local_host(Settings["Multiplayer"][3], Settings["Multiplayer"][1])
				# connecting = True
				# while connecting:
				#	mouse_x, mouse_y = pygame.mouse.get_pos()
				#	for event in pygame.event.get():
				#		if event.type == pygame.QUIT:
				#			win_darken(win)
				#			sys.exit()
				#	win.fill(menu_color_light)
				#	for event in net.server_events["Game"]:
				#		if event["event_type"] == "world_info":
				#			connecting = False
				#	animate_click(dt, mouse_x, mouse_y)
				#	pygame.display.update()
				#	clock.tick(MAX_FPS)
			start_game()

		if alt_pressed: draw_key("ESC", 44, 108)
		animate_click(dt, mouse_x, mouse_y)
		win_fill(alpha=100 - Settings["Display"][0])   # Если в настройках установлена яркость ниже 100, то экран становится темнее

		if not does_lighten:
			win_lighten(win)
			does_lighten = True
		
		pygame.display.update()


# Меню миров

def worlds():

	global world_name, keys, alt_pressed, does_lighten, multiplayer, multiplayer_role

	create_new_world_button = Button(Width // 2, 130, textInfo.render(t("Create world"), True, menu_color_medium), textInfo.render(t("Create world"), True, menu_color_dark), alignment=True)
	enter_another_game_button = Button(Width // 2, 130, textInfo.render("Подключиться в мир хоста", True, menu_color_medium), textInfo.render("Подключиться в мир хоста", True, menu_color_dark), alignment=True)
	single_player_button = Button(Width // 4, 50, textInfo.render(t("Single play"), True, menu_color_medium), textInfo.render(t("Single play"), True, menu_color_dark), alignment=True)
	multiplayer_button = Button(Width * 3 // 4, 50, textInfo.render(t("Multiplayer"), True, menu_color_medium), textInfo.render(t("Multiplayer"), True, menu_color_dark), alignment=True)
	back_button = Button(-20, -20, load(path + "Images/Buttons/Back.png", 128), load(path + "Images/Buttons/Back 2.png", 128, 128))
	page = 1
	world_name_input = False
	does_lighten = False
	bias = 0

	win_darken(win)

	inside_folders = []	
	for dirs, folder, files in os.walk(path + "Saves/Worlds/"):
		inside_folders = folder
		break

	inside_folders.sort()
	release = False

	while True:

		mouse_x, mouse_y = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		release = False
		dt = clock.tick(MAX_FPS) / 1000.0
		events = pygame.event.get()
		for event in events:

			if event.type == pygame.QUIT:
				win_darken(win)
				sys.exit()

			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					release = True
			elif event.type == pygame.MOUSEWHEEL:
				bias = (min(bias + event.y * Settings["Game"][2], 0))

			if event.type == pygame.KEYUP:
				if event.key == hot_keys["Show keys"]:
					alt_pressed = not alt_pressed
				if event.key == hot_keys["Close"]:
					if world_name_input:
						input_system.stop_input()
						world_name_input = False
					else:
						win_darken(win)
						menu()

		win.fill(menu_color_light)

		if world_name_input:
			text(t("Enter world name:"), Width // 2, Height // 2 - 20, menu_color_medium, alignment=True)
			if not input_system.inputting:
				world_name = input_system.last_text
				edit_world()
		else:

			if create_new_world_button.get_pressed():
				input_system.start_input("World name", Width // 2, Height // 2 + 20, text_alignment=True)
				world_name_input = True
			
			if back_button.get_pressed():
				input_system.stop_input()
				win_darken(win)
				menu()

			if len(inside_folders) == 0:
				pass #TODO надпись что типа нет миров ещё
			else:

				for temp_y, name_of_world in enumerate(inside_folders):

					text_y = 150 + bias + temp_y * 50

					win.blit(textInfo.render(name_of_world, True, menu_color_medium), (50, text_y))

					if 50 + textInfo.size(name_of_world)[0] <= mouse_x <= 82 + textInfo.size(name_of_world)[0] and text_y <= mouse_y <= text_y + 32:
						win.blit(load(path + "Images/Buttons/Edit 2.png", 32), (50 + textInfo.size(name_of_world)[0], text_y))
						if release:
							world_name = name_of_world
							win_darken(win)
							edit_world()

					if 50 <= mouse_x <= 50 + textInfo.size(name_of_world)[0] and text_y <= mouse_y <= text_y + textInfo.size(name_of_world)[1]:

						win.blit(textInfo.render(name_of_world, True, menu_color_dark), (50, text_y))
						
						win.blit(load(path + "Images/Buttons/Edit.png", 32), (50 + textInfo.size(name_of_world)[0], text_y))
						
						if release:
							if multiplayer:
								world_name = name_of_world
								multiplayer_role = "Host"
								win_darken(win)
								multiplayer_settings_menu()
							else:
								world_name = name_of_world
								start_game()
			
			pygame.draw.rect(win, menu_color_light, (0, 0, Width, 103))
			pygame.draw.line(win, menu_color_medium, (0, 103), (Width, 103), 8)
			pygame.draw.line(win, menu_color_medium, (Width // 2, 0), (Width // 2, 103), 8)
			back_button.main()
			if multiplayer:
				single_player_button.main()
				if single_player_button.get_pressed():
					multiplayer = False
				win.blit(textInfo.render(t("Multiplayer"), True, menu_color_dark), (Width * 3 // 4 - textInfo.size(t("Multiplayer"))[0] // 2, 50 - textInfo.size(t("Multiplayer"))[1] // 2))
				enter_another_game_button.main()
				if enter_another_game_button.get_pressed():
					multiplayer_role = "Client"
					win_darken(win)
					multiplayer_settings_menu()
			else:
				win.blit(textInfo.render(t("Single play"), True, menu_color_dark), (Width // 4 - textInfo.size(t("Single play"))[0] // 2, 50 - textInfo.size(t("Single play"))[1] // 2))
				multiplayer_button.main()
				if multiplayer_button.get_pressed():
					multiplayer = True
				create_new_world_button.main()
		
		input_system.handle_input(events)
		if alt_pressed: draw_key("ESC", 44, 108)
		
		animate_click(dt, mouse_x, mouse_y)

		win_fill(alpha=100 - Settings["Display"][0])   # Если в настройках установлена яркость ниже 100, то экран становится темнее
		if not does_lighten:
			win_lighten(win)
			does_lighten = True
		
		pygame.display.update()



# Меню

def menu():
	
	global win, screenmode, num, does_lighten

	play_button = Button(Width / 2, Height / 2 - 150, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Play.png"), (264, 128)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Play 2.png"), (264, 128)), alignment=True, info="Подсказка: вы можете нажать enter, чтобы сразу начать игру.", action=worlds)
	settings_button = Button(Width / 2, Height / 2, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Settings.png"), (488, 128)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Settings 2.png"), (488, 128)), alignment=True, action=settings)
	change_a_character_button = Button(Width / 2, Height / 2 + 150, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Change a character.png"), (960, 128)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Change a character 2.png"), (960, 128)), alignment=True, action=change_a_character)

	version = f"Version {open(path + 'Version.txt').read()} (Build {str(get_build_number())})"
	more_menu_open = False
	does_lighten = False

	while True:
		
		mouse_x, mouse_y = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		release = False
		dt = clock.tick(MAX_FPS) / 1000.0

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				save()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				release = True
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_RETURN:
					worlds()
				if event.key == hot_keys["Close"]:
					more_menu_open = False
				if event.key == hot_keys["Change screen"]:
					if screenmode == "FULLSCREEN":
						win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
						screenmode = "RESIZABLE"
						play_button.x = 500
						play_button.y = 200
						settings_button.x = 500
						settings_button.y = 350
						change_a_character_button.x = 500
						change_a_character_button.y = 500
					else:
						win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
						screenmode = "FULLSCREEN"
						play_button.x = Width / 2
						play_button.y = Height / 2 - 150
						settings_button.x = Width / 2
						settings_button.y = Height / 2
						change_a_character_button.x = Width / 2
						change_a_character_button.y = Height / 2 + 150

		win.blit(Screensaver2, (0, 0))

		if not more_menu_open:
			play_button.main()
			settings_button.main()
			change_a_character_button.main()
		
		text(version, 5, Height - 30, (255, 255, 255))

		win.blit(load(path + "Images/Discord logo.png", 108, 81), (Width - 90, Height - 80))
		if mouse_x > Width - 70 and mouse_y > Height - 80:
			win_fill()
			if click[0]:
				import webbrowser
				webbrowser.open("https://discord.com/invite/aQNgcCQkHc")
				del webbrowser
				break
			
		if Width - 140 < mouse_x < Width - 76 and Height - 70 < mouse_y < Height - 6:
			win.blit(pygame.transform.scale(load(path + "Images/Buttons/More 2.png"), 64), (Width - 140, Height - 70))

			if release:
				more_menu_open = not more_menu_open
				
		else:
			win.blit(load(path + "Images/Buttons/More.png", 64), (Width - 140, Height - 70))

		if more_menu_open:
			
			pygame.draw.rect(win, menu_color_light, (100, 100, Width - 200, Height - 200))
			pygame.draw.rect(win, menu_color_dark, (100, 100, Width - 200, Height - 200), 10)
			pygame.draw.rect(win, menu_color_medium, (110, 110, Width - 220, Height - 220), 10)
			
			win.blit(load(path + "Images/Telegram logo.png", 100), (200, Height // 2 + 50))
			text("Telegram\n@Gannitto", 250, Height // 2 + 180, menu_color_medium, alignment=True)
			
			win.blit(load(path + "Images/Discord logo.png", 200, 150), (Width // 2 - 100, Height // 2 + 30))
			text("Discord\nGannitto#0694", Width // 2, Height // 2 + 180, menu_color_medium, alignment=True)
			
			win.blit(load(path + "Images/Gmail logo.png", 100, 100), (Width - 300, Height // 2 + 50))
			text("Gmail", Width - 250, Height // 2 + 180, menu_color_medium, alignment=True)
			text("danilaserezhin@gmail.com", Width - 250, Height // 2 + 200, menu_color_medium, 16, True)
			
			win.blit(load(path + "Images/Rickrolling QR-code.png"), (Width // 2 - 100, Height // 2 - 200))
			text(t("You can get other information from this QR code"), Width // 2, Height // 2 + 10, menu_color_medium, alignment=True)

		animate_click(dt, mouse_x, mouse_y)

		win_fill(alpha=100 - Settings["Display"][0])   # Если в настройках установлена яркость ниже 100, то экран становится темнее

		if not does_lighten:
			win_lighten(win)
			does_lighten = True

		pygame.display.update()



def show_intro():
	
	if Settings["Display"][10]:
		
		# import cv2
		# video = cv2.VideoCapture(path + "Intro.mp4")
		# success, video_image = video.read()
		
		# while success:
		#	for event in pygame.event.get():
		#		if event.type == pygame.QUIT:
		#			run = False
	
		#	success, video_image = video.read()
		#	if success:
		#		video_surf = pygame.image.frombuffer(
		#			video_image.tobytes(), 
		#			video_image.shape[1::-1], 
		#			"BGR"
		#		)	
		#	else:
		#		run = False
		#	win.blit(pygame.transform.scale(video_surf, (Width, Height)), (0, 0))
		#	pygame.display.flip()
		#	clock.tick(20)
		pass
	if Settings["User"][1]:
		menu()
	else:
		try:
			menu()
		except Exception as e:
			music_channel.stop()
			if multiplayer:
				net.disconnect()
			show_error_window(e)

if __name__ == "__main__":
	show_intro()

