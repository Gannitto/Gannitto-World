import pygame
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
import Saver
from Functions import *
from Build import check_build_objects, draw_select_image, draw_select_image_arbitrarily
from Chunks import ChunkManager
from Inventory import inventory
from Translator import translator, t
from Cache import load
from TimeSystem import TimeSystem
from Commands import CommandSystem
from Sound import play_sound, set_sound_volume, music_channel, update_sounds
from InputSystem import input_system
from Weather import WeatherSystem
from ItemActions import ItemActions
from Assets import *
from Globals import *
from UI import SettingsMenu, CharactersMenu, WorldsMenu, EditWorldMenu, MultiplayerSettingsMenu, MainMenu, TabMenu
from Classes import Player, World, Object, Particle, Slime, Spider, Butterfly, Projectile, ExplodingProjectile, Wall, Farmland, Wire, Lever, Motherboard, RandomBox, Ron, Button, Portal
from GameState import GameState
from Light import create_light_circle, create_light_circle_with_falloff, remove_light_circle

pygame.init()

"""
Чтобы найти что-то на карте кода, просто вбейте в поиск

Карта кода:

Инициализация игры
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

def save(darken:bool=True, save_world_settings:bool=False):

	"""
	Сохраняет игру
	darken - Затемнять ли экран
	save_world_settings - Сохранять ли настройки мира
	"""

	Saver.save_objects(path + "Saves/Settings/Statistics.save", statistics)
	
	if game.world_name is not None:
		
		if game.multiplayer:
			pass
			# TODO сохранение данных о других игроках
		else:
			
			Saver.save_objects(path + "Saves/Worlds/" + game.world_name + "/Mobs.save", world.mobs)
			Saver.save_objects(path + "Saves/Worlds/" + game.world_name + "/Info.save", [player.x, player.y, Backrooms.InBackrooms, Backrooms.Level, world.current_cave, player.speed, player.HP, game.start_time, ron.x, ron.y, ron.home, ron.inventory, world.chunk_manager.generator.seed, time_system.current_time])
			Saver.save_objects(path + "Saves/Worlds/" + game.world_name + "/Inventory.save", inventory.whole_inventory)
			Saver.save_objects(path + "Saves/Worlds/" + game.world_name + "/Resources.save", inventory.resources)
			Saver.save_objects(path + "Saves/Worlds/" + game.world_name + "/Effects.save", player.effects)

			new_particles = []
			particle_count = 1
			for particle in new_particles:
				if particle.save_particle:
					pygame.image.save(particle.image, path + "Saves/Worlds/" + game.world_name +"/Images/Particle " + str(particle_count) + ".png")
					particle.image_path = path + "Saves/Worlds/Images/Particle " + str(particle_count) + ".png"
					particle_count += 1
					new_particles.append(particle)
			Saver.save_objects(path + "Saves/Worlds/" + game.world_name + "/Particles.save", new_particles)
			world.chunk_manager.save_all_loaded_chunks()
				
	if darken and Settings["Display"][9]:
		win_darken(win)
		
	if save_world_settings: Saver.save_objects(path + "Saves/Worlds/" + game.world_name + "/Settings.save", [game.difficulty, player.god_mode])

# Применение настроек TODO

statistics[0] += 1

pygame.display.set_icon(pygame.image.load(path + "Images/Icon.png"))
pygame.display.set_caption("Gannitto World")



# Инициализация игры

game = GameState()

mouse_x = game.mouse_x
mouse_y = game.mouse_y
alt_pressed = game.alt_pressed

game.player = Player()
player = game.player
game.inventory = inventory
game.world_to_screen = lambda X, Y, W, H, player=player: (X - player.x + Width // 2 - W // 2, player.y - Y + Height // 2 - H // 2)
world_to_screen = game.world_to_screen
game.world_rect_to_screen = lambda X, Y, W, H: (X - player.x + Width // 2 - W // 2, player.y - Y + Height // 2 - H // 2, W, H)
world_rect_to_screen = game.world_rect_to_screen
game.world = World(game)
world = game.world
game.time_system = TimeSystem()
time_system = game.time_system
ron = Ron(game)
game.command_system = CommandSystem(game)
command_system = game.command_system
game.item_actions = ItemActions(game)
item_actions = game.item_actions
game.tab_menu = TabMenu(game, save)

weather = WeatherSystem(world)

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


hot_keys = Saver.load_objects(path + "Saves/Settings/Hot keys.save")
objects_templates = {
		"Table": Object("Table", 0, 0, "Images/Objects/Table.png", (256, 256), is_solid=True, breakable_by_hammer=True),
		"Wall table": Object("Wall table", 0, 0, "Images/Objects/Wall table.png", (256, 256), special_flags=1, is_solid=True, breakable_by_hammer=True),
		"Furnace": Object("Furnace", 0, 0, "Images/Items/Furnace.png", (256, 256), special_flags=1, is_solid=True, breakable_by_hammer=True),
		"Punch": Object("Punch", 0, 0, "Images/Objects/Punch 1.png", (256, 256), is_solid=True, breakable_by_hammer=True)
		}

# Основной цикл игры

def start_game():
	
	global backrooms, text_color, mouse_x, mouse_y, color, new_particles, game, alt_pressed, player, world, FPS, win

	bigTextInfo = pygame.font.Font(path + "Font.ttf", 36)
	aaa = 0
	AA = 0
	use_item_pressed = False
	game.start_time = time.time()

	tile_size = 256
	Width, Height = pygame.display.get_surface().get_size()
	tiles_x = (Width // tile_size) + 3
	tiles_y = (Height // tile_size) + 3
	dx = 0
	dy = 0
	release = False
	game.craft_list_max_offset = (len(inventory.recipes) + 1) * -80 + Height

	new_particles = []

	if Settings["Game"][1]:
		up_b = Button(Width - 148, Height - 148, arrow_up, arrow_up, sound=False, cooldown=0)
		left_b = Button(Width - 222, Height - 74, arrow_left, arrow_left, sound=False, cooldown=0)
		down_b = Button(Width - 148, Height - 74, arrow_down, arrow_down, sound=False, cooldown=0)
		right_b = Button(Width - 74, Height - 74, arrow_right, arrow_right, sound=False, cooldown=0)

	
	craft_list_back_button = Button(114, Height - 176, bigTextInfo.render("<", True, (0, 150, 0)), bigTextInfo.render("<", True, (0, 100, 0)))
	craft_list_next_button = Button(Width - 144, Height - 176, bigTextInfo.render(">", True, (0, 150, 0)), bigTextInfo.render(">", True, (0, 100, 0)))

	# Загрузка данных мира
	if not game.multiplayer or game.multiplayer_role == "Host":
		world.chunk_manager.save_directory = path + "Saves/Worlds/" + game.world_name + "/Chunks/"

		if os.path.exists(path + "Saves/Worlds/" + game.world_name):
			
			world.mobs = Saver.load_objects(path + "Saves/Worlds/" + game.world_name + "/Mobs.save")
			player.x, player.y, Backrooms.InBackrooms, Backrooms.Level, world.current_cave, player.speed, player.HP, game.start_time, ron.x, ron.y, ron.home, ron.inventory, world.chunk_manager.generator.seed, time_system.current_time = Saver.load_objects(path + "Saves/Worlds/" + game.world_name + "/Info.save")
			world.chunk_manager.update_seed()
			game.difficulty, player.god_mode = Saver.load_objects(path + "Saves/Worlds/" + game.world_name + "/Settings.save")
			inventory.whole_inventory = Saver.load_objects(path + "Saves/Worlds/" + game.world_name + "/Inventory.save")
			player.effects = Saver.load_objects(path + "Saves/Worlds/" + game.world_name + "/Effects.save")

			if game.multiplayer:
				game.net.peers[game.net.player_id].x = player.x
				game.net.peers[game.net.player_id].y = player.y
				game.net.peers[game.net.player_id].direction = player.direction
			
		else:

			os.mkdir(path + "Saves/Worlds/" + game.world_name)
			os.mkdir(path + "Saves/Worlds/" + game.world_name + "/Images")

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
						if b and game.world_name == i[6]:
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
		player.hovered_object = None
		player.breaking_object = None

		FPS = int(clock.get_fps())
		dt = clock.tick(MAX_FPS) / 1000.0
		time_system.update(dt)
		player.changed_item = inventory.whole_inventory[inventory.changed_slot]
		if game.multiplayer:
			game.events.clear()
		events = pygame.event.get()
		for event in events:
			
			if event.type == pygame.QUIT:
				statistics[1] += (time.time() - game.start_time) / 3600
				if game.multiplayer:
					game.net.disconnect()
				save()
				sys.exit()

			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					release = True
			
			elif event.type == pygame.MOUSEWHEEL and not any((game.item_settings_open, ron.window[0], game.in_motherboard)):
				if game.craft_list_open:
					game.craft_list_offset = max((min(game.craft_list_offset + event.y * Settings["Game"][2], 0)), game.craft_list_max_offset)
				else:
					inventory.changed_slot -= event.y
					if inventory.changed_slot > 9: inventory.changed_slot = 0
					if inventory.changed_slot < 0: inventory.changed_slot = 9

			if event.type == pygame.KEYUP:
				if game.chat_open:
					if event.key == hot_keys["Close"]:
						game.chat_open = False
						input_system.stop_input()
				else:
					if event.key == hot_keys["Show keys"]:
						alt_pressed = not alt_pressed
					if event.key == hot_keys["Use item"]:
						use_item_pressed = True
					if event.key == hot_keys["Multiplayer menu"]:
						game.multiplayer_menu_open = True
					if event.key == hot_keys["Set Ron home"]:
						ron.home = [player.x, player.y]
					if event.key == hot_keys["Menu"]:
						game.menu_open = not game.menu_open
					if event.key == hot_keys["Open chat"]:
						game.chat_open = True
						input_system.start_input("Chat", 20, Height - 40, (255, 255, 255))
					if event.key == hot_keys["Execute command"]:
						game.chat_open = True
						input_system.start_input("Chat", 20, Height - 40, (255, 255, 255), input_text="/")

					if event.key == hot_keys["Close"]:
	
						if game.item_settings_open:
							game.item_settings_open = False
						elif ron.window[0]:
							ron.window[0] = False
						elif game.in_motherboard is not None:
							game.in_motherboard = None
						elif game.craft_list_open:
							game.craft_list_open = False
						elif game.inventory_open:
							game.inventory_open = False
						else:
							music_channel.stop()
							statistics[1] += (time.time() - game.start_time) / 3600
							save()
							world.chunk_manager.chunks = {}
							world.mobs = []
							player.effects = []
							particles = []
							game.chat = []
							game.main_chat = []
							game.chat_tick = 0
							inventory.whole_inventory = [None] * 30
							game.world_name = None
							if game.multiplayer:
								game.net.disconnect()
							win_darken(win)
							game.does_lighten = False
							return game.main_menu.main_menu

					if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0, ):
						last_changed_slot = inventory.changed_slot
						inventory.changed_slot = int(event.unicode) - 1 + 10 * (event.key == pygame.K_0)
						player.changed_item = inventory.whole_inventory[inventory.changed_slot]
						if player.changed_item is not None:
							player.changed_item = player.changed_item.name

					# if event.key == pygame.K_o and Settings["User"][1]:
						# world.mobs.append(Spider(player.x, player.y))

					if event.key == hot_keys["Help"]:
						music_channel.stop()
						statistics[1] += (time.time() - game.start_time) / 3600
						save(False)
						return game.settings_menu.help

					if event.key == hot_keys["Inventory"]:
						game.inventory_open = not game.inventory_open
						if not game.inventory_open:
							if inventory.craft_items_list != [None] * 7:
								for item_index, item in enumerate(inventory.craft_items_list):
									if item is not None:
										inventory.increate(item, inventory.craft_amounts_list[item_index])
							inventory.craft_items_list = [None] * 7
							inventory.craft_amounts_list = [None] * 7
							inventory.craft_images_list = [None] * 7

					if event.key == hot_keys["Throw away the item"] and inventory.whole_inventory[inventory.changed_slot] is not None:
						
						if Backrooms.InBackrooms:
							world.backrooms_objects.append(Object(inventory.whole_inventory[inventory.changed_slot].name, player.x, player.y, "Images/Items/" + inventory.whole_inventory[inventory.changed_slot].name + ".png", special_flags="Item"))
						else:
							world.particles.append(create_throw_particle(Object, Particle, player, world, game, inventory.whole_inventory[inventory.changed_slot].image, inventory.whole_inventory[inventory.changed_slot].name))
						
						inventory.reduce(inventory.changed_slot)

		if game.inventory_open:
			if click[0] and not game.hold_left:
				inventory.set_start_cell(mouse_x, mouse_y)
				game.hold_left = True
			if game.hold_left and not click[0]:
				inventory.craft_items_list, inventory.craft_amounts_list, inventory.craft_images_list = inventory.set_end_cell(mouse_x, mouse_y)
				game.hold_left = False

		keys = pygame.key.get_pressed()

		if not game.chat_open:

			if keys[hot_keys["Move left"]]: dx = -1
			if keys[hot_keys["Move right"]]: dx = 1
			if keys[hot_keys["Move down"]]: dy = -1
			if keys[hot_keys["Move up"]]: dy = 1

			if abs(dx) == abs(dy) == 1:
				dx *= 0.7
				dy *= 0.7

		# Если есть движение - двигаем игрока
		if dx != 0 or dy != 0:
			player.move(dx, dy, dt, world)
			game.events.append({"event_type": "player_moved", "x": player.x, "y": player.y, "direction": player.direction})
			if game.multiplayer:
				game.net.peers[game.net.player_id].x = player.x
				game.net.peers[game.net.player_id].y = player.y
				game.net.peers[game.net.player_id].direction = player.direction
		else:
			if player.is_moving:
				game.events.append({"event_type": "player_stopped", "x": player.x, "y": player.y})
			player.stop()
		
		# Обновляем анимацию
		player.update_animation(dt)

		win.fill((0, 0, 0))

		if Width // 2 - 100 <= mouse_x <= Width // 2 + 100 and Height // 2 - 100 <= mouse_y <= Height // 2 + 100 and not any((game.item_settings_open, ron.window[0], game.in_motherboard, game.craft_list_open)):
			mouse_object = t("It's you")

		if Backrooms.InBackrooms:
			
			for i, ii in product(range(-6, 6), range(-3, 3)):
				win.blit(biome_textures["Backrooms " + str(Backrooms.Level)], (Width - player.x % 256 + i * 256, player.y % 256 + ii * 256))

		else:

			current_chunk = world.chunk_manager.get_chunk_at(player.x, player.y)
			if current_chunk is not None:
				game.current_biome = current_chunk.biome
			else:
				game.current_biome = None
			world.render_loaded_chunks()
			update_sounds(game, player, world)
		
		for mechanism in world.mechanisms:
			mechanism.main(world, player)
		
		for farmland in world.visible_farmlands.values():
			farmland.main(release, dt, game, mouse_x, mouse_y)

		if not Backrooms.InBackrooms and world.current_cave is None:
			
			pass
			# TODO тут сделать переход в закулисье

			# Backrooms.InBackrooms = True
			# color = colors["Backrooms"]
			# text_color = colors["Backrooms2"]
			# i = -1

			# for object in Backrooms.objects:
			# 	i += 1
			# 	world.backrooms_objects.append(Object(object, Backrooms.objects_x[i], Backrooms.objects_y[i], "Images/Items/" + inventory.resources[object].name + ".png", special_flags="Item"))

			# x = 0
			# y = 0

			# play_sound("1", loops=-1)
			# pygame.mixer.music.set_volume(0.5)

			# aaa = 100
			# AA = 0

		elif Backrooms.InBackrooms:
			
			Backrooms.handle_backrooms_logic(game, keys)

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

					object.main(game, dt)

					if object.__class__ == Object:

						if object.x - player.x + Width // 2 - object.w // 2 <= mouse_x <= object.x - player.x + Width // 2 + object.w // 2 and player.y - object.y + Height // 2 - object.h // 2 <= mouse_y <= player.y - object.y + Height // 2 + object.h // 2:

							if object.name == "Iron ore" and click[0] and inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].name in ("Stone pickaxe"):

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

							if object.name == "Gold ore" and click[0] and inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].name in ("Stone pickaxe"):

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
							if object.get_right_pressed(mouse_x, mouse_y, player) and inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].type == "Flower":
								world.chunk_manager.get_chunk_at(object.x, object.y).items.append(Object(inventory.whole_inventory[inventory.changed_slot].name, object.x, object.y + 36, 64, 64, inventory.whole_inventory[inventory.changed_slot].image))
								inventory.reduce(inventory.changed_slot)
				
			else:

				# Обновление мира
				world.update() #TODO оптимизировать

				# Отображение объектов

				for object in world.visible_objects:

					object.main(game, dt)

					if object.get_left_pressed(mouse_x, mouse_y, player):

						if object.name == "Pond":
							if object.special_flags[0] != 0 and inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].name == "Bucket":

								inventory.reduce(inventory.changed_slot)

								inventory.increate("Water bucket")
								object.special_flags[0] -= 1
			
							if object.special_flags[1] != 0 and inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].name == "Stone shovel" and object.get_left_pressed(mouse_x, mouse_y, player) and random.randint(1, 30) == 1:
								rand_x, rand_y = object.x +random.randint(-128, 128), object.y + random.randint(-128, 128)
								world.chunk_manager.get_chunk_at(rand_x, rand_y).items.append(Object("Clay", rand_x, rand_y, "Images/Items/Clay.png", pickable=True))
								object.special_flags[1] -= 1

						mouse_object = object.name

						if object.name == "Pot":

							if inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].type == "Flower":
								world.chunk_manager.get_chunk_at(object.x, object.y + 36).items.append(Object(inventory.whole_inventory[inventory.changed_slot].name, object.x, object.y + 36, 64, 64, inventory.whole_inventory[inventory.changed_slot].image))
								inventory.reduce(inventory.changed_slot)

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

						if object.get_left_pressed(mouse_x, mouse_y, player) and inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].name in ("Mushroom", "Red mushroom", "Thread", "Poppy", "Purple tulip", "Orange tulip", "Black tulip", "Red tulip", "Yellow tulip", "Dandelion", "Cotton grass", "Onion"):
							if object.special_flags < 11:
								object.special_flags += 1
								if object.special_flags > 6:
									object.image = load(path + "Images/Objects/Punch " + str(object.special_flags - 5) + ".png")
							else:
								object.special_flags = 1
								world.chunk_manager.get_chunk_at(object.x, object.y).items.append(Object("Punch", object.x, object.y, "Images/Items/Powder.png"))

				if player.breaking_object is None and player.started_break:
					player.started_break = False
					if game.multiplayer:
						game.events.append({"event_type": "object_stopped_breaking", "x": player.breaking_object_info[0], "y": player.breaking_object_info[1], "name": player.breaking_object_info[2]})
					player.breaking_object_info = None

				# Отображение предметов
				if inventory.whole_inventory[inventory.changed_slot] is None:
					last_changed_item = None
				else:
					last_changed_item = inventory.whole_inventory[inventory.changed_slot].name

				for item in world.visible_items:
					item.main(game, dt)
					try_pick = True
					if item.pickable and Settings["Game"][0] and player.x - 150 < item.x < player.x + 150 and player.y - 150 < item.y < player.y + 150:
						world.particles.append(Particle(item.x, item.y, item.image, lambda particle: round(((player.x - particle.x) // 2) / 10 * 5), lambda particle: round(((player.y - particle.y) // 2) / 10 * 5), track_ticks=True, del_self_condition=lambda particle: abs(particle.x - player.x) < 30 and abs(particle.y - player.y) < 30, end_command=lambda particle: (inventory.increate(particle.special_flags), play_sound("Pick an item")), special_flags=item.name))
						if game.multiplayer:
							game.events.append({"event_type": "item_removed", "x": item.x, "y": item.y, "name": item.name})

						world.chunk_manager.get_chunk_at(item.x, item.y).items.remove(item)
						try_pick = False

					if try_pick and item.x - player.x + Width // 2 - item.image.get_width() // 2 <= mouse_x <= item.x - player.x + Width // 2 + item.image.get_width() // 2 and player.y - item.y + Height // 2 - item.image.get_height() // 2 <= mouse_y <= player.y - item.y + Height // 2 + item.image.get_height() // 2:
						mouse_object = t("Click to pick the ") + t("Item name " + item.name)
						
						if click[0]:
							world.particles.append(Particle(item.x, item.y, item.image, lambda particle: round(((player.x - particle.x) // 2) / 10 * 5), lambda particle: round(((player.y - particle.y) // 2) / 10 * 5), track_ticks=True, del_self_condition=lambda particle: abs(particle.x - player.x) < 30 and abs(particle.y - player.y) < 30, end_command=lambda particle: (inventory.increate(particle.special_flags), play_sound("Pick an item")), special_flags=item.name))
									
							if game.multiplayer:
								game.events.append({"event_type": "item_removed", "x": item.x, "y": item.y, "name": item.name})
							world.chunk_manager.get_chunk_at(item.x, item.y).items.remove(item)
						elif item.pickable and click[2] and inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].name in ("Blue slime", "Pink slime"):
							item.pickable = False
							inventory.reduce(inventory.changed_slot)

		else:

			for object in world.backrooms_objects:

				object.main()

				if click[0] and object.x - player.x + Width // 2 - object.w // 2 <= mouse_x <= object.x - player.x + Width // 2 + object.w // 2 and player.y - object.y + Height // 2 - object.h // 2 <= mouse_y <= player.y - object.y + Height // 2 + object.h // 2:

					mouse_object = object.name

					if object.name == "Pot":

						if object.get_right_pressed(mouse_x, mouse_y, player) and inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].type == "Flower":
							world.chunk_manager.get_chunk_at(object.x, object.y).items.append(Object(inventory.whole_inventory[inventory.changed_slot].name, object.x, object.y + 36, 64, 64, inventory.whole_inventory[inventory.changed_slot].image))
							inventory.reduce(inventory.changed_slot)

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
			projectile.main(game)

		for wall in world.visible_walls.values():
			wall.main(release, mouse_x, mouse_y, game)
		
		if not Backrooms.InBackrooms and world.current_cave is None:

			# Отображение мобов
			for mob in world.mobs:

				mob.update(game, dt)
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
		
		player.render()

		if game.multiplayer:
			with game.net.lock:
				peers_copy = dict(game.net.peers.items())  # Создаем копию
			for pid, peer in peers_copy.items():
				if pid != game.net.player_id:
					if pid in game.net.server_events:
						for event in game.net.server_events[pid]:
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

							game.net.server_events[pid].remove(event)
					peer.render(game)
					peer.update_animation(dt)
					if peer.breaking_object_info is not None:
						for object in world.visible_objects:
							if (object.x, object.y, object.name) == (*peer.breaking_object_info,):
								object.image = crack_surface(world, Particle, object, (object.max_break - object.breaked) // object.max_break, 8)
								break

		# Анимации Хиро

		if player.animation[0] is None:
			
			if random.randint(1, 300) == 1:
				player.animation = ["Close eyes", 0, 16]

		elif player.animation[1] <= player.animation[2]:
			player.animation[1] += 1
		else:
			player.animation = [None, 0]

		changed_item_x = 0
		changed_item_y = 0

		match player.direction:

			case "Down":

				match player.costum:
					# 97, 209
					case 0 | 1 | 3 | 4 | 6 | 7:

						changed_item_x = Width // 2 - 80
						changed_item_y = Height // 2

						match player.animation[0]:

							case "Close eyes":

								if player.animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 32, 8, player.animation[1] * 2))
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 32, 8, player.animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 32, 8, (8 - player.animation[1] + 8) * 2))
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 32, 8, (8 - player.animation[1] + 8) * 2))

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

						match player.animation[0]:

							case "Close eyes":

								if player.animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, player.animation[1] * 2))
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, player.animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, (8 - player.animation[1] + 8) * 2))
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, (8 - player.animation[1] + 8) * 2))

					case 5:

						changed_item_x = Width // 2 - 94
						changed_item_y = Height // 2 - 16

						match player.animation[0]:

							case "Close eyes":

								if player.animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, player.animation[1] * 2))
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, player.animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, (8 - player.animation[1] + 8) * 2))
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, (8 - player.animation[1] + 8) * 2))

			case "Left":

				match player.costum:

					case 0 | 1 | 3 | 4 | 6 | 7:

						changed_item_x = Width // 2 - 84
						changed_item_y = Height // 2 - 16

						match player.animation[0]:

							case "Close eyes":

								if player.animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 32, 8, player.animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 32, 8, (8 - player.animation[1] + 8) * 2))

					case 2:

						changed_item_x = Width // 2 - 104
						changed_item_y = Height // 2

						match player.animation[0]:

							case "Close eyes":

								if player.animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, player.animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, (8 - player.animation[1] + 8) * 2))

					case 5:

						changed_item_x = Width // 2 - 70
						changed_item_y = Height // 2

						match player.animation[0]:

							case "Close eyes":

								if player.animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, player.animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 - 24, Height / 2 - 24, 8, (8 - player.animation[1] + 8) * 2))

			case "Right":

				match player.costum:

					case 0 | 1 | 3 | 4:

						changed_item_x = Width // 2 - 20
						changed_item_y = Height // 2

						match player.animation[0]:

							case "Close eyes":

								if player.animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 32, 8, player.animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 32, 8, (8 - player.animation[1] + 8) * 2))

					case 2:

						changed_item_x = Width // 2 - 32
						changed_item_y = Height // 2

						match player.animation[0]:

							case "Close eyes":

								if player.animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, player.animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, (8 - player.animation[1] + 8) * 2))

					case 5 | 6 | 7:

						changed_item_x = Width // 2 - 16
						changed_item_y = Height // 2 + 16

						match player.animation[0]:

							case "Close eyes":

								if player.animation[1] < 9:
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, player.animation[1] * 2))
								else:
									win.fill((62, 39, 49), (Width // 2 + 16, Height / 2 - 24, 8, (8 - player.animation[1] + 8) * 2))

		if inventory.whole_inventory[inventory.changed_slot] is not None and player.direction != "Up" and not (changed_item_x == changed_item_y == 0):
			win.blit(inventory.whole_inventory[inventory.changed_slot].image, (changed_item_x, changed_item_y))

		# Рон
		old_ron_pos = ron.x, ron.y
		ron.update(world, dt, not game.multiplayer or game.multiplayer_role == "Host")
		if game.multiplayer and game.multiplayer_role == "Host" and old_ron_pos != (ron.x, ron.y):
			game.events.append({"event_type": "ron_moved", "x": ron.x, "y": ron.y, "direction": ron.direction})

		# Механика использования еды и некоторых предметов через пробел

		for i in range(Settings["Display"][2]):
			win.blit(pygame.transform.scale(win, (Width - i * 2, Height - i * 2)), (i, i))

		if inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].name in ("Gun", "Bow") and Settings["Game"][1]:
			win.blit(Inventory_slot, (Width - 370, Height - 74))
			win.blit(inventory.whole_inventory[inventory.changed_slot].image, (Width - 370, Height - 74))
		
		if (inventory.whole_inventory[inventory.changed_slot] is not None and (use_item_pressed or (click[0] and Settings["Game"][1]))) and not game.chat_open:
			item_actions.handle_item_actions(mouse_x, mouse_y)

		if keys[hot_keys["Screenshot"]] and keys[hot_keys["Show keys"]]:
			
			pygame.image.save(win, str(Path.home()) + "/Your Screenshot " + time.asctime().replace(":", " ") + ".png")
			command_system.chat_message(t("Game: Your screenshot is in ") + str(Path.home()) + "/Your Screenshot " + time.asctime().replace(":", " ") + ".png")
			
			for _ in range(3):
				win.fill((200, 255, 200))
				clock.tick(MAX_FPS)
				pygame.display.update()
			time.sleep(0.1)

		# Отрисовка погоды

		weather.update()
		weather.draw()
		
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
					if game.slot_animations[yy * 10 + xx][0]:
						if game.slot_animations[yy * 10 + xx][1] < dt * 150:
							game.slot_animations[yy * 10 + xx][1] += 1
							game.slot_animations[yy * 10 + xx][2] -= 3
							game.slot_animations[yy * 10 + xx][2] = abs(game.slot_animations[yy * 10 + xx][2])
					else:
						game.slot_animations[yy * 10 + xx] = [True, 0, 10]
					
				elif game.slot_animations[yy * 10 + xx][0]:
					game.slot_animations[yy * 10 + xx][0] = False
					game.slot_animations[yy * 10 + xx][1] = 0
				elif game.slot_animations[yy * 10 + xx][1] < dt * 250:
					game.slot_animations[yy * 10 + xx][1] += 1	

		# Меню на клавише TAB

		if keys[hot_keys["TAB menu"]] and not game.chat_open:
			result = game.tab_menu.tab_menu()
			if result:
				return result

		if Settings["Game"][1]:

			up_b.main()
			left_b.main()
			down_b.main()
			right_b.main()
			if game.inventory_open:
				win.blit(load(path + "Images/Slots/Open inventory slot.png", 64), (890, 10))
				if 890 <= mouse_x <= 954 and 10 <= mouse_y <= 74 and click[0]:
					game.inventory_open = False
			else:
				win.blit(load(path + "Images/Slots/Open inventory slot.png", 64), (810, 10))
				if 810 <= mouse_x <= 874 and 10 <= mouse_y <= 74 and click[0]:
					game.inventory_open = True
		
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
		if game.inventory_open:

			if 10 < mouse_x < 794 and 10 < mouse_y < 314:
				mouse_object = t("Inventory (I)")

			slot_x = 10
			slot_y = 10

			for slot in range(30):
				
				if slot == inventory.changed_slot: win.blit(Changed_inventory_slot, (slot_x, slot_y))
				else:
					
					if game.slot_animations[slot][0]:
						try:win.blit(pygame.transform.scale(Inventory_slot, (64 - game.slot_animations[slot][2], 64 - game.slot_animations[slot][2])), (slot_x, slot_y))
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

			item_to_get = inventory.check_recipies(need_object)
			
			if item_to_get is not None:

				win.blit(Changed_inventory_slot, (730, 250))
				win.blit(inventory.resources[item_to_get[0]].image, (730, 250))

				if item_to_get[2] is not None:
					win.blit(inventory.resources[item_to_get[2]].image, (10, 250))
				if item_to_get[3] is not None:
					win.blit(inventory.resources[item_to_get[3]].image, (90, 250))
				if 730 <= mouse_x <= 810 and 250 <= mouse_y <= 330 and release:
					inventory.increate(item_to_get[0], item_to_get[1])
					inventory.craft_items_list = [None] * 7
					inventory.craft_amounts_list = [None] * 7
					inventory.craft_images_list = [None] * 7
			
			# Разделение предметов
			if 810 <= mouse_x <= 874 and 10 <= mouse_y <= 74:
				if game.special_slot_animations["Split items slot"][0]:
					if game.special_slot_animations["Split items slot"][1] < FPS / 6:
						game.special_slot_animations["Split items slot"][1] += 1
						game.special_slot_animations["Split items slot"][2] -= 3
						game.special_slot_animations["Split items slot"][2] = abs(game.special_slot_animations["Split items slot"][2])
				else:
					game.special_slot_animations["Split items slot"] = [True, 0, 10]
				
				if release:
					inventory.Split_items = not inventory.Split_items
				
			elif game.special_slot_animations["Split items slot"][0]:
				game.special_slot_animations["Split items slot"][0] = False
				game.special_slot_animations["Split items slot"][1] = 0
			elif game.special_slot_animations["Split items slot"][1] < FPS / 4:
				game.special_slot_animations["Split items slot"][1] += 1   

			if game.special_slot_animations["Split items slot"][0] or inventory.Split_items:
				try:
					if Settings["Display"][5]: win.blit(pygame.transform.scale(Split_items2, (64 - game.special_slot_animations["Split items slot"][2], 64 - game.special_slot_animations["Split items slot"][2])), (810, 10))
					else: win.blit(pygame.transform.scale(Split_items2, (64, 64)), (810, 10))
				except: win.blit(pygame.transform.scale(Split_items2, (64, 64)), (810, 10))
				mouse_object = t("Split items")
			
			else:
				win.blit(pygame.transform.scale(Split_items1, (64, 64)), (810, 10))
			
			# Сжатие инвентаря
			
			if 810 <= mouse_x <= 874 and 170 <= mouse_y <= 234:
				if game.special_slot_animations["Compact inventory slot"][0]:
					if game.special_slot_animations["Compact inventory slot"][1] < FPS / 6:
						game.special_slot_animations["Compact inventory slot"][1] += 1
						game.special_slot_animations["Compact inventory slot"][2] -= 3
						game.special_slot_animations["Compact inventory slot"][2] = abs(game.special_slot_animations["Compact inventory slot"][2])
				else:
					game.special_slot_animations["Compact inventory slot"] = [True, 0, 10]
				
				if release:
					inventory.compact_inventory()
				
			elif game.special_slot_animations["Compact inventory slot"][0]:
				game.special_slot_animations["Compact inventory slot"][0] = False
				game.special_slot_animations["Compact inventory slot"][1] = 0
			elif game.special_slot_animations["Compact inventory slot"][1] < FPS / 4:
				game.special_slot_animations["Compact inventory slot"][1] += 1	

			if game.special_slot_animations["Compact inventory slot"][0]:
				try:
					if Settings["Display"][5]: win.blit(pygame.transform.scale(Compact_inventory2, (64 - game.special_slot_animations["Compact inventory slot"][2], 64 - game.special_slot_animations["Compact inventory slot"][2])), (810, 170))
					else: win.blit(pygame.transform.scale(Compact_inventory2, (64, 64)), (810, 170))
				except: win.blit(pygame.transform.scale(Compact_inventory2, (64, 64)), (810, 170))
				mouse_object = t("Compact inventory")
			
			else:
				win.blit(pygame.transform.scale(Compact_inventory1, (64, 64)), (810, 170))

			inventory.draw_whole()
			
			if game.craft_list_open:

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
							win.blit(Inventory_slot, (970 + cell_x * 80, 10 + game.craft_list_offset + cell_y * 80))
							win.blit(inventory.resources[ii].image, (970 + cell_x * 80, 10 + game.craft_list_offset + cell_y * 80))
							win.blit(textInfo.render(str(recipe.ingredients_amounts[cell_x]), True, (0, 150, 0)), (980 + cell_x * 80, 52 + game.craft_list_offset + cell_y * 80))
					if recipe.need_object is not None:
						cell_x = 8
						win.blit(Changed_inventory_slot, (990 + cell_x * 80, 10 + game.craft_list_offset + cell_y * 80))
						win.blit(inventory.resources[recipe.need_object].image, (990 + cell_x * 80, 10 + game.craft_list_offset + cell_y * 80))
					if recipe.need_tool is not None:
						cell_x = 9
						win.blit(Changed_inventory_slot, (990 + cell_x * 80, 10 + game.craft_list_offset + cell_y * 80))
						win.blit(inventory.resources[recipe.need_tool].image, (990 + cell_x * 80, 10 + game.craft_list_offset + cell_y * 80))
					cell_x = 10
					win.blit(Changed_inventory_slot, (990 + cell_x * 80, 10 + game.craft_list_offset + cell_y * 80))
					win.blit(inventory.resources[recipe.result].image, (990 + cell_x * 80, 10 + game.craft_list_offset + cell_y * 80))
					win.blit(textInfo.render(str(recipe.result_amount), True, (0, 150, 0)), (1000 + cell_x * 80, 52 + game.craft_list_offset + cell_y * 80))

				if 810 <= mouse_x <= 874 and 90 <= mouse_y <= 154 and release:
					game.craft_list_open = False
						
			else:
				
				if 810 <= mouse_x <= 874 and 90 <= mouse_y <= 154:
					if game.special_slot_animations["Craft list slot"][0]:
						if game.special_slot_animations["Craft list slot"][1] < FPS / 6:
							game.special_slot_animations["Craft list slot"][1] += 1
							game.special_slot_animations["Craft list slot"][2] -= 3
							game.special_slot_animations["Craft list slot"][2] = abs(game.special_slot_animations["Craft list slot"][2])
					else:
						game.special_slot_animations["Craft list slot"] = [True, 0, 10]
					
					if release:
						game.craft_list_open = True
					
				elif game.special_slot_animations["Craft list slot"][0]:
					game.special_slot_animations["Craft list slot"][0] = False
					game.special_slot_animations["Craft list slot"][1] = 0
				elif game.special_slot_animations["Craft list slot"][1] < FPS / 4:
					game.special_slot_animations["Craft list slot"][1] += 1	 

				if game.special_slot_animations["Craft list slot"][0] and Settings["Display"][5]:
					try:win.blit(pygame.transform.scale(Changed_craft_list_inventory_slot, (64 - game.special_slot_animations["Craft list slot"][2], 64 - game.special_slot_animations["Craft list slot"][2])), (810, 90))
					except: win.blit(pygame.transform.scale(Changed_craft_list_inventory_slot, (64, 64)), (810, 90))
					mouse_object = t("Craft list")
			
				else:
					win.blit(pygame.transform.scale(Craft_list_inventory_slot, (64, 64)), (810, 90))

			if alt_pressed:
				draw_key(" I ", 42, 344)

			if inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].name == "Wrench":

				if 900 <= mouse_x <= 964 and 10 <= mouse_y <= 74:
					win.blit(Changed_inventory_slot, (900, 10))
					if release: game.item_settings_open = True
				else:
					win.blit(Inventory_slot, (900, 10))
		else:
			
			if 10 < mouse_x < 794 and 10 < mouse_y < 74:
				mouse_object = t("Inventory (I)")

			for slot_x in range(10):
				if slot_x == inventory.changed_slot: win.blit(Changed_inventory_slot, (slot_x * 80 + 10, 10))
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
		
		if game.item_settings_open:

			if inventory.whole_inventory[inventory.changed_slot].name == "Wrench":

				win_fill()

				pygame.draw.rect(win, text_color, (100, 100, Width - 200, Height - 200))
				pygame.draw.rect(win, (0, 150, 0), (100, 100, Width - 200, Height - 200), 10)
				win.blit(pygame.transform.scale2x(inventory.whole_inventory[inventory.changed_slot].image), (Width // 2 - 64, 130))
				pygame.draw.line(win, (0, 150, 0), (150, 308), (Width - 150, 308), 10)
				win.blit(textInfo.render(t("Only wire"), True, (0, 150, 0)), (130, 348))
				win.blit(textInfo.render(t("All mechanisms"), True, (0, 150, 0)), (Width // 2 - textInfo.size(t("All mechanisms"))[0] // 2, 348))
				win.blit(textInfo.render(t("All mechanisms except wire"), True, (0, 150, 0)), (Width - 150 - textInfo.size(t("All mechanisms except wire"))[0], 378))

				if inventory.whole_inventory[inventory.changed_slot].settings == ["Only wire"]:
					pygame.draw.rect(win, (0, 150, 0), (120, 278, 60, 60), 30)
					pygame.draw.circle(win, (0, 150, 0), (Width // 2, 308), 30)
					pygame.draw.circle(win, (0, 150, 0), (Width - 150, 308), 30)
				if inventory.whole_inventory[inventory.changed_slot].settings == []:
					pygame.draw.circle(win, (0, 150, 0), (150, 308), 30)
					pygame.draw.rect(win, (0, 150, 0), (Width // 2 - 30, 278, 60, 60), 30)
					pygame.draw.circle(win, (0, 150, 0), (Width - 150, 308), 30)
				if inventory.whole_inventory[inventory.changed_slot].settings == ["All mechanisms, but wire"]:
					pygame.draw.circle(win, (0, 150, 0), (150, 308), 30)
					pygame.draw.circle(win, (0, 150, 0), (Width // 2, 308), 30)
					pygame.draw.rect(win, (0, 150, 0), (Width - 180, 278, 60, 60), 30)

				if 120 <= mouse_x <= 180 and 278 <= mouse_y <= 338 and release:
					inventory.whole_inventory[inventory.changed_slot].settings = ["Only wire"]
				if Width // 2 - 30 <= mouse_x <= Width // 2 + 30 and 278 <= mouse_y <= 338 and release:
					inventory.whole_inventory[inventory.changed_slot].settings = []
				if Width - 180 <= mouse_x <= Width - 120 and 278 <= mouse_y <= 338 and release:
					inventory.whole_inventory[inventory.changed_slot].settings = ["All mechanisms, but wire"]
					
				
				win.blit(bigTextInfo.render("x", True, (0, 150, 0)), (Width - 160, 130))
				
				if alt_pressed:
					draw_key("ESC", Width - 160, 170)
					
				if Width - 160 <= mouse_x <= Width - 130 and 130 <= mouse_y <= 160:
					win.blit(bigTextInfo.render("x", True, (0, 100, 0)), (Width - 160, 130))
					if release:
						game.item_settings_open = False
		
		if inventory.whole_inventory[inventory.changed_slot] is not None:
			text(t("Item name " + inventory.whole_inventory[inventory.changed_slot].name), 10, 320 if game.inventory_open else 80)

		if ron.x - player.x + Width // 2 - 128 <= mouse_x <= ron.x - player.x + Width // 2 + 128 and player.y - ron.y + Height // 2 - 128 <= mouse_y <= player.y - ron.y + Height // 2 + 128 and release and (not game.multiplayer or game.multiplayer_role == "Host"):
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
					
		if game.in_motherboard is not None:

			win_fill()

			pygame.draw.rect(win, text_color, (Width // 2 - 300, Height // 2 - 300, 600, 600))
			pygame.draw.rect(win, (0, 150, 0), (Width // 2 - 300, Height // 2 - 300, 600, 600), 10)
			
			a = -1
			b = 0

			for i in game.in_motherboard.objects:
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
					game.in_motherboard = None

		if game.menu_open:

			text(f"""X {player.x // 50}
Y {player.y // 50}
Ron X {ron.x // 50}
Ron Y {ron.y // 50}
FPS {FPS}""" + (f"""
You are in backrooms lol
Level {Backrooms.Level}""" if Backrooms.InBackrooms else ""), 10, 400 if game.inventory_open else 300)
		
		if inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].name == "Wire":

			if game.in_motherboard is None:
				pos = (player.x + mouse_x - Width // 2) // 64 * 64 + 32, (player.y - mouse_y + Height // 2) // 64 * 64 + 32
				draw_select_image(64, 64, game, mouse_x, mouse_y)


				a = True
				if click[0]:
					for mechanism in world.mechanisms:
						if mechanism.x == (player.x + mouse_x - Width // 2) // 64 and mechanism.y == (player.y - mouse_y + Height // 2) // 64:
							a = False
							break
				
					if a:
						inventory.reduce(inventory.changed_slot)
						world.mechanisms.append(Wire(player, world, mouse_x, mouse_y, None))
			else:
				a = True
				if click[0]:
					for mechanism in game.in_motherboard.objects:
						if mechanism is not None and mechanism.x == (mouse_x - Width // 2 - 300) // 18.75 and mechanism.y == (mouse_y + Width // 2 - 300) // 18.75:
							a = False
							break
				
					if a and Width // 2 - 300 <= mouse_x <= Width // 2 + 300 and  Height // 2 - 310 <= mouse_y < Height // 2 + 290:
						inventory.reduce(inventory.changed_slot)
						game.in_motherboard.objects[(mouse_x - Width // 2 - 300) // 19 + ((mouse_y + Width // 2 - 300) // 19 - 19) * 32] = (Wire(player, world, mouse_x, mouse_y, game.in_motherboard))

		if inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].name == "Lever":

			pos = (player.x + mouse_x - Width // 2) // 64 * 64 + 32, (player.y - mouse_y + Height // 2) // 64 * 64 + 32
			draw_select_image(64, 64, game, mouse_x, mouse_y)

			a = True
			if click[0]:
				for mechanism in world.mechanisms:
					if mechanism.x == (player.x + mouse_x - Width // 2) // 64 and mechanism.y == (player.y - mouse_y + Height // 2) // 64:
						a = False
				
				if a:
					inventory.reduce(inventory.changed_slot)
					world.mechanisms.append(Lever(Player, world, mouse_x, mouse_y, None))

		if inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].name == "Wrench":

			pos = (player.x + mouse_x - Width // 2) // 64 * 64 + 32, (player.y - mouse_y + Height // 2) // 64 * 64 + 32
			draw_select_image(64, 64, game, mouse_x, mouse_y)
			if click[0]:
				for mechanism in world.mechanisms:
					if mechanism.x == (player.x + mouse_x - Width // 2) // 64 and mechanism.y == (player.y - mouse_y + Height // 2) // 64:
						if (inventory.whole_inventory[inventory.changed_slot].settings == ["Only wire"] and mechanism.__class__ == Wire) or inventory.whole_inventory[inventory.changed_slot].settings == [] or (inventory.whole_inventory[inventory.changed_slot].settings == ["All mechanisms, but wire"] and mechanism.__class__ != Wire):
							world.mechanisms.remove(mechanism)
						break

		if inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].name == "Random box":

			pos = (player.x + mouse_x - Width // 2) // 64 * 64 + 32, (player.y - mouse_y + Height // 2) // 64 * 64 + 32
			draw_select_image(64, 64, game, mouse_x, mouse_y)
			a = True

			if click[0]:

				for mechanism in world.mechanisms:
					if mechanism.x == (player.x + mouse_x - Width // 2) // 64 and mechanism.y == (player.y - mouse_y + Height // 2) // 64:
						a = False
				
				if a:
					inventory.reduce(inventory.changed_slot)
					world.mechanisms.append(RandomBox(None))

		if inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].name == "Motherboard":

			pos = (player.x + mouse_x - Width // 2) // 64 * 64 + 32, (player.y - mouse_y + Height // 2) // 64 * 64 + 32
			draw_select_image(64, 64, game, mouse_x, mouse_y)

			a = True
			if click[0]:
				for mechanism in world.mechanisms:
					if mechanism.x == (player.x + mouse_x - Width // 2) // 64 and mechanism.y == (player.y - mouse_y + Height // 2) // 64:
						a = False
				
				if a:
					inventory.reduce(inventory.changed_slot)
					world.mechanisms.append(Motherboard(player, world, mouse_x, mouse_y, None))
		if inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].name == "Portal gun":

			draw_select_image(128, 256, game, mouse_x, mouse_y)

			if click[0]:

				a = 0
				if not check_collision(pygame.Rect((player.x + mouse_x - Width // 2) // 256 * 256 + 128, (player.y - mouse_y + Height // 2) // 256 * 256 + 128, 256, 256), world, False):
					world.chunk_manager.get_chunk_at((player.x + mouse_x - Width // 2) // 128, (player.y + mouse_y - Height // 2) // 256).objects.append(Portal())
		new_object = check_build_objects(objects_templates, game, mouse_x, mouse_y)

		if game.multiplayer and new_object:
			game.events.append({"event_type": "object_added", "object": new_object.__getstate__()})

		if inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].name == "Stone hoe":
			
			farmland_pos = (player.x + mouse_x - Width // 2) // 128 * 128 + 128, (player.y - mouse_y + Height // 2) // 128 * 128
			draw_select_image(128, 128, game, mouse_x, mouse_y)

			if click[0] and farmland_pos not in world.visible_farmlands and not check_collision(pygame.Rect(farmland_pos[0] - 128, farmland_pos[1], 128, 128), world, False):
				world.chunk_manager.get_chunk_at(*farmland_pos).farmlands[farmland_pos] = Farmland(farmland_pos[0], farmland_pos[1])
				game.events.append({"event_type": "farmland_added", "farmland_pos": farmland_pos})

				play_sound("Dirt")
				# for farmland in (((farmland_pos[0] - 128, farmland_pos[1]), (farmland_pos[0] + 128, farmland_pos[1]), (farmland_pos[0], farmland_pos[1] - 128), (farmland_pos[0], farmland_pos[1] + 128))):
				#	if farmland in world.visible_farmlands:
				#		world.visible_farmlands[farmland].update_neigboors()

		if inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].name in wall_types:
			
			wall_pos = (player.x + mouse_x - Width // 2) // 256 * 256 + 128, (player.y - mouse_y + Height // 2) // 256 * 256 + 128
			draw_select_image(256, 256, game, mouse_x, mouse_y)

			if click[0] and wall_pos not in world.visible_walls and not check_collision(pygame.Rect(wall_pos[0], wall_pos[1], 256, 256), world, False, False):
				world.chunk_manager.get_chunk_at(*wall_pos).walls[wall_pos] = Wall(world, inventory.whole_inventory[inventory.changed_slot].name, wall_pos[0], wall_pos[1])
				for wall in (((wall_pos[0] - 256, wall_pos[1]), (wall_pos[0] + 256, wall_pos[1]), (wall_pos[0], wall_pos[1] - 256), (wall_pos[0], wall_pos[1] + 256))):
					if wall in world.visible_walls:
						world.visible_walls[wall].update_neigboors(world)
				if game.multiplayer:
					game.events.append({"event_type": "wall_added", "wall": world.chunk_manager.get_chunk_at(*wall_pos).walls[wall_pos].__getstate__()})
				inventory.reduce(inventory.changed_slot)

		if inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].name in door_types:

			wall_pos = (player.x + mouse_x - Width // 2) // 256 * 256 + 128, (player.y - mouse_y + Height // 2) // 256 * 256 + 128
			draw_select_image(256, 256, game, mouse_x, mouse_y)

			if click[0] and wall_pos not in world.visible_walls and not check_collision(pygame.Rect(wall_pos[0], wall_pos[1], 256, 256), world, False, False):
				world.chunk_manager.get_chunk_at(*wall_pos).walls[wall_pos] = Wall(world, inventory.whole_inventory[inventory.changed_slot].name, wall_pos[0], wall_pos[1], True)
				for wall in (((wall_pos[0] - 256, wall_pos[1]), (wall_pos[0] + 256, wall_pos[1]), (wall_pos[0], wall_pos[1] - 256), (wall_pos[0], wall_pos[1] + 256))):
					if wall in world.visible_walls:
						world.visible_walls[wall].update_neigboors(world)
				if game.multiplayer:
					game.events.append({"event_type": "wall_added", "wall": world.chunk_manager.get_chunk_at(*wall_pos).walls[wall_pos].__getstate__()})
				inventory.reduce(inventory.changed_slot)

		if inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].name == "Stone hammer":

			break_pos = (player.x + mouse_x - Width // 2) // 256 * 256 + 128, (player.y - mouse_y + Height // 2) // 256 * 256 + 128
			draw_select_image(256, 256, game, mouse_x, mouse_y)

			if click[0]:
				if break_pos in world.visible_walls:
					inventory.increate(world.chunk_manager.get_chunk_at(*break_pos).walls[break_pos].wall_type)
					destroy_object(world.visible_walls[break_pos].image, world.visible_walls[break_pos].x, world.visible_walls[break_pos].y, world, Particle)
					game.events.append({"event_type": "wall_removed", "break_pos": break_pos})
					world.chunk_manager.get_chunk_at(*break_pos).walls.pop(break_pos, None)
					for wall in ((break_pos[0] - 256, break_pos[1]), (break_pos[0] + 256, break_pos[1]), (break_pos[0], break_pos[1] - 256), (break_pos[0], break_pos[1] + 256)):
						if wall in world.chunk_manager.get_chunk_at(*wall).walls:
							world.chunk_manager.get_chunk_at(*wall).walls[wall].update_neigboors(world)

				for object in world.visible_objects:
					if object.breakable_by_hammer and (object.x, object.y) == break_pos:
						inventory.increate(object.name)
						destroy_object(object.image, object.x, object.y, world, Particle)
						game.events.append({"event_type": "object_removed", "x": object.x, "y": object.y, "name": object.name})
						world.chunk_manager.get_chunk_at(object.x, object.y).objects.remove(object)
						break

		if mouse_object is not None and Settings["Display"][8]:
			# text(mouse_object, Width - textInfo.size(mouse_object)[0] - 10, 10)
			win.blit(textInfo.render(mouse_object, True, text_color), (Width - textInfo.size(mouse_object)[0] - 10, 10))
		
		if game.chat_open:
			win_fill()
			win_fill(rect=(10, Height - 50, Width - 20, 40))
			if not input_system.inputting:

				game.chat_open = False
				if input_system.last_text[0:2] == "/!" and Settings["User"][1]:
					try:
						eval(input_system.last_text[2:])
						# Команды через eval - опасная штука, так что они доступны только в режиме разработчика
					except Exception as e:
						command_system.chat_message(languages("<<< Команда " + Settings["User"][0] + f" получила ошибку {e}" + ". >>>", "<<< " + Settings["User"][0] + f"'s command got an {e}" + "error. >>>", ""))
					else:
						command_system.chat_message(languages("<<< Команда " + Settings["User"][0] + " была успешно исполнена. >>>", "<<< " + Settings["User"][0] + "'s command was successfully executed. >>>", ""))
				elif input_system.last_text != "" and input_system.last_text[0] == "/":
					command_system.chat_message(command_system.execute(input_system.last_text))
				elif input_system.last_text != "":
					if game.multiplayer:
						message_text = f"{game.net.peers[game.net.player_id].name}: {input_system.last_text}"
					else:
						message_text = f"{Settings['User'][0]}: {input_system.last_text}"
					command_system.chat_message(message_text, True)
		
		if len(game.chat) != 0:

			if game.chat_tick == 0:
				game.chat.remove(game.chat[0])
				try:
					game.chat_tick = len(game.chat[0]) // 1.5 * FPS
				except: pass
			
		reversed_chat = game.main_chat.copy() if game.chat_open else game.chat.copy()
		reversed_chat.reverse()
		message_y = 80
		for message in reversed_chat:
			message_y += get_text_height(message)
			text(message, 10, Height - message_y)
		
		game.chat_tick = max(0, game.chat_tick - 1)
		
		if game.multiplayer_menu_open:
			
			enable_multiplayer = Button(Width // 2, Height // 2 - 30, bigTextInfo.render(t("Enable game.multiplayer"), True, menu_color_medium), bigTextInfo.render(t("Enable game.multiplayer"), True, menu_color_dark), alignment=True, info=t("Your IP-address - ") + socket.gethostbyname(socket.gethostname()))
			enter_another_game = Button(Width // 2, Height // 2 + 30, bigTextInfo.render(t("Enter another game"), True, menu_color_medium), bigTextInfo.render(t("Enter another game"), True, menu_color_dark), alignment=True)
			
			pygame.image.save(win, path + "Saves/Cache/Win.png")
			win_darken(win)
			a, b = True, None
			animation_showed = False
			release = False

			while game.multiplayer_menu_open:

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
						game.multiplayer_menu_open = False						

				win.fill(menu_color_light)

				if mouse_x <= 128 and mouse_y <= 128:
					win.blit(load(path + "Images/Buttons/Back 2.png", 128), (0, 0))
					if release:
						game.multiplayer_menu_open = False
						
				else:
					win.blit(load(path + "Images/Buttons/Back.png", 128), (0, 0))

				pygame.draw.rect(win, menu_color_dark, (0, 0, Width, Height), 10)
				pygame.draw.rect(win, menu_color_medium, (10, 10, Width - 20, Height - 20), 10)
				
				enable_multiplayer.main()
				enter_another_game.main()

				if enable_multiplayer.is_released:
					b = 1
					game.multiplayer_menu_open = False

				elif enter_another_game.is_released:
					b = 2
					game.multiplayer_menu_open = False
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
						if i.is_released:
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
					#		if a.is_released:
					#			break
							
					#		pygame.display.update()
					#		clock.tick(MAX_FPS)
				
		if inventory.whole_inventory[inventory.start_cell] is not None and inventory.start_cell > -1 and game.hold_left:

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

		if game.multiplayer:

			if inventory.check_new_items():
				if inventory.whole_inventory[inventory.changed_slot] is None:
					player.changed_item = None
				else:
					player.changed_item = inventory.whole_inventory[inventory.changed_slot].name
				game.events.append({"event_type": "changed_item", "changed_item": player.changed_item})
			if len(game.events) != 0:
				game.net.send_events(tuple(game.events))
			for event in game.net.server_events["Game"]:
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
							chunk.walls[wall_pos] = Wall(world, wall["wall_type"], wall["x"], wall["y"], wall["is_door"])
							chunk.walls[wall_pos].__setstate__(wall)
							for wall in (((wall_pos[0] - 256, wall_pos[1]), (wall_pos[0] + 256, wall_pos[1]), (wall_pos[0], wall_pos[1] - 256), (wall_pos[0], wall_pos[1] + 256))):
								if wall in world.visible_walls:
									world.visible_walls[wall].update_neigboors(world)

					case "wall_removed":
						break_pos = tuple(event["break_pos"])
						chunk = world.chunk_manager.get_chunk_at(*break_pos)
						if chunk is not None and break_pos in chunk.walls:
							del chunk.walls[break_pos]
							for wall in (((break_pos[0] - 256, break_pos[1]), (break_pos[0] + 256, break_pos[1]), (break_pos[0], break_pos[1] - 256), (break_pos[0], break_pos[1] + 256))):
								if wall in world.visible_walls:
									world.visible_walls[wall].update_neigboors(world)

					case "wall_interaction":
						wall_pos = tuple(event["wall_pos"])
						chunk = world.chunk_manager.get_chunk_at(*wall_pos)
						if chunk is not None and wall_pos in chunk.walls:
							chunk.walls[wall_pos].open = not chunk.walls[wall_pos].open
							chunk.walls[wall_pos].update_neigboors(world)

					case "farmland_added":
						farmland_pos = tuple(event["farmland_pos"])
						chunk = world.chunk_manager.get_chunk_at(*farmland_pos)
						if chunk is not None:
							chunk.farmlands[farmland_pos] = Farmland(*farmland_pos)
							play_sound("Dirt")

					case "projectile_added":
						world.projectiles.append(Projectile(event["x"], event["y"], event["mouse_x"], event["mouse_y"], event["projectile_type"]))

					case "chat_message":
						command_system.chat_message(event["message_text"])

					case _:
						remove_event = False

				if remove_event:
					game.net.server_events["Game"].remove(event)

			if game.multiplayer_role == "Host":
				for event in game.net.server_events["Game"]:
					match event["event_type"]:
						case "peer_joined":
							game.net._send_packet({"type": "server_event", "player_id": "Game", "event_type": "world_info", "world_info": (
								0, 0, False, 0, None, player.speed, player.HP, game.start_time, ron.x, ron.y, ron.home, ron.inventory, world.chunk_manager.generator.seed, time_system.current_time, game.difficulty
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
							if event["player_id"] in game.net.peers:
								game.net._send_packet({"type": "server_event", "event_type": "chunk", "player_id": "Game", "chunk_key": chunk_key, "chunk_state": state}, game.net.peers[event["player_id"]].address)

					game.net.server_events["Game"].remove(event)
			else:
				if time.time() - game.net.last_heartbeat > 3:
					game.net.send_heartbeat()
				for event in game.net.server_events["Game"]:
					match event["event_type"]:
						case "world_info":
							player.x, player.y, Backrooms.InBackrooms, Backrooms.Level, world.current_cave, player.speed, player.HP, game.start_time, ron.x, ron.y, ron.home, ron.inventory, world.chunk_manager.generator.seed, time_system.current_time, game.difficulty = event["world_info"]
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
								new_walls[(wall["x"], wall["y"])] = Wall(world, wall["wall_type"], wall["x"], wall["y"])
								new_walls[(wall["x"], wall["y"])].__setstate__(wall)
							chunk.walls = new_walls

							new_farmlands = {}
							for farmland in chunk.farmlands:
								new_farmlands[(farmland["x"], farmland["y"])] = Farmland(farmland["x"], farmland["y"])
								new_farmlands[(farmland["x"], farmland["y"])].__setstate__(farmland)
							chunk.farmlands = new_farmlands
							world.chunk_manager.chunks_to_get.remove(chunk_key)

					game.net.server_events["Game"].remove(event)

		if keys[hot_keys["Screenshot"]] and not keys[hot_keys["Show keys"]]:
			
			pygame.image.save(win, str(Path.home()) + "/Your Screenshot " + str(time.asctime().replace(":", " ")) + ".png")
	
			for _ in range(3):
				win.fill((200, 255, 200))
				clock.tick(MAX_FPS)
				pygame.display.update()
			time.sleep(0.1)
			
		if keys[hot_keys["Plugin manager"]] and not game.chat_open:
			
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

game.start_game = start_game
game.settings_menu = SettingsMenu(game, save, music_channel, set_sound_volume, Settings, hot_keys)
game.characters_menu = CharactersMenu(game, player, save)
game.edit_world_menu = EditWorldMenu(game, player, Settings, world)
game.multiplayer_settings_menu = MultiplayerSettingsMenu(game, world, command_system, start_game)
game.worlds_menu = WorldsMenu(game, input_system)
game.main_menu = MainMenu(game, save)

def show_intro():
	
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

def loop():
	game.does_lighten = False
	current_screen = game.main_menu.main_menu
	while current_screen is not None:
		current_screen = current_screen()
	win_darken(win)
	game.does_lighten = False

def main():
	
	if Settings["Display"][10]:
		show_intro()

	if Settings["User"][1]:
		loop()
	else:
		try:
			loop()
		except Exception as e:
			music_channel.stop()
			if game.multiplayer:
				game.net.disconnect()
			show_error_window(e)

if __name__ == "__main__":
	main()

