import pygame
import subprocess
import pyperclip
from pathlib import Path
import time
import random
import numpy as np
import math
from itertools import product
import socket
import sys
import os
import Backrooms
from Ron import Ron
import Saver
from Functions import *
from Build import build, check_build_objects, draw_select_image, draw_select_image_arbitrarily
from Chunks import ChunkManager
from Inventory import inventory
from Translator import translator
from Cache import TextureCache
from SettingsUI import SettingsUI
from GameTime import GameTime
from Commands import command_system
from Globals import *
from Light import create_light_circle, create_light_circle_with_falloff, remove_light_circle

pygame.init()

"""
Чтобы найти что-то на карте кода, просто вбейте в поиск

Карта кода:

Текстуры
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

def text(
		text: str,
		text_x: int,
		text_y: int,
		color: tuple=text_color,
		size: int=20,
		alignment: bool=False,
		letter_spasing: int=10,
		surface: pygame.Surface=win,
		max_width: int=0,
		max_height: int=0,
		return_surface: bool=False,
		spase_between_strings: int=10
		):
	
	"""
	Выводит текст на экран
	Аргументы:
	text - Сам текст
	text_x, text_y - Координаты текста
	color - Цвет текста
	size - Размер шрифта
	alignment - Выравнивание текста по центру
	letter_spasing - Размер пробела
	surface - Поверхность, на которой будет текст
	max_width - Максимальная длина текста
	return_surface - Выводить ли текст на экран или методом return
	"""
	
	pos = (text_x, text_y)
	text = text.replace("\t\t", "")
	X, Y = pos
	
	if max_width == 0:
		max_width = surface.get_size()[0] - 10
	if max_height == 0:
		max_height = surface.get_size()[1] - 10

	all_text_surface = pygame.Surface((max_width, max_height), pygame.SRCALPHA)

	temp_font = pygame.font.Font(path + "Font.ttf", size)

	for line in (word.split(" ") for word in text.splitlines()):
		
		line_surface = pygame.Surface((max_width, size), pygame.SRCALPHA)
		TextX = 0

		for word in line:

			word_surface = temp_font.render(word, True, color)
			word_width, word_height = word_surface.get_size()
			if TextX + word_width >= max_width:
				surface.blit(line_surface, (X - TextX // 2 if alignment else X, Y))
				line_surface = pygame.Surface((max_width, size), pygame.SRCALPHA)
				TextX = 0
				Y += word_height + spase_between_strings
			
			line_surface.blit(word_surface, (TextX, 0))
			TextX += word_width + letter_spasing

		if return_surface:
			all_text_surface.blit(line_surface, (X - TextX // 2 if alignment else X, Y))
		else:
			surface.blit(line_surface, (X - TextX // 2 if alignment else X, Y))
		Y += word_height + spase_between_strings

	return all_text_surface

def get_text_height(
		text: str,
		size: int=20,
		letter_spasing: int=10,
		max_width: int=0,
		spase_between_strings: int=10
		) -> int:
	
	"""
	Возвращает ширину текста
	Аргументы:
	text - Сам текст
	size - Размер шрифта
	letter_spasing - Размер пробела
	max_width - Максимальная длина текста
	space_between_strings - Расстояние между строками
	"""
	
	text = text.replace("\t\t", "")
	tempTextInfo = pygame.font.Font(path + "Font.ttf", size)
	text_height = 0

	for line in (word.split(" ") for word in text.splitlines()):
		TextX = 0
		text_height += size - 2 + spase_between_strings
		for word in line:
			word_width = tempTextInfo.size(word)[0]
			if TextX + word_width >= Width // 3:
				TextX = 0
				text_height += size - 2 + spase_between_strings
			TextX += word_width + 10

	return text_height

def save(darken:bool=True, save_world_settings:bool=False):

	"""
	Сохраняет игру
	darken - Затемнять ли экран
	save_world_settings - Сохранять ли настройки мира
	"""

	global player
	Saver.save_objects(path + "Settings/Statistics.save", statistics)
	
	if world_name is not None:
		
		if multyplayer:
			another_players = []
			for player in ...:
				another_players.append(...)   # TODO
				another_players.append(...)
				
		else:
			
			Saver.save_objects(path + "Worlds/" + world_name + "/Mobs.save", world.mobs)
			Saver.save_objects(path + "Worlds/" + world_name + "/Info.save", [player.x, player.y, Backrooms.InBackrooms, Backrooms.Level, world.current_cave, player.speed, player.HP, start_time, ron.x, ron.y, ron.home, ron.inventory, world.chunk_manager.generator.seed, game_time.current_time])
			Saver.save_objects(path + "Worlds/" + world_name + "/Inventory.save", inventory.whole_inventory)
			Saver.save_objects(path + "Worlds/" + world_name + "/Resources.save", inventory.resources)
			Saver.save_objects(path + "Worlds/" + world_name + "/Effects.save", player.effects)

			new_particles = []
			particle_count = 1
			for particle in new_particles:
				if particle.save_particle:
					pygame.image.save(particle.image, path + "Worlds/" + world_name +"/Images/Particle " + str(particle_count) + ".png")
					particle.image_path = path + "Worlds/Images/Particle " + str(particle_count) + ".png"
					particle_count += 1
					new_particles.append(particle)
			Saver.save_objects(path + "Worlds/" + world_name + "/Particles.save", new_particles)
			world.chunk_manager.save_all_loaded_chunks()
				
	if darken and Settings["Display"][9]:
		win_darken(win)
		
	if save_world_settings: Saver.save_objects(path + "Worlds/" + world_name + "/Settings.save", [game.difficulty, player.god_mode])

# Применение настроек TODO

# Текстуры

statistics[0] += 1

pygame.display.set_icon(pygame.image.load(path + "Images/Icon.png"))
pygame.display.set_caption("Gannitto World")

arrow_down = pygame.transform.scale(pygame.image.load(path + "Images/DOWN.png"), (64, 64))
arrow_left = pygame.transform.scale(pygame.image.load(path + "Images/LEFT.png"), (64, 64))
arrow_right = pygame.transform.scale(pygame.image.load(path + "Images/RIGHT.png"), (64, 64))
arrow_up = pygame.transform.scale(pygame.image.load(path + "Images/UP.png"), (64, 64))

Inventory_slot = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Inventory slot.png"), (64, 64))
Changed_inventory_slot = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Inventory slot 2.png"), (64, 64))

Craft_list_inventory_slot = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Craft list slot.png"), (64, 64))
Changed_craft_list_inventory_slot = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Craft list slot 2.png"), (64, 64))

Object_inventory_slot = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Object inventory slot 2.png"), (64, 64))

Tool_inventory_slot = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Tool inventory slot 2.png"), (64, 64))

Split_items1 = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Split items.png"), (64, 64))
Split_items2 = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Split items 2.png"), (64, 64))

Compact_inventory1 = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Compact inventory.png"), (64, 64))
Compact_inventory2 = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Compact inventory 2.png"), (64, 64))

Craft_list_slot1 = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Craft list slot.png"), (64, 64))
Craft_list_slot2 = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Craft list slot 2.png"), (64, 64))

Game_menu_slot1 = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Game menu slot.png"), (64, 64))
Game_menu_slot2 = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Game menu slot 2.png"), (64, 64))

Menu_slot1 = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Menu slot.png"), (64, 64))
Menu_slot2 = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Menu slot 2.png"), (64, 64))

Multyplayer_slot1 = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Multyplayer slot.png"), (64, 64))
Multyplayer_slot2 = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Multyplayer slot 2.png"), (64, 64))

Close_slot1 = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Close slot.png"), (64, 64))
Close_slot2 = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Close slot 2.png"), (64, 64))

Reference_slot1 = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Reference slot.png"), (64, 64))
Reference_slot2 = pygame.transform.scale(pygame.image.load(path + "Images/Slots/Reference slot 2.png"), (64, 64))

Inventory_slot.set_alpha(Settings["Display"][1])
Changed_inventory_slot.set_alpha(Settings["Display"][1])
Craft_list_inventory_slot.set_alpha(Settings["Display"][1])
Changed_craft_list_inventory_slot.set_alpha(Settings["Display"][1])
Object_inventory_slot.set_alpha(Settings["Display"][1])
Tool_inventory_slot.set_alpha(Settings["Display"][1])
Split_items1.set_alpha(Settings["Display"][1])
Split_items2.set_alpha(Settings["Display"][1])
Compact_inventory1.set_alpha(Settings["Display"][1])
Compact_inventory2.set_alpha(Settings["Display"][1])
Craft_list_slot1.set_alpha(Settings["Display"][1])
Craft_list_slot2.set_alpha(Settings["Display"][1])
Game_menu_slot1.set_alpha(Settings["Display"][1])
Game_menu_slot2.set_alpha(Settings["Display"][1])
Menu_slot1.set_alpha(Settings["Display"][1])
Menu_slot2.set_alpha(Settings["Display"][1])
Multyplayer_slot1.set_alpha(Settings["Display"][1])
Multyplayer_slot2.set_alpha(Settings["Display"][1])
Close_slot1.set_alpha(Settings["Display"][1])
Close_slot2.set_alpha(Settings["Display"][1])
Reference_slot1.set_alpha(Settings["Display"][1])
Reference_slot2.set_alpha(Settings["Display"][1])

Portal_1 = pygame.image.load(path + "Images/Objects/Portal 1.png")
Portal_1 = pygame.transform.scale(Portal_1, (128, 256))
Portal_2 = pygame.image.load(path + "Images/Objects/Portal 2.png")
Portal_2 = pygame.transform.scale(Portal_2, (128, 256))

Vending_machine_image = pygame.transform.scale(pygame.image.load(path + "Images/Objects/Vending machine.png"), (304, 560))

Wire_1 = pygame.image.load(path + "Images/Objects/Wire 1.png")
Wire_1 = pygame.transform.scale(Wire_1, (64, 64))
Wire_2 = pygame.image.load(path + "Images/Objects/Wire 2.png")
Wire_2 = pygame.transform.scale(Wire_2, (64, 64))
Wire_3 = pygame.image.load(path + "Images/Objects/Wire 3.png")
Wire_3 = pygame.transform.scale(Wire_3, (64, 64))
Wire_4 = pygame.image.load(path + "Images/Objects/Wire 4.png")
Wire_4 = pygame.transform.scale(Wire_4, (64, 64))
Wire_5 = pygame.image.load(path + "Images/Objects/Wire 5.png")
Wire_5 = pygame.transform.scale(Wire_5, (64, 64))
Wire_6 = pygame.image.load(path + "Images/Objects/Wire 6.png")
Wire_6 = pygame.transform.scale(Wire_6, (64, 64))
Wire_7 = pygame.image.load(path + "Images/Objects/Wire 7.png")
Wire_7 = pygame.transform.scale(Wire_7, (64, 64))
Wire_8 = pygame.image.load(path + "Images/Objects/Wire 8.png")
Wire_8 = pygame.transform.scale(Wire_8, (64, 64))
Wire_9 = pygame.image.load(path + "Images/Objects/Wire 9.png")
Wire_9 = pygame.transform.scale(Wire_9, (64, 64))
Wire_10 = pygame.image.load(path + "Images/Objects/Wire 10.png")
Wire_10 = pygame.transform.scale(Wire_10, (64, 64))
Wire_11 = pygame.image.load(path + "Images/Objects/Wire 11.png")
Wire_11 = pygame.transform.scale(Wire_11, (64, 64))

Random_box_1 = pygame.image.load(path + "Images/Objects/Random Box 1.png")
Random_box_1 = pygame.transform.scale(Random_box_1, (64, 64))
Random_box_2 = pygame.image.load(path + "Images/Objects/Random Box 2.png")
Random_box_2 = pygame.transform.scale(Random_box_2, (64, 64))
Random_box_3 = pygame.image.load(path + "Images/Objects/Random Box 3.png")
Random_box_3 = pygame.transform.scale(Random_box_3, (64, 64))
Random_box_4 = pygame.image.load(path + "Images/Objects/Random Box 4.png")
Random_box_4 = pygame.transform.scale(Random_box_4, (64, 64))

Slime1 = pygame.image.load(path + "Images/Objects/Blue Slime 1.png")
Slime1 = pygame.transform.scale(Slime1, (128, 128))
Slime1_2 = pygame.image.load(path + "Images/Objects/Blue Slime 2.png")
Slime1_2 = pygame.transform.scale(Slime1_2, (128, 128))
Slime1_3 = pygame.image.load(path + "Images/Objects/Blue Slime 3.png")
Slime1_3 = pygame.transform.scale(Slime1_3, (128, 128))
Slime1_4 = pygame.image.load(path + "Images/Objects/Blue Slime 4.png")
Slime1_4 = pygame.transform.scale(Slime1_4, (128, 128))
Slime2 = pygame.image.load(path + "Images/Objects/Pink Slime 1.png")
Slime2 = pygame.transform.scale(Slime2, (128, 128))
Slime2_2 = pygame.image.load(path + "Images/Objects/Pink Slime 2.png")
Slime2_2 = pygame.transform.scale(Slime2_2, (128, 128))
Slime2_3 = pygame.image.load(path + "Images/Objects/Pink Slime 3.png")
Slime2_3 = pygame.transform.scale(Slime2_3, (128, 128))
Slime2_4 = pygame.image.load(path + "Images/Objects/Pink Slime 4.png")
Slime2_4 = pygame.transform.scale(Slime2_4, (128, 128))


SLIME_TYPES = {
	1: [Slime1, Slime1_2, Slime1_3, Slime1_4],
	2: [Slime2, Slime2_2, Slime2_3, Slime2_4]
}

Butterfly1 = pygame.image.load(path + "Images/Objects/Butterfly 1 1.png")
Butterfly1 = pygame.transform.scale(Butterfly1, (32, 32))
Butterfly1_2 = pygame.image.load(path + "Images/Objects/Butterfly 1 2.png")
Butterfly1_2 = pygame.transform.scale(Butterfly1_2, (32, 32))
Butterfly1_3 = pygame.image.load(path + "Images/Objects/Butterfly 1 3.png")
Butterfly1_3 = pygame.transform.scale(Butterfly1_3, (32, 32))

web_texture = pygame.transform.scale(pygame.image.load(path + "Images/Objects/Piece of web.png"), (128, 128))
explosion_texture = pygame.transform.scale(pygame.image.load(path + "Images/Objects/Explosion.png"), (128, 128))

Bacteria_walk_left = (

	pygame.transform.scale(pygame.image.load(path + "Images/Objects/Bacteria 1.png"), (256, 512)),
	pygame.transform.scale(pygame.image.load(path + "Images/Objects/Bacteria 2.png"), (256, 512)),
	pygame.transform.scale(pygame.image.load(path + "Images/Objects/Bacteria 3.png"), (256, 512)),
	pygame.transform.scale(pygame.image.load(path + "Images/Objects/Bacteria 4.png"), (256, 512)),
	pygame.transform.scale(pygame.image.load(path + "Images/Objects/Bacteria 5.png"), (256, 512)),
	pygame.transform.scale(pygame.image.load(path + "Images/Objects/Bacteria 6.png"), (256, 512))

	)

Screensaver2 = pygame.image.load(path + "Images/Screensavers/Screensaver 2.png")
Screensaver2 = pygame.transform.scale(Screensaver2, (Height * 2, Height))

Heart = pygame.transform.scale(pygame.image.load(path + "Images/Heart.png"), (32, 32))

wall_types = ("Wooden wall", "Brick wall", "Stone brick wall")
door_types = ("Wooden door",)
wall_images = {}

for wall_type in wall_types:
	wall_images[wall_type] = (
		pygame.transform.scale(pygame.image.load(path + "Images/Objects/" + wall_type + " 1.png"), (256, 256)),
		pygame.transform.scale(pygame.image.load(path + "Images/Objects/" + wall_type + " 2.png"), (256, 256)),
		pygame.transform.scale(pygame.image.load(path + "Images/Objects/" + wall_type + " 3.png"), (256, 256)),
		pygame.transform.scale(pygame.image.load(path + "Images/Objects/" + wall_type + " 4.png"), (256, 256)),
		pygame.transform.scale(pygame.image.load(path + "Images/Objects/" + wall_type + " 5.png"), (256, 256)),
		pygame.transform.scale(pygame.image.load(path + "Images/Objects/" + wall_type + " 6.png"), (256, 256)),
		pygame.transform.scale(pygame.image.load(path + "Images/Objects/" + wall_type + " 7.png"), (256, 256)),
		pygame.transform.scale(pygame.image.load(path + "Images/Objects/" + wall_type + " 8.png"), (256, 256)),
		pygame.transform.scale(pygame.image.load(path + "Images/Objects/" + wall_type + " 9.png"), (256, 256)),
		pygame.transform.scale(pygame.image.load(path + "Images/Objects/" + wall_type + " 10.png"), (256, 256)),
		pygame.transform.scale(pygame.image.load(path + "Images/Objects/" + wall_type + " 11.png"), (256, 256))
	)

for door_type in door_types:
	wall_images[door_type] = (
		pygame.transform.scale(pygame.image.load(path + "Images/Objects/" + door_type + " 1.png"), (256, 256)),
		pygame.transform.scale(pygame.image.load(path + "Images/Objects/" + door_type + " 2.png"), (256, 256)),
		pygame.transform.scale(pygame.image.load(path + "Images/Objects/" + door_type + " 1 Open.png"), (256, 256)),
		pygame.transform.scale(pygame.image.load(path + "Images/Objects/" + door_type + " 2 Open.png"), (256, 256))
	)

farmland_images = (pygame.transform.scale(pygame.image.load(path + "Images/Objects/Farmland.png"), (128, 128)),)

textures = {

	"Forest": pygame.transform.scale(pygame.image.load(path + "Images/Bioms/Forest.png"), (256, 256)),
	"Desert": pygame.transform.scale(pygame.image.load(path + "Images/Bioms/Desert.png"), (256, 256)),
	"Field": pygame.transform.scale(pygame.image.load(path + "Images/Bioms/Field.png"), (256, 256)),
	"Taiga": pygame.transform.scale(pygame.image.load(path + "Images/Bioms/Taiga.png"), (256, 256)),
	"Swamp": pygame.transform.scale(pygame.image.load(path + "Images/Bioms/Swamp.png"), (256, 256)),
	"Backrooms 0": pygame.transform.scale(pygame.image.load(path + "Images/Bioms/Backrooms 0.png"), (256, 256)),
	"Backrooms 0.2": pygame.transform.scale(pygame.image.load(path + "Images/Bioms/Backrooms 0.2.png"), (256, 256)),
	"Backrooms 1": pygame.transform.scale(pygame.Surface((256, 256)), (256, 256)),

	}

Backrooms_portal_images = (
	pygame.transform.scale(pygame.image.load(path + "Images/Objects/Backrooms portal 1.png"), (256, 256)),
	pygame.transform.scale(pygame.image.load(path + "Images/Objects/Backrooms portal 2.png"), (256, 256)),
	pygame.transform.scale(pygame.image.load(path + "Images/Objects/Backrooms portal 3.png"), (256, 256)),
	pygame.transform.scale(pygame.image.load(path + "Images/Objects/Backrooms portal 4.png"), (256, 256)),
	pygame.transform.scale(pygame.image.load(path + "Images/Objects/Backrooms portal 5.png"), (256, 256)),
	pygame.transform.scale(pygame.image.load(path + "Images/Objects/Backrooms portal 6.png"), (256, 256)),
	pygame.transform.scale(pygame.image.load(path + "Images/Objects/Backrooms portal 7.png"), (256, 256)),
	pygame.transform.scale(pygame.image.load(path + "Images/Objects/Backrooms portal 8.png"), (256, 256)),
	pygame.transform.scale(pygame.image.load(path + "Images/Objects/Backrooms portal 9.png"), (256, 256)),
	pygame.transform.scale(pygame.image.load(path + "Images/Objects/Backrooms portal 10.png"), (256, 256))
)

no_file_texture = pygame.transform.scale(pygame.image.load(path + "Images/No-file texture.png"), (64, 64))

Button_click = pygame.mixer.Sound(path + "Sounds/Button Pressed.mp3")
Stone_breaking1 = pygame.mixer.Sound(path + "Sounds/Stone breaking 1.mp3")
Stone_breaking2 = pygame.mixer.Sound(path + "Sounds/Stone breaking 2.mp3")
Grass_walking1 = pygame.mixer.Sound(path + "Sounds/Grass walking 1.mp3")
Grass_walking2 = pygame.mixer.Sound(path + "Sounds/Grass walking 2.mp3")
Grass_walking3 = pygame.mixer.Sound(path + "Sounds/Grass walking 3.mp3")
Snow_walking1 = pygame.mixer.Sound(path + "Sounds/Snow walking 1.mp3")
Snow_walking2 = pygame.mixer.Sound(path + "Sounds/Snow walking 2.mp3")
Snow_walking3 = pygame.mixer.Sound(path + "Sounds/Snow walking 3.mp3")
Sand_walking1 = pygame.mixer.Sound(path + "Sounds/Sand walking 1.mp3")
Sand_walking2 = pygame.mixer.Sound(path + "Sounds/Sand walking 2.mp3")
Sand_walking3 = pygame.mixer.Sound(path + "Sounds/Sand walking 3.mp3")
Swamp_walking1 = pygame.mixer.Sound(path + "Sounds/Swamp walking 1.mp3")
Swamp_walking2 = pygame.mixer.Sound(path + "Sounds/Swamp walking 2.mp3")
Swamp_walking3 = pygame.mixer.Sound(path + "Sounds/Swamp walking 3.mp3")
Cave_walking1 = pygame.mixer.Sound(path + "Sounds/Cave walking 1.mp3")
Cave_walking2 = pygame.mixer.Sound(path + "Sounds/Cave walking 2.mp3")
Cave_walking3 = pygame.mixer.Sound(path + "Sounds/Cave walking 3.mp3")
Backrooms_lamps = pygame.mixer.Sound(path + "Sounds/Backrooms/1.mp3")
Backrooms_rand_sound_1 = pygame.mixer.Sound(path + "Sounds/Backrooms/Random Sounds/1.mp3")
Pick_an_item = pygame.mixer.Sound(path + "Sounds/Pick an item.mp3")

music_channel = pygame.mixer.Channel(1)
music_channel.set_volume(Settings["Sound"][0], Settings["Sound"][0])

colors = {
	"Normal": (39, 155, 80),
	"Normal2": (0, 255, 0),
	"Backrooms": (100, 100, 0),
	"Backrooms2": (100, 80, 0)
}



# Классы

class Player:

	def __init__(self, X=0, Y=0):

		self.x = X
		self.y = Y
		self.speed = 50
		
		# Анимация
		self.direction = "Down"
		self.frame_index = 0
		self.animation_speed = 0.05  # Скорость анимации (секунды между кадрами)
		self.animation_timer = 0
		self.move_timer = 0
		self.costum = 0
		directions = ("Down", "Up", "Left", "Right", "Down-left", "Down-right", "Up-left", "Up-right")
		self.animations = {}
		
		for direction in directions:

			frames = []
			for frame_num in range(1, 7):
				path_to_image = f"{path}Images/Players/Hiro/Normal/{direction}/{frame_num}.png"
				frames.append(pygame.transform.scale(pygame.image.load(path_to_image), (256, 256)))	
			self.animations[direction] = frames

		# Игровые параметры
		self.HP = 100
		self.HP_TICK = 90
		self.HP_animation_tick = 0
		self.effects = []
		self.god_mode = False
		self.pass_through_walls = False # TODO
		self.is_moving = False
		self.rect = pygame.Rect(self.x - 25, self.y - 112, 50, 224)
		self.hovered_object = None
		self.breaking_object = None
		
		# Текущий спрайт
		self.image = self.get_current_frame()
		
	def get_current_frame(self):
		"""Возвращает текущий кадр анимации"""
		frames = self.animations[self.direction]
		return frames[self.frame_index % len(frames)]
	
	def update_animation(self, dt):
		"""Обновляет анимацию на основе времени"""
		if self.is_moving:
			self.animation_timer += dt
			
			# Если прошло достаточно времени, кадр меняется
			if self.animation_timer >= self.animation_speed:
				self.animation_timer = 0
				self.frame_index += 1
		
		self.image = self.get_current_frame()

	def collides_with_walls(self):
		"""Проверяет, пересекается ли игрок с какой-либо стеной."""
		if self.pass_through_walls:
			return False
		self.rect = pygame.Rect(self.x - 25, self.y - 112, 50, 224)
		return check_collision(self.rect, world)

	def move(self, dx, dy, dt):
		"""Двигает игрока и обновляет направление"""

		self.is_moving = True

		# Обновление позиции

		self.x += dx * self.speed * dt * 30
		if self.collides_with_walls():
			self.x -= dx * self.speed * dt * 30

		self.y += dy * self.speed * dt * 30
		if self.collides_with_walls():
			self.y -= dy * self.speed * dt * 30
		
		# Определение направления
		if dx > 0 and dy == 0:
			self.direction = "Right"
		elif dx < 0 and dy == 0:
			self.direction = "Left"
		elif dy > 0 and dx == 0:
			self.direction = "Up"
		elif dy < 0 and dx == 0:
			self.direction = "Down"
		elif dx > 0 and dy > 0:
			self.direction = "Up-right"
		elif dx < 0 and dy > 0:
			self.direction = "Up-left"
		elif dx > 0 and dy < 0:
			self.direction = "Down-right"
		elif dx < 0 and dy < 0:
			self.direction = "Down-left"
	
	def stop(self):
		"""Останавливает движение"""
		self.is_moving = False
		self.frame_index = 0
		self.animation_timer = 0
		self.move_timer = 0
	
	def render(self, screen, dx, dy):
		"""Отрисовывает игрока на экране"""
		
		screen.blit(shadow(self.image, f"Player {self.direction} {self.frame_index}"), (Width / 2 - 128, Height / 2 - 128))
		
		if Settings["Display"][3]:
			self.rect = pygame.Rect(self.x - 25, self.y - 112, 50, 224)
			pygame.draw.rect(screen, (0, 255, 0), (Width / 2 - 128, Height / 2 - 128, self.image.get_width(), self.image.get_height()), 2)
			pygame.draw.rect(win, (0, 0, 0), (self.rect[0] - self.x + Width // 2, self.y - self.rect[1] - self.rect[3] + Height // 2, self.rect[2], self.rect[3]), 3)
	
player = Player()
world_to_screen = lambda X, Y, W, H, player=player: (X - player.x + Width // 2 - W // 2, player.y - Y + Height // 2 - H // 2)
world_rect_to_screen = lambda X, Y, W, H, player=player: (X - player.x + Width // 2 - W // 2, player.y - Y + Height // 2 - H // 2, W, H)

class Object:

	def __init__(self,
			  name: str,
			  object_x: int,
			  object_y: int,
			  image_path: str,
			  scale: tuple[int, int] = (64, 64),
			  image = None,
			  special_flags: str = None,
			  add_path=True,
			  start_time=None,
			  is_solid=False,
			  rect=(),
			  pickable=False,
			  breakable=False,
			  max_break=1,
			  breakable_by_hammer=False,
			  drop_items=()):

		"""
		Класс основного объекта игры. Такого, как например дерево.
		Аргументы:
		name - Имя объекта
		object_x - X объекта
		object_y - Y объекта
		image_path - Путь к изображению объекта
		scale - На сколько нужно изменить размер изображения объекта
		image - Изображение объекта
		special_flags - Специальные флаги объекта
		add_path - Добавлять ли путь до папки игры к путю до изображения
		start_time - Время, когда был создан объект
		rect - Хитбокс объекта
		pickable - Можно ли подобрать объект
		breakable - Можно ли сломать объект
		max_break - Сколько нужно ударов чтобы сломать
		breakable_by_hammer - Можно ли моментально сломать объект молотом
		drop_items - Предметы, которые дропаются из объекта (название, мин количество, макс количество)
		"""

		if start_time is None:
			self.start_time = time.time()
		else:
			self.start_time = start_time

		self.name = name
		self.x = object_x
		self.y = object_y

		if image is None:
			if add_path:
				self.image = TextureCache.get(path + image_path, scale)
			else:
				self.image = TextureCache.get(image_path, scale)
		else:
			self.image = pygame.transform.scale(image, (scale[0], scale[1]))

		self.image_path = image_path
		self.w = self.image.get_width()
		self.h = self.image.get_height()
		self.special_flags = special_flags
		self.add_path = add_path
		self.scale = scale
		self.is_solid = is_solid
		self.pickable = pickable
		self.breakable = breakable
		self.max_break = max_break
		self.breaked = max_break
		self.breakable_by_hammer = breakable_by_hammer
		self.drop_items = drop_items

		if rect == ():
			self.rect = pygame.Rect(self.x - self.w / 2, self.y - self.h / 2, self.w, self.h)
		else:
			self.rect = pygame.Rect(rect[0] + self.x, rect[1] + self.y, rect[2], rect[3])
	
	def main(self, dt):

		if player.hovered_object is None and self.get_hovered():
			player.hovered_object = self
			if self.breakable and pygame.mouse.get_pressed()[0]:

				player.breaking_object = self
				self.breaked -= dt * 100
				self.image = crack_surface(world, Particle, self, (self.max_break - self.breaked) // self.max_break, 8)

				if self.breaked < 1:

					destroy_object(self.image, self.x, self.y, world, Particle)
					world.chunk_manager.get_chunk_at(self.x, self.y).objects.remove(self)

					statistics[2] += 1
					for item_name, min_amount, max_amount in self.drop_items:
						for _ in range(random.randint(min_amount, max_amount)):
							rand_x, rand_y = self.x + random.randint(-self.w // 2, self.w // 2), self.y + random.randint(-self.h // 2, self.h // 2)
							world.chunk_manager.get_chunk_at(rand_x, rand_y).items.append(Object(item_name, rand_x, rand_y, f"Images/Items/{item_name}.png", pickable=True))

		if player.x - Width // 2 - self.w // 2 <= self.x <= player.x + Width // 2 + self.w // 2 and player.y - Height // 2 <= player.y + Height // 2:
			win.blit(self.image, world_to_screen(self.x, self.y, self.w, self.h, player))
		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), (*world_to_screen(self.rect[0] + self.w // 2, self.rect[1] + self.h // 2, self.rect[2], self.rect[3], player), self.rect[2], self.rect[3]), 3)

	def get_left_pressed(self):

		click = pygame.mouse.get_pressed()
		if click[0] and self.x - player.x + Width // 2 - self.image.get_width() // 2 <= mouse_x <= self.x - player.x + Width // 2 + self.w // 2 and player.y - self.y + Height // 2 - self.h // 2 <= mouse_y <= player.y - self.y + Height // 2 + self.h // 2:
			return True
		else:
			return False

	def get_right_pressed(self):

		click = pygame.mouse.get_pressed()
		if click[2] == 1 and self.x - player.x + Width // 2 - self.image.get_width() // 2 <= mouse_x <= self.x - player.x + Width // 2 + self.w // 2 and player.y - self.y + Height // 2 - self.h // 2 <= mouse_y <= player.y - self.y + Height // 2 + self.h // 2:
			return True
		else:
			return False

	def get_hovered(self):
		return pygame.Rect((*world_to_screen(self.rect[0] + self.w // 2, self.rect[1] + self.h // 2, self.rect[2], self.rect[3], player), self.rect[2], self.rect[3])).collidepoint(pygame.mouse.get_pos())

	def copy(self):
		return Object(self.name, self.x, self.y, self.image_path, self.scale, self.image, self.special_flags, self.add_path, self.start_time, self.is_solid, self.rect, self.is_solid, self.breakable, self.max_break, self.breakable_by_hammer, self.drop_items)

	
	def __getstate__(self):
		
		state = self.__dict__.copy()
		del state["image"]
		return state

	def __setstate__(self, state):
		
		self.__dict__.update(state)
		if self.add_path:
			self.image = TextureCache.get(path + self.image_path, self.scale)
		else:
			self.image = TextureCache.get(self.image_path, self.scale)

class Particle:

	def __init__(self,
				 start_x: int=0,
				 start_y: int=0,
				 image: pygame.Surface=no_file_texture.copy(),
				 x_bias=0, y_bias=0,
				 rotate: int=None,
				 display_mode=world_to_screen,
				 tick_command=None,
				 increased_transparency: int=0,
				 twisting_in_width: int=0, twisting_in_height: int=0,
				 remove_particle_after_twisting: bool=True,
				 track_ticks: bool=False,
				 del_self_condition=None,
				 can_interfere_with_placing: bool=False,
				 save_particle: bool=False,
				 save_start_time: bool=True,
				 start_time: float|None=None,
				 end_x: int=None, end_y: int=None,
				 end_zone: int=0, end_time: float=None,
				 end_command=None,
				 special_flags: list=[]):

		"""
		Частицы, с помощью которых можно сделать много всего
		
		Аргументы:
		start_x - Координата X, где появится частица
		start_y - Координата Y, где появится частица
		image - Изображение частицы, по умолчанию иконка файла без текстуры
		x_bias - Смещение по оси X
		y_bias - Смещение по оси Y
		rotate - Поворот частцы на каждом тике
		display_mode - Режим отображения частицы
		tick_command - Код, который будет срабатывать при каждом тике часлицы
		increased_transparency - Число, на которое будет уменьшаться прозрачность частицы, если нужно
		twisting_in_width - Сжимает изображение цастицы по длине
		twisting_in_height - Сжимает изображение частицы по ширине
		remove_particle_after_twisting - Удалить частицу после после полного скручивания
		track_ticks - Слитать ли каждый тик в переменную ticks после создания частицы
		del_self_condition - Условие, при котором удалится частица
		can_interfere_with_placing - Может ли частица мешать ставить объекты
		save_particle - Сохранять ли частицу после выхода из мира
		save_start_time - Сохранять ли параметр start_time после выхода из мира, если включён save_particle
		start_time - Время создания частицы. По умолчанию выставляется автоматически
		end_x - Координата X, при достижении которой частица пропадёт
		end_y - Координата Y, при достижении которой частица пропадёт
		end_zone - Если нужно, чтобы частица пропадала, когда она находится не именно на end_x и/или end_y, а на определённом растоянии или ближе, то можно использовать end_zone. За это расстояние этот аргумент и отвечает.
		end_time - Время, после которого частица пропадает
		end_command - Команда, которая будет срабатывать после удаления частицы
		special_flags - Специальные флаги частицы, с помощью которых можно реализовать её механики
		"""

		self.calculated_variable = 0   # Эта переменная должна быть в самом начале обязательно

		self.x = start_x
		self.y = start_y

		self.image = image
		self.w = self.image.get_width()
		self.h = self.image.get_height()
		self.x_bias = x_bias
		self.y_bias = y_bias
		self.rotate = rotate
		self.display_mode = display_mode
		
		self.tick_command = tick_command

		self.special_flags = special_flags
		self.increased_transparency = increased_transparency
		if self.increased_transparency > 0:
			self.image = self.image.convert_alpha()
		self.can_interfere_with_placing = can_interfere_with_placing
		
		self.twisting_in_width = twisting_in_width
		self.twisting_in_height = twisting_in_height
		self.remove_particle_after_twisting = remove_particle_after_twisting

		self.calculated_variable = 0
		
		self.track_ticks = track_ticks
		self.ticks = -1

		self.del_self_condition = del_self_condition
		
		self.save_particle = save_particle
		self.save_start_time = start_time

		self.end_x = end_x
		self.end_y = end_y
		self.end_zone = end_zone
		self.end_time = end_time
		self.end_command = end_command

		self.start_time = time.time()

		self.w, self.h = self.image.get_size()
	
	def __getstate__(self):
		
		state = self.__dict__.copy()
		del state["image"]
		return state

	def __setstate__(self, state):
		
		self.__dict__.update(state)
		self.image = pygame.transform.scale(pygame.image.load(self.image_path), (self.w, self.h))
	
	def main(self, dt):
		
		if self.tick_command is not None:
			self.tick_command(self)

		if self.track_ticks: self.ticks += 1
		if self.increased_transparency != 0:
			self.image.set_alpha(self.image.get_alpha() - self.increased_transparency * dt * 25)
		
		if self.twisting_in_width or self.twisting_in_height:
			try:
				self.image = pygame.transform.scale(
						self.image,
						(self.image.get_width() - self.twisting_in_width * dt * 100,
						self.image.get_height() - self.twisting_in_height * dt * 100)
						)
			except:
				if self.remove_particle_after_twisting:
					if self.end_command is not None: self.end_command(self)
					world.particles.remove(self)
					return
		if self.x_bias:
			self.x += dt * 25 * self.x_bias if self.x_bias.__class__ in (int, float) else self.x_bias(self)
		if self.y_bias:
			self.y += dt * 25 * self.y_bias if self.y_bias.__class__ in (int, float) else self.y_bias(self)

		if self.rotate is not None:
			image_rect = self.image.get_rect()
			rotated_image = pygame.transform.rotate(self.image, self.rotate)
			rect_copy = image_rect.copy()
			rect_copy.center = rotated_image.get_rect().center
			self.image = rotated_image.subsurface(rect_copy).copy()
			
		if (self.end_x is not None and self.end_y is None and self.end_x - self.end_zone <= self.x <= self.end_x + self.end_zone) or (self.end_y is not None and self.end_x is None and self.end_y - self.end_zone <= self.y <= self.end_y + self.end_zone) or (self.end_x is not None and self.end_y is not None and self.end_x - self.end_zone <= self.x <= self.end_x + self.end_zone and self.end_y - self.end_zone <= self.y <= self.end_y + self.end_zone):
			if self.end_command is not None: self.end_command(self)
			world.particles.remove(self)

		win.blit(self.image, (self.display_mode(self.x, self.y, self.w, self.h)))

		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), (self.display_mode(self.x, self.y, self.w, self.h)[0], self.display_mode(self.x, self.y, self.w, self.h)[1], self.w, self.h), 3)
	
class BaseEnemy:
	def __init__(self, x, y, HP, speed, animation_frames):
		self.x = x
		self.y = y
		self.HP = HP
		self.max_hp = HP
		self.speed = speed
		self.animation_frames = animation_frames
		self.animation_count = 0
		self.rect = animation_frames[0].get_rect()
		self.state = "Idle"  # Idle, Wonder, Jumping, Retreat
		self.attack_cooldown = 0
		self.detection_range = 1000
		self.attack_range = 200
		
	def update(self, player, world):
		"""Обновляет состояние моба"""
		self._update_animation()
		self._update_state(player, world)
		self._update_position(world)
		
	def _update_animation(self):
		self.animation_count = (self.animation_count + 1) % 20
		
	def _update_state(self, player, world):
		"""Определяет текущее состояние на основе расстояния до игрока"""
		distance = self._get_distance_to(player)
		
		if self.HP <= 0:
			self.state = "Dead"
		elif distance < self.attack_range:
			self.state = "Attacking"
			self._attack(player)
		elif distance < self.detection_range:
			self.state = "Chasing"
		else:
			self.state = "Idle"
			
	def _update_position(self, world):
		"""Обновляет позицию в зависимости от состояния"""
		if self.state == "chasing":
			self._move_towards_player(world)
		elif self.state == "idle":
			self._random_movement(world)
			
	def _move_towards_player(self, world):
		"""Движение к игроку с проверкой стен"""
		dx = player.x - self.x
		dy = player.y - self.y
		distance = math.sqrt(dx**2 + dy**2)
		
		if distance > 0:
			# Нормализуем вектор движения
			dx = dx / distance * self.speed
			dy = dy / distance * self.speed
			
			# Пробуем движение по X
			new_x = self.x + dx
			if not self._check_collision(new_x, self.y, world):
				self.x = new_x
				
			# Пробуем движение по Y
			new_y = self.y + dy
			if not self._check_collision(self.x, new_y, world):
				self.y = new_y

def check_collision(rect: pygame.Rect, world, only_solid=True, check_walls=True):
	"""Проверяет столкновение с твёрдыми объектами"""
	if check_walls:
		for wall in world.visible_walls.values():
			if rect.colliderect(wall.rect):
				return True
	for object in world.visible_objects:
		if (not only_solid or object.is_solid) and rect.colliderect(object.rect):
			return True
	return False

def check_projectiles_collision(rect: pygame.Rect, remove_projectile=True):

	for projectile in world.projectiles:
		if rect.collidepoint((projectile.x, projectile.y)):
			if remove_projectile:
				world.projectiles.remove(projectile)
			return True
	return False


class Slime(BaseEnemy):
	
	def __init__(self, x, y):

		slime_type = random.choice((1, 2))
		animation_frames = SLIME_TYPES[slime_type]
		self.name = "Slime"
		
		super().__init__(
			x=x, y=y,
			HP=50,
			speed=random.randint(10, 20),
			animation_frames=animation_frames
		)
		
		self.slime_type = slime_type
		self.state = "Wander"

		self.wander_radius = 1000
		self.wander_angle = random.uniform(0, 2 * math.pi)
		self.wander_distance = random.uniform(100, self.wander_radius)
		self.wander_timer = 0
		self.wander_change_interval = FPS
		self.rect = pygame.Rect(self.x - 50, self.y - 50, 100, 100)

		# Параметры атаки
		self.attack_cooldown = 0
		self.attack_charge_time = 0.5 * FPS
		self.charge_timer = 0
		self.jump_speed = 50  # Скорость прыжка
		self.retreat_speed = 50	# Скорость отскока
		self.attack_range = 150  # Дистанция атаки
		self.detection_range = 1000	# Дистанция обнаружения
		
		# Состояние прыжка
		self.start_x = x
		self.start_y = y
		self.target_x = x
		self.target_y = y
		
		# Флаг урона
		self.damage_dealt = False
	
	def update(self, player, world):

		self._update_animation()
		
		if self.HP < 16 and self.speed < 8:
			self.speed += 10  # Ускорение при низком HP
	
		self.attack_cooldown = max(0, self.attack_cooldown - 1)

		match self.state:
			case "Wander": self._handle_wander(player, world)
			case "Prepare attak": self._handle_prepare_attack(player, world)
			case "Jumping": self._handle_jumping(player, world)
			case "Retreat": self._handle_retreat(player, world)
	
	def _handle_wander(self, player, world):

		"""Блуждание вокруг игрока"""

		distance = math.sqrt((player.x - self.x) ** 2 + (player.y - self.y) ** 2)
		if (distance < self.detection_range and 
			self.attack_cooldown == 0 and
			random.random() < 0.02):  # 2% шанс начать атаку
			self.state = "Prepare attak"
			self.charge_timer = self.attack_charge_time
			self.start_x = self.x
			self.start_y = self.y
			return
			
		# Случайное блуждание по окружности вокруг игрока
		self.wander_timer += 1
		
		# Меняем направление через определенные интервалы
		if self.wander_timer >= self.wander_change_interval:
			self.wander_timer = 0
			self.wander_angle += random.uniform(-math.pi/4, math.pi/4)
			self.wander_distance = random.uniform(150, self.wander_radius)
			
		# Целевая точка для блуждания
		target_x = player.x + math.cos(self.wander_angle) * self.wander_distance
		target_y = player.y + math.sin(self.wander_angle) * self.wander_distance
		
		# Движение к целевой точке
		dx = target_x - self.x
		dy = target_y - self.y
		dist = math.sqrt(dx**2 + dy**2)
		
		if dist > 10:  # Если не достигли цели
			move_x = dx / dist * self.speed
			move_y = dy / dist * self.speed
			
			# Проверка стен
			if not self._check_collision(self.x + move_x, self.y, world):
				self.x += move_x
			if not self._check_collision(self.x, self.y + move_y, world):
				self.y += move_y
				
	def _handle_prepare_attack(self, player, world):
		"""Подготовка к прыжку (прицеливание)"""
		self.charge_timer -= 1
		
		# Слизень слегка дрожит в процессе подготовки
		if self.charge_timer % 4 < 2:
			self.y -= 2
		else:
			self.y += 2
			
		if self.charge_timer <= 0:
			self.state = "Jumping"
			self.target_x = player.x
			self.target_y = player.y
			self.damage_dealt = False
			self.start_x = self.x
			self.start_y = self.y
			
	def _handle_jumping(self, player, world):
		"""Прыжок на игрока"""
		# Движение к цели
		dx = self.target_x - self.x
		dy = self.target_y - self.y
		dist = math.sqrt(dx**2 + dy**2)
		
		if dist > 5:
			# Движение к цели
			move_x = dx / dist * self.jump_speed
			move_y = dy / dist * self.jump_speed
			
			# Проверяем стены
			if not self._check_collision(self.x + move_x, self.y, world):
				self.x += move_x
			if not self._check_collision(self.x, self.y + move_y, world):
				self.y += move_y
				
			# Эффект прыжка - немного подпрыгиваем вверх
			jump_height = math.sin((1 - dist / (math.sqrt((self.x - self.target_x)**2 + (self.y - self.target_y)**2))) * math.pi) * 20
			self._jump_offset = -jump_height
			
			# Наносим урон, если достигли игрока
			if dist < 50 and not self.damage_dealt:
				self._attack(player)
				self.damage_dealt = True
				self.state = "Retreat"
				
		else:
			# Достигли цели - отскок назад
			self.state = "Retreat"
			self._jump_offset = 0
			
			# TODO Создать частицы при столкновении
			
	def _handle_retreat(self, player, world):
		"""Отскок на начальную позицию"""
		# Движение обратно к начальной позиции
		dx = self.start_x - self.x
		dy = self.start_y - self.y
		dist = math.sqrt(dx**2 + dy**2)
		
		if dist > 10:
			move_x = dx / dist * self.retreat_speed
			move_y = dy / dist * self.retreat_speed
			
			if not self._check_collision(self.x + move_x, self.y, world):
				self.x += move_x
			if not self._check_collision(self.x, self.y + move_y, world):
				self.y += move_y
		else:
			# Вернулись на место
			self.x = self.start_x
			self.y = self.start_y
			self.state = "Wander"
			self.attack_cooldown = FPS * 2

	def _attack(self, player):
		"""Атака игрока"""
		if not player.god_mode and self.attack_cooldown <= 0:
			if pygame.Rect(self.x - 50, self.y + 50, 100, 100).colliderect(pygame.Rect(player.x - 100, player.y + 100, 200, 200)):
				player.HP -= 10
				player.HP_animation_tick = 1
			self.attack_cooldown = FPS

	def _check_collision(self, x, y, world):
		"""Проверка столкновения со стенами"""
		self.rect = pygame.Rect(x - 50, y - 50, 100, 100)
		return check_collision(self.rect, world)

	def draw(self, player):
		"""Отрисовка слизня"""
		screen_x = self.x - player.x + Width // 2 - 64
		screen_y = player.y - self.y + Height // 2 - 64
		
		frame_index = (self.animation_count - self.animation_count % 5) // 5
		frame = self.animation_frames[frame_index]
		
		win.blit(frame, (screen_x, screen_y))
		
		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), (screen_x, screen_y - 8, 128, 128), 3)

	def __getstate__(self):
		
		state = self.__dict__.copy()
		del state["animation_frames"]
		return state

	def __setstate__(self, state):
		
		self.__dict__.update(state)
		self.animation_frames = SLIME_TYPES[self.slime_type]

class Spider(BaseEnemy):
	
	def __init__(self, x, y):

		self.name = "Spider"
		self.direction = "Right"
		self.rect = pygame.Rect(self.x - 50, self.y - 50, 100, 100)
		
		super().__init__(
			x=x, y=y,
			HP=50,
			speed=random.randint(10, 20),
			animation_frames=[
				pygame.transform.scale(pygame.image.load(path + "Images/Objects/Spider.png"), (256, 256)),
				pygame.transform.scale(pygame.image.load(path + "Images/Objects/Spider 2.png"), (256, 256))]
		)
		
		self.animation_images = {
			"Left": pygame.transform.scale(pygame.image.load(path + "Images/Objects/Spider.png"), (256, 256)),
			"Left attack": pygame.transform.scale(pygame.image.load(path + "Images/Objects/Spider attack.png"), (256, 256)),
			"Right": pygame.transform.scale(pygame.image.load(path + "Images/Objects/Spider 2.png"), (256, 256)),
			"Right attack": pygame.transform.scale(pygame.image.load(path + "Images/Objects/Spider 2 attack.png"), (256, 256))}
		
		self.state = "Going towards player"

		# Параметры атаки
		self.attack_cooldown = 0
		self.attack_charge_time = 0.5 * FPS
		self.attack_range = 150  # Дистанция атаки
		self.shoot_range = 900
		self.shoot_cooldown = 0
		self.shoot_charge_time = FPS * 3
		self.shoot_prepare_charge_time = FPS * 0.5
		self.shoot_charge_timer = 0
		self.detection_range = 1000	# Дистанция обнаружения
		
		# Флаг урона
		self.damage_dealt = False
	
	def update(self, player, world):

		if self.HP < 16 and self.speed < 8:
			self.speed += 10  # Ускорение при низком HP
		
		self.attack_cooldown = max(0, self.attack_cooldown - 1)
		self.shoot_cooldown = max(0, self.shoot_cooldown - 1)

		distance = math.sqrt((player.x - self.x) ** 2 + (player.y - self.y) ** 2)

		match self.state:
			case "Attacking": self.state = "Going towards player"
			case "Prepare shoot": self._handle_prepare_shoot(player, world)
			case "Going towards player": self._handle_go_towards_player(player, world)
		
	def _handle_prepare_shoot(self, player, world):
		"""Подготовка к атаке паутиной (прицеливание)"""
		self.shoot_charge_timer -= 1
		
		# Паук слегка дрожит в процессе подготовки
		if self.shoot_charge_timer % 4 < 2:
			self.y -= 2
		else:
			self.y += 2
			
		if self.shoot_charge_timer <= 0:
			self.shoot_cooldown = self.shoot_charge_time
			dx = player.x - self.x
			dy = player.y - self.y
			dist = math.sqrt(dx**2 + dy**2)
			move_x = dx / dist * FPS * 1.5
			move_y = dy / dist * FPS * 1.5
			world.particles.append(Particle(self.x, self.y, pygame.transform.rotate(web_texture, -math.degrees(math.atan2(-move_y, move_x))), move_x, move_y, del_self_condition=lambda particle: (pygame.Rect(particle.x - 32, particle.y + 32, 64, 64).colliderect(pygame.Rect(player.x - 100, player.y + 100, 200, 200))), end_time=FPS*3)) # TODO наложить эффект замедления
			self.state = "Attacking"

	def _handle_go_towards_player(self, player, world):
		
		dx = player.x - self.x
		dy = player.y - self.y
		dist = math.sqrt(dx**2 + dy**2)

		if dist <= self.detection_range:
			if dist > 100:
				# Движение к цели
				move_x = dx / dist * self.speed
				move_y = dy / dist * self.speed
				if not self._check_collision(self.x + move_x, self.y, world):
					self.x += move_x
					if move_x > 0: self.direction = "Right"
					else: self.direction = "Left"
				if not self._check_collision(self.x, self.y + move_y, world):
					self.y += move_y

			else:
				self._attack(player)
			
			if dist <= self.shoot_range and self.shoot_cooldown <= 0:
				self.shoot_charge_timer = self.shoot_prepare_charge_time
				self.state = "Prepare shoot"
			
	def _attack(self, player):
		"""Атака игрока"""
		if not player.god_mode and self.attack_cooldown <= 0:
			self.state = "Attacking"
			if pygame.Rect(self.x - 50, self.y + 50, 100, 100).colliderect(pygame.Rect(player.x - 100, player.y + 100, 200, 200)):
				player.HP -= 10
				player.HP_animation_tick = 1
			self.attack_cooldown = self.attack_charge_time

	def _check_collision(self, x, y, world):
		"""Проверка столкновения со стенами"""
		self.rect = pygame.Rect(x - 50, y - 50, 100, 100)
		return check_collision(self.rect)
		
	def draw(self, player, show_hitbox=False):
		"""Отрисовка паука"""
		screen_x = self.x - player.x + Width // 2 - 128
		screen_y = player.y - self.y + Height // 2 - 128
		
		if self.state == "Attacking":
			frame = self.animation_images[self.direction + " attack"]
		else:
			frame = self.animation_images[self.direction]

		win.blit(frame, (screen_x, screen_y))
		
		if show_hitbox:
			pygame.draw.rect(win, (0, 0, 0), (screen_x, screen_y - 8, 128, 128), 3)

	def __getstate__(self):
		
		state = self.__dict__.copy()
		del state["animation_frames"]
		del state["animation_images"]
		return state

	def __setstate__(self, state):
		
		self.__dict__.update(state)
		self.animation_frames=(
			pygame.transform.scale(pygame.image.load(path + "Images/Objects/Spider.png"), (256, 256)),
			pygame.transform.scale(pygame.image.load(path + "Images/Objects/Spider 2.png"), (256, 256))
		)
		self.animation_images = {
			"Left": pygame.transform.scale(pygame.image.load(path + "Images/Objects/Spider.png"), (256, 256)),
			"Left attack": pygame.transform.scale(pygame.image.load(path + "Images/Objects/Spider attack.png"), (256, 256)),
			"Right": pygame.transform.scale(pygame.image.load(path + "Images/Objects/Spider 2.png"), (256, 256)),
			"Right attack": pygame.transform.scale(pygame.image.load(path + "Images/Objects/Spider 2 attack.png"), (256, 256))}

class ButterflyEnemy:

	def __init__(self, mob_x: int, mob_y: int):

		self.name = "Butterfly"
		self.x = mob_x
		self.y = mob_y
		self.rand_mob = random.randint(1, 2)
		self.animation_images = [Butterfly1, Butterfly1_2, Butterfly1_3, Butterfly1_2]
		self.HP = 10
		self.animation_count = -1
		self.reset_offset = 0
		self.offset_x = random.randint(-3000, 3000)
		self.offset_y = random.randint(-3000, 3000)
	
	def main(self):

		self.animation_count += 1
		if self.animation_count == 8:
			self.animation_count = 0
		
		if self.reset_offset == 0:
			self.reset_offset = random.randint(120, 150)
			self.offset_x = random.randint(-3000, 3000)
			self.offset_y = random.randint(-3000, 3000)
		else:
			self.reset_offset -= 1
		
		if player.x + self.offset_x > self.x:

			a = True
			for i in world.visible_walls.values():
				if i.x - 300 < self.x < i.x + 256 and i.y - 256 < self.y < i.y + 256:
					a = False
					break
			   
				if a:
					self.x += 1

		elif player.x + self.offset_x < self.x:

			a = True
			for i in world.visible_walls.values():
				if i.x - 256 < self.x < i.x + 300 and i.y - 256 < self.y < i.y + 256:
					a = False
					break

			if a:
				self.x -= 1
		
		if player.y + self.offset_y > self.y:

			a = True
			for i in world.visible_walls.values():
				if i.x - 256 < self.x < i.x + 256 and i.y - 300 < self.y < i.y + 256:
					a = False
					break

			if a:
				self.y += 1

		elif player.y + self.offset_y < self.y - player.y:

			a = True
			for i in world.visible_walls.values():
				if i.x - 256 < self.x < i.x + 256 and i.y - 256 < self.y < i.y + 300:
					a = False
					break

			if a:
				self.y -= 1
		
		win.blit(self.animation_images[(self.animation_count - self.animation_count % 2) // 2], (self.x - player.x + Width // 2 - 64, player.y - self.y + Height // 2 - 32))
		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), (self.x - player.x + Width // 2 - 32, player.y - self.y + Height // 2 - 32, 64, 64), 3)

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
		self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(path + "Images/Items/" + type + ".png"),
																	(64, 64)), math.atan2(mouse_x - Width / 2, mouse_y - Height / 2) * 180 / math.pi + 180)
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
		self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(path + "Images/Items/" + type + ".png"),
																	(64, 64)), math.atan2(mouse_x - Width / 2, mouse_y - Height / 2) * 180 / math.pi + 180)
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
				pygame.draw.rect(self.surface, (139, 155, 180), (self.x - textInfo.size(self.info)[0] // 2 - 5, self.y - self.h / 2 - self.info_y - 5, textInfo.size(self.info)[0] + 10, 28))
				self.surface.blit(textInfo.render(self.info, True, (139, 155, 180), (192, 203, 220)), (self.x - textInfo.size(self.info)[0] // 2, self.y - self.h / 2 - self.info_y))
			else:
				pygame.draw.rect(self.surface, (139, 155, 180), (self.x - self.w // 2 - textInfo.size(self.info)[0] // 2 - 5, self.y - self.h / 2 - self.info_y - 5, textInfo.size(self.info)[0] + 10, 28))
				self.surface.blit(textInfo.render(self.info, True, (139, 155, 180), (192, 203, 220), ), (self.x - self.w // 2 - textInfo.size(self.info)[0] // 2, self.y - self.info_y))

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
							pygame.mixer.Sound.play(Button_click)
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
		self.image = Wire_1
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
				self.image = Wire_2
			else:
				self.image = Wire_1

		elif len(self.neigbords) == 2:

			if self.neigbords[0].x == self.x == self.neigbords[1].x:
				self.image = Wire_2
			elif self.neigbords[0].y == self.y == self.neigbords[1].y:
				self.image = Wire_1
			elif (self.neigbords[0].x == self.x - 1 and self.neigbords[1].y == self.y + 1) or (self.neigbords[1].x == self.x - 1 and self.neigbords[0].y == self.y + 1):
				self.image = Wire_3
			elif (self.neigbords[0].x == self.x + 1 and self.neigbords[1].y == self.y + 1) or (self.neigbords[1].x == self.x + 1 and self.neigbords[0].y == self.y + 1):
				self.image = Wire_4
			elif (self.neigbords[0].x == self.x + 1 and self.neigbords[1].y == self.y - 1) or (self.neigbords[1].x == self.x + 1 and self.neigbords[0].y == self.y - 1):
				self.image = Wire_5
			elif (self.neigbords[0].x == self.x - 1 and self.neigbords[1].y == self.y - 1) or (self.neigbords[1].x == self.x - 1 and self.neigbords[0].y == self.y - 1):
				self.image = Wire_6

		elif len(self.neigbords) == 3:

			if self.neigbords[0].y != self.y + 1 and self.neigbords[1].y != self.y + 1 and self.neigbords[2].y != self.y + 1:
				self.image = Wire_7
			if self.neigbords[0].y != self.y - 1 and self.neigbords[1].y != self.y - 1 and self.neigbords[2].y != self.y - 1:
				self.image = Wire_8
			if self.neigbords[0].x != self.x + 1 and self.neigbords[1].x != self.x + 1 and self.neigbords[2].x != self.x + 1:
				self.image = Wire_9
			if self.neigbords[0].x != self.x - 1 and self.neigbords[1].x != self.x - 1 and self.neigbords[2].x != self.x - 1:
				self.image = Wire_10

		if len(self.neigbords) == 4:
			self.image = Wire_11

		if self.neigbords_on != 0 and self.condition == "Off":
			self.condition = "On"
		if self.condition is None:
			self.condition = "Off"
		elif self.neigbords_none != 0:
			self.condition = None
		
		if self.in_motherboard is None:

			win.blit(textInfo.render(self.condition, True, (0, 0, 0)), (self.x * 64 + Width // 2 - player.x, player.y - self.y * 64 + Height // 2 - 16))
			win.blit(self.image, (self.x * 64 + Width // 2 - player.x, player.y - self.y * 64 + Height // 2 - 16))
		else:
			...#win.blit(pygame.transform.scale(self.image, (18.75, 18.75)), (Width // 2 + 300 + self.x * 18.75, 0 - Height // 2 + self.y * 18.75 + 18.75 * 2 + 9.4))

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
			time.sleep(0.15)

		win.blit(self.image, (self.x * 64 + Width // 2 - player.x, player.y - self.y * 64 + Height // 2 - 16))

class Wall:

	def __init__(self, wall_type: str, X, Y, is_door: bool=False):

		self.x = X
		self.y = Y

		self.wall_type = wall_type
		self.neigbords = []
		self.is_door = is_door
		self.open = False
		self.rect = pygame.Rect(self.x - 128, self.y - 128, 256, 256)
		self.images = wall_images[self.wall_type]

		self.image = self.images[0]
		self.update_neigboors()

	def update_neigboors(self):

		self.neigbords = []
		for wall in ((self.x - 256, self.y), (self.x + 256, self.y), (self.x, self.y - 256), (self.x, self.y + 256)):
			if wall in world.chunk_manager.get_chunk_at(*wall).walls:
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

				if self.neigbords[0][0] == self.x:
					self.image = self.images[1]
				else:
					self.image = self.images[0]

			elif len(self.neigbords) == 2:

				if self.neigbords[0][0] == self.x == self.neigbords[1][0]:
					self.image = self.images[1]
				elif self.neigbords[0][1] == self.y == self.neigbords[1][1]:
					self.image = self.images[0]
				elif (self.neigbords[0][0] == self.x - 256 and self.neigbords[1][1] == self.y + 256) or (self.neigbords[1][0] == self.x - 256 and self.neigbords[0][1] == self.y + 256):
					self.image = self.images[2]
				elif (self.neigbords[0][0] == self.x + 256 and self.neigbords[1][1] == self.y + 256) or (self.neigbords[1][0] == self.x + 256 and self.neigbords[0][1] == self.y + 256):
					self.image = self.images[3]
				elif (self.neigbords[0][0] == self.x + 256 and self.neigbords[1][1] == self.y - 256) or (self.neigbords[1][0] == self.x + 256 and self.neigbords[0][1] == self.y - 256):
					self.image = self.images[4]
				elif (self.neigbords[0][0] == self.x - 256 and self.neigbords[1][1] == self.y - 256) or (self.neigbords[1][0] == self.x - 256 and self.neigbords[0][1] == self.y - 256):
					self.image = self.images[5]

			elif len(self.neigbords) == 3:

				if self.neigbords[0][1] != self.y + 256 and self.neigbords[1][1] != self.y + 256 and self.neigbords[2][1] != self.y + 256:
					self.image = self.images[6]
				if self.neigbords[0][1] != self.y - 256 and self.neigbords[1][1] != self.y - 256 and self.neigbords[2][1] != self.y - 256:
					self.image = self.images[7]
				if self.neigbords[0][0] != self.x + 256 and self.neigbords[1][0] != self.x + 256 and self.neigbords[2][0] != self.x + 256:
					self.image = self.images[8]
				if self.neigbords[0][0] != self.x - 256 and self.neigbords[1][0] != self.x - 256 and self.neigbords[2][0] != self.x - 256:
					self.image = self.images[9]

			elif len(self.neigbords) == 4:
				self.image = self.images[10]
		
	def main(self, release):

		if self.is_door and release and self.x + Width // 2 - player.x <= mouse_x <= self.x + Width // 2 - player.x + 256 and player.y - self.y + Height // 2 - 128 <= mouse_y <= player.y - self.y + Height // 2 + 128:
			self.open = not self.open
		win.blit(self.image, world_to_screen(self.x, self.y, 256, 256))
		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), world_rect_to_screen(self.x, self.y, 256, 256), 3)
		
	def __getstate__(self):
		
		state = self.__dict__.copy()
		state["image"] = self.images.index(self.image)
		del state["images"]
		return state

	def __setstate__(self, state):
		
		self.__dict__.update(state)
		self.images = wall_images[self.wall_type]
		self.image = self.images[self.image]

class Farmland:

	def __init__(self, X, Y):

		self.x = X
		self.y = Y

		self.neigbords = []
		self.rect = pygame.Rect(self.x - 64, self.y - 64, 128, 128)
		self.images = farmland_images
		self.image = self.images[0]
		# self.update_neigboors()

		self.plant = None
		self.plant_growth_stage = 0
		self.watered = False

	def update_neigboors(self):

		self.neigbords = []
		for farmland in ((self.x - 128, self.y), (self.x + 128, self.y), (self.x, self.y - 128), (self.x, self.y + 128)):
			if farmland in world.chunk_manager.get_chunk_at(*farmland).farmlands:
				self.neigbords.append(farmland)
		if len(self.neigbords) == 1:

			if self.neigbords[0][0] == self.x:
				self.image = self.images[1]
			else:
				self.image = self.images[0]

		elif len(self.neigbords) == 2:

			if self.neigbords[0][0] == self.x == self.neigbords[1][0]:
				self.image = self.images[1]
			elif self.neigbords[0][1] == self.y == self.neigbords[1][1]:
				self.image = self.images[0]
			elif (self.neigbords[0][0] == self.x - 256 and self.neigbords[1][1] == self.y + 256) or (self.neigbords[1][0] == self.x - 256 and self.neigbords[0][1] == self.y + 256):
				self.image = self.images[2]
			elif (self.neigbords[0][0] == self.x + 256 and self.neigbords[1][1] == self.y + 256) or (self.neigbords[1][0] == self.x + 256 and self.neigbords[0][1] == self.y + 256):
				self.image = self.images[3]
			elif (self.neigbords[0][0] == self.x + 256 and self.neigbords[1][1] == self.y - 256) or (self.neigbords[1][0] == self.x + 256 and self.neigbords[0][1] == self.y - 256):
				self.image = self.images[4]
			elif (self.neigbords[0][0] == self.x - 256 and self.neigbords[1][1] == self.y - 256) or (self.neigbords[1][0] == self.x - 256 and self.neigbords[0][1] == self.y - 256):
				self.image = self.images[5]

		elif len(self.neigbords) == 3:

			if self.neigbords[0][1] != self.y + 256 and self.neigbords[1][1] != self.y + 256 and self.neigbords[2][1] != self.y + 256:
				self.image = self.images[6]
			if self.neigbords[0][1] != self.y - 256 and self.neigbords[1][1] != self.y - 256 and self.neigbords[2][1] != self.y - 256:
				self.image = self.images[7]
			if self.neigbords[0][0] != self.x + 256 and self.neigbords[1][0] != self.x + 256 and self.neigbords[2][0] != self.x + 256:
				self.image = self.images[8]
			if self.neigbords[0][0] != self.x - 256 and self.neigbords[1][0] != self.x - 256 and self.neigbords[2][0] != self.x - 256:
				self.image = self.images[9]

		elif len(self.neigbords) == 4:
			self.image = self.images[10]
		
	def main(self, release):

		if False and release and self.x + Width // 2 - player.x <= mouse_x <= self.x + Width // 2 - player.x + 256 and player.y - self.y + Height // 2 - 128 <= mouse_y <= player.y - self.y + Height // 2 + 128:
			...
		win.blit(self.image, world_to_screen(self.x, self.y, 256, 256))
		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), world_rect_to_screen(self.x, self.y, 128, 128), 3)
		
	def __getstate__(self):
		
		state = self.__dict__.copy()
		state["image"] = self.images.index(self.image)
		del state["images"]
		return state

	def __setstate__(self, state):
		
		self.__dict__.update(state)
		self.images = farmland_images
		self.image = self.images[self.image]

class Random_box:

	def __init__(self, in_motherboard):
		
		self.x = (player.x + mouse_x - Width // 2) // 64
		self.y = (player.y - mouse_y + Height // 2) // 64

		self.on = False
		self.image = Random_box_1
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
				self.image = Random_box_2
			else:
				self.image = Random_box_3

		elif len(self.neigbords) == 2:
			self.image = Random_box_4

		else:
			self.image = Random_box_1
		
		win.blit(self.image, (self.x * 64 + Width // 2 - player.x, player.y - self.y * 64 + Height // 2 - 16))

class LogicGate:

	def __init__(self, in_motherboard):

		self.x = (player.x + mouse_x - Width // 2) // 64
		self.y = (player.y - mouse_y + Height // 2) // 64

		self.image = Wire_11
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
				self.image = Wire_2
			else:
				self.image = Wire_1

		elif len(self.neigbords) == 2:
			if self.neigbords[0].x == self.x == self.neigbords[1].x:
				self.image = Wire_2
			elif self.neigbords[0].y == self.y == self.neigbords[1].y:
				self.image = Wire_1
			elif (self.neigbords[0].x == self.x - 1 and self.neigbords[1].y == self.y + 1) or (self.neigbords[1].x == self.x - 1 and self.neigbords[0].y == self.y + 1):
				self.image = Wire_3
			elif (self.neigbords[0].x == self.x + 1 and self.neigbords[1].y == self.y + 1) or (self.neigbords[1].x == self.x + 1 and self.neigbords[0].y == self.y + 1):
				self.image = Wire_4
			elif (self.neigbords[0].x == self.x + 1 and self.neigbords[1].y == self.y - 1) or (self.neigbords[1].x == self.x + 1 and self.neigbords[0].y == self.y - 1):
				self.image = Wire_5
			elif (self.neigbords[0].x == self.x - 1 and self.neigbords[1].y == self.y - 1) or (self.neigbords[1].x == self.x - 1 and self.neigbords[0].y == self.y - 1):
				self.image = Wire_6

		elif len(self.neigbords) == 3:
			if self.neigbords[0].y != self.y + 1 and self.neigbords[1].y != self.y + 1 and self.neigbords[2].y != self.y + 1:
				self.image = Wire_7
			if self.neigbords[0].y != self.y - 1 and self.neigbords[1].y != self.y - 1 and self.neigbords[2].y != self.y - 1:
				self.image = Wire_8
			if self.neigbords[0].x != self.x + 1 and self.neigbords[1].x != self.x + 1 and self.neigbords[2].x != self.x + 1:
				self.image = Wire_9
			if self.neigbords[0].x != self.x - 1 and self.neigbords[1].x != self.x - 1 and self.neigbords[2].x != self.x - 1:
				self.image = Wire_10

		if len(self.neigbords) == 4:
			self.image = Wire_11

		if self.neigbords_on != 0 and self.condition == "Off":
			self.condition = "On"
		if self.condition is None:
			self.condition = "Off"
		elif self.neigbords_none != 0:
			self.condition = None
		
		if self.in_motherboard:
			...#win.blit(self.image, (self.x * 64 + Width // 2 - player.x, player.y - self.y * 64 + Height // 2 - 16))
		else:
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

		if self.in_motherboard:
			...#win.blit(self.image, (self.x * 64 + Width // 2 - player.x, player.y - self.y * 64 + Height // 2 - 16))
		else:
			win.blit(self.image, (self.x * 64 + Width // 2 - player.x, player.y - self.y * 64 + Height // 2 - 16))

	def get_pressed(self):
		global in_motherboard, mouse_x, mouse_y, click
		mouse_x, mouse_y = pygame.mouse.get_pos()
		if self.in_motherboard is None:
			if self.x * 64 + Width // 2 - player.x <= mouse_x <= self.x * 64 + Width // 2 - player.x + 64 and player.y - self.y * 64 + Height // 2 - 16 <= mouse_y <= player.y - self.y * 64 + Height // 2 - 16 + 64 and in_motherboard is None and click[0]:
				in_motherboard = self
		else:
			...

class World:

	def __init__(self):

		self.chunk_manager = ChunkManager(Object, world_rect_to_screen)
		self.current_cave = None

		self.visible_objects = []
		self.visible_items = []
		self.visible_walls = {}
		self.visible_farmlands = {}
		self.visible_caves = []

		self.mobs = []
		self.particles = []
		self.mechanisms = []
		self.projectiles = []
		
	def update(self):
		self.chunk_manager.update_visible_chunks(player.x, player.y)
		# Сборка объектов из загруженных чанков
		self.visible_objects.clear()
		self.visible_items.clear()
		self.visible_walls.clear()
		self.visible_farmlands.clear()
		self.visible_caves.clear()
		for chunk_key in self.chunk_manager.loaded_chunks:
			chunk = self.chunk_manager.chunks[chunk_key]
			self.visible_objects.extend(chunk.objects)
			self.visible_items.extend(chunk.items)
			self.visible_walls.update(chunk.walls)
			self.visible_farmlands.update(chunk.farmlands)
			self.visible_caves.extend(chunk.caves)

	def render_loaded_chunks(self):

		"""Отрисовка загруженных чанков с их биомами"""

		for chunk_key in self.chunk_manager.loaded_chunks:
			chunk = self.chunk_manager.chunks.get(chunk_key)
			if chunk and chunk.is_generated:
				bounds = chunk.get_world_bounds()
				
				# Проверка, виден ли чанк на экране
				if (bounds["x2"] > player.x - Width // 2 and 
					bounds["x1"] < player.x + Width // 2 and
					bounds["y2"] > player.y - Height // 2 and 
					bounds["y1"] < player.y + Height):
					
					biome_texture = textures.get(chunk.biome)
					if biome_texture:
						# Смещение чанка относительно игрока
						offset_x = bounds["x1"] - player.x + Width // 2
						offset_y = player.y - bounds["y1"] + Height // 2
						
						# Отрисовка тайлов чанка
						tiles_per_chunk = 2048 // 256
						for tile_x, tile_y in product(range(tiles_per_chunk), range(tiles_per_chunk)):
							tile_screen_x = offset_x + tile_x * 256
							tile_screen_y = offset_y - tile_y * 256
							if (tile_screen_x > -256 and 
								tile_screen_x < Width and
								tile_screen_y > -256 and 
								tile_screen_y < Height):
								win.blit(biome_texture, (tile_screen_x, tile_screen_y))

world = World()
game_time = GameTime()
ron = Ron(world_to_screen, Projectile, player)

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
		self.image = pygame.transform.scale(pygame.image.load(path + "Images/Objects/Cave.png"), (128, 128))
		self.objects = []
		self.seed = (int(self.x) * 888888 + int(self.y) * 425269) ^ 0x9e3779b9
		self.noise = world.chunk_manager.generator.get_cave_noise(self.seed)
		self.generate()

	def generate(self):

		# for _ in range(self.own_width // 100 + random.randint(-10, 10)):
		# 	self.objects.append(Object("Stone", random.randint(self.own_width // 2 * -1, self.own_width // 2), random.randint(self.own_height // 2 * -1, self.own_height // 2), "Images/Items/Stone.png"))
			
		# for _ in range(self.own_width // 300 + random.randint(-10, 10)):
		# 	self.objects.append(Object("Iron ore", random.randint(self.own_width // 2 * -1, self.own_width // 2), random.randint(self.own_height // 2 * -1, self.own_height // 2), "Images/Objects/Iron ore.png", (256, 256), special_flags=100, is_solid=True))

		# for _ in range(self.own_width // 300 + random.randint(-10, 10)):
		# 	self.objects.append(Object("Gold ore", random.randint(self.own_width // 2 * -1, self.own_width // 2), random.randint(self.own_height // 2 * -1, self.own_height // 2), "Images/Objects/Gold ore.png", (256, 256), special_flags=100, is_solid=True))
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
		self.image = pygame.transform.scale(pygame.image.load(path + "Images/Objects/Cave.png"), (128, 128))

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

class Vending_machine:

	def __init__(self) -> None:

		self.x = (player.x + mouse_x - Width // 2) // 304
		self.y = (player.y + mouse_y - Height // 2) // 560
		self.owner = Settings["User"][0]
		self.image = Vending_machine_image

settings_ui = SettingsUI(win, Settings, statistics, bigTextInfo, path)

# Загрузка команд

def tp(x, y, player=player):
	"""Телепортация игрока на указанные координаты"""
	player.x = x
	player.y = y

def chat_message(message: str):
	"""Отправляет сообщение в чат"""
	global chat_tick
	chat.append(message)
	chat_tick = len(message) // 1.5 * FPS

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
		"get_brightness": (game_time.get_brightness, "Получение текущей яркости днейвного цикла\n/get_brightness"),
		"get_time_of_day": (game_time.get_time_of_day, "Получение текущего времени в 24-часовом формате\n/get_time_of_day"),
		"set_time_speed": (game_time.set_time_speed, "Изменить скорость времени\n/time_scale МНОЖИТЕЛЬ"),
		"reset_to_day": (game_time.reset_to_day, "Обнулить время до дня\n/reset_to_day"),
		"skip_time": (game_time.skip_time, "Перемотать время вперёд\n/skip_time СЕКУНДЫ"),
		"chat_message": (chat_message, "Вывести сообщение в чат\n/chat_message ТЕКСТ")

		}

# def show_bar(times):
# 	import matplotlib.pyplot as plt
# 	categories = range(len(times))
# 	values = []
# 	for i in times:
# 		values.append(sum(i) / len(i))

# 	plt.bar(categories, values, color="orange")
# 	plt.title("Время на обработку")
# 	plt.xlabel('Часть кода')
# 	plt.ylabel('Время')
# 	plt.show()
# 	plt.savefig("aboba.png")

# time_values = []
# time_index = 0

# def add_time(t):
# 	global time_index
# 	if len(time_values) <= time_index:
# 		time_values.append([])
# 	time_values[time_index].append(t)
# 	time_index += 1
# def reset_time():
# 	global time_index
# 	time_index = 0

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
			win.blit(bigTextInfo.render(t("Reset settings"), True, (58, 68, 102)), (Width - 30 - bigTextInfo.size(t("Reset settings"))[0], 30))
			if pygame.mouse.get_pressed()[0]:
					
				Settings = {
					
					"Display": [100, 90, 0, False, True, True, 30, True, True, True, True],
					"Languages": ["English"],
					"User": ["Player"],
					"Sound": [100, 100],
					"Keys": ["a", "s", "w", "d", "e", "c", "TAB", "SPACE"],
					"Game": [True, False]
						
					}
		else:
			win.blit(bigTextInfo.render(t("Reset settings"), True, (139, 155, 180)), (Width - 30 - bigTextInfo.size(t("Reset settings"))[0], 30))

	def help():

		global win, screenmode, mouse_x, mouse_y, does_lighten, page, alt_pressed
		
		while True:

			mouse_x, mouse_y = pygame.mouse.get_pos()
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
						Saver.save_objects(path + "Settings/Settings.save", Settings)
						win_darken(win)
						menu()

			win.fill((192, 203, 220))
			pygame.draw.rect(win, (139, 155, 180), (-8, 100, 373, Height), 8)
			pygame.draw.line(win, (139, 155, 180), (307, 103), (Width, 103), 8)
			back_button.main()
			show_reset_settings()
			
			if back_button.get_pressed():
				Saver.save_objects(path + "Settings/Settings.save", Settings)
				win_darken(win)
				menu()
				
			page_back_button.main()
			page_next_button.main()
			page = min(page, 2)

			win.blit(bigTextInfo.render(str(page), True, (139, 155, 180)), ((Width - 415) // 2 + 391, Height - 96))
			win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Help 2.png"), (132, 64)), (10, 117))
			display_button.main(display)
			languages_button.main(Languages)
			user_button.main(User)
			sound_button.main(Sound)
			statistics_button.main(Statistics)
			keys_button.main(Keys)
			game_button.main(Game)

			if page == 1:
				
				win.blit(bigTextInfo.render(t("Start game"), True, (139, 155, 180)), (385, 123))
				win.blit(textInfo.render(t(" • To move, you can use the arrows or A, S, W and D"), True, (139, 155, 180)), (385, 209)) # между строками 86 пикселей
				win.blit(arrow_up, (459, 239))
				win.blit(arrow_left, (385, 313))
				win.blit(arrow_down, (459, 313))
				win.blit(arrow_right, (533, 313))
				pygame.draw.rect(win, (139, 155, 180), (701, 239, 64, 64), 6)
				pygame.draw.rect(win, (139, 155, 180), (627, 313, 64, 64), 6)
				pygame.draw.rect(win, (139, 155, 180), (701, 313, 64, 64), 6)
				pygame.draw.rect(win, (139, 155, 180), (775, 313, 64, 64), 6)
				win.blit(bigTextInfo.render("W", True, (139, 155, 180)), (710, 247))
				win.blit(bigTextInfo.render("A", True, (139, 155, 180)), (640, 321))
				win.blit(bigTextInfo.render("S", True, (139, 155, 180)), (716, 321))
				win.blit(bigTextInfo.render("D", True, (139, 155, 180)), (790, 321))
				win.blit(textInfo.render(t("  Also, you can put an item on the ground by pressing E, and to get it, just click"), True, (139, 155, 180)), (385, 381)) # между строками 30 пикселей
				win.blit(textInfo.render(t("on it!"), True, (139, 155, 180)), (385, 411))
				win.blit(textInfo.render(languages(" • Если вы хотите узнать свой координаты, или что-нибудь ещё, нажмите F2", " • If you want to know you coordinate, or anything more, press F2", "• Координаттарды немесе басқа кез келген нәрсені білгіңіз келсе, F2 пернесін басыңыз"), True, (139, 155, 180)), (385, 441))
				win.blit(textInfo.render(languages("для открытия меню.", "to open the menu", "мәзірді ашу үшін"), True, (139, 155, 180)), (385, 471))
				win.blit(textInfo.render(languages(" • При нажатии на I откроется весь инвентарь, чтобы его закрыть, нажмите", " • Clicking on I will open the entire inventory, to close it, click again.", "• Мен түймешігін бассаңыз, бүкіл тізімді ашамын, оны жабу үшін қайтадан басыңыз"), True, (139, 155, 180)), (385, 501))
				win.blit(textInfo.render(languages("ещё раз", None, None), True, (139, 155, 180)), (385, 531))
				win.blit(textInfo.render(languages(" • В верхнем правом углу есть пункт, в котором можно узнать информацию", " • In the upper right corner there is an item where you can find out", " • Жоғарғы оң жақ бұрышта ақпаратты табуға болатын элемент бар"), True, (139, 155, 180)), (385, 561))
				win.blit(textInfo.render(languages("об объекте, на который вы навели.", "information about the object you hovered over", "меңзерді апарған нысан туралы."), True, (139, 155, 180)), (385, 591))
				
			elif page == 2:
				
				win.blit(bigTextInfo.render(languages("Крафт", "Craft", "Қолөнер"), True, (139, 155, 180)), (385, 123))
				win.blit(textInfo.render(languages("   Наверняка, тебе было интересно, что это за слоты под инвентарём. Это", "    Forsnre, you were interesting about the cells under the inventory. This is", "Әлбетте, сіз бұл слоттардың түгендеу астында не бар екенін сұрадыңыз. Бұл"), True, (139, 155, 180)), (385, 209))
				win.blit(textInfo.render(languages("система крафта", "crafting system", "Қолөнер жүйесі"), True, (139, 155, 180)), (385, 239))
				win.blit(Changed_inventory_slot, (385, 269))
				win.blit(Changed_inventory_slot, (465, 269))
				win.blit(Inventory_slot, (545, 269))
				win.blit(textInfo.render(languages("   На первый взгляд, всё как-то уныло, но на самом деле, крафтить весело!", "  At first glance, everything is somehow dull, but in fact, crafting is fun!", "Бір қарағанда, бәрі қандай да бір түсініксіз, бірақ шын мәнінде қолөнер қызықты!"), True, (139, 155, 180)), (385, 359))
				win.blit(textInfo.render(languages("Первый слот обозначает объект, который нужен для крафта, например стол.", "The first slot denotes an object that is needed for crafting, such as a table.", "Бірінші ұяшық кесте сияқты өңдеуге қажет нысанды білдіреді"), True, (139, 155, 180)), (385, 389))
				win.blit(textInfo.render(languages("Второй слот - инструмент, который тебе нужен, например молоток. Дальше", "The second slot is the tool you need, like a hammer. Еhen there are 7 slots", "Екінші ұяшық - балға сияқты сізге қажет құрал. Әрі қарай"), True, (139, 155, 180)), (385, 419))
				win.blit(textInfo.render(languages("идут 7 слотов для предметов. Если положить предмет в первый, то", "for items. If you put an item in the first one, then the second one is", "7 элемент ұясы бар. Егер объектіні біріншіге қойсақ, онда"), True, (139, 155, 180)), (385, 449))
				win.blit(textInfo.render(languages("разблокируется второй, потом третий, и так далее.", "unlocked, then the third, and so on.", "екіншісі құлыптан босатылады, содан кейін үшінші және т.б."), True, (139, 155, 180)), (385, 479))
				win.blit(Changed_inventory_slot, (385, 509))
				win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Items/Furnace.png"), (64, 64)), (385, 509))
				win.blit(Changed_inventory_slot, (465, 509))
				win.blit(Inventory_slot, (545, 509))
				win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Items/Clay.png"), (64, 64)), (545, 509))
				win.blit(Inventory_slot, (625, 509))
				win.blit(Changed_inventory_slot, (1185, 509))
				win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Items/Brick.png"), (64, 64)), (1185, 509))
				win.blit(textInfo.render(languages("   Если положить определённую комбинацию предметов, то можно будет", "	 If you put a certain combination of items, then you can", "Егер сіз элементтердің белгілі бір комбинациясын қойсаңыз, онда сіз жасай аласыз"), True, (139, 155, 180)), (385, 599))
				win.blit(textInfo.render(languages("получить что-либо. Например, если поставить печь и положить глину в ячейки", "get something. For example, if you put a furnace and put clay in the cells of", "бірдеңе алу. Мысалы, пешті қойып, ұяшықтарға балшық салсаңыз"), True, (139, 155, 180)), (385, 629))
				win.blit(textInfo.render(languages("крафта, то можно будет получить кирпич, а чтобы его получить, нажми.", "crafting, you can get a brick, and to get it, click.", "қолөнер, сіз кірпіш алуға болады, және оны алу үшін басыңыз."), True, (139, 155, 180)), (385, 659))
			

			if alt_pressed:
				
				draw_key("ESC", 44, 108)
				draw_key("<-", 425, Height - 168)
				draw_key("->", Width - 74, Height - 168)

			animate_click(Settings, win, mouse_x, mouse_y)

			win_fill(alpha=100 - Settings["Display"][0])   # Если в настройках установлена яркость ниже 100, то экран становится темнее
			
			if not does_lighten:
				win_lighten(win)
				does_lighten = True

			pygame.display.update()
			clock.tick(MAX_FPS)

	def display():

		global win, screenmode, Settings, alt_pressed, MAX_FPS

		bias = 0
		max_bias = -settings_ui._set_positions(bias, "Display", True) + 900

		while True:
			
			click = pygame.mouse.get_pressed()
			mouse_x, mouse_y = pygame.mouse.get_pos()
			release = False
			
			events = pygame.event.get()
			
			for event in events:
				if event.type == pygame.QUIT:
					Saver.save_objects(path + "Settings/Settings.save", Settings)
					save()
					sys.exit()
				
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					release = True
				
				elif event.type == pygame.KEYUP:
					if event.key == hot_keys["Show keys"]:
						alt_pressed = not alt_pressed
					if event.key == hot_keys["Close"]:
						Saver.save_objects(path + "Settings/Settings.save", Settings)
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
					bias = max((min(bias + event.y * 100, 0)), max_bias)
					settings_ui._set_positions(bias, "Display")
			
			# Очистка экрана
			win.fill((192, 203, 220))
			
			# Обработка UI
			settings_ui.handle_events(events, mouse_x, mouse_y, release, "Display")
			settings_ui.draw("Display", win, Width, Height, bias, max_bias)
			
			help_button.main(help)
			win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Display 2.png"), (222, 64)), (10, 192))
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
				Saver.save_objects(path + "Settings/Settings.save", Settings)
				win_darken(win)
				menu()
				
			# Анимация и эффекты
			animate_click(Settings, win, mouse_x, mouse_y)
			win_fill(alpha=100 - Settings["Display"][0])
			
			pygame.display.update()
			clock.tick(MAX_FPS)

	def Languages():

		global win, screenmode, does_lighten, page, alt_pressed
		
		while True:
			
			mouse_x, mouse_y = pygame.mouse.get_pos()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					save()
					sys.exit()
				if event.type == pygame.KEYUP:
					if event.key == hot_keys["Show keys"]:
						alt_pressed = not alt_pressed
					if event.key == hot_keys["Close"]:
						Saver.save_objects(path + "Settings/Settings.save", Settings)
						win_darken(win)
						menu()

					if event.key == pygame.K_1:
						Settings["Languages"][0] = "English"
						translator.load_language("English")
						for element_list in settings_ui.elements.values():
							for element in element_list:
								element.label_width = element.font.size(t(element.label))[0] + 10
								element.rect = pygame.Rect(element.x + element.label_width, element.y, element.width, element.height)

					if event.key == pygame.K_2:
						Settings["Languages"][0] = "Russian"
						translator.load_language("Russian")
						for element_list in settings_ui.elements.values():
							for element in element_list:
								element.label_width = element.font.size(t(element.label))[0] + 10
								element.rect = pygame.Rect(element.x + element.label_width, element.y, element.width, element.height)

					if event.key == pygame.K_3:
						Settings["Languages"][0] = "Kazach"
						translator.load_language("Karach")
						for element_list in settings_ui.elements.values():
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

			win.fill((192, 203, 220))
			pygame.draw.rect(win, (139, 155, 180), (-8, 100, 373, Height), 8)
			pygame.draw.line(win, (139, 155, 180), (307, 103), (Width, 103), 8)
			back_button.main()
			if back_button.get_pressed():
				Saver.save_objects(path + "Settings/Settings.save", Settings)
				win_darken(win)
				menu()
			show_reset_settings()
			
			page_back_button.main()
			page_next_button.main()
			page = min(page, 1)

			win.blit(bigTextInfo.render(t("You can choose one of these"), True, (139, 155, 180)), (385, 123))
			win.blit(bigTextInfo.render(t("languages:"), True, (139, 155, 180)), (385, 153))

			english_button.main()
			if english_button.get_pressed():
				Settings["Languages"][0] = "English"
				translator.load_language("English")
				for element_list in settings_ui.elements.values():
					for element in element_list:
						element.label_width = element.font.size(t(element.label))[0] + 10
						element.rect = pygame.Rect(element.x + element.label_width, element.y, element.width, element.height)

			russian_button.main()
			if russian_button.get_pressed():
				Settings["Languages"][0] = "Russian"
				translator.load_language("Russian")
				for element_list in settings_ui.elements.values():
					for element in element_list:
						element.label_width = element.font.size(t(element.label))[0] + 10
						element.rect = pygame.Rect(element.x + element.label_width, element.y, element.width, element.height)

			kazach_button.main()
			if kazach_button.get_pressed():
				Settings["Languages"][0] = "Kazach"
				translator.load_language("Kazach")
				for element_list in settings_ui.elements.values():
					for element in element_list:
						element.label_width = element.font.size(t(element.label))[0] + 10
						element.rect = pygame.Rect(element.x + element.label_width, element.y, element.width, element.height)

			win.blit(bigTextInfo.render(str(page), True, (139, 155, 180)), ((Width - 415) // 2 + 391, Height - 96))
			help_button.main(help)
			display_button.main(display)
			win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Languages 2.png"), (272, 64)), (10, 267))
			user_button.main(User)
			sound_button.main(Sound)
			statistics_button.main(Statistics)
			keys_button.main(Keys)
			game_button.main(Game)
			
			if alt_pressed:
				
				draw_key("ESC", 44, 108)
				draw_key("<-", 425, Height - 168)
				draw_key("->", Width - 74, Height - 168)

			animate_click(Settings, win, mouse_x, mouse_y)
			win_fill(alpha=100 - Settings["Display"][0])   # Если в настройках установлена яркость ниже 100, то экран становится темнее

			if not does_lighten:
				win_lighten(win)
				does_lighten = True

			pygame.display.update()
			clock.tick(MAX_FPS)

	def User_old():

		global win, screenmode, Settings, click, mouse_x, mouse_y, does_lighten, page, alt_pressed
		
		mouse_x, mouse_y = pygame.mouse.get_pos()
		Nick = False
		Inventory_alpha = False
		input_text = ""
		
		while True:
			click = pygame.mouse.get_pressed()
			mouse_x, mouse_y = pygame.mouse.get_pos()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					save()
					sys.exit()

				elif event.type == pygame.KEYDOWN and (Nick or Inventory_alpha):
					if event.key == pygame.K_RETURN or ((Nick and len(input_text) == 10) or (Inventory_alpha and len(input_text) == 3)):
						if Nick:
							Nick = False
							if input_text != "":
								Settings["User"][0] = input_text
						elif Inventory_alpha:
							Inventory_alpha = False
							if input_text != "":
								Settings["User"][1] = int(input_text)
						input_text = ""
					elif event.key == pygame.K_BACKSPACE:
						input_text = input_text[:-1]
					elif Nick or event.unicode in "0123456789":
						input_text += event.unicode
				if event.type == pygame.KEYUP:
					if event.key == hot_keys["Show keys"]:
						alt_pressed = not alt_pressed
					if event.key == hot_keys["Close"]:
						Saver.save_objects(path + "Settings/Settings.save", Settings)
						win_darken(win)
						menu()
					if event.key == hot_keys["Change screen"]:
						if screenmode == "FULLSCREEN":
							win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
							screenmode = "RESIZABLE"
						else:
							win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
							screenmode = "FULLSCREEN"

			if bigTextInfo.size(t("Nickname"))[0] + 337 <= mouse_x <= bigTextInfo.size(t("Nickname"))[0] + 467 + 120 and 113 <= mouse_y <= 184 and click[0]:
				Nick = True
			if bigTextInfo.size(t("Comming soon"))[0] + 337 <= mouse_x <= bigTextInfo.size(t("Comming soon"))[0] + 467 + 120 and 199 <= mouse_y <= 270 and click[0]:
				Inventory_alpha = True
			
			win.fill((192, 203, 220))
			pygame.draw.rect(win, (139, 155, 180), (-8, 100, 373, Height), 8)
			pygame.draw.line(win, (139, 155, 180), (307, 103), (Width, 103), 8)
			back_button.main()
			if back_button.get_pressed():
				Saver.save_objects(path + "Settings/Settings.save", Settings)
				win_darken(win)
				menu()
			show_reset_settings()
				
			page_back_button.main()
			page_next_button.main()
			page = min(page, 1)

			win.blit(bigTextInfo.render(str(page), True, (139, 155, 180)), ((Width - 415) // 2 + 391, Height - 96))
			help_button.main(help)
			display_button.main(display)
			languages_button.main(Languages)
			win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/User 2.png"), (132, 64)), (10, 342))
			sound_button.main(Sound)
			statistics_button.main(Statistics)
			keys_button.main(Keys)
			game_button.main(Game)

			if page == 1:
				win.blit(bigTextInfo.render(t("Nickname"), True, (139, 155, 180)), (385, 123))
				pygame.draw.rect(win, (139, 155, 180), (bigTextInfo.size(t("Nickname"))[0] + 395, 113, 200, 71), 5)
				if Nick:
					win.blit(bigTextInfo.render(input_text, True, (139, 155, 180)), (bigTextInfo.size(t("Nickname"))[0] + 405, 123))
				else:
					win.blit(bigTextInfo.render(Settings["User"][0], True, (139, 155, 180)), (bigTextInfo.size(t("Nickname"))[0] + 405, 123))
				
				win.blit(bigTextInfo.render(t("Comming soon"), True, (139, 155, 180)), (385, 209))
				pygame.draw.rect(win, (139, 155, 180), (bigTextInfo.size(t("Comming soon"))[0] + 395, 199, 120, 71), 5)
				if Inventory_alpha:
					win.blit(bigTextInfo.render(input_text, True, (139, 155, 180)), (bigTextInfo.size(t("Comming soon"))[0] + 405, 209))
				else:
					win.blit(bigTextInfo.render(str(Settings["Display"][1]), True, (139, 155, 180)), (bigTextInfo.size(t("Comming soon"))[0] + 405, 209))
					
			
			if alt_pressed:
				
				draw_key("ESC", 44, 108)
				draw_key("<-", 425, Height - 168)
				draw_key("->", Width - 74, Height - 168)

			animate_click(Settings, win, mouse_x, mouse_y)

			win_fill(alpha=100 - Settings["Display"][0])   # Если в настройках установлена яркость ниже 100, то экран становится темнее
			
			if not does_lighten:
				win_lighten(win)
				does_lighten = True

			pygame.display.update()
			clock.tick(MAX_FPS)

	def User():

		global win, screenmode, Settings, alt_pressed, MAX_FPS

		bias = 0
		max_bias = -settings_ui._set_positions(bias, "User", True) + 900

		while True:
			
			click = pygame.mouse.get_pressed()
			mouse_x, mouse_y = pygame.mouse.get_pos()
			release = False
			
			events = pygame.event.get()
			
			for event in events:
				if event.type == pygame.QUIT:
					Saver.save_objects(path + "Settings/Settings.save", Settings)
					save()
					sys.exit()
				
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					release = True
				
				elif event.type == pygame.KEYUP:
					if event.key == hot_keys["Show keys"]:
						alt_pressed = not alt_pressed
					if event.key == hot_keys["Close"]:
						Saver.save_objects(path + "Settings/Settings.save", Settings)
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
					bias = max((min(bias + event.y * 100, 0)), max_bias)
					settings_ui._set_positions(bias, "User")
			
			# Очистка экрана
			win.fill((192, 203, 220))
			
			# Обработка UI
			settings_ui.handle_events(events, mouse_x, mouse_y, release, "User")
			settings_ui.draw("User", win, Width, Height, bias, max_bias)
			
			help_button.main(help)
			display_button.main(display)
			languages_button.main(Languages)
			win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/User 2.png"), (132, 64)), (10, 342))
			sound_button.main(Sound)
			statistics_button.main(Statistics)
			keys_button.main(Keys)
			game_button.main(Game)
			back_button.main()
			show_reset_settings()
			
			if alt_pressed:
				draw_key("ESC", 44, 108)

			if back_button.get_pressed():
				Saver.save_objects(path + "Settings/Settings.save", Settings)
				win_darken(win)
				menu()
				
			# Анимация и эффекты
			animate_click(Settings, win, mouse_x, mouse_y)
			win_fill(alpha=100 - Settings["Display"][0])
			
			pygame.display.update()
			clock.tick(MAX_FPS)


	def Sound():

		global win, screenmode, Settings, alt_pressed, MAX_FPS

		bias = 0
		max_bias = -settings_ui._set_positions(bias, "Sound", True) + 900

		while True:
			
			click = pygame.mouse.get_pressed()
			mouse_x, mouse_y = pygame.mouse.get_pos()
			release = False
			
			events = pygame.event.get()
			
			for event in events:
				if event.type == pygame.QUIT:
					Saver.save_objects(path + "Settings/Settings.save", Settings)
					save()
					sys.exit()
				
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					release = True
				
				elif event.type == pygame.KEYUP:
					if event.key == hot_keys["Show keys"]:
						alt_pressed = not alt_pressed
					if event.key == hot_keys["Close"]:
						Saver.save_objects(path + "Settings/Settings.save", Settings)
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
						Button_click.set_volume(Settings["Sound"][1] / 100)
						Stone_breaking1.set_volume(Settings["Sound"][1] / 100)
						Stone_breaking2.set_volume(Settings["Sound"][1] / 100)
						Grass_walking1.set_volume(Settings["Sound"][1] / 100)
						Grass_walking2.set_volume(Settings["Sound"][1] / 100)
						Grass_walking3.set_volume(Settings["Sound"][1] / 100)
						Snow_walking1.set_volume(Settings["Sound"][1] / 100)
						Snow_walking2.set_volume(Settings["Sound"][1] / 100)
						Snow_walking3.set_volume(Settings["Sound"][1] / 100)
						Sand_walking1.set_volume(Settings["Sound"][1] / 100)
						Sand_walking2.set_volume(Settings["Sound"][1] / 100)
						Sand_walking3.set_volume(Settings["Sound"][1] / 100)
						Swamp_walking1.set_volume(Settings["Sound"][1] / 100)
						Swamp_walking2.set_volume(Settings["Sound"][1] / 100)
						Swamp_walking3.set_volume(Settings["Sound"][1] / 100)
						Cave_walking1.set_volume(Settings["Sound"][1] / 100)
						Cave_walking2.set_volume(Settings["Sound"][1] / 100)
						Cave_walking3.set_volume(Settings["Sound"][1] / 100)
						Backrooms_lamps.set_volume(Settings["Sound"][1] / 100)
						Backrooms_rand_sound_1.set_volume(Settings["Sound"][1] / 100)
						Pick_an_item.set_volume(Settings["Sound"][1] / 100)

				elif event.type == pygame.MOUSEWHEEL:
					bias = max((min(bias + event.y * 100, 0)), max_bias)
					settings_ui._set_positions(bias, "Sound")
			
			# Очистка экрана
			win.fill((192, 203, 220))
			
			# Обработка UI
			settings_ui.handle_events(events, mouse_x, mouse_y, release, "Sound")
			settings_ui.draw("Sound", win, Width, Height, bias, max_bias)
			
			help_button.main(help)
			display_button.main(display)
			languages_button.main(Languages)
			user_button.main(User)
			win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Sound 2.png"), (160, 64)), (10, 417))
			statistics_button.main(Statistics)
			keys_button.main(Keys)
			game_button.main(Game)
			back_button.main()
			show_reset_settings()
			
			if alt_pressed:
				draw_key("ESC", 44, 108)

			if back_button.get_pressed():
				Saver.save_objects(path + "Settings/Settings.save", Settings)
				win_darken(win)
				menu()
				
			# Анимация и эффекты
			animate_click(Settings, win, mouse_x, mouse_y)
			win_fill(alpha=100 - Settings["Display"][0])
			
			pygame.display.update()
			clock.tick(MAX_FPS)

	def Statistics():

		global win, screenmode, Settings, alt_pressed, MAX_FPS

		bias = 0
		max_bias = -settings_ui._set_positions(bias, "Statistics", True) + 900

		while True:
			
			click = pygame.mouse.get_pressed()
			mouse_x, mouse_y = pygame.mouse.get_pos()
			release = False
			
			events = pygame.event.get()
			
			for event in events:
				if event.type == pygame.QUIT:
					Saver.save_objects(path + "Settings/Settings.save", Settings)
					save()
					sys.exit()
				
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					release = True
				
				elif event.type == pygame.KEYUP:
					if event.key == hot_keys["Show keys"]:
						alt_pressed = not alt_pressed
					if event.key == hot_keys["Close"]:
						Saver.save_objects(path + "Settings/Settings.save", Settings)
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
					bias = max((min(bias + event.y * 100, 0)), max_bias)
					settings_ui._set_positions(bias, "Statistics")
			
			# Очистка экрана
			win.fill((192, 203, 220))
			
			# Обработка UI
			settings_ui.draw("Statistics", win, Width, Height, bias, max_bias)
			
			help_button.main(help)
			display_button.main(display)
			languages_button.main(Languages)
			user_button.main(User)
			sound_button.main(Sound)
			win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Statistics 2.png"), (300, 64)), (10, 492))
			keys_button.main(Keys)
			game_button.main(Game)
			back_button.main()
			show_reset_settings()
			
			if alt_pressed:
				draw_key("ESC", 44, 108)

			if back_button.get_pressed():
				Saver.save_objects(path + "Settings/Settings.save", Settings)
				win_darken(win)
				menu()
				
			# Анимация и эффекты
			animate_click(Settings, win, mouse_x, mouse_y)
			win_fill(alpha=100 - Settings["Display"][0])
			
			pygame.display.update()
			clock.tick(MAX_FPS)

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
			
			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					Saver.save_objects(path + "Settings/Hot keys.save", hot_keys)
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
							Saver.save_objects(path + "Settings/Settings.save", Settings)
							Saver.save_objects(path + "Settings/Hot keys.save", hot_keys)
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
					time.sleep(0.1)
				else:
					Saver.save_objects(path + "Settings/Settings.save", Settings)
					Saver.save_objects(path + "Settings/Hot keys.save", hot_keys)
					win_darken(win)
					menu()
				
			win.fill((192, 203, 220))
			pygame.draw.rect(win, (139, 155, 180), (-8, 100, 373, Height), 8)
			pygame.draw.line(win, (139, 155, 180), (307, 103), (Width, 103), 8)
			back_button.main()
			show_reset_settings()
			help_button.main(help)
			display_button.main(display)
			languages_button.main(Languages)
			user_button.main(User)
			sound_button.main(Sound)
			statistics_button.main(Statistics)
			win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Keys 2.png"), (132, 64)), (10, 567))
			game_button.main(Game)
			
			littleTextInfo = pygame.font.Font(path + "Font.ttf", 8)
			key_color = (139, 155, 180)
			X = 385
			Y = 123
			close_key = ""

			for line_num, line in enumerate(key_values):
				for key_x, key in enumerate(line):
					key_size = key_sizes[line_num][key_x]
					key_rect = pygame.Rect(X, Y, key_size, 40)
					key_color = (139, 155, 180)
					if check_keys(key): key_color = (58, 68, 102)
					if key == looked_key: key_color = (139, 155, 180)
					if check_blocked_keys(key): key_color = (255, 255, 255)
					if key_values_combined[key] == hot_keys["Close"]: close_key = key
					if key_rect.collidepoint((mouse_x, mouse_y)): changed_key = key
					
					pygame.draw.rect(win, key_color, (X, Y, key_size, 40), 6 if changed_key == key else 3)
					win.blit(littleTextInfo.render(key, True, key_color), (X + 5, Y + 7))
					X += key_size + 10
				X = 385
				Y += 50
			
			text(t("Hotkeys are highlighted in dark blue"), 385, 440, (58, 68, 102))
			text(t("Locked keys are highlighted in white"), 385, 470, (255, 255, 255))
			text(t("To change the hot key, click on it"), 385, 500, (139, 155, 180))

			if Width - 30 - textInfo.size(t("Reset key settings"))[0] < mouse_x < Width - 30 and 420 < mouse_y < 450:
				win.blit(textInfo.render(t("Reset key settings"), True, (58, 68, 102)), (Width - 30 - textInfo.size(t("Reset key settings"))[0], 420))
				if click[0]:
					hot_keys = default_hot_keys
			else:
				win.blit(textInfo.render(t("Reset key settings"), True, (139, 155, 180)), (Width - 30 - textInfo.size(t("Reset key settings"))[0], 420))

			pygame.draw.rect(win, (139, 155, 180), (385, 530, Width - 500, 150))
			pygame.draw.rect(win, (58, 68, 102), (385, 530, Width - 500, 150), 5)
			text(changed_key if looked_key is None else f"Выбрана клавиша {looked_key}.\nНажмите {close_key}, чтобы отменить, либо выберите клавишу, которую Вы хотите назначить вместо неё.", 400, 545, (58, 68, 102))
			
			changed_key_key = ""
			if changed_key == "":
				changed_key_value = None
			else:
				changed_key_value = key_values_combined[changed_key]

			if changed_key_value is None:
				win.blit(textInfo.render(changed_key_key, True, (58, 68, 102)), (400, 575))
			else:
				for key, val in hot_keys.items():
					if val == changed_key_value:
						text("\n" + key, 400, 575, (58, 68, 102))
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

			animate_click(Settings, win, mouse_x, mouse_y)

			win_fill(alpha=100 - Settings["Display"][0])   # Если в настройках установлена яркость ниже 100, то экран становится темнее
			
			if not does_lighten:
				win_lighten(win)
				does_lighten = True

			pygame.display.update()
			clock.tick(MAX_FPS)

	def Game():

		global win, screenmode, Settings, alt_pressed, MAX_FPS

		bias = 0
		max_bias = -settings_ui._set_positions(bias, "Game", True) + 900

		while True:
			
			click = pygame.mouse.get_pressed()
			mouse_x, mouse_y = pygame.mouse.get_pos()
			release = False
			
			events = pygame.event.get()
			
			for event in events:
				if event.type == pygame.QUIT:
					Saver.save_objects(path + "Settings/Settings.save", Settings)
					save()
					sys.exit()
				
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					release = True
				
				elif event.type == pygame.KEYUP:
					if event.key == hot_keys["Show keys"]:
						alt_pressed = not alt_pressed
					if event.key == hot_keys["Close"]:
						Saver.save_objects(path + "Settings/Settings.save", Settings)
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
					bias = max((min(bias + event.y * 100, 0)), max_bias)
					settings_ui._set_positions(bias, "Game")
			
			# Очистка экрана
			win.fill((192, 203, 220))
			
			# Обработка UI
			settings_ui.handle_events(events, mouse_x, mouse_y, release, "Game")
			settings_ui.draw("Game", win, Width, Height, bias, max_bias)
			
			help_button.main(help)
			display_button.main(display)
			languages_button.main(Languages)
			user_button.main(User)
			sound_button.main(Sound)
			statistics_button.main(Statistics)
			keys_button.main(Keys)
			win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Game 2.png"), (132, 64)), (10, 642))
			back_button.main()
			show_reset_settings()
			
			if alt_pressed:
				draw_key("ESC", 44, 108)

			if back_button.get_pressed():
				Saver.save_objects(path + "Settings/Settings.save", Settings)
				win_darken(win)
				menu()
				
			# Анимация и эффекты
			animate_click(Settings, win, mouse_x, mouse_y)
			win_fill(alpha=100 - Settings["Display"][0])
			
			pygame.display.update()
			clock.tick(MAX_FPS)
	
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
			
			win.fill((192, 203, 220))

			pygame.draw.rect(win, (139, 155, 180), (-8, 100, 315, Height), 8)
			pygame.draw.rect(win, (139, 155, 180), (315, 100, Width - 325, 100), 8)
			pygame.draw.rect(win, (139, 155, 180), (316 + changed_character_num * 300, 210, 256, 256), 8)
			pygame.draw.rect(win, (139, 155, 180), (316, 476, 256, Height - 604), 8)
			pygame.draw.rect(win, (139, 155, 180), ((Width - 415) // 2 + 230, 476, 256, Height - 604), 8)
			pygame.draw.rect(win, (139, 155, 180), (Width - 266, 476, 256, Height - 604), 8)

			win.blit(textInfo.render(t("Name") + ":", True, (139, 155, 180)), (335, 120))
			win.blit(bigTextInfo.render(changed_character.name, True, (139, 155, 180)), (335, 140))
			pygame.draw.line(win, (139, 155, 180), (325 + len(changed_character.name) * 30, 100), (325 + len(changed_character.name) * 30, 198), 8)
			win.blit(textInfo.render(t("Info") + ":", True, (139, 155, 180)), (Width - len(changed_character.info) * 30 - 28, 120))
			win.blit(bigTextInfo.render(changed_character.info, True, (139, 155, 180)), (Width - len(changed_character.info) * 30 - 28, 140))
			back_button.main()
			
			if back_button.get_pressed():
				win_darken(win)
				menu()
			win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Character 2.png"), (278, 64)), (10, 120))
			pets_button.main(pets)
			
			page_back_button.main()
			if page_back_button.get_pressed() and page > 1: page -= 1
			page_next_button.main()
			
			if page_next_button.get_pressed() and page < 3: page += 1
			win.blit(bigTextInfo.render(str(page), True, (139, 155, 180)), ((Width - 415) // 2 + 340, Height - 96))

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

			animate_click(Settings, win, mouse_x, mouse_y)

			win_fill(alpha=100 - Settings["Display"][0])
			
			if not does_lighten:
				win_lighten(win)
				does_lighten = True

			pygame.display.update()
			clock.tick(MAX_FPS)
	
	def pets():

		global win, screenmode, does_lighten
		
		while True:
			
			mouse_x, mouse_y = pygame.mouse.get_pos()

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


			win.fill((192, 203, 220))

			pygame.draw.rect(win, (139, 155, 180), (-8, 100, 315, Height), 8)
			pygame.draw.rect(win, (139, 155, 180), (315, 100, Width - 325, 100), 8)

			back_button.main()

			if back_button.get_pressed():
				win_darken(win)
				menu()

			character_button.main(characters)

			win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Pets 2.png"), (132, 64)), (10, 192))

			animate_click(Settings, win, mouse_x, mouse_y)

			win_fill(alpha=100 - Settings["Display"][0])
			
			if not does_lighten:
				win_lighten(win)
				does_lighten = True
			
			pygame.display.update()
			clock.tick(MAX_FPS)

	characters()



multyplayer = False

hot_keys = Saver.load_objects(path + "Settings/Hot keys.save")
objects_templates = {
		"Table": Object("Table", 0, 0, "Images/Objects/Table.png", (256, 256), is_solid=True, breakable_by_hammer=True),
		"Wall table": Object("Wall table", 0, 0, "Images/Objects/Wall table.png", (256, 256), special_flags=1, is_solid=True, breakable_by_hammer=True),
		"Furnace": Object("Furnace", 0, 0, "Images/Items/Furnace.png", (256, 256), special_flags=1, is_solid=True, breakable_by_hammer=True),
		"Punch": Object("Punch", 0, 0, "Images/Objects/Punch 1.png", (256, 256), is_solid=True, breakable_by_hammer=True)
		}

# Основной цикл игры

def start_game():
	
	global win, changed_slot, menu_open, multyplayer_menu_open, screenmode, inventory_open, hold_left, backrooms, text_color, bullet_num, craft_items_list, craft_amounts_list, craft_images_list, screenshot_num, mouse_x, mouse_y, item_settings_open, multyplayer_panel, chat_tick, chat, main_chat, craft_list_open, craft_list_page, click, in_motherboard, os, world_name, color, multyplayer_mode, multyplayer, animation, start_time, new_particles, inside_files, game, alt_pressed, player, world, FPS, MAX_FPS, screen_rect, time_index

	night_playing = False
	input_text = ""
	chat_input = False
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

	new_particles = []

	if Settings["Game"][1]:
		up_b = Button(Width - 148, Height - 148, arrow_up, arrow_up, sound=False, cooldown=0)
		left_b = Button(Width - 222, Height - 74, arrow_left, arrow_left, sound=False, cooldown=0)
		down_b = Button(Width - 148, Height - 74, arrow_down, arrow_down, sound=False, cooldown=0)
		right_b = Button(Width - 74, Height - 74, arrow_right, arrow_right, sound=False, cooldown=0)

	# Загрузка данных мира

	from Inventory import Resource

	world.chunk_manager.save_directory = path + "Worlds/" + world_name + "/Chunks/"

	if os.path.exists(path + "Worlds/" + world_name):
		
		world.mobs = Saver.load_objects(path + "Worlds/" + world_name + "/Mobs.save")
		player.x, player.y, Backrooms.InBackrooms, Backrooms.Level, world.current_cave, player.speed, player.HP, start_time, ron.x, ron.y, ron.home, ron.inventory, world.chunk_manager.generator.seed, game_time.current_time = Saver.load_objects(path + "Worlds/" + world_name + "/Info.save")
		game.difficulty, player.god_mode = Saver.load_objects(path + "Worlds/" + world_name + "/Settings.save")
		inventory.whole_inventory = Saver.load_objects(path + "Worlds/" + world_name + "/Inventory.save")
		player.effects = Saver.load_objects(path + "Worlds/" + world_name + "/Effects.save")
		
	else:

		os.mkdir(path + "Worlds/" + world_name)
		os.mkdir(path + "Worlds/" + world_name + "/Images")

		save(False, True)

	inside_files = []
	for dirs, folder, files in os.walk(os.path.dirname(path) + "/Plugins/"):
		inside_files = files
		break
	
	for file in inside_files:

		for i in Saver.load_objects(path + "" + file):

			match i[0]:

				case "Item":

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
						a = Object(i[1], i[3], i[4], i[2], (pygame.image.load(i[2]).get_width(), pygame.image.load(i[2]).get_height()), special_flags=i[5], add_path=False)
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
		game_time.update(dt)
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT:
				statistics[1] += (time.time() - start_time) / 3600
				save()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					release = True
			elif event.type == pygame.KEYDOWN and chat_input:
				if event.key == pygame.K_RETURN:
					chat_input = False
					if input_text[0:2] == "/!" and player.god_mode:
						try:
							eval(input_text[2:])
							# команды лучше не использовать, так как из-за eval возникает проблема безопасности
						except Exception as e:
							chat_message(languages("<<< Команда " + Settings["User"][0] + f" получила ошибку {e}" + ". >>>", "<<< " + Settings["User"][0] + f"'s command got an {e}" + "error. >>>", ""))
						else:
							chat_message(languages("<<< Команда " + Settings["User"][0] + " была успешно исполнена. >>>", "<<< " + Settings["User"][0] + "'s command was successfully executed. >>>", ""))
					elif input_text[0] == "/":
						chat_message(command_system.execute(input_text))
					else:
						chat_message(Settings["User"][0] + ": " + input_text)

					input_text = ""
				elif event.key == pygame.K_BACKSPACE:
					input_text = input_text[:-1]
				elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
					clipboard_text = pyperclip.paste()
					if clipboard_text:
						input_text += clipboard_text
				elif len(input_text) <= 500:
					input_text += event.unicode
			
			elif event.type == pygame.MOUSEWHEEL and not any((item_settings_open, ron.window[0], in_motherboard, craft_list_open)):
				
				changed_slot += event.y
				if changed_slot > 9: changed_slot = 0
				if changed_slot < 0: changed_slot = 9

			if event.type == pygame.KEYUP:
				if chat_input:
					if event.key == hot_keys["Close"]:
						input_text = ""
						chat_input = False
				else:
					if event.key == hot_keys["Show keys"]:
						alt_pressed = not alt_pressed
					if event.key == hot_keys["Use item"]:
						use_item_pressed = True
					if event.key == hot_keys["Multyplayer menu"]:
						multyplayer_menu_open = True
					if event.key == hot_keys["Set Ron home"]:
						ron.home = [player.x, player.y]
					if event.key == hot_keys["Menu"]:
						menu_open = not menu_open
					if event.key == hot_keys["Open chat"]:
						chat_input = True
					if event.key == hot_keys["Execute command"]:
						chat_input = True
						input_text = "/"

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
							pygame.mixer.Sound.stop(Backrooms_lamps)
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
							menu()

					if event.key == pygame.K_1: changed_slot = 0
					if event.key == pygame.K_2: changed_slot = 1
					if event.key == pygame.K_3: changed_slot = 2
					if event.key == pygame.K_4: changed_slot = 3
					if event.key == pygame.K_5: changed_slot = 4
					if event.key == pygame.K_6: changed_slot = 5
					if event.key == pygame.K_7: changed_slot = 6
					if event.key == pygame.K_8: changed_slot = 7
					if event.key == pygame.K_9: changed_slot = 8
					if event.key == pygame.K_0: changed_slot = 9
					if event.key == pygame.K_o and False:
						create_light_circle(world.chunk_manager, player.x, player.y, 10, 15)
						# world.chunk_manager.chunks[(0, 0)].shadow_map.update({(0, 0): 0, (1, 0): 1, (2, 0): 2, (3, 0): 3, (4, 0): 4, (5, 0): 5, (6, 0): 6, (7, 0): 7, (8, 0): 8, (9, 0): 9, (10, 0): 10, (11, 0): 11, (12, 0): 12, (13, 0): 13, (14, 0): 14, (15, 0): 15})
						# world.chunk_manager.chunks[(0, 0)].light_map.update({(0, 1): 0, (1, 1): 1, (2, 1): 2, (3, 1): 3, (4, 1): 4, (5, 1): 5, (6, 1): 6, (7, 1): 7, (8, 1): 8, (9, 1): 9, (10, 1): 10, (11, 1): 11, (12, 1): 12, (13, 1): 13, (14, 1): 14, (15, 1): 15})


					if event.key == hot_keys["Help"]:
						music_channel.stop()
						pygame.mixer.Sound.stop(Backrooms_lamps)
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
							
							match player.direction:
								
								case "Down":
									x_bias_ = 0
									y_bias_ = lambda particle: -(30 - particle.ticks * 2.5)
								case "Up":
									x_bias_ = 0
									y_bias_ = lambda particle: (30 - particle.ticks * 2.5)
								case "Left":
									x_bias_ = lambda particle: -(30 - particle.ticks * 2.5)
									y_bias_ = lambda particle: (15 - particle.ticks * 4)
								case "Right":
									x_bias_ = lambda particle: (30 - particle.ticks * 2.5)
									y_bias_ = lambda particle: (15 - particle.ticks * 4)
								case "Up-right":
									x_bias_ = lambda particle: (30 - particle.ticks * 2.5)
									y_bias_ = lambda particle: (30 - particle.ticks * 2.5)
								case "Up-left":
									x_bias_ = lambda particle: -(30 - particle.ticks * 2.5)
									y_bias_ = lambda particle: (30 - particle.ticks * 2.5)
								case "Down-right":
									x_bias_ = lambda particle: (30 - particle.ticks * 2.5)
									y_bias_ = lambda particle: -(30 - particle.ticks * 2.5)
								case "Down-left":
									x_bias_ = lambda particle: -(30 - particle.ticks * 2.5)
									y_bias_ = lambda particle: -(30 - particle.ticks * 2.5)

							world.particles.append(Particle(player.x, player.y,
									   inventory.whole_inventory[changed_slot].image,
									   x_bias_, y_bias_,
									   track_ticks=True,
									   end_time=0.5,
									   end_command=lambda particle: (world.chunk_manager.get_chunk_at(particle.x, particle.y).items.append(Object(particle.special_flags, particle.x, particle.y, "Images/Items/" + particle.special_flags + ".png", pickable=True))),
									   special_flags=inventory.whole_inventory[changed_slot].name))
							
							del x_bias_
							del y_bias_
						
						inventory.whole_inventory[changed_slot].amount -= 1
						if inventory.whole_inventory[changed_slot].amount == 0:
							inventory.whole_inventory[changed_slot] = None

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

		inside_files = []

		for dirs, folder, files in os.walk(os.path.dirname(path) + "/Plugins/"):
			inside_files = files
			break
		
		for file in inside_files:
			for i in Saver.load_objects(path + "" + file):
				if i[0] == "Command" and i[2] == "2":
					try:
						eval(i[1])
					except:
						pass
		
		keys = pygame.key.get_pressed()

		if not chat_input:

			if keys[hot_keys["Move left"]]: dx = -1 + (keys[hot_keys["Move up"]] or keys[hot_keys["Move down"]]) * 0.3
			if keys[hot_keys["Move right"]]: dx = 1 - (keys[hot_keys["Move up"]] or keys[hot_keys["Move down"]]) * 0.3
			if keys[hot_keys["Move down"]]: dy = -1 + (keys[hot_keys["Move left"]] or keys[hot_keys["Move right"]]) * 0.3
			if keys[hot_keys["Move up"]]: dy = 1 - (keys[hot_keys["Move left"]] or keys[hot_keys["Move right"]]) * 0.3

		# Если есть движение - двигаем игрока
		if dx != 0 or dy != 0:
			player.move(dx, dy, dt)
		else:
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
			world.render_loaded_chunks()
			if game_time.day_phase == "Night" and not night_playing:
				music_channel.stop()
				music_channel.play(pygame.mixer.Sound(path + "Soundtracks/Night " + str(random.randint(1, 2)) + ".mp3"))
				night_playing = True

			elif not music_channel.get_busy() or (night_playing and game_time.day_phase != "Night"):

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
						
			elif not chat_input and any((keys[hot_keys["Move left"]], keys[hot_keys["Move right"]], keys[hot_keys["Move up"]], keys[hot_keys["Move down"]], Settings["Game"][1] and any((left_b.get_pressed(), up_b.get_pressed(), down_b.get_pressed(), right_b.get_pressed())))) and random.randint(1, 10) == 1:

				if world.current_cave is not None:
					pygame.mixer.Sound.play(random.choice((Cave_walking1, Cave_walking2, Cave_walking3)), maxtime=1000)

				elif current_biome in ("Forest", "Field"):
					pygame.mixer.Sound.play(random.choice((Grass_walking1, Grass_walking2, Grass_walking3)), maxtime=1000)

				elif current_biome == "Desert":
					pygame.mixer.Sound.play(random.choice((Sand_walking1, Sand_walking2, Sand_walking3)), maxtime=1000)

				elif current_biome == "Taiga":
					pygame.mixer.Sound.play(random.choice((Snow_walking1, Snow_walking2, Snow_walking3)), maxtime=1000)

				elif current_biome == "Swamp":
					pygame.mixer.Sound.play(random.choice((Swamp_walking1, Swamp_walking2, Swamp_walking3)), maxtime=1000)

		else:

			for i, ii in product(range(-6, 6), range(-3, 3)):
				win.blit(textures["Backrooms " + str(Backrooms.Level)], (Width - player.x % 256 + i * 256, player.y % 256 + ii * 256))
		
		for mechanism in world.mechanisms:
			mechanism.main()

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

				pygame.mixer.Sound.play(Backrooms_lamps, -1)
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
					...#win.fill((120, 100, 40))
				case 0.2:
					...#win.fill((170, 60, 50))
				case 1:
					win.fill((100, 100, 100))
				case 2:
					win.fill((50, 50, 50))

			for room in Backrooms.rooms:
				room.main(player.x, player.y)

			if random.randint(1, 1000) == 1:
				pygame.mixer.Sound.play(Backrooms_rand_sound_1)
			
			match Backrooms.Level:

				case 0:

					wall_color = Color(180, 159, 50)
					next_levels = [0.2, 1]

				case 0.2:

					wall_color = Color(200, 180, 70)
					next_levels = [0, 1]

				case 1:

					wall_color = Color(50, 50, 50)
					next_levels = [2]

				case 2:

					wall_color = Color(50, 50, 50)

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

				if Backrooms.Level == 0:
					pygame.mixer.Sound.stop(Backrooms_lamps)

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
				win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Objects/Cave.png"), (128, 128)), (0 - player.x + Width // 2 - world.current_cave.w // 2, player.y - 0 + Height // 2 - world.current_cave.h // 2))

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
									pygame.mixer.Sound.play(random.choice((Stone_breaking1, Stone_breaking2)))

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
									pygame.mixer.Sound.play(random.choice((Stone_breaking1, Stone_breaking2)))

								if object.special_flags == -1:
									world.current_cave.objects.remove(object)
									for _ in range(random.randint(1, 3)):
										world.current_cave.objects.append(Object("Gold ore", random.randint(object.x - 128, object.x + 128), random.randint(object.y - 128, object.y + 128), "Images/Items/Gold ore.png", special_flags="Item"))
									break

						if object.name == "Pot":
							if object.get_right_pressed() and inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].type == "Flower":
								world.chunk_manager.get_chunk_at(object.x, object.y).items.append(Object(inventory.whole_inventory[changed_slot].name, object.x, object.y + 36, 64, 64, inventory.whole_inventory[changed_slot].image))
								inventory.whole_inventory[changed_slot].amount -= 1
								inventory.resources[inventory.whole_inventory[changed_slot].name].amount -= 1
								if inventory.whole_inventory[changed_slot].amount == 0:
									inventory.whole_inventory[changed_slot] = None
				
			else:

				# Обновление мира
				world.update() #TODO оптимизировать

				# Отображение объектов

				for object in world.visible_objects:

					object.main(dt)

					if object.get_left_pressed():

						if object.name == "Pond":

							if object.special_flags[0] == 0:
								...
							elif inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name == "Bucket":

								if inventory.whole_inventory[changed_slot].amount > 1:
									inventory.whole_inventory[changed_slot].amount -= 1
								else:
									inventory.whole_inventory[changed_slot] = None

								inventory.increate("Water bucket")
								object.special_flags[0] -= 1
								time.sleep(0.15)
			
							if object.special_flags[1] != 0 and inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name == "Stone shovel" and object.get_left_pressed() and random.randint(1, 30) == 1:
								rand_x, rand_y = object.x +random.randint(-128, 128), object.y + random.randint(-128, 128)
								world.chunk_manager.get_chunk_at(rand_x, rand_y).items.append(Object("Clay", rand_x, rand_y, "Images/Items/Clay.png", pickable=True))
								object.special_flags[1] -= 1

						mouse_object = object.name

						if object.name == "Pot":

							if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].type == "Flower":
								world.chunk_manager.get_chunk_at(object.x, object.y + 36).items.append(Object(inventory.whole_inventory[changed_slot].name, object.x, object.y + 36, 64, 64, inventory.whole_inventory[changed_slot].image))
								inventory.whole_inventory[changed_slot].amount -= 1
								inventory.resources[inventory.whole_inventory[changed_slot].name].amount -= 1
								if inventory.whole_inventory[changed_slot].amount == 0:
									inventory.whole_inventory[changed_slot] = None

					if object.name == "Dandelion" and time.time() - object.start_time > 1200:

						object.start_time = time.time()
						
						try:
							object.image_path = path + "Images/Objects/Dandelion " + str(int(object.image_path[-5]) + 1) + ".png"
							object.image = pygame.transform.scale(pygame.image.load(object.image_path), (64, 64))
						except:
							world.chunk_manager.get_chunk_at(object.x, object.y).objects.remove(object)

						if object.image_path[-5] == "5":

							for _ in range(5):

								if random.randint(1, 5) == 1:
									world.particles.append(Particle(object.x, object.y, pygame.transform.scale(pygame.image.load(path + "Images/Items/Dandelion seed.png"), (32, 32)), random.randint(-30, 30), random.randint(-30, 30), end_time=5, end_command=lambda particle: (world.chunk_manager.get_chunk_at(particle.x, particle.y).items.append(Object("Dandelion", particle.x, particle.y, "Images/Objects/Dandelion 1.png")))))
								else:
									world.particles.append(Particle(object.x, object.y, pygame.transform.scale(pygame.image.load(path + "Images/Items/Dandelion seed.png"), (32, 32)), random.randint(-30, 30), random.randint(-30, 30), end_time=5))

					if object.name == "Punch" and False:

						if object.get_left_pressed() and inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name in ("Mushroom", "Red mushroom", "Thread", "Poppy", "Purple tulip", "Orange tulip", "Black tulip", "Red tulip", "Yellow tulip", "Dandelion", "Cotton grass", "Onion"):
							if object.special_flags < 11:
								object.special_flags += 1
								if object.special_flags > 6:
									object.image = pygame.image.load(path + "Images/Objects/Punch " + str(object.special_flags - 5) + ".png")
							else:
								object.special_flags = 1
								world.chunk_manager.get_chunk_at(object.x, object.y).items.append(Object("Punch", object.x, object.y, "Images/Items/Powder.png"))

				# Отображение предметов
				for item in world.visible_items:
					item.main(player)
					try_pick = True
					if item.pickable and Settings["Game"][0] and player.x - 150 < item.x < player.x + 150 and player.y - 150 < item.y < player.y + 150:
						world.particles.append(Particle(item.x, item.y, item.image, lambda particle: round(((player.x - particle.x) // 2) / 10 * 5), lambda particle: round(((player.y - particle.y) // 2) / 10 * 5), track_ticks=True, del_self_condition=lambda particle: abs(particle.x - player.x) < 30 and abs(particle.y - player.y) < 30, end_command=lambda particle: (inventory.increate(item.name), pygame.mixer.Sound.play(Pick_an_item))))
						world.chunk_manager.get_chunk_at(item.x, item.y).items.remove(item)
						try_pick = False

					if try_pick and item.x - player.x + Width // 2 - item.image.get_width() // 2 <= mouse_x <= item.x - player.x + Width // 2 + item.image.get_width() // 2 and player.y - item.y + Height // 2 - item.image.get_height() // 2 <= mouse_y <= player.y - item.y + Height // 2 + item.image.get_height() // 2:
						mouse_object = t("Click to pick the ") + t("Item name " + item.name)
						
						if click[0]:
							world.particles.append(Particle(item.x, item.y, item.image, lambda particle: round(((player.x - particle.x) // 2) / 10 * 5), lambda particle: round(((player.y - particle.y) // 2) / 10 * 5), track_ticks=True, del_self_condition=lambda particle: abs(particle.x - player.x) < 30 and abs(particle.y - player.y) < 30, end_command=lambda particle: (inventory.increate(particle.special_flags), pygame.mixer.Sound.play(Pick_an_item)), special_flags=item.name))
									
							world.chunk_manager.get_chunk_at(item.x, item.y).items.remove(item)

		elif len(Backrooms.objects) != 1:

			for object in backrooms_objects:

				object.main()

				if click[0] and object.x - player.x + Width // 2 - object.w // 2 <= mouse_x <= object.x - player.x + Width // 2 + object.w // 2 and player.y - object.y + Height // 2 - object.h // 2 <= mouse_y <= player.y - object.y + Height // 2 + object.h // 2:

					mouse_object = object.name

					if object.name == "Pot":

						if object.get_right_pressed() and inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].type == "Flower":
							world.chunk_manager.get_chunk_at(object.x, object.y).items.append(Object(inventory.whole_inventory[changed_slot].name, object.x, object.y + 36, 64, 64, inventory.whole_inventory[changed_slot].image))
							inventory.whole_inventory[changed_slot].amount -= 1
							inventory.resources[inventory.whole_inventory[changed_slot].name].amount -= 1
							if inventory.whole_inventory[changed_slot].amount == 0:
								inventory.whole_inventory[changed_slot] = None

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
		
		if not Backrooms.InBackrooms and world.current_cave is None and (not multyplayer or multyplayer_mode == "My game"):

			if game_time.day_phase == "Night":
				if random.randint(1, 800) == 1:
					try: world.mobs.append(Spider(random.randint(player.x - Width, player.x + Width), random.randint(player.y - Height, player.y + Height)))
					except:pass
			else:
				if random.randint(1, 800) == 1:
					try: world.mobs.append(Slime(random.randint(player.x - Width, player.x + Width), random.randint(player.y - Height, player.y + Height)))
					except:pass

		for projectile in world.projectiles:
			projectile.main()
		
		for farmland in world.visible_farmlands.values():
			farmland.main(release)

		for wall in world.visible_walls.values():
			wall.main(release)
		
		if not Backrooms.InBackrooms and world.current_cave is None:

			# Отображение мобов
			for mob in world.mobs:

				mob.update(player, world)
				mob.draw(player)

				if world.projectiles != []:

					if mob.name == "Slime": mob_rect = pygame.Rect((mob.x, mob.y - 64, 128, 128))
					else: mob_rect = pygame.Rect((mob.x, mob.y - 128, 256, 256))

					if check_projectiles_collision(mob_rect):

						mob.HP -= 15

						if mob.name == "Slime":
							temp = mob.animation_frames[(mob.animation_count - mob.animation_count % 5) // 5].copy().convert_alpha()
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
		
		player.render(win, dx, dy)

		# Анимации Хиро

		if animation[0] is None:
			
			if random.randint(1, 300) == 1:
				animation = ["Close eyes", 0, 16]

		elif animation[1] <= animation[2]:
			animation[1] += 1
		else:
			animation = [None, 0]
		
		if inventory.whole_inventory[changed_slot] is None:
			a = False
		else:
			a = True

		match player.direction:

			case "Down":

				match player.costum:
					# 97, 209
					case 0 | 1 | 3 | 4 | 6 | 7:

						if a:
							win.blit(inventory.whole_inventory[changed_slot].image, (Width // 2 - 80, Height // 2))

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

						if a:
							win.blit(inventory.whole_inventory[changed_slot].image, (Width // 2 - 74, Height // 2 - 16))

						match animation[0]:

							case "Close eyes":

								if animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, animation[1] * 2))
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, (8 - animation[1] + 8) * 2))
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, (8 - animation[1] + 8) * 2))

					case 5:

						if a:
							win.blit(inventory.whole_inventory[changed_slot].image, (Width // 2 - 94, Height // 2 - 16))

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

						if a:
							win.blit(inventory.whole_inventory[changed_slot].image, (Width // 2 - 84, Height // 2 - 16))

						match animation[0]:

							case "Close eyes":

								if animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 32, 8, animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 32, 8, (8 - animation[1] + 8) * 2))

					case 2:

						if a:
							win.blit(inventory.whole_inventory[changed_slot].image, (Width // 2 - 104, Height // 2))

						match animation[0]:

							case "Close eyes":

								if animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, (8 - animation[1] + 8) * 2))

					case 5:

						if a:
							win.blit(inventory.whole_inventory[changed_slot].image, (Width // 2 - 70, Height // 2))

						match animation[0]:

							case "Close eyes":

								if animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, (8 - animation[1] + 8) * 2))

			case "Right":

				match player.costum:

					case 0 | 1 | 3 | 4:

						if a:
							win.blit(pygame.transform.flip(inventory.whole_inventory[changed_slot].image, True, False), (Width // 2 - 20, Height // 2))

						match animation[0]:

							case "Close eyes":

								if animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 32, 8, animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 32, 8, (8 - animation[1] + 8) * 2))

					case 2:

						if a:
							win.blit(pygame.transform.flip(inventory.whole_inventory[changed_slot].image, True, False), (Width // 2 - 32, Height // 2))

						match animation[0]:

							case "Close eyes":

								if animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, (8 - animation[1] + 8) * 2))

					case 5 | 6 | 7:

						if a:
							win.blit(pygame.transform.flip(inventory.whole_inventory[changed_slot].image, True, False), (Width // 2 - 16, Height // 2 + 16))

						match animation[0]:

							case "Close eyes":

								if animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, (8 - animation[1] + 8) * 2))

		# Рон

		ron.update(world, dt)

		# Механика использования еды и некоторых предметов через пробел

		for i in range(Settings["Display"][2]):
			win.blit(pygame.transform.scale(win, (Width - i * 2, Height - i * 2)), (i, i))

		if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name in ("Gun", "Bow") and Settings["Game"][1]:
			win.blit(Inventory_slot, (Width - 370, Height - 74))
			win.blit(inventory.whole_inventory[changed_slot].image, (Width - 370, Height - 74))
		
		if (inventory.whole_inventory[changed_slot] is not None and (use_item_pressed or (click[0] and Settings["Game"][1]))) and not chat_input:

			match inventory.whole_inventory[changed_slot].name:

				case "Gun":

					for item_index, slot in enumerate(inventory.whole_inventory):
						if slot is not None and slot.name == "Bullet":
							if inventory.whole_inventory[item_index].amount > 1:
								inventory.whole_inventory[item_index].amount -= 1
							else:
								inventory.whole_inventory[item_index] = None
							world.projectiles.append(Projectile(player.x, player.y, mouse_x, mouse_y, "Bullet"))
							bullet_num += 1
							break
					else:
						text(t("You don't have bullets to shoot"), Width // 2, Height // 2, (200, 30, 30), alignment=True)

				case "Bow":

					for item_index, slot in enumerate(inventory.whole_inventory):
						if slot is not None and slot.name == "Arrow":
							if inventory.whole_inventory[item_index].amount > 1:
								inventory.whole_inventory[item_index].amount -= 1
							else:
								inventory.whole_inventory[item_index] = None
							world.projectiles.append(Projectile(player.x, player.y, mouse_x, mouse_y, "Arrow"))
							bullet_num += 1
							break
					else:
						text(t("You don't have arrows to shoot"), Width // 2, Height // 2, (200, 30, 30), alignment=True)

				case "Beer":

					player.effects.append(["Drunk", 180])
					if inventory.whole_inventory[changed_slot].amount > 1:
						inventory.whole_inventory[changed_slot].amount -= 1
					else:
						inventory.whole_inventory[changed_slot] = None

				case "Grenade":

					world.projectiles.append(ExplodingProjectile(player.x, player.y, mouse_x, mouse_y, "Grenade", (player.x + mouse_x - Width // 2, player.y - mouse_y + Height // 2)))

					if inventory.whole_inventory[changed_slot].amount > 1:
						inventory.whole_inventory[changed_slot].amount -= 1
					else:
						inventory.whole_inventory[changed_slot] = None
						
			if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].type == "Food":
				
				player.HP += inventory.whole_inventory[changed_slot].special_info
				if inventory.whole_inventory[changed_slot].amount > 1:
					inventory.whole_inventory[changed_slot].amount -= 1
				else:
					inventory.whole_inventory[changed_slot] = None
				
		

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
					world.particles.append(Particle(random.randint(1, Width), -50, pygame.transform.scale(pygame.image.load(path + "Images/Objects/Drop.png"), (64, 64)),  x_bias=random.randint(-5, 5) + offset, y_bias=random.randint(30, 40), display_mode=lambda X, Y, w, h: (X, Y), end_y=Height, end_zone=30))

		# Отображение частиц

		for particle in world.particles:

			particle.main(dt)
			
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
			current_brightness = game_time.get_brightness()
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

		if keys[hot_keys["TAB menu"]] and not chat_input:

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
						multyplayer_menu_open = True
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
					if special_slot_animations["Multyplayer slot"][0]:
						if special_slot_animations["Multyplayer slot"][1] < FPS / 6:
							special_slot_animations["Multyplayer slot"][1] += 1
							special_slot_animations["Multyplayer slot"][2] -= 3
							special_slot_animations["Multyplayer slot"][2] = abs(special_slot_animations["Multyplayer slot"][2])
					else:
						special_slot_animations["Multyplayer slot"] = [True, 0, 10]
					
					if click[0]:
						multyplayer_menu_open = True
						b = True
						display_speed = 7

				elif special_slot_animations["Multyplayer slot"][0]:
					special_slot_animations["Multyplayer slot"][0] = False
					special_slot_animations["Multyplayer slot"][1] = 0
				elif special_slot_animations["Multyplayer slot"][1] < FPS / 4:
					special_slot_animations["Multyplayer slot"][1] += 1   

				if special_slot_animations["Multyplayer slot"][0] and Settings["Display"][5]:
					try:win.blit(pygame.transform.scale(Multyplayer_slot2, (64 - special_slot_animations["Multyplayer slot"][2], 64 - special_slot_animations["Multyplayer slot"][2])), (Width // 2 + math.cos((2 * math.pi * 3) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 3) / 6) * radius - 32))
					except: win.blit(Multyplayer_slot2, (Width // 2 + math.cos((2 * math.pi * 3) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 3) / 6) * radius - 32))
				
				else:
					win.blit(Multyplayer_slot1, (Width // 2 + math.cos((2 * math.pi * 3) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 3) / 6) * radius - 32))

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
				win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Slots/Open inventory slot.png"), (64, 64)), (890, 10))
				if 890 <= mouse_x <= 954 and 10 <= mouse_y <= 74 and click[0]:
					inventory_open = False
			else:
				win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Slots/Open inventory slot.png"), (64, 64)), (810, 10))
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
			win.blit(Tool_inventory_slot, (90, 250))

			item_to_get = inventory.check_recipies(player, world, craft_items_list, craft_amounts_list)
			
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

				back_button = Button(114, Height - 176, bigTextInfo.render("<", True, (0, 150, 0)), bigTextInfo.render("<", True, (0, 100, 0)))
				next_button = Button(Width - 144, Height - 176, bigTextInfo.render(">", True, (0, 150, 0)), bigTextInfo.render(">", True, (0, 100, 0)))
				win.blit(Changed_craft_list_inventory_slot, (810, 90))
				win_fill()
				pygame.draw.rect(win, text_color, (100, 100, Width - 200, Height - 200))
				pygame.draw.rect(win, (0, 150, 0), (100, 100, Width - 200, Height - 200), 10)
				win.blit(bigTextInfo.render("x", True, (0, 150, 0)), (Width - 160, 130))
				
				if alt_pressed:
					draw_key("ESC", Width - 160, 170)
					
				if Width - 160 <= mouse_x <= Width - 130 and 130 <= mouse_y <= 160:
					win.blit(bigTextInfo.render("x", True, (0, 100, 0)), (Width - 160, 130))
					if release:
						craft_list_open = False
						
				win.blit(bigTextInfo.render(str(craft_list_page), True, (0, 150, 0)), (Width // 2 - 15, Height - 230))
				back_button.main()
				if back_button.get_pressed() and craft_list_page != 1:
					craft_list_page -= 1
				next_button.main()
				if next_button.get_pressed() and craft_list_page < len(inventory.recipes) / 5:
					craft_list_page += 1
				a = -1
				if craft_list_page < len(inventory.recipes) / 5 or len(inventory.recipes) % 5 == 0:
					for i in range((craft_list_page - 1) * 5 - 1, (craft_list_page - 1) * 5 + 5 - 1):
						a += 1
						aa = -1
						for ii in inventory.recipes[i].ingredients:
							if ii is None:
								break
							else:
								aa += 1
								win.blit(Inventory_slot, (130 + aa * 80, 130 + a * 80))
								try:
									win.blit(inventory.resources[ii].image, (130 + aa * 80, 130 + a * 80))
								except KeyError:
									win.blit(no_file_texture, (130 + aa * 80, 130 + a * 80))
								win.blit(textInfo.render(str(inventory.recipes[i].ingredients_amounts[aa]), True, (0, 150, 0)), (140 + aa * 80, 172 + a * 80))
						aa += 1
						if inventory.recipes[i].need_object is not None:
							win.blit(Changed_inventory_slot, (150 + aa * 80, 130 + a * 80))
							try:
								win.blit(inventory.resources[inventory.recipes[i].need_object].image, (200 + aa * 80, 130 + a * 80))
							except KeyError:
								win.blit(no_file_texture, (200 + aa * 80, 130 + a * 80))
						aa += 1
						if inventory.recipes[i].need_tool is not None:
							win.blit(Changed_inventory_slot, (150 + aa * 80, 130 + a * 80))
							try:
								win.blit(inventory.resources[inventory.recipes[i].need_tool].image, (200 + aa * 80, 130 + a * 80))
							except KeyError:
								win.blit(no_file_texture, (200 + aa * 80, 130 + a * 80))
						aa += 1
						win.blit(Changed_inventory_slot, (150 + aa * 80, 130 + a * 80))
						try:
							win.blit(inventory.resources[inventory.recipes[i].result].image, (200 + aa * 80, 130 + a * 80))
							win.blit(textInfo.render(str(inventory.recipes[i].result_amount), True, (0, 150, 0)), (210 + aa * 80, 172 + a * 80))
						except KeyError:
							win.blit(no_file_texture, (200 + aa * 80, 130 + a * 80))
						
				else:

					b = ""

					for i in ((craft_list_page - 1) * 5 - 1, (craft_list_page - 1) * 5 - 1 + len(inventory.recipes) % 5):
						b += str(i) + " "

					for craft_y, i in enumerate(((craft_list_page - 1) * 5 - 1, (craft_list_page - 1) * 5 - 1 + len(inventory.recipes) % 5)):

						aa = -1

						for ii in inventory.recipes[i].ingredients:

							if ii is None:
								break
							
							else:
								aa += 1
								win.blit(Inventory_slot, (130 + aa * 80, 130 + craft_y * 80))
								win.blit(inventory.resources[ii].image, (130 + aa * 80, 130 + craft_y * 80))
								win.blit(textInfo.render(str(inventory.recipes[i].ingredients_amounts[aa]), True, (0, 150, 0)), (140 + aa * 80, 172 + craft_y * 80))

						aa += 1

						if inventory.recipes[i].need_object is not None:
							win.blit(Changed_inventory_slot, (150 + aa * 80, 130 + craft_y * 80))
							win.blit(inventory.resources[inventory.recipes[i].need_object].image, (200 + aa * 80, 130 + craft_y * 80))

						aa += 1

						if inventory.recipes[i].need_tool is not None:
							win.blit(Changed_inventory_slot, (150 + aa * 80, 130 + craft_y * 80))
							win.blit(inventory.resources[inventory.recipes[i].need_tool].image, (200 + aa * 80, 130 + craft_y * 80))

						aa += 1

						win.blit(Changed_inventory_slot, (150 + aa * 80, 130 + craft_y * 80))
						win.blit(inventory.resources[inventory.recipes[i].result].image, (200 + aa * 80, 130 + craft_y * 80))
						win.blit(textInfo.render(str(inventory.recipes[i].result_amount), True, (0, 150, 0)), (210 + aa * 80, 172 + craft_y * 80))
						
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

		if ron.x - player.x + Width // 2 - 128 <= mouse_x <= ron.x - player.x + Width // 2 + 128 and player.y - ron.y + Height // 2 - 128 <= mouse_y <= player.y - ron.y + Height // 2 + 128 and release:
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
						inventory.whole_inventory[changed_slot].amount -= 1
						if inventory.whole_inventory[changed_slot].amount == 0:
							inventory.whole_inventory[changed_slot] = None
						world.mechanisms.append(Wire(None))
			else:
				a = True
				if click[0]:
					for mechanism in in_motherboard.objects:
						if mechanism is not None and mechanism.x == (mouse_x - Width // 2 - 300) // 18.75 and mechanism.y == (mouse_y + Width // 2 - 300) // 18.75:
							a = False
							break
				
					if a and Width // 2 - 300 <= mouse_x <= Width // 2 + 300 and  Height // 2 - 310 <= mouse_y < Height // 2 + 290:
						inventory.whole_inventory[changed_slot].amount -= 1
						if inventory.whole_inventory[changed_slot].amount == 0:
							inventory.whole_inventory[changed_slot] = None
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
					inventory.whole_inventory[changed_slot].amount -= 1
					if inventory.whole_inventory[changed_slot].amount == 0:
						inventory.whole_inventory[changed_slot] = None
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
					inventory.whole_inventory[changed_slot].amount -= 1
					if inventory.whole_inventory[changed_slot].amount == 0:
						inventory.whole_inventory[changed_slot] = None
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
					inventory.whole_inventory[changed_slot].amount -= 1
					if inventory.whole_inventory[changed_slot].amount == 0:
						inventory.whole_inventory[changed_slot] = None
					world.mechanisms.append(Motherboard(None))
		if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name == "Portal gun":

			draw_select_image(128, 256, player, mouse_x, mouse_y)

			if click[0]:

				a = 0
				if not check_collision(pygame.Rect((player.x + mouse_x - Width // 2) // 256 * 256 + 128, (player.y - mouse_y + Height // 2) // 256 * 256 + 128, 256, 256), world, False):
					world.chunk_manager.get_chunk_at((player.x + mouse_x - Width // 2) // 128, (player.y + mouse_y - Height // 2) // 256).objects.append(Portal())
		build_tuple = (changed_slot, player, world, inventory.whole_inventory)
		check_build_objects(objects_templates, build_tuple)
		# if build(build_tuple, Object("Farmland", 0, 0, "Images/Objects/Farmland.png", (128, 128), special_flags=1), "Stone hoe", get_item_from_inventory=0):
		# 	pygame.mixer.Sound.play(pygame.mixer.Sound(path + "Sounds/Dirt.mp3"))
		# if inventory.whole_inventory[changed_slot] is None: a = ""
		# else:
		# 	a = inventory.whole_inventory[changed_slot].name[:-6] if " seeds" in inventory.whole_inventory[changed_slot].name else inventory.whole_inventory[changed_slot].name
		
		# try: build(build_tuple, Particle(0, 0, pygame.transform.scale(pygame.image.load(path + "Images/Objects/" + a + " 1.png"), (128, 128)), can_interfere_with_placing=True, end_time=random.randint(1, 3),
		# 			end_command="world.particles.append(Particle(particle.x, particle.y, pygame.transform.scale(pygame.image.load(path + 'Images/Objects/' + particle.special_flags[0] + ' 2.png'), (128, 128)), can_interfere_with_placing=True, end_time=random.randint(5, 10), save_particle=True, tick_command=particle.special_flags[1], tick_command_locals={'a': 0, 'b': 0}, tick_command_globals={'world_to_screen': world_to_screen, 'win_fill': win_fill, 'random': random}, tick_command_globals_in_the_end=('inventory', 'changed_slot'), end_command=particle.special_flags[3], end_command_globals={'random': random}, special_flags=particle.special_flags))", end_command_globals={"world.particles": world.particles, "Particle": Particle, "random": random, "world_to_screen": world_to_screen, "win_fill": win_fill}, save_particle=True, special_flags=[a, """
