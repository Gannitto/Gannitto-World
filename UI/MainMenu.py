import pygame
import sys
from Assets import load, Screensaver2
from Translator import t
from Functions import win_lighten, win_darken, win_fill, get_build_number, text, animate_click
from Globals import Width, Height, win, path, clock, menu_color_dark, menu_color_light, menu_color_medium
from Config import Settings, hot_keys
from Classes import Button

class MainMenu():

	def __init__(self, game, save):
		self.game = game
		self.save = save
		self.init_buttons()

	def init_buttons(self):
		self.play_button = Button(Width / 2, Height / 2 - 150, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Play.png"), (264, 128)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Play 2.png"), (264, 128)), alignment=True, info="Подсказка: вы можете нажать enter, чтобы сразу начать игру.")
		self.settings_button = Button(Width / 2, Height / 2, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Settings.png"), (488, 128)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Settings 2.png"), (488, 128)), alignment=True)
		self.change_a_character_button = Button(Width / 2, Height / 2 + 150, pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Change a character.png"), (960, 128)), pygame.transform.scale(pygame.image.load(path + "Images/Buttons/Change a character 2.png"), (960, 128)), alignment=True)

	def main_menu(self):
		version = f"Version Alpha 1.5 (Build {str(get_build_number())})"
		more_menu_open = False

		while True:
			
			mouse_x, mouse_y = pygame.mouse.get_pos()
			click = pygame.mouse.get_pressed()
			release = False
			dt = clock.tick(self.game.max_fps) / 1000.0

			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					self.save()
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					release = True
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_RETURN:
						win_darken(win)
						self.game.does_lighten = False
						return self.game.worlds_menu.worlds_menu
					if event.key == hot_keys["Close"]:
						more_menu_open = False
			win.blit(Screensaver2, (0, 0))

			if not more_menu_open:
				self.play_button.main()
				if self.play_button.is_released:
					win_darken(win)
					self.game.does_lighten = False
					return self.game.worlds_menu.worlds_menu
				self.settings_button.main()
				if self.settings_button.is_released:
					win_darken(win)
					self.game.does_lighten = False
					return self.game.settings_menu.help
				self.change_a_character_button.main()
				if self.change_a_character_button.is_released:
					win_darken(win)
					self.game.does_lighten = False
					return self.game.characters_menu.characters
			
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

			win_fill(alpha=100 - Settings["Display"]["Brightness"])   # Если в настройках установлена яркость ниже 100, то экран становится темнее

			if not self.game.does_lighten:
				win_lighten(win)
				self.game.does_lighten = True

			pygame.display.update()
