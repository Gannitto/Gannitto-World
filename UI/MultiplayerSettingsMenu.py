import pygame
import sys
import os
from Multiplayer import NetworkManager
from Assets import load
from Functions import win_darken, win_lighten, win_fill, draw_key, animate_click
from Globals import textInfo, menu_color_dark, menu_color_medium, menu_color_light, textInfo, bigTextInfo, Width, Height, path, clock, win
from Config import Settings, hot_keys
from Classes import Button, Peer
from UI.UISystem import UISystem

ui_system = UISystem()

class MultiplayerSettingsMenu():

	def __init__(self, game, world, command_system, start_game):

		self.game = game
		self.world = world
		self.command_system = command_system
		self.start_game = start_game
		self.init_buttons()

	def init_buttons(self):

		self.back_button = Button(-20, -20, load(path + "Images/Buttons/Back.png", 128), load(path + "Images/Buttons/Back 2.png", 128))
		self.host_button = Button(Width // 4, 50, textInfo.render("Хост (в твой мир заходят игроки)", True, menu_color_medium), textInfo.render("Хост (в твой мир заходят игроки)", True, menu_color_dark), alignment=True)
		self.client_button = Button(Width * 3 // 4, 50, textInfo.render("Клиент (ты заходишь в мир хоста)", True, menu_color_medium), textInfo.render("Клиент (ты заходишь в мир хоста)", True, menu_color_dark), alignment=True)
		self.start_game_button = Button(Width - 10 - bigTextInfo.size("Начать игру")[0], 150, bigTextInfo.render("Начать игру", True, menu_color_medium), bigTextInfo.render("Начать игру", True, menu_color_dark), alignment=True)

	def multiplayer_settings_menu(self):

		create_world = False
		release = False
		max_bias = -ui_system._set_positions(0, "Multiplayer settings menu")
		max_bias = (max_bias + Height - 103) * max_bias > Height - 103

		while True:
			
			mouse_x, mouse_y = pygame.mouse.get_pos()
			click = pygame.mouse.get_pressed()
			keys = pygame.key.get_pressed()
			release = False
			events = pygame.event.get()
			dt = clock.tick(self.game.max_fps) / 1000.0

			for event in events:

				if event.type == pygame.QUIT:
					win_darken(win)
					sys.exit()
					
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						release = True
				
				if event.type == pygame.KEYUP:
					
					if event.key == hot_keys["Show keys"]:
						self.game.alt_pressed = not self.game.alt_pressed
					if event.key == hot_keys["Close"]:
						win_darken(win)
						self.game.does_lighten = False
						return self.game.worlds_menu.worlds_menu
			
			win.fill(menu_color_light)

			pygame.draw.rect(win, menu_color_light, (0, 0, Width, 103))
			pygame.draw.line(win, menu_color_medium, (0, 103), (Width, 103), 8)
			pygame.draw.line(win, menu_color_medium, (Width // 2, 0), (Width // 2, 103), 8)
			ui_system.handle_events(events, mouse_x, mouse_y, release, "Multiplayer settings menu")
			ui_system.draw("Multiplayer settings menu",show_settings_lines=False)
			self.back_button.main()
			if self.back_button.is_released:
				win_darken(win)
				self.game.does_lighten = False
				return self.game.worlds_menu.worlds_menu

			if self.game.multiplayer_role == "Client":
				self.host_button.main()
				if self.host_button.is_released:
					self.game.multiplayer_role = "Host"
				win.blit(textInfo.render("Клиент (ты заходишь в мир хоста)", True, menu_color_dark), (Width * 3 // 4 - textInfo.size("Клиент (ты заходишь в мир хоста)")[0] // 2, 50 - textInfo.size("Клиент (ты заходишь в мир хоста)")[1] // 2))
			else:
				win.blit(textInfo.render("Хост (в твой мир заходят игроки)", True, menu_color_dark), (Width // 4 - textInfo.size("Хост (в твой мир заходят игроки)")[0] // 2, 50 - textInfo.size("Хост (в твой мир заходят игроки)")[1] // 2))
				self.client_button.main()
				if self.client_button.is_released:
					self.game.multiplayer_role = "Client"
			self.start_game_button.main()

			if self.start_game_button.is_released:
				self.game.net = NetworkManager(Peer, self.command_system.chat_message, self.world.chunk_manager.view_distance)
				if self.game.multiplayer_role == "Host":
					if Settings["Multiplayer"]["Соединение через интернет"]:
						self.game.net.start_host(Settings["Multiplayer"]["Порт"], Settings["Multiplayer"]["Внешний порт"])
					else:
						self.game.net.start_local_host(Settings["Multiplayer"]["Порт"])
				else:
					if not os.path.exists(path + "Saves/Cache/Multiplayer"):
						os.mkdir(path + "Saves/Cache/Multiplayer")
					self.world.chunk_manager.save_directory = path + "Saves/Cache/Multiplayer/"
					if Settings["Multiplayer"]["Соединение через интернет"]:
						self.game.net.connect_to_host(Settings["Multiplayer"]["IP хоста"], Settings["Multiplayer"]["Порт хоста"])
					else:
						self.game.net.connect_to_local_host(Settings["Multiplayer"]["IP хоста"], Settings["Multiplayer"]["Порт"])
					# connecting = True
					# while connecting:
					#	mouse_x, mouse_y = pygame.mouse.get_pos()
					#	for event in pygame.event.get():
					#		if event.type == pygame.QUIT:
					#			win_darken(win)
					#			sys.exit()
					#	win.fill(menu_color_light)
					#	for event in self.game.net.server_events["Game"]:
					#		if event["event_type"] == "world_info":
					#			connecting = False
					#	animate_click(dt, mouse_x, mouse_y)
					#	pygame.display.update()
					#	clock.tick(self.game.max_fps)
				return self.start_game

			if self.game.alt_pressed: draw_key("ESC", 44, 108)
			animate_click(dt, mouse_x, mouse_y)
			win_fill(alpha=100 - Settings["Display"]["Brightness"])   # Если в настройках установлена яркость ниже 100, то экран становится темнее

			if not self.game.does_lighten:
				win_lighten(win)
				self.game.does_lighten = True
			
			pygame.display.update()