# if self.special_flags[2]:
	# a, b = world_to_screen(self.x, self.y, 128, 128)
	# win_fill((255, 255, 255), 30, (a, b, 128, 128))
	# if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name == "Water bucket" and pygame.Rect(a, b, 128, 128).collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
		# inventory.whole_inventory[changed_slot].amount -= 1
		# if inventory.whole_inventory[changed_slot].amount < 1: inventory.whole_inventory[changed_slot] = None
		# inventory.increate("Bucket", 1)
		# self.special_flags[2] = False
		# pygame.mixer.Sound.play(pygame.mixer.Sound(path + "Sounds/Watering plants " + str(random.randint(1, 2)) + ".mp3"))""", True, """
# if particle.special_flags[2]: world.particles.append(Particle(particle.x, particle.y, pygame.transform.scale(pygame.image.load(path + 'Images/Objects/' + particle.special_flags[0] + ' 4.png'), (128, 128)), can_interfere_with_placing=True, save_particle=True, del_self_condition=lambda particle: (click[0] and pygame.Rect(particle.x - player.x + Width // 2 - particle.image.get_width() // 2, player.y - particle.y + Height // 2 - particle.image.get_height() // 2, particle.w, particle.h).collidepoint(mouse_x, mouse_y)), end_command='pygame.mixer.Sound.play(pygame.mixer.Sound(path + "Sounds/Breaking.mp3"))'))
# else: world.particles.append(Particle(particle.x, particle.y, pygame.transform.scale(pygame.image.load(path + 'Images/Objects/' + particle.special_flags[0] + ' 3.png'), (128, 128)), can_interfere_with_placing=True, save_particle=True, tick_command='''
# if click[0] and pygame.Rect(self.display_mode(self.x, self.y, self.w, self.h)[0], self.display_mode(self.x, self.y, self.w, self.h)[1], self.w, self.h).collidepoint(mouse_x, mouse_y):
	# for _ in range(random.randint(1, 3)):
		# rand_x, rand_y = self.x + random.randint(-30, 30), self.y + random.randint(-30, 30)
		# world.chunk_manager.get_chunk_at(rand_x, rand_y).items.append(Object(self.special_flags[0], rand_x, rand_y, "Images/Items/" + self.special_flags[0] + ".png"))
	# if self.special_flags[0] == "Wheat":
		# for _ in range(random.randint(0, 2)):
		# 	rand_x, rand_y = self.x + random.randint(-30, 30), self.y + random.randint(-30, 30)
		# 	world.chunk_manager.get_chunk_at(rand_x, rand_y).items.append(Object("Wheat seeds", rand_x, rand_y, "Images/Items/Wheat seeds.png"))
	# ''', tick_command_globals={"random": random}, tick_command_globals_in_the_end=("Object", "world", "click", "x", "y", "Width", "Height", "mouse_x", "mouse_y"), del_self_condition=lambda particle: (click[0] and pygame.Rect(particle.x - player.x + Width // 2 - particle.image.get_width() // 2, player.y - particle.y + Height // 2 - particle.image.get_height() // 2, particle.w, particle.h).collidepoint(mouse_x, mouse_y)), special_flags=particle.special_flags))
