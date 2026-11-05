import pygame
import sys
from Assets import load
from Translator import t
from Functions import win_lighten, win_darken, draw_key, animate_click, win_fill
from Globals import Width, Height, path, win, clock, MAX_FPS, hot_keys, menu_color_medium, menu_color_light, textInfo, bigTextInfo, Settings
from Classes import Button

class CharactersMenu():

	def __init__(self, game, player, save):
		self.game = game
		self.player = player
		self.save = save
		self.init_buttons()

	def init_buttons(self):

		self.back_button = Button(-20, -20, load(path + "Images/Buttons/Back.png", 128), load(path + "Images/Buttons/Back 2.png", 128))
		self.character_button = Button(10, 120, load(path + "Images/Buttons/Character.png", 272, 64), load(path + "Images/Buttons/Character 2.png", 272, 64))
		self.pets_button = Button(10, 192, load(path + "Images/Buttons/Pets.png", 132, 64), load(path + "Images/Buttons/Pets 2.png", 132, 64))
		self.page_back_button = Button(361, Height - 138, load(path + "Images/Buttons/Back.png", 128), load(path + "Images/Buttons/Back 2.png", 128))
		self.page_next_button = Button(Width - 138, Height - 138, pygame.transform.flip(load(path + "Images/Buttons/Back.png", 128), True, False), pygame.transform.flip(load(path + "Images/Buttons/Back 2.png", 128), True, False))
		
	def characters(self):

		page = 1
		
		class Character():

			def __init__(self, name: str, info: str, images_list: list):
				self.name = name
				self.info = info
				self.images_list = images_list
				self.image_num = 0
		
		characters_list = [
			Character("Hiro", "123", [
				self.player.animations["Down"][0],
				self.player.animations["Down-left"][0],
				self.player.animations["Left"][0],
				self.player.animations["Up-left"][0],
				self.player.animations["Up"][0],
				self.player.animations["Up-right"][0],
				self.player.animations["Right"][0],
				self.player.animations["Down-right"][0],
			])
		]

		changed_character = characters_list[0]
		changed_character_num = 0

		while True:

			mouse_x, mouse_y = pygame.mouse.get_pos()
			dt = clock.tick(MAX_FPS) / 1000.0

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.save()
					sys.exit()
				if event.type == pygame.KEYUP:
					if event.key == hot_keys["Show keys"]:
						self.game.alt_pressed = not self.game.alt_pressed
					if event.key == hot_keys["Close"]:
						win_darken(win)
						self.game.does_lighten = False
						return self.game.main_menu.main_menu
					if event.key == pygame.K_1:
						changed_character_num = 0
					if event.key == pygame.K_2:
						changed_character_num = 1
					if event.key == pygame.K_LEFT and page > 1:
						page -= 1
					if event.key == pygame.K_RIGHT and page < 3:
						page += 1
			win.fill(menu_color_light)

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
			self.back_button.main()
			
			if self.back_button.is_released:
				win_darken(win)
				self.game.does_lighten = False
				return self.game.main_menu.main_menu
			win.blit(load(path + "Images/Buttons/Character 2.png", 278, 64), (10, 120))
			self.pets_button.main()
			if self.pets_button.is_released: return self.pets
			
			self.page_back_button.main()
			if self.page_back_button.is_released and page > 1: page -= 1
			self.page_next_button.main()
			
			if self.page_next_button.is_released and page < 3: page += 1
			win.blit(bigTextInfo.render(str(page), True, menu_color_medium), ((Width - 415) // 2 + 340, Height - 96))

			for index, character in enumerate(characters_list):
				
				character.image_num += 1
				if character.image_num == 40:
					character.image_num = 0
				if index // 3 == page - 1:
					win.blit(character.images_list[character.image_num // 5], (316, 216))
					
			if self.game.alt_pressed:
				
				draw_key("ESC", 44, 108)
				draw_key("<-", 425, Height - 168)
				draw_key("->", Width - 74, Height - 168)

			animate_click(dt, mouse_x, mouse_y)

			win_fill(alpha=100 - Settings["Display"][0])
			
			if not self.game.does_lighten:
				win_lighten(win)
				self.game.does_lighten = True

			pygame.display.update()
	
	def pets(self):

		while True:
			
			mouse_x, mouse_y = pygame.mouse.get_pos()
			dt = clock.tick(MAX_FPS) / 1000.0

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.save()
					sys.exit()
				if event.type == pygame.KEYUP:
					if event.key == hot_keys["Close"]:
						win_darken(win)
						self.game.does_lighten = False
						return self.game.main_menu.main_menu

			win.fill(menu_color_light)

			pygame.draw.rect(win, menu_color_medium, (-8, 100, 315, Height), 8)
			pygame.draw.rect(win, menu_color_medium, (315, 100, Width - 325, 100), 8)

			self.back_button.main()

			if self.back_button.is_released:
				win_darken(win)
				self.game.does_lighten = False
				return self.game.main_menu.main_menu

			self.character_button.main()
			if self.character_button.is_released: return self.characters

			win.blit(load(path + "Images/Buttons/Pets 2.png", 132, 64), (10, 192))

			animate_click(dt, mouse_x, mouse_y)

			win_fill(alpha=100 - Settings["Display"][0])
			
			if not self.game.does_lighten:
				win_lighten(win)
				self.game.does_lighten = True
			
			pygame.display.update()

