import pygame
import time
import random
import math
from itertools import product
import Backrooms
import Saver
from Functions import win_fill, win_darken, draw_key, text,get_text_height, show_error_window, animate_click, crack_surface, destroy_object, take_screenshot, pick_up_item
from Build import check_build_objects, draw_select_image, draw_select_image_arbitrarily
from Chunks import ChunkManager
from Inventory import Inventory
from Translator import translator, t
from Cache import load
from TimeSystem import TimeSystem
from Commands import CommandSystem
from Sound import play_sound, set_sound_volume, music_channel, update_sounds
from InputSystem import input_system
from Weather import WeatherSystem
from ItemActions import ItemActions
from Effects import EffectsSystem
from WorldLoader import WorldLoader
from InputHandler import InputHandler
from MobileControl import MobileControl
from VisualEffects import VisualEffects
from BarRenderer import BarRenderer
from Assets import cave_texture, biome_textures, Inventory_slot
from Globals import path, win, Width, Height, text_color, textInfo, bigTextInfo, clock, colors
from Config import Settings, hot_keys
from UI import SettingsMenu, CharactersMenu, WorldsMenu, EditWorldMenu, MultiplayerSettingsMenu, MainMenu, TabMenu
from Classes import Player, World, Object, Particle, Slime, Spider, Butterfly, Projectile, ExplodingProjectile, Wall, Farmland, Wire, Lever, Motherboard, RandomBox, Ron, Button
from GameState import GameState

pygame.init()