# """]),
		# 	 "Carrot,Onion,Tomato", "Seed", particle_to_build=True, needed_object="Farmland", remove_part=" seeds")
		
		# except: pass
		#world.particles.append(Particle(particle.x, particle.y, pygame.transform.scale(pygame.image.load(path + "Images/Objects/" + particle.special_flags[0] + " 2.png"), (128, 128)), end_time=random.randint(1, 3), save_particle=True, tick_command=particle.special_flags[1], end_command=particle.special_flags[3]))
		
		#world.particles.append(Particle(particle.x, particle.y, path + "Images/Objects/" + particle.special_flags[0] + " 3.png"))
		
		if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name == "Stone hoe":
			
			farmland_pos = (player.x + mouse_x - Width // 2) // 128 * 128 + 128, (player.y - mouse_y + Height // 2) // 128 * 128
			draw_select_image(128, 128, player, mouse_x, mouse_y)

			if click[0] and farmland_pos not in world.visible_farmlands and not check_collision(pygame.Rect(farmland_pos[0], farmland_pos[1], 256, 256), world, False, False):
				world.chunk_manager.get_chunk_at(*farmland_pos).farmlands[farmland_pos] = Farmland(farmland_pos[0], farmland_pos[1])
				pygame.mixer.Sound.play(pygame.mixer.Sound(path + "Sounds/Dirt.mp3"))
				# for farmland in (((farmland_pos[0] - 128, farmland_pos[1]), (farmland_pos[0] + 128, farmland_pos[1]), (farmland_pos[0], farmland_pos[1] - 128), (farmland_pos[0], farmland_pos[1] + 128))):
				# 	if farmland in world.visible_farmlands:
				# 		world.visible_farmlands[farmland].update_neigboors()

		if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name in wall_types:
			
			wall_pos = (player.x + mouse_x - Width // 2) // 256 * 256 + 128, (player.y - mouse_y + Height // 2) // 256 * 256 + 128
			draw_select_image(256, 256, player, mouse_x, mouse_y)

			if click[0] and wall_pos not in world.visible_walls and not check_collision(pygame.Rect(wall_pos[0], wall_pos[1], 256, 256), world, False, False):
				world.chunk_manager.get_chunk_at(*wall_pos).walls[wall_pos] = Wall(inventory.whole_inventory[changed_slot].name, wall_pos[0], wall_pos[1])
				for wall in (((wall_pos[0] - 256, wall_pos[1]), (wall_pos[0] + 256, wall_pos[1]), (wall_pos[0], wall_pos[1] - 256), (wall_pos[0], wall_pos[1] + 256))):
					if wall in world.visible_walls:
						world.visible_walls[wall].update_neigboors()
				inventory.whole_inventory[changed_slot].amount -= 1
				if inventory.whole_inventory[changed_slot].amount == 0:
					inventory.whole_inventory[changed_slot] = None

		if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name == "Wooden door":

			wall_pos = (player.x + mouse_x - Width // 2) // 256 * 256 + 128, (player.y - mouse_y + Height // 2) // 256 * 256 + 128
			draw_select_image(256, 256, player, mouse_x, mouse_y)

			if click[0] and wall_pos not in world.visible_walls and check_collision(pygame.Rect(wall_pos[0], wall_pos[1], 256, 256), world, False, False):
				world.chunk_manager.get_chunk_at(*wall_pos).walls[wall_pos] = Wall(inventory.whole_inventory[changed_slot].name, wall_pos[0], wall_pos[1], True)
				for wall in (((wall_pos[0] - 256, wall_pos[1]), (wall_pos[0] + 256, wall_pos[1]), (wall_pos[0], wall_pos[1] - 256), (wall_pos[0], wall_pos[1] + 256))):
					if wall in world.visible_walls:
						world.visible_walls[wall].update_neigboors()
				inventory.whole_inventory[changed_slot].amount -= 1
				if inventory.whole_inventory[changed_slot].amount == 0:
					inventory.whole_inventory[changed_slot] = None

		if inventory.whole_inventory[changed_slot] is not None and inventory.whole_inventory[changed_slot].name == "Stone hammer":

			break_pos = (player.x + mouse_x - Width // 2) // 256 * 256 + 128, (player.y - mouse_y + Height // 2) // 256 * 256 + 128
			draw_select_image(256, 256, player, mouse_x, mouse_y)

			if click[0]:
				if break_pos in world.visible_walls:
					inventory.increate(world.chunk_manager.get_chunk_at(*break_pos).walls[break_pos].wall_type)
					destroy_object(world.visible_walls[break_pos].image, world.visible_walls[break_pos].x, world.visible_walls[break_pos].y, world, Particle)
					world.chunk_manager.get_chunk_at(*break_pos).walls.pop(break_pos, None)
					for wall in ((break_pos[0] - 256, break_pos[1]), (break_pos[0] + 256, break_pos[1]), (break_pos[0], break_pos[1] - 256), (break_pos[0], break_pos[1] + 256)):
						if wall in world.chunk_manager.get_chunk_at(*wall).walls:
							world.chunk_manager.get_chunk_at(*wall).walls[wall].update_neigboors()

				for object in world.visible_objects:
					if object.breakable_by_hammer and (object.x, object.y) == break_pos:
						inventory.increate(object.name)
						destroy_object(object.image, object.x, object.y, world, Particle)
						world.chunk_manager.get_chunk_at(object.x, object.y).objects.remove(object)
						break

		if mouse_object is not None and Settings["Display"][8]:
			if screenmode == "FULLSCREEN":
				win.blit(textInfo.render(mouse_object, True, text_color), (Width - textInfo.size(mouse_object)[0] - 10, 10))
			else:
				win.blit(textInfo.render(mouse_object, True, text_color), (990 - textInfo.size(mouse_object)[0], 10))
		
		if chat_input:
			win_fill()
			win_fill(rect=(10, Height - 50, Width - 20, 40))

		text(input_text, 20, Height - 40)
		
		if len(chat) != 0:

			if chat_tick == 0:
				main_chat.append(chat[0])
				chat.remove(chat[0])
				try:
					chat_tick = len(chat[0]) // 1.5 * FPS
				except: pass
			
			reversed_chat = chat.copy()
			reversed_chat.reverse()
			message_y = 80
			for message in reversed_chat:
				message_y += get_text_height(message)
				text(message, 10, Height - message_y)
		
		chat_tick = max(0, chat_tick - 1)
		
		if multyplayer_menu_open:
			
			enable_multiplayer = Button(Width // 2, Height // 2 - 30, bigTextInfo.render(t("Enable multiplayer"), True, (139, 155, 180)), bigTextInfo.render(t("Enable multiplayer"), True, (58, 68, 102)), alignment=True, info=t("Your IP-address - ") + socket.gethostbyname(socket.gethostname()))
			enter_another_game = Button(Width // 2, Height // 2 + 30, bigTextInfo.render(t("Enter another game"), True, (139, 155, 180)), bigTextInfo.render(t("Enter another game"), True, (58, 68, 102)), alignment=True)
			
			pygame.image.save(win, path + "Cache/Win.png")
			win_darken(win)
			a, b = True, None
			animation_showed = False
			release = False

			while multyplayer_menu_open:

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
						multyplayer_menu_open = False						

				win.fill((192, 203, 220))

				if mouse_x <= 128 and mouse_y <= 128:
					win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back 2.png"), (128, 128)), (0, 0))
					if release:
						multyplayer_menu_open = False
						
				else:
					win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back.png"), (128, 128)), (0, 0))

				pygame.draw.rect(win, (58, 68, 102), (0, 0, Width, Height), 10)
				pygame.draw.rect(win, (139, 155, 180), (10, 10, Width - 20, Height - 20), 10)
				
				enable_multiplayer.main()
				enter_another_game.main()

				if enable_multiplayer.get_pressed():
					b = 1
					multyplayer_menu_open = False

				elif enter_another_game.get_pressed():
					b = 2
					multyplayer_menu_open = False
				if not animation_showed:
					win_lighten(win)
					animation_showed = True
				pygame.display.update()
				clock.tick(MAX_FPS)

			win_darken(win)
			win_lighten(win, pygame.image.load(path + "Cache/Win.png"))

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

					multyplayer_mode = "My game"
					multyplayer = True

					import Multyplayer

					main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
					main_socket.bind(("0.0.0.0", 10000))
					main_socket.setblocking(0)
					main_socket.listen(5)
				
					chat_message("[ Server started ]")

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

						win.fill((192, 203, 220))
						pygame.draw.rect(win, (58, 68, 102), (0, 0, Width, Height), 10)
						pygame.draw.rect(win, (139, 155, 180), (10, 10, Width - 20, Height - 20), 10)

						win.blit(textInfo.render("Enter server host", True, (139, 155, 180)), ((Width - textInfo.size("Enter server host")[0]) // 2, Height // 2 - 30))
						win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2))

						pygame.display.update()
						clock.tick(MAX_FPS)

					save(False)

					multyplayer_mode = "Your game"
					multyplayer = True
					try:
						
						sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
						sock.connect((input_text, 10000))
						world_name = "ᴥᴥᴥ░▒▓█╬█▓▒░ᴥᴥᴥ_Multiplayer_ᴥᴥᴥ░▒▓█╬█▓▒░ᴥᴥᴥ"
						world.mobs = []
						world.mechanisms = []
						world.projectiles = []
						player.effects = []
						#player.x, player.y, player.speed
						
					except:
						
						a = Button(Width // 2, Height // 2 + 20, bigTextInfo.render(i("Next"), True, (139, 155, 180)), bigTextInfo.render(t("Next"), True, (58, 68, 102)), alignment=True)

						while True:
						
							for event in pygame.event.get():
								if event.type == pygame.QUIT:
									save()
									sys.exit()
						   
									
							win.fill((192, 203, 220))
							pygame.draw.rect(win, (58, 68, 102), (0, 0, Width, Height), 10)
							pygame.draw.rect(win, (139, 155, 180), (10, 10, Width - 20, Height - 20), 10)
							
							win.blit(textInfo.render(t("Connection error"), True, (139, 155, 180)), ((Width - textInfo.size(t("Connection error"))[0]) // 2, Height // 2 - 20))

							a.main()
							if a.get_pressed():
								break
							
							pygame.display.update()
							clock.tick(MAX_FPS)
				
		if multyplayer:
			
			if multyplayer_mode == "My game":

				try:
					new_socket, addr = main_socket.accept()
					chat_message("Новое подключение от: " + str(addr))
					new_socket.setblocking(0)
					Multyplayer.players.append(Multyplayer.Player(new_socket, addr, 0, 0, "new player"))

				except:
					pass   # Нет желающих войти в игру
				
				# Считываем команды игроков
				
				new_objects = ""

				for object in world.visible_objects:
					if object.object_class == "Object":
						new_objects += "Object" + "!" + object.name + "!" + str(object.x) + "!" + str(object.y) + "!" + object.image_path + "!" + str(object.w) + "!" + str(object.h) + "!" + str(object.special_flags) + "!" + str(object.start_time) + "#"

				new_mobs = ""

				for mob in world.mobs:
					if mob.name == "Slime":
						new_mobs += "Slime" + "!" + str(mob.x) + "!" + str(mob.y) + "!" + str(mob.rand_mob) + "!" + str(mob.HP) + "!" + str(mob.animation_count) + "!" + str(mob.attak) + "!" + str(mob.reset_offset) + "!" + str(mob.offset_x) + "!" + str(mob.offset_y) + "!" + str(mob.speed) + "#"

				message = str(ron.x) + ", " + str(ron.y) + ", " + str(ron.home) + ", " + str(start_time) + ", " + new_rects + ", " + new_objects + "|" + str(player.x) + ", " + str(player.y) + ", " + player.direction + ", " + str(player.costum) + "|"
				
				for player in Multyplayer.players:

					try:
						data = player.connection_socket.recv(1024)
						data = data.decode()
						data = data.split(", ")
						player.x, player.y = int(data[0]), int(data[1])
						player.run = data[2]
						player.costum = data[3]
						if player.costum == "0":
							player.costum = "1"
						win.blit(eval("Hiro_" + player.run.lower() + "_run_" + str(player.costum)), (player.x - player.x + Width // 2 - 128, player.y - player.y + Height // 2 - 128))
						message += str(player.x) + ", " + str(player.y) + ", " + player.run + ", " + str(player.ostum) + "|"
						player.errors = 0

					except:

						try:
							win.blit(eval("Hiro_" + player.run.lower() + "_run_" + str(player.costum)), (player.x - player.x + Width // 2 - 128, player.y - player.y + Height // 2 - 128))
						except:
							win.blit(eval("Hiro_" + player.run.lower() + "_run_1"), (player.x - player.x + Width // 2 - 128, player.y - player.y + Height // 2 - 128))

						player.errors += 1

				# Новое состояние игры

				for player in Multyplayer.players:

					try:
						player.connection_socket.send(message.encode())
						player.errors = 0
					except:
						player.errors += 1

				for player in Multyplayer.players:

					if player.errors >= 500:

						player.connection_socket.close()
						chat_message(player.nickname + " отключился от сервера.")
						Multyplayer.players.remove(player)
					
			else:

				message = str(player.x) + ", " + str(player.y) + ", " + player.direction + ", " + str(player.costum)

				try:
					sock.send(message.encode())
				except:
					sock.close()
					chat_message(t("Connection error"))
					multyplayer = False

				# Получение нового состояния игры

				try:

					data = sock.recv(2 ** 20)
					data = data.decode()
					data = data.split("|")
					
					ron.x, ron.y, ron.home, start_time = int(data[0].split(", ")[0]), int(data[0].split(", ")[1]), eval(data[0].split(", ")[2]), float(data[0].split(", ")[3])
					
					
					world.visible_objects = []
					
					for i in data[0].split(", ")[5].split("#")[:-1]:
						
						if i.split("!")[0] == "Object":

							if i.split("!")[7][0] == "[":
								a = eval(i.split("!")[7])
							else:
								a = i.split("!")[7]
							world.visible_objects.append(Object(i.split("!")[1], int(i.split("!")[2]), int(i.split("!")[3]), i.split("!")[4], [int(i.split("!")[5]), int(i.split("!")[6])], special_flags=a, start_time=i.split("!")[8]))

					for i in data[1:]:
						
						data2 = i.split(", ")
						
						if data2 != [""]:
							if data2[3] == "0":
								data2[3] = "1" 
								
							win.blit(player.animations[data2[2]][int(data2[3])], (int(data2[0]) - player.x + Width // 2 - 128, player.y - int(data2[1]) + Height // 2 - 128))

				except:
					pass

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
				win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Heart.png"), (64, 64)), (mouse_x + 20, mouse_y + text_height - 84))
				win.blit(textInfo.render(str(inventory.whole_inventory[inventory.start_cell].special_info), True, text_color), (mouse_x + 52 - textInfo.size(str(inventory.whole_inventory[inventory.start_cell].special_info))[0] // 2, mouse_y + text_height - 59))
			
			win.blit(inventory.whole_inventory[inventory.start_cell].image, (mouse_x - 32, mouse_y - 32))
		
		if keys[hot_keys["Screenshot"]] and not keys[hot_keys["Show keys"]]:
			
			pygame.image.save(win, str(Path.home()) + "/Your Screenshot " + str(time.asctime().replace(":", " ")) + ".png")
	
			for _ in range(3):
				win.fill((200, 255, 200))
				clock.tick(MAX_FPS)
				pygame.display.update()
			time.sleep(0.1)
			
		if keys[hot_keys["Plugin manager"]] and not chat_input:
			
			win = pygame.display.set_mode((0, 0), pygame.RESIZABLE)

			win.fill((192, 203, 220))
			pygame.draw.rect(win, (58, 68, 102), (0, 0, Width, Height), 10)
			pygame.draw.rect(win, (139, 155, 180), (10, 10, Width - 20, Height - 20), 10)

			win.blit(textInfo.render(t("The gameplay will continue, when you close the plugin creator"), True, (139, 155, 180)), ((Width - textInfo.size(t("The gameplay will continue, when you close the plugin creator"))[0]) // 2, Height // 2 - 32))
			pygame.display.update()
			os.system("python " + path + "Plugin_creater.py")

		animate_click(Settings, win, mouse_x, mouse_y)

		win_fill((200, 0, 0), 100 - Settings["Display"][0])

		pygame.display.update()



# Меню редактирования мира

def edit_world():
	
	global world_name, game, player, alt_pressed, does_lighten

	create_world = False
	release = False
	does_lighten = False

	try:
		game.difficulty, player.god_mode = Saver.load_objects(path + "Worlds/" + world_name + "/Settings.save")
	except:
		game.difficulty = "norm"
		player.god_mode = False
		create_world = True

	input_text = ""
	world_name_input = False
	seed_input = False

	easy_but = Button(50, 200, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Easy.png"), (132, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Easy 2.png"), (132, 64)))
	norm_but = Button(50, 270, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Norm.png"), (132, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Norm 2.png"), (132, 64)))
	hard_but = Button(50, 340, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Hard.png"), (132, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Hard 2.png"), (132, 64)))
	skull_but = Button(50, 410, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Skull.png"), (132, 64)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Skull 2.png"), (132, 64)))
	
	win.fill((192, 203, 220))

	if create_world:
		world.chunk_manager.generator.seed = random.randint(0, 2**31 - 1)

	while True:
		
		mouse_x, mouse_y = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		keys = pygame.key.get_pressed()
		release = False

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				win_darken(win)
				sys.exit()
				
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					release = True

			elif event.type == pygame.KEYDOWN and (world_name_input or seed_input):
				if event.key == pygame.K_RETURN or len(input_text) == 50:
					if world_name_input:
						world_name_input = False
						if input_text != "":
							os.rename(path + "Worlds/" + world_name, path + "Worlds/" + input_text)
							world_name = input_text
					if seed_input:
						if input_text != "":
							world.chunk_manager.generator.seed = int(input_text)
						seed_input = False
					input_text = ""
				elif event.key == pygame.K_BACKSPACE:
					input_text = input_text[:-1]
				elif not seed_input or event.unicode in "0123456789":
					input_text += event.unicode
			
			if event.type == pygame.KEYUP:
				
				if event.key == hot_keys["Close"] and not create_world: Saver.save_objects(path + "Worlds/" + world_name + "/Settings.save", [game.difficulty, player.god_mode]); worlds()
				
				if event.key == hot_keys["Show keys"]:
					alt_pressed = not alt_pressed
		
		if bigTextInfo.size(t("World name"))[0] + 100 <= mouse_x <= bigTextInfo.size(t("World name"))[0] + 900 and 50 <= mouse_y <= 121 and release:
			world_name_input = True
		
		win.fill((192, 203, 220))

		win.blit(bigTextInfo.render("x", True, (139, 155, 180)), (Width - 50, 15))
		
		if Width - 50 < mouse_x < Width - 20 and 15 < mouse_y < 45:
			
			win.blit(bigTextInfo.render("x", True, (58, 68, 102)), (Width - 50, 15))
			
			if pygame.mouse.get_pressed()[0]:
				
				if not create_world: Saver.save_objects(path + "Worlds/" + world_name + "/Settings.save", [game.difficulty, player.god_mode])
				worlds()

		win.blit(bigTextInfo.render(t("World name"), True, (139, 155, 180)), (50, 60))
		pygame.draw.rect(win, (139, 155, 180), (bigTextInfo.size(t("World name"))[0] + 100, 50, 800, 71), 5)
		if world_name_input:
			win.blit(bigTextInfo.render(input_text, True, (139, 155, 180)), (bigTextInfo.size(t("World name"))[0] + 120, 60))
		else:
			win.blit(bigTextInfo.render(world_name, True, (139, 155, 180)), (bigTextInfo.size(t("World name"))[0] + 120, 60))
			
		win.blit(bigTextInfo.render(t("Game difficulty:"), True, (139, 155, 180)), (50, 150))

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

		win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Modes/" + game.difficulty + ".png"), (548, 274)), (232, 200))
		
		match game.difficulty:
			
			case "easy":
				win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Easy 2.png"), (132, 64)), (50, 200))
				
			case "norm":
				win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Norm 2.png"), (132, 64)), (50, 270))
				
			case "hard":
				win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Hard 2.png"), (132, 64)), (50, 340))
				
			case "skull":
				win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Skull 2.png"), (132, 64)), (50, 410))

		win.blit(bigTextInfo.render(t("God mode"), True, (139, 155, 180)), (50, 520))
		
		pygame.draw.rect(win, (139, 155, 180), (bigTextInfo.size(t("God mode"))[0] + 60, 510, 71, 71), 5)
		if player.god_mode:
			win.blit(bigTextInfo.render(" ✓", True, (139, 155, 180)), (bigTextInfo.size(t("God mode"))[0] + 60, 520))
			if bigTextInfo.size(t("God mode"))[0] + 60 <= mouse_x <= bigTextInfo.size(t("God mode"))[0] + 131 and 510 <= mouse_y <= 568 and release:
				player.god_mode = False
		else:
			win.blit(bigTextInfo.render(" x", True, (139, 155, 180)), (bigTextInfo.size(t("God mode"))[0] + 60, 520))
			if bigTextInfo.size(t("God mode"))[0] + 60 <= mouse_x <= bigTextInfo.size(t("God mode"))[0] + 131 and 510 <= mouse_y <= 568 and release:
				player.god_mode = True

		if create_world:
			
		
			if bigTextInfo.size(t("World seed"))[0] + 100 <= mouse_x <= bigTextInfo.size(t("World seed"))[0] + 900 and 590 <= mouse_y <= 661 and release:
				seed_input = True
			win.blit(bigTextInfo.render(t("World seed"), True, (139, 155, 180)), (50, 600))
			pygame.draw.rect(win, (139, 155, 180), (bigTextInfo.size(t("World seed"))[0] + 100, 590, 800, 71), 5)
			if seed_input:
				win.blit(bigTextInfo.render(input_text, True, (139, 155, 180)), (bigTextInfo.size(t("World seed"))[0] + 120, 600))
			else:
				win.blit(bigTextInfo.render(str(world.chunk_manager.generator.seed), True, (139, 155, 180)), (bigTextInfo.size(t("World seed"))[0] + 120, 600))
			win.blit(bigTextInfo.render(t("Create world"), True, (139, 155, 180)), (Width - bigTextInfo.size(t("Create world"))[0] - 50, 150))
			
			if Width - bigTextInfo.size(t("Create world"))[0] - 50 < mouse_x < Width - 50 and 150 < mouse_y < 180:
				
				win.blit(bigTextInfo.render(t("Create world"), True, (58, 68, 102)), (Width - bigTextInfo.size(t("Create world"))[0] - 50, 150))
				if release:
					win_darken(win)
					start_game()
		else:
			
			win.blit(bigTextInfo.render(t("Delete world"), True, (139, 155, 180)), (50, 660))

			if 50 < mouse_x < 50 + bigTextInfo.size(t("Delete world"))[0] and 660 < mouse_y < 690:
		   
				win.blit(bigTextInfo.render(t("Delete world"), True, (58, 68, 102)), (50, 660))
			
				if release:
				
					win_fill()
					a = win.copy()
				
					yes_button = Button(Width // 2 - 150, Height // 2, bigTextInfo.render(t("Yes"), True, (139, 155, 180)), bigTextInfo.render(t("Yes"), True, (58, 68, 102)), alignment=True)
					no_button = Button(Width // 2 + 150, Height // 2, bigTextInfo.render(t("No"), True, (139, 155, 180)), bigTextInfo.render(t("No"), True, (58, 68, 102)), alignment=True)

					while True:
					
						for event in pygame.event.get():
							if event.type == pygame.QUIT:
								win_darken(win)
								sys.exit()
							
						mouse_x, mouse_y = pygame.mouse.get_pos()
						click = pygame.mouse.get_pressed()
						keys = pygame.key.get_pressed()
					
						win.blit(a, (0, 0))
					
						pygame.draw.rect(win, (192, 203, 220), (Width // 2 - 300, Height // 2 - 150, 600, 300))
						pygame.draw.rect(win, (139, 155, 180), (Width // 2 - 300, Height // 2 - 150, 600, 300), 5)
					
						win.blit(textInfo.render(t("Are you sure want to delete this world?"), True, (139, 155, 180)), ((Width - textInfo.size(t("Are you sure want to delete this world?"))[0]) // 2, Height // 2 - 100))

						yes_button.main()
						if yes_button.get_pressed():   # Удалить выбранный мир
							import shutil
							shutil.rmtree(path + "Worlds/" + world_name)
							del shutil
							win_darken(win)
							worlds()
						
						no_button.main()
						if no_button.get_pressed() or keys[hot_keys["Close"]]:
							break
					
						win_fill(alpha=100 - Settings["Display"][0])   # Если в настройках установлена яркость ниже 100, то экран становится темнее
					
						pygame.display.update()
						clock.tick(30)
					
			win.blit(bigTextInfo.render(t("Copy world"), True, (139, 155, 180)), (50, 600))

			if 50 < mouse_x < 50 + bigTextInfo.size(t("Copy world"))[0] and 600 < mouse_y < 630:
				win.blit(bigTextInfo.render(t("Copy world"), True, (58, 68, 102)), (50, 600))
				if release:
					import shutil
					shutil.copytree(path + "Worlds/" + world_name, path + "Worlds/" + world_name + t(" - copy"))
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
			Saver.save_objects(path + "Worlds/" + world_name + "/Settings.save", [game.difficulty, player.god_mode])

		if not does_lighten:
			win_lighten(win)
			does_lighten = True
		
		pygame.display.update()
		clock.tick(30)



# Меню миров

def worlds():

	global world_name, mouse, keys, alt_pressed

	page_back_button = Button(10, Height - 138, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back.png"), (128, 128)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back 2.png"), (128, 128)))
	page_next_button = Button(Width - 148, Height - 148, pygame.transform.flip(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back.png"), (128, 128)), True, False), pygame.transform.flip(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back 2.png"), (128, 128)), True, False))
	create_new_world_button = Button(Width // 2, 50, textInfo.render(t("Create world"), True, (139, 155, 180)), textInfo.render(t("Create world"), True, (58, 68, 102)), alignment=True)
	back_button = Button(-20, -20, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back.png"), (128, 128)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Back 2.png"), (128, 128)))
	page = 1
	input_text = None

	win_darken(win)

	inside_folders = []	
	for dirs, folder, files in os.walk(path + "Worlds/"):
		inside_folders = folder
		break

	inside_folders.sort()
	win.fill((192, 203, 220))

	create_new_world_button.main()

	if inside_folders != []:

		if page < len(inside_folders) / 5 or len(inside_folders) % 5 == 0:
			a = 0
			for i in range((page - 1) * 5, (page - 1) * 5 + 5):
		
				a += 1
		
				win.blit(textInfo.render(inside_folders[i], True, (139, 155, 180)), (50, 50 + a * 50))
		
		else:
		
			a = 0
		
			for i in range((page - 1) * 5, (page - 1) * 5 + len(inside_folders) % 5):
		
				a += 1
				win.blit(textInfo.render(inside_folders[i], True, (139, 155, 180)), (50, 50 + a * 50))

	page_back_button.main()
	page_next_button.main()
	back_button.main()
	release = False

	win_lighten(win)

	while True:

		mouse_x, mouse_y = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		keys = pygame.key.get_pressed()
		release = False

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				win_darken(win)
				sys.exit()

			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					release = True

			elif event.type == pygame.KEYDOWN and input_text is not None:
				
				if event.key == pygame.K_BACKSPACE:
					input_text = input_text[:-1]
				elif event.key == pygame.K_RETURN:
					world_name = input_text
					inventory.get_start_items()
					ron.get_start_items()
					win_darken(win)
					edit_world()
				else:
					input_text += event.unicode
			if event.type == pygame.KEYUP:
				if event.key == hot_keys["Show keys"]:
					alt_pressed = not alt_pressed


		for dirs, folder, files in os.walk(path + "Worlds/"):
			inside_folders = folder
			break

		inside_folders.sort()
		win.fill((192, 203, 220))

		if input_text is None:

			create_new_world_button.main()

			if create_new_world_button.get_pressed():
				input_text = ""

			page_back_button.main()
			if page_back_button.get_pressed() and page != 1:
				page -= 1

			page_next_button.main()
			if page_next_button.get_pressed() and page < len(inside_folders) / 5:
				page += 1

			back_button.main()
			
			if keys[hot_keys["Close"]] or back_button.get_pressed():
				win_darken(win)
				menu()

			text(str(page), Width // 2, Height - 60, blue_color, alignment=True)

			if inside_folders != []:

				if page < len(inside_folders) / 5 or len(inside_folders) % 5 == 0:
					a = 0
					for i in range((page - 1) * 5, (page - 1) * 5 + 5):

						a += 1

						win.blit(textInfo.render(inside_folders[i], True, (139, 155, 180)), (50, 50 + a * 50))

						if 50 + textInfo.size(inside_folders[i])[0] <= mouse_x <= 82 + textInfo.size(inside_folders[i])[0] and 50 + a * 50 <= mouse_y <= 82 + a * 50:
							win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Edit 2.png"), (32, 32)), (50 + textInfo.size(inside_folders[i])[0], 50 + a * 50))
							if release:
								world_name = inside_folders[i]
								
								win_darken(win)
								edit_world()

						if 50 <= mouse_x <= 50 + textInfo.size(inside_folders[i])[0] and 50 + a * 50 <= mouse_y <= 50 + a * 50 + textInfo.size(inside_folders[i])[1]:

							win.blit(textInfo.render(inside_folders[i], True, (58, 68, 102)), (50, 50 + a * 50))
							
							win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Edit.png"), (32, 32)), (50 + textInfo.size(inside_folders[i])[0], 50 + a * 50))
							
							if release:
								world_name = inside_folders[i]
								start_game()

				else:

					a = 0

					for i in range((page - 1) * 5, (page - 1) * 5 + len(inside_folders) % 5):

						a += 1

						win.blit(textInfo.render(inside_folders[i], True, (139, 155, 180)), (50, 50 + a * 50))
						
						if 50 + textInfo.size(inside_folders[i])[0] <= mouse_x <= 82 + textInfo.size(inside_folders[i])[0] and 50 + a * 50 <= mouse_y <= 82 + a * 50:
							win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Edit 2.png"), (32, 32)), (50 + textInfo.size(inside_folders[i])[0], 50 + a * 50))
							if release:
								world_name = inside_folders[i]

								win_darken(win)
								edit_world()

						if 50 <= mouse_x <= 50 + textInfo.size(inside_folders[i])[0] and 50 + a * 50 <= mouse_y <= 50 + a * 50 + textInfo.size(inside_folders[i])[1]:

							win.blit(textInfo.render(inside_folders[i], True, (58, 68, 102)), (50, 50 + a * 50))
							
							win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Edit.png"), (32, 32)), (50 + textInfo.size(inside_folders[i])[0], 50 + a * 50))
							
							if release:
								world_name = inside_folders[i]
								start_game()

		else:
			text(f"""{t("Enter world name:")}
{input_text}""", Width // 2, Height // 2 - 15, blue_color, alignment=True)
			
		if alt_pressed: draw_key("ESC", 44, 108)

		animate_click(Settings, win, mouse_x, mouse_y)

		win_fill(alpha=100 - Settings["Display"][0])   # Если в настройках установлена яркость ниже 100, то экран становится темнее
		
		pygame.display.update()
		clock.tick(30)



# Меню

def menu():
	
	global win, screenmode, num, does_lighten

	play_button = Button(Width / 2, Height / 2 - 150, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Play.png"), (264, 128)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Play 2.png"), (264, 128)), alignment=True, info="Подсказка: вы можете нажать enter, чтобы сразу начать игру.", action=worlds)
	settings_button = Button(Width / 2, Height / 2, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Settings.png"), (488, 128)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Settings 2.png"), (488, 128)), alignment=True, action=settings)
	change_a_character_button = Button(Width / 2, Height / 2 + 150, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Change a character.png"), (960, 128)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Change a character 2.png"), (960, 128)), alignment=True, action=change_a_character)

	version = f"Version {open(path + 'Version.txt').read()} (Build {str(get_build_number())})"
	more_menu_open = False
	mouse_press = False
	does_lighten = False

	while True:
		
		mouse_x, mouse_y = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				save()
				sys.exit()
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

		win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Discord logo.png"), (108, 81)), (Width - 90, Height - 80))
		if mouse_x > Width - 70 and mouse_y > Height - 80:
			win_fill()
			if click[0]:
				import webbrowser
				webbrowser.open("https://discord.com/invite/aQNgcCQkHc")
				del webbrowser
				break
			
		if Width - 140 < mouse_x < Width - 76 and Height - 70 < mouse_y < Height - 6:
			win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/More 2.png"), (64, 64)), (Width - 140, Height - 70))

			if mouse_press and not click:
				if more_menu_open: more_menu_open = False
				else: more_menu_open = True
				
			if click[0]: mouse_press = True
			else: mouse_press = False
		else:
			win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Buttons/More.png"), (64, 64)), (Width - 140, Height - 70))

		if more_menu_open:
			
			pygame.draw.rect(win, (192, 203, 220), (100, 100, Width - 200, Height - 200))
			pygame.draw.rect(win, (58, 68, 102), (100, 100, Width - 200, Height - 200), 10)
			pygame.draw.rect(win, (139, 155, 180), (110, 110, Width - 220, Height - 220), 10)
			
			win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Telegram logo.png"), (100, 100)), (200, Height // 2 + 50))
			text("Telegram\n@Gannitto", 250, Height // 2 + 180, blue_color, alignment=True)
			
			win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Discord logo.png"), (200, 150)), (Width // 2 - 100, Height // 2 + 30))
			text("Discord\nGannitto#0694", Width // 2, Height // 2 + 180, blue_color, alignment=True)
			
			win.blit(pygame.transform.scale(pygame.image.load(path + "Images/Gmail logo.png"), (100, 100)), (Width - 300, Height // 2 + 50))
			text("Gmail", Width - 250, Height // 2 + 180, blue_color, alignment=True)
			text("danilaserezhin@gmail.com", Width - 250, Height // 2 + 200, blue_color, 16, True)
			
			win.blit(pygame.image.load(path + "Images/Rickrolling QR-code.png"), (Width // 2 - 100, Height // 2 - 200))
			text(t("You can get other information from this QR code"), Width // 2, Height // 2 + 10, blue_color, alignment=True)

		animate_click(Settings, win, mouse_x, mouse_y)

		win_fill(alpha=100 - Settings["Display"][0])   # Если в настройках установлена яркость ниже 100, то экран становится темнее

		if not does_lighten:
			win_lighten(win)
			does_lighten = True


		pygame.display.update()
		clock.tick(MAX_FPS)



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

	try:
		menu()
	except Exception as e:
		music_channel.stop()
		pygame.mixer.Sound.stop(Backrooms_lamps)
		show_error_window(e)

if __name__ == "__main__":
	show_intro()

