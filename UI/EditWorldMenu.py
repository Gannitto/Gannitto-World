import pygame
import random
import sys
import os
import Saver
from Translator import t
from Assets import load
from Functions import win_darken, win_lighten, win_fill, draw_key
from Globals import path, win, clock, menu_color_dark, menu_color_medium, menu_color_light, textInfo, bigTextInfo, Width, Height
from Config import hot_keys
from Classes import Button
from UI.UISystem import UISystem

ui_system = UISystem()

class EditWorldMenu():
	
	def __init__(self, game, player, Settings, world):
		self.game = game
		self.player = player
		self.Settings = Settings
		self.world = world
		self.init_buttons()

	def init_buttons(self):

		self.easy_but = Button(50, 200, load(path + "Images/Buttons/Easy.png", 132, 64), load(path + "Images/Buttons/Easy 2.png", 132, 64))
		self.norm_but = Button(50, 270, load(path + "Images/Buttons/Norm.png", 132, 64), load(path + "Images/Buttons/Norm 2.png", 132, 64))
		self.hard_but = Button(50, 340, load(path + "Images/Buttons/Hard.png", 132, 64), load(path + "Images/Buttons/Hard 2.png", 132, 64))
		self.skull_but = Button(50, 410, load(path + "Images/Buttons/Skull.png", 132, 64), load(path + "Images/Buttons/Skull 2.png", 132, 64))

	def edit_world_menu(self):

		create_world = False
		release = False
		self.game.does_lighten = False

		try:
			self.game.difficulty, self.player.god_mode = Saver.load_objects(path + "Saves/Worlds/" + self.game.world_name + "/Settings.save")
		except:
			self.game.difficulty = "norm"
			self.player.god_mode = False
			create_world = True
		self.Settings["Edit world"]["World name"] = self.game.world_name
		self.Settings["Edit world"]["God mode"] = self.player.god_mode

		input_text = ""
		world_name_input = False
		seed_input = False

		if create_world:
			self.world.chunk_manager.generator.seed = random.randint(0, 2**31 - 1)
			self.world.chunk_manager.update_seed()
		while True:
			
			mouse_x, mouse_y = pygame.mouse.get_pos()
			click = pygame.mouse.get_pressed()
			keys = pygame.key.get_pressed()
			release = False
			events = pygame.event.get()

			for event in events:

				if event.type == pygame.QUIT:
					if not create_world:
						if self.game.world_name != self.Settings["Edit world"]["World name"]:
							os.rename(path + "Saves/Worlds/" + self.game.world_name, path + "Worlds/" + self.Settings["Edit world"]["World name"])
						self.game.world_name = self.Settings["Edit world"]["World name"]
						self.player.god_mode = self.Settings["Edit world"]["Edit world"]
						Saver.save_objects(path + "Saves/Worlds/" + self.game.world_name + "/Settings.save", [self.game.difficulty, self.player.god_mode])
					win_darken(win)
					sys.exit()
					
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						release = True

				elif event.type == pygame.KEYDOWN and (world_name_input or seed_input):
					if event.key == pygame.K_RETURN or len(input_text) == 50:
						if seed_input:
							if input_text != "":
								self.world.chunk_manager.generator.seed = int(input_text)
								self.world.chunk_manager.update_seed()
							seed_input = False
						input_text = ""
					elif event.key == pygame.K_BACKSPACE:
						input_text = input_text[:-1]
					elif not seed_input or event.unicode in "0123456789":
						input_text += event.unicode
				
				if event.type == pygame.KEYUP:
					
					if event.key == hot_keys["Close"] and not create_world:
						if self.game.world_name != self.Settings["Edit world"]["World name"]:
							os.rename(path + "Saves/Worlds/" + self.game.world_name, path + "Worlds/" + self.Settings["Edit world"]["World name"])
						self.game.world_name = self.Settings["Edit world"]["World name"]
						self.player.god_mode = self.Settings["Edit world"]["Edit world"]
						Saver.save_objects(path + "Saves/Worlds/" + self.game.world_name + "/Settings.save", [self.game.difficulty, self.player.god_mode])
						win_darken(win)
						self.game.does_lighten = False
						return self.game.worlds_menu.worlds_menu
					
					if event.key == hot_keys["Show keys"]:
						self.game.alt_pressed = not self.game.alt_pressed
			
			win.fill(menu_color_light)
			ui_system.handle_events(events, mouse_x, mouse_y, release, "World settings")
			ui_system.draw("World settings", show_settings_lines=False)

			win.blit(bigTextInfo.render("x", True, menu_color_medium), (Width - 50, 15))
			
			if Width - 50 < mouse_x < Width - 20 and 15 < mouse_y < 45:
				
				win.blit(bigTextInfo.render("x", True, menu_color_dark), (Width - 50, 15))
				
				if pygame.mouse.get_pressed()[0]:
					
					if not create_world:
						os.rename(path + "Saves/Worlds/" + self.game.world_name, path + "Saves/Worlds/" + self.Settings["Edit world"]["World name"])
						self.game.world_name = self.Settings["Edit world"]["World name"]
						self.player.god_mode = self.Settings["Edit world"]["Edit world"]
						Saver.save_objects(path + "Saves/Worlds/" + self.game.world_name + "/Settings.save", [self.game.difficulty, self.player.god_mode])
					win_darken(win)
					self.game.does_lighten = False
					return self.game.worlds_menu.worlds_menu

			win.blit(bigTextInfo.render(t("Game difficulty:"), True, menu_color_medium), (50, 150))

			self.easy_but.main()
			if self.easy_but.is_released:
				self.game.difficulty = "easy"
			
			self.norm_but.main()
			if self.norm_but.is_released:
				self.game.difficulty = "norm"
			
			self.hard_but.main()
			if self.hard_but.is_released:
				self.game.difficulty = "hard"
			
			self.skull_but.main()
			if self.skull_but.is_released:
				self.game.difficulty = "skull"

			win.blit(load(path + "Images/Modes/" + self.game.difficulty + ".png", 548, 274), (232, 200))
			
			match self.game.difficulty:
				
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
					win.blit(bigTextInfo.render(str(self.world.chunk_manager.generator.seed), True, menu_color_medium), (bigTextInfo.size(t("World seed"))[0] + 120, 600))
				win.blit(bigTextInfo.render(t("Create world"), True, menu_color_medium), (Width - bigTextInfo.size(t("Create world"))[0] - 50, 150))
				
				if Width - bigTextInfo.size(t("Create world"))[0] - 50 < mouse_x < Width - 50 and 150 < mouse_y < 180:
					
					win.blit(bigTextInfo.render(t("Create world"), True, menu_color_dark), (Width - bigTextInfo.size(t("Create world"))[0] - 50, 150))
					if release:
						self.game.world_name = self.Settings["Edit world"]["World name"]
						self.player.god_mode = self.Settings["Edit world"]["Edit world"]
						win_darken(win)
						self.game.does_lighten = False
						return self.game.start_game
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
							if yes_button.is_released:   # Удалить выбранный мир
								import shutil
								shutil.rmtree(path + "Saves/Worlds/" + self.game.world_name)
								del shutil
								win_darken(win)
								self.game.does_lighten = False
								return self.game.worlds_menu.worlds_menu
							
							no_button.main()
							if no_button.is_released or keys[hot_keys["Close"]]:
								break
						
							win_fill(alpha=100 - self.Settings["Display"]["Brightness"])   # Если в настройках установлена яркость ниже 100, то экран становится темнее
						
							pygame.display.update()
							clock.tick(self.game.max_fps)
						
				win.blit(bigTextInfo.render(t("Copy world"), True, menu_color_medium), (50, 600))

				if 50 < mouse_x < 50 + bigTextInfo.size(t("Copy world"))[0] and 600 < mouse_y < 630:
					win.blit(bigTextInfo.render(t("Copy world"), True, menu_color_dark), (50, 600))
					if release:
						import shutil
						shutil.copytree(path + "Saves/Worlds/" + self.game.world_name, path + "Worlds/" + self.game.world_name + t(" - copy"))
						del shutil
						win_darken(win)
						if create_world:
							return self.game.start_game
						else:
							return self.game.worlds_menu.worlds_menu
							
			if self.game.alt_pressed:
				draw_key("ESC", Width - 50, 55)
				
			win_fill(alpha=100 - self.Settings["Display"]["Brightness"])   # Если в настройках установлена яркость ниже 100, то экран становится темнее
			
			if not create_world:
				Saver.save_objects(path + "Saves/Worlds/" + self.game.world_name + "/Settings.save", [self.game.difficulty, self.player.god_mode])

			if not self.game.does_lighten:
				win_lighten(win)
				self.game.does_lighten = True
			
			pygame.display.update()
			clock.tick(self.game.max_fps)

