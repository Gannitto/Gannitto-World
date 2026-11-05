import pygame
import sys
import os
from Translator import t
from Assets import load
from Functions import win_darken, win_lighten, text, draw_key, animate_click, win_fill
from Globals import Width, Height, menu_color_medium, menu_color_dark, menu_color_light, textInfo, win, clock, MAX_FPS, path, Settings, hot_keys
from Classes import Button

class WorldsMenu():

	def __init__(self, game, input_system):
		self.game = game
		self.input_system = input_system
		self.init_buttons()

	def init_buttons(self):

		self.create_new_world_button = Button(Width // 2, 130, textInfo.render(t("Create world"), True, menu_color_medium), textInfo.render(t("Create world"), True, menu_color_dark), alignment=True)
		self.enter_another_game_button = Button(Width // 2, 130, textInfo.render("Подключиться в мир хоста", True, menu_color_medium), textInfo.render("Подключиться в мир хоста", True, menu_color_dark), alignment=True)
		self.single_player_button = Button(Width // 4, 50, textInfo.render(t("Single play"), True, menu_color_medium), textInfo.render(t("Single play"), True, menu_color_dark), alignment=True)
		self.multiplayer_button = Button(Width * 3 // 4, 50, textInfo.render(t("Multiplayer"), True, menu_color_medium), textInfo.render(t("Multiplayer"), True, menu_color_dark), alignment=True)
		self.back_button = Button(-20, -20, load(path + "Images/Buttons/Back.png", 128), load(path + "Images/Buttons/Back 2.png", 128, 128))
	
	def worlds_menu(self):

		inside_folders = []	
		for dirs, folder, files in os.walk(path + "Saves/Worlds/"):
			inside_folders = folder
			break

		inside_folders.sort()
		release = False
		bias = 0
		world_name_input = len(inside_folders) == 0

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
						self.game.alt_pressed = not self.game.alt_pressed
					if event.key == hot_keys["Close"]:
						if world_name_input:
							self.input_system.stop_input()
							world_name_input = False
						else:
							win_darken(win)
							self.game.does_lighten = False
							return self.game.main_menu.main_menu

			win.fill(menu_color_light)

			if world_name_input:
				text(t("Enter world name:"), Width // 2, Height // 2 - 20, menu_color_medium, alignment=True)
				if not self.input_system.inputting:
					self.game.world_name = self.input_system.last_text
					win_darken(win)
					return self.game.edit_world_menu.edit_world_menu
			else:

				if self.create_new_world_button.is_released:
					self.input_system.start_input("World name", Width // 2, Height // 2 + 20, text_alignment=True)
					world_name_input = True
				
				if self.back_button.is_released:
					self.input_system.stop_input()
					win_darken(win)
					self.game.does_lighten = False
					return self.game.main_menu.main_menu

				for temp_y, name_of_world in enumerate(inside_folders):

					text_y = 150 + bias + temp_y * 50

					win.blit(textInfo.render(name_of_world, True, menu_color_medium), (50, text_y))

					if 50 + textInfo.size(name_of_world)[0] <= mouse_x <= 82 + textInfo.size(name_of_world)[0] and text_y <= mouse_y <= text_y + 32:
						win.blit(load(path + "Images/Buttons/Edit 2.png", 32), (50 + textInfo.size(name_of_world)[0], text_y))
						if release:
							self.game.world_name = name_of_world
							win_darken(win)
							self.game.does_lighten = False
							return self.game.edit_world_menu.edit_world_menu

					if 50 <= mouse_x <= 50 + textInfo.size(name_of_world)[0] and text_y <= mouse_y <= text_y + textInfo.size(name_of_world)[1]:

						win.blit(textInfo.render(name_of_world, True, menu_color_dark), (50, text_y))
						
						win.blit(load(path + "Images/Buttons/Edit.png", 32), (50 + textInfo.size(name_of_world)[0], text_y))
						
						if release:
							if self.game.multiplayer:
								self.game.world_name = name_of_world
								self.game.multiplayer_role = "Host"
								win_darken(win)
								self.game.does_lighten = False
								return self.game.multiplayer_settings_menu.multiplayer_settings_menu
							else:
								self.game.world_name = name_of_world
								return self.game.start_game
				
				pygame.draw.rect(win, menu_color_light, (0, 0, Width, 103))
				pygame.draw.line(win, menu_color_medium, (0, 103), (Width, 103), 8)
				pygame.draw.line(win, menu_color_medium, (Width // 2, 0), (Width // 2, 103), 8)
				self.back_button.main()
				if self.game.multiplayer:
					self.single_player_button.main()
					if self.single_player_button.is_released:
						self.game.multiplayer = False
					win.blit(textInfo.render(t("Multiplayer"), True, menu_color_dark), (Width * 3 // 4 - textInfo.size(t("Multiplayer"))[0] // 2, 50 - textInfo.size(t("Multiplayer"))[1] // 2))
					self.enter_another_game_button.main()
					if self.enter_another_game_button.is_released:
						self.game.multiplayer_role = "Client"
						return self.game.multiplayer_settings_menu.multiplayer_settings_menu
				else:
					win.blit(textInfo.render(t("Single play"), True, menu_color_dark), (Width // 4 - textInfo.size(t("Single play"))[0] // 2, 50 - textInfo.size(t("Single play"))[1] // 2))
					self.multiplayer_button.main()
					if self.multiplayer_button.is_released:
						self.game.multiplayer = True
					self.create_new_world_button.main()
			
			self.input_system.handle_input(events)
			if self.game.alt_pressed: draw_key("ESC", 44, 108)
			
			animate_click(dt, mouse_x, mouse_y)

			win_fill(alpha=100 - Settings["Display"][0])   # Если в настройках установлена яркость ниже 100, то экран становится темнее
			if not self.game.does_lighten:
				win_lighten(win)
				self.game.does_lighten = True
			
			pygame.display.update()