"""
Чтобы найти что-то на карте кода, просто вбейте в поиск

Карта кода:

Инициализация игры
Загрузка данных мира
Основной цикл игры
	Отображение объектов
	Отображение мобов
	Рон
	Механика использования еды и некоторых предметов через пробел
	Отрисовка погоды
	Отображение частиц
	Механика освещения
	Механика анимации слотов
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

	Saver.save_objects(path + "Saves/Settings/Statistics.save", game.statistics)
	
	if game.world_name is not None:
		
		if game.multiplayer:
			pass
			# TODO сохранение данных о других игроках
		else:
			
			Saver.save_objects(path + "Saves/Worlds/" + game.world_name + "/Mobs.save", world.mobs)
			Saver.save_objects(path + "Saves/Worlds/" + game.world_name + "/Info.save", [player.x, player.y, Backrooms.InBackrooms, Backrooms.Level, world.current_cave, player.speed, player.HP, game.start_time, ron.x, ron.y, ron.home, ron.inventory, world.chunk_manager.generator.seed, time_system.current_time])
			Saver.save_objects(path + "Saves/Worlds/" + game.world_name + "/Inventory.save", inventory.whole_inventory)
			Saver.save_objects(path + "Saves/Worlds/" + game.world_name + "/Resources.save", inventory.resources)
			Saver.save_objects(path + "Saves/Worlds/" + game.world_name + "/Effects.save", effects.effects)

			new_particles = []
			particle_count = 1
			for particle in world.particles:
				if particle.save_particle:
					pygame.image.save(particle.image, path + "Saves/Worlds/" + game.world_name +"/Images/Particle " + str(particle_count) + ".png")
					particle.image_path = path + "Saves/Worlds/" + game.world_name + "/Images/Particle " + str(particle_count) + ".png"
					particle_count += 1
					new_particles.append(particle)
			Saver.save_objects(path + "Saves/Worlds/" + game.world_name + "/Particles.save", new_particles)
			world.chunk_manager.save_all_loaded_chunks()
				
	if darken and Settings["Display"]["Dim screen when turned off"]:
		win_darken(win)
		
	if save_world_settings: Saver.save_objects(path + "Saves/Worlds/" + game.world_name + "/Settings.save", [game.difficulty, player.god_mode])

# Применение настроек TODO

pygame.display.set_icon(pygame.image.load(path + "Images/Icon.png"))
pygame.display.set_caption("Gannitto World")



# Инициализация игры

game = GameState()

game.player = Player()
player = game.player
game.world_to_screen = lambda X, Y, W, H, player=player: (X - player.x + Width // 2 - W // 2, player.y - Y + Height // 2 - H // 2)
world_to_screen = game.world_to_screen
game.world_rect_to_screen = lambda X, Y, W, H: (X - player.x + Width // 2 - W // 2, player.y - Y + Height // 2 - H // 2, W, H)
world_rect_to_screen = game.world_rect_to_screen
game.world = World(game)
world = game.world
game.time_system = TimeSystem()
time_system = game.time_system
game.ron = Ron(game)
ron = game.ron
game.inventory = Inventory(game)
inventory = game.inventory
game.command_system = CommandSystem(game)
command_system = game.command_system
game.item_actions = ItemActions(game)
item_actions = game.item_actions
game.tab_menu = TabMenu(game, save, music_channel)
game.effects = EffectsSystem()
effects = game.effects
game.Backrooms = Backrooms
game.input_system = input_system
game.world_loader = WorldLoader(game, save)
game.input_handler = InputHandler(game, save, music_channel)
game.bar_renderer = BarRenderer(game)
game.weather = WeatherSystem(world)
game.mobile_control = MobileControl(game)
game.visual_effects = VisualEffects(game)

# Основной цикл игры

def start_game():
	
	game.start_time = time.time()
	mouse_x = game.mouse_x
	mouse_y = game.mouse_y
	Width, Height = pygame.display.get_surface().get_size()

	game.craft_list_max_offset = (len(inventory.recipes) + 1) * -80 + Height

	# Загрузка данных мира
	if not game.multiplayer or game.multiplayer_role == "Host":
		game.world_loader.load_world()
	if inventory.whole_inventory[inventory.changed_slot]:
		player.changed_item = inventory.whole_inventory[inventory.changed_slot].name
	else:
		player.changed_item = None

	while True:

		mouse_x, mouse_y = pygame.mouse.get_pos()
		mouse_object = None
		click = pygame.mouse.get_pressed()
		Width, Height = pygame.display.get_surface().get_size()
		game.release = False
		player.hovered_object = None
		player.breaking_object = None
		game.use_item_pressed = False

		dt = clock.tick(game.max_fps) / 1000.0
		time_system.update(dt)
		if game.multiplayer:
			game.events.clear()
		events = pygame.event.get()
		result = game.input_handler.handle_events(events)
		if result:
			return result

		keys = pygame.key.get_pressed()

		# Если есть движение - двигаем игрока
		if player.dx != 0 or player.dy != 0:
			player.move(dt, game)
			game.events.append({"event_type": "player_moved", "x": player.x, "y": player.y, "direction": player.direction})
			if game.multiplayer:
				game.net.peers[game.net.player_id].x = player.x
				game.net.peers[game.net.player_id].y = player.y
				game.net.peers[game.net.player_id].direction = player.direction
		else:
			if player.is_moving:
				game.events.append({"event_type": "player_stopped", "x": player.x, "y": player.y})
			player.stop()
		
		# Обновляем анимацию и положение
		player.dx = 0
		player.dy = 0
		player.update_animation(dt)
		# Обновление системы здоровья
		player.update_health_and_death(game, mouse_x, mouse_y)

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
			farmland.main(game.release, dt, game, mouse_x, mouse_y)

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

		elif Backrooms.InBackrooms:
			
			Backrooms.handle_backrooms_logic(game, keys)

		if not Backrooms.InBackrooms:

			if world.current_cave is not None and -64 <= player.x <= 64 and -64 <= player.y <= 64 and game.release:

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
					if item.pickable and Settings["Game"]["Automatically pick up items"] and player.x - 150 < item.x < player.x + 150 and player.y - 150 < item.y < player.y + 150:
						pick_up_item(game, Particle, item)
						try_pick = False

					if try_pick and item.x - player.x + Width // 2 - item.image.get_width() // 2 <= mouse_x <= item.x - player.x + Width // 2 + item.image.get_width() // 2 and player.y - item.y + Height // 2 - item.image.get_height() // 2 <= mouse_y <= player.y - item.y + Height // 2 + item.image.get_height() // 2:
						mouse_object = t("Click to pick the ") + t("Item name " + item.name)
						
						if click[0]:
							pick_up_item(game, Particle, item)
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
			wall.main(game.release, mouse_x, mouse_y, game)
		
		if not Backrooms.InBackrooms and world.current_cave is None:

			# Отображение мобов
			for mob in world.mobs:
				mob.update(game, dt)
				mob.draw(game)

		# Отрисовка игрока
		player.render(game, dt)

		if game.multiplayer:
			game.net.show_players(game, dt)

		# Рон
		old_ron_pos = ron.x, ron.y
		ron.update(world, dt, not game.multiplayer or game.multiplayer_role == "Host")
		if game.multiplayer and game.multiplayer_role == "Host" and old_ron_pos != (ron.x, ron.y):
			game.events.append({"event_type": "ron_moved", "x": ron.x, "y": ron.y, "direction": ron.direction})

		# Механика использования еды и некоторых предметов через пробел

		for i in range(Settings["Display"]["Distance"]):
			win.blit(pygame.transform.scale(win, (Width - i * 2, Height - i * 2)), (i, i))

		if inventory.whole_inventory[inventory.changed_slot] is not None and inventory.whole_inventory[inventory.changed_slot].name in ("Gun", "Bow") and Settings["Game"]["Telephone control"]:
			win.blit(Inventory_slot, (Width - 370, Height - 74))
			win.blit(inventory.whole_inventory[inventory.changed_slot].image, (Width - 370, Height - 74))
		
		if (inventory.whole_inventory[inventory.changed_slot] is not None and (game.use_item_pressed or (click[0] and Settings["Game"]["Telephone control"]))) and not game.chat_open:
			item_actions.handle_item_actions(mouse_x, mouse_y)

		if keys[hot_keys["Screenshot"]] and keys[hot_keys["Show keys"]]:
			take_screenshot(game)
		# Отрисовка погоды

		game.weather.update()
		game.weather.draw()
		
		# Отображение частиц

		particles_to_delete = []
		for particle in world.particles:

			particle.main(dt, game)
			
			if (particle.end_time is not None and time.time() - particle.start_time >= particle.end_time) or (particle.del_self_condition is not None and particle.del_self_condition(particle)):
				if particle.end_command is not None:
					particle.end_command(particle)
				particles_to_delete.append(particle)
		
		for particle in particles_to_delete:
			world.particles.remove(particle)

		# Механика освещения

		# 1 слой - естественный свет
		if world.current_cave is None:
			current_brightness = time_system.get_brightness()
			light_level = max((1 - current_brightness) * 200, 0)
		else:
			light_level = 180

		game.shadow_surface = pygame.Surface((Width, Height), pygame.SRCALPHA)
		game.shadow_surface.fill((0, 0, 0, light_level))
		# 2 слой - тени
		# 3 слой - искусственное освещение
		world.chunk_manager.show_light_and_dark(light_level, player, game.shadow_surface) #TODO оптимизировать
		if player.hovered_object is not None:
			draw_select_image_arbitrarily(player.hovered_object.x, player.hovered_object.y, player.hovered_object.w, player.hovered_object.h, world_to_screen, world_rect_to_screen)
			mouse_object = player.hovered_object.name

		game.mobile_control.show_buttons(mouse_x, mouse_y, click)
		game.visual_effects.show_effects(dt)

		# Отображение инвентаря

		min_dist = 512
		near_object = None
		for object in world.visible_objects:
			if object.name in ("Table", "Wall table", "Furnace"):
				distance = math.dist((player.x, player.y), (object.x, object.y))
				if distance < min_dist:
					near_object = object.name
					min_dist = distance

		inventory.draw_inventory(mouse_x, mouse_y, dt, near_object)
		# Отображение полосы здоровья
		game.bar_renderer.show_health_bar(mouse_x, mouse_y)

		effects.handle_effects(dt)
	
		inventory.draw_item_settings(mouse_x, mouse_y)

		if inventory.whole_inventory[inventory.changed_slot] is not None:
			text(t("Item name " + inventory.whole_inventory[inventory.changed_slot].name), 10, 320 if game.inventory_open else 80)

		if ron.x - player.x + Width // 2 - 128 <= mouse_x <= ron.x - player.x + Width // 2 + 128 and player.y - ron.y + Height // 2 - 128 <= mouse_y <= player.y - ron.y + Height // 2 + 128 and game.release and (not game.multiplayer or game.multiplayer_role == "Host"):
			ron.window[0] = True
		ron.show_window(mouse_x, mouse_y)
		if game.menu_open:

			text(f"""X {player.x // 50}
Y {player.y // 50}
Ron X {ron.x // 50}
Ron Y {ron.y // 50}
FPS {int(clock.get_fps())}""" + (f"""
You are in backrooms lol
Level {Backrooms.Level}""" if Backrooms.InBackrooms else ""), 10, 400 if game.inventory_open else 300)

		check_build_objects(game, mouse_x, mouse_y)

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
							world.chunk_manager.get_chunk_at(*wall).walls[wall].update_neighbors(world)

				for object in world.visible_objects:
					if object.breakable_by_hammer and (object.x, object.y) == break_pos:
						inventory.increate(object.name)
						destroy_object(object.image, object.x, object.y, world, Particle)
						game.events.append({"event_type": "object_removed", "x": object.x, "y": object.y, "name": object.name})
						world.chunk_manager.get_chunk_at(object.x, object.y).objects.remove(object)
						break

		if mouse_object is not None and Settings["Display"]["Description of the object on hover"]:
			# text(mouse_object, Width - textInfo.size(mouse_object)[0] - 10, 10)
			win.blit(textInfo.render(mouse_object, True, text_color), (Width - textInfo.size(mouse_object)[0] - 10, 10))
		
		if game.chat_open:
			win_fill()
			win_fill(rect=(10, Height - 50, Width - 20, 40))
			if not input_system.inputting:

				game.chat_open = False
				if input_system.last_text[0:2] == "/!" and Settings["User"]["Nickname"]:
					try:
						eval(input_system.last_text[2:])
						# Команды через eval - опасная штука, так что они доступны только в режиме разработчика
					except Exception as e:
						command_system.chat_message(f"Ошибка выполнения команды {input_system.last_text[2:]}: {e}")
					else:
						command_system.chat_message(t("The command has been executed."))
				elif input_system.last_text != "" and input_system.last_text[0] == "/":
					command_system.chat_message(command_system.execute(input_system.last_text))
				elif input_system.last_text != "":
					if game.multiplayer:
						message_text = f"{game.net.peers[game.net.player_id].name}: {input_system.last_text}"
					else:
						message_text = f"{Settings['User']['Nickname']}: {input_system.last_text}"
					command_system.chat_message(message_text, True)
		
		if len(game.chat) != 0:

			if game.chat_tick == 0:
				game.chat.remove(game.chat[0])
				if len(game.chat) != 0:
					game.chat_tick = 10
			
		reversed_chat = game.main_chat.copy() if game.chat_open else game.chat.copy()
		reversed_chat.reverse()
		message_y = 80
		for message in reversed_chat:
			message_y += get_text_height(message)
			text(message, 10, Height - message_y)
		
		input_system.handle_input(events)
		game.chat_tick = max(0, game.chat_tick - dt)

		inventory.show_description(mouse_x, mouse_y, click)

		# Механика мультиплеера
		if game.multiplayer:
			game.net.handle_multiplayer(game)

		if keys[hot_keys["Screenshot"]] and not keys[hot_keys["Show keys"]]:
			take_screenshot(game)
		
		animate_click(dt, mouse_x, mouse_y)
		win_fill((200, 0, 0), 100 - Settings["Display"]["Brightness"])

		pygame.display.update()

game.start_game = start_game
game.settings_menu = SettingsMenu(game, save, music_channel, set_sound_volume, Settings, hot_keys)
game.characters_menu = CharactersMenu(game, player, save)
game.edit_world_menu = EditWorldMenu(game, Settings)
game.multiplayer_settings_menu = MultiplayerSettingsMenu(game, world, command_system, start_game)
game.worlds_menu = WorldsMenu(game, input_system)
game.main_menu = MainMenu(game, save)

def loop():
	game.does_lighten = False
	current_screen = game.main_menu.main_menu
	while current_screen is not None:
		current_screen = current_screen()
	win_darken(win)
	game.does_lighten = False

def main():
	
	game.statistics[0] += 1
	if Settings["Display"]["Show intro"]:
		pass # TODO сделать интро

	if Settings["User"]["Nickname"]:
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

