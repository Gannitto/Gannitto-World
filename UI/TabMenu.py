import pygame
import math
import sys
from Translator import t
from Assets import Craft_list_slot1, Craft_list_slot2, Game_menu_slot1, Game_menu_slot2, Menu_slot1, Menu_slot2, Multiplayer_slot1, Multiplayer_slot2, Close_slot1, Close_slot2, Reference_slot1, Reference_slot2
from Functions import text, win_darken
from Globals import win, Width, Height, hot_keys, FPS, MAX_FPS, clock, Settings

class TabMenu:

	def __init__(self, game, save):
		self.game = game
		self.save = save

	def tab_menu(self):

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
					self.save()
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
				if self.game.special_slot_animations["Craft list slot"][0]:
					if self.game.special_slot_animations["Craft list slot"][1] < FPS / 6:
						self.game.special_slot_animations["Craft list slot"][1] += 1
						self.game.special_slot_animations["Craft list slot"][2] -= 3
						self.game.special_slot_animations["Craft list slot"][2] = abs(self.game.special_slot_animations["Craft list slot"][2])
				else:
					self.game.special_slot_animations["Craft list slot"] = [True, 0, 10]
				
				if release:
					self.game.inventory_open = True
					self.game.craft_list_open = True
					b = True
					display_speed = 7
				
			elif self.game.special_slot_animations["Craft list slot"][0]:
				self.game.special_slot_animations["Craft list slot"][0] = False
				self.game.special_slot_animations["Craft list slot"][1] = 0
			elif self.game.special_slot_animations["Craft list slot"][1] < FPS / 4:
				self.game.special_slot_animations["Craft list slot"][1] += 1	 
			if self.game.special_slot_animations["Craft list slot"][0] and Settings["Display"][5]:
				try:win.blit(pygame.transform.scale(Craft_list_slot2, (64 - self.game.special_slot_animations["Craft list slot"][2], 64 - self.game.special_slot_animations["Craft list slot"][2])), (Width // 2 + radius - 32, Height // 2 - 32))
				except: win.blit(Craft_list_slot2, (Width // 2 + radius - 32, Height // 2 - 32))
			
			else:
				win.blit(Craft_list_slot1, (Width // 2 + radius - 32, Height // 2 - 32))

			text(t("Craft list"), Width // 2 + radius, Height // 2 + 40, alignment=True)
			


			if Width // 2 + math.cos((2 * math.pi) / 6) * radius - 32 < mouse_x < Width // 2 + math.cos((2 * math.pi) / 6) * radius + 32 and Height // 2 + math.sin((2 * math.pi) / 6) * radius - 32 < mouse_y < Height // 2 + math.sin((2 * math.pi) / 6) * radius + 32:
				if self.game.special_slot_animations["Game menu slot"][0]:
					if self.game.special_slot_animations["Game menu slot"][1] < FPS / 6:
						self.game.special_slot_animations["Game menu slot"][1] += 1
						self.game.special_slot_animations["Game menu slot"][2] -= 3
						self.game.special_slot_animations["Game menu slot"][2] = abs(self.game.special_slot_animations["Game menu slot"][2])
				else:
					self.game.special_slot_animations["Game menu slot"] = [True, 0, 10]
				
				if click[0]:
					self.save(False)
					if self.game.multiplayer:
						self.game.net.disconnect()
					win_darken(win)
					self.game.does_lighten = False
					return self.game.main_menu.main_menu
				
			elif self.game.special_slot_animations["Game menu slot"][0]:
				self.game.special_slot_animations["Game menu slot"][0] = False
				self.game.special_slot_animations["Game menu slot"][1] = 0
			elif self.game.special_slot_animations["Game menu slot"][1] < FPS / 4:
				self.game.special_slot_animations["Game menu slot"][1] += 1

			if self.game.special_slot_animations["Game menu slot"][0] and Settings["Display"][5]:
				try:win.blit(pygame.transform.scale(Game_menu_slot2, (64 - self.game.special_slot_animations["Game menu slot"][2], 64 - self.game.special_slot_animations["Game menu slot"][2])), (Width // 2 + math.cos((2 * math.pi) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi) / 6) * radius - 32))
				except: win.blit(Game_menu_slot2, (Width // 2 + math.cos((2 * math.pi) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi) / 6) * radius - 32))
			
			else:
				win.blit(Game_menu_slot1, (Width // 2 + math.cos((2 * math.pi) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi) / 6) * radius - 32))

			text(t("Game menu"), Width // 2 + math.cos((2 * math.pi) / 6) * radius, Height // 2 + math.sin((2 * math.pi) / 6) * radius + 40, alignment=True)
			

			
			if Width // 2 + math.cos((2 * math.pi * 2) / 6) * radius - 32 < mouse_x < Width // 2 + math.cos((2 * math.pi * 2) / 6) * radius + 32 and Height // 2 + math.sin((2 * math.pi * 2) / 6) * radius - 32 < mouse_y < Height // 2 + math.sin((2 * math.pi * 2) / 6) * radius + 32:
				if self.game.special_slot_animations["Menu slot"][0]:
					if self.game.special_slot_animations["Menu slot"][1] < FPS / 6:
						self.game.special_slot_animations["Menu slot"][1] += 1
						self.game.special_slot_animations["Menu slot"][2] -= 3
						self.game.special_slot_animations["Menu slot"][2] = abs(self.game.special_slot_animations["Menu slot"][2])
				else:
					self.game.special_slot_animations["Menu slot"] = [True, 0, 10]
				
				if click[0]:
					self.game.multiplayer_menu_open = True
					b = True
					display_speed = 7

			elif self.game.special_slot_animations["Menu slot"][0]:
				self.game.special_slot_animations["Menu slot"][0] = False
				self.game.special_slot_animations["Menu slot"][1] = 0
			elif self.game.special_slot_animations["Menu slot"][1] < FPS / 4:
				self.game.special_slot_animations["Menu slot"][1] += 1   

			if self.game.special_slot_animations["Menu slot"][0] and Settings["Display"][5]:
				try:win.blit(pygame.transform.scale(Menu_slot2, (64 - self.game.special_slot_animations["Menu slot"][2], 64 - self.game.special_slot_animations["Menu slot"][2])), (Width // 2 + math.cos((2 * math.pi * 2) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi) / 6) * radius - 32))
				except: win.blit(Menu_slot2, (Width // 2 + math.cos((2 * math.pi * 2) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 2) / 6) * radius - 32))
			
			else:
				win.blit(Menu_slot1, (Width // 2 + math.cos((2 * math.pi * 2) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 2) / 6) * radius - 32))

			text(t("Extra info menu"), Width // 2 + math.cos((2 * math.pi * 2) / 6) * radius, Height // 2 + math.sin((2 * math.pi * 2) / 6) * radius + 40, alignment=True)
			


			if Width // 2 + math.cos((2 * math.pi * 3) / 6) * radius - 32 < mouse_x < Width // 2 + math.cos((2 * math.pi * 3) / 6) * radius + 32 and Height // 2 + math.sin((2 * math.pi * 3) / 6) * radius - 32 < mouse_y < Height // 2 + math.sin((2 * math.pi * 3) / 6) * radius + 32:
				if self.game.special_slot_animations["Multiplayer slot"][0]:
					if self.game.special_slot_animations["Multiplayer slot"][1] < FPS / 6:
						self.game.special_slot_animations["Multiplayer slot"][1] += 1
						self.game.special_slot_animations["Multiplayer slot"][2] -= 3
						self.game.special_slot_animations["Multiplayer slot"][2] = abs(self.game.special_slot_animations["Multiplayer slot"][2])
				else:
					self.game.special_slot_animations["Multiplayer slot"] = [True, 0, 10]
				
				if click[0]:
					self.game.multiplayer_menu_open = True
					b = True
					display_speed = 7

			elif self.game.special_slot_animations["Multiplayer slot"][0]:
				self.game.special_slot_animations["Multiplayer slot"][0] = False
				self.game.special_slot_animations["Multiplayer slot"][1] = 0
			elif self.game.special_slot_animations["Multiplayer slot"][1] < FPS / 4:
				self.game.special_slot_animations["Multiplayer slot"][1] += 1   

			if self.game.special_slot_animations["Multiplayer slot"][0] and Settings["Display"][5]:
				try:win.blit(pygame.transform.scale(Multiplayer_slot2, (64 - self.game.special_slot_animations["Multiplayer slot"][2], 64 - self.game.special_slot_animations["Multiplayer slot"][2])), (Width // 2 + math.cos((2 * math.pi * 3) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 3) / 6) * radius - 32))
				except: win.blit(Multiplayer_slot2, (Width // 2 + math.cos((2 * math.pi * 3) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 3) / 6) * radius - 32))
			
			else:
				win.blit(Multiplayer_slot1, (Width // 2 + math.cos((2 * math.pi * 3) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 3) / 6) * radius - 32))

			text(t("Multiplayer menu"), Width // 2 + math.cos((2 * math.pi * 3) / 6) * radius, Height // 2 + math.sin((2 * math.pi * 3) / 6) * radius + 40, alignment=True)
			

			
			if Width // 2 + math.cos((2 * math.pi * 4) / 6) * radius - 32 < mouse_x < Width // 2 + math.cos((2 * math.pi * 4) / 6) * radius + 32 and Height // 2 + math.sin((2 * math.pi * 4) / 6) * radius - 32 < mouse_y < Height // 2 + math.sin((2 * math.pi * 4) / 6) * radius + 32:
				if self.game.special_slot_animations["Close slot"][0]:
					if self.game.special_slot_animations["Close slot"][1] < FPS / 6:
						self.game.special_slot_animations["Close slot"][1] += 1
						self.game.special_slot_animations["Close slot"][2] -= 3
						self.game.special_slot_animations["Close slot"][2] = abs(self.game.special_slot_animations["Close slot"][2])
				else:
					self.game.special_slot_animations["Close slot"] = [True, 0, 10]
				
				if click[0]:
					b = True
					display_speed = 7

			elif self.game.special_slot_animations["Close slot"][0]:
				self.game.special_slot_animations["Close slot"][0] = False
				self.game.special_slot_animations["Close slot"][1] = 0
			elif self.game.special_slot_animations["Close slot"][1] < FPS / 4:
				self.game.special_slot_animations["Close slot"][1] += 1	

			if self.game.special_slot_animations["Close slot"][0] and Settings["Display"][5]:
				try:win.blit(pygame.transform.scale(Close_slot2, (64 - self.game.special_slot_animations["Close slot"][2], 64 - self.game.special_slot_animations["Close slot"][2])), (Width // 2 + math.cos((2 * math.pi * 4) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 4) / 6) * radius - 32))
				except: win.blit(Close_slot2, (Width // 2 + math.cos((2 * math.pi * 4) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 4) / 6) * radius - 32))
			
			else:
				win.blit(Close_slot1, (Width // 2 + math.cos((2 * math.pi * 4) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 4) / 6) * radius - 32))

			text(t("Close"), Width // 2 + math.cos((2 * math.pi * 4) / 6) * radius, Height // 2 + math.sin((2 * math.pi * 4) / 6) * radius + 40, alignment=True)



			if Width // 2 + math.cos((2 * math.pi * 5) / 6) * radius - 32 < mouse_x < Width // 2 + math.cos((2 * math.pi * 5) / 6) * radius + 32 and Height // 2 + math.sin((2 * math.pi * 5) / 6) * radius - 32 < mouse_y < Height // 2 + math.sin((2 * math.pi * 5) / 6) * radius + 32:
				if self.game.special_slot_animations["Reference slot"][0]:
					if self.game.special_slot_animations["Reference slot"][1] < FPS / 6:
						self.game.special_slot_animations["Reference slot"][1] += 1
						self.game.special_slot_animations["Reference slot"][2] -= 3
						self.game.special_slot_animations["Reference slot"][2] = abs(self.game.special_slot_animations["Reference slot"][2])
				else:
					self.game.special_slot_animations["Reference slot"] = [True, 0, 10]
				
				if click[0]:
					self.save(False)
					return self.game.settings_menu.help

			elif self.game.special_slot_animations["Reference slot"][0]:
				self.game.special_slot_animations["Reference slot"][0] = False
				self.game.special_slot_animations["Reference slot"][1] = 0
			elif self.game.special_slot_animations["Reference slot"][1] < FPS / 4:
				self.game.special_slot_animations["Reference slot"][1] += 1	

			if self.game.special_slot_animations["Reference slot"][0] and Settings["Display"][5]:
				try:win.blit(pygame.transform.scale(Reference_slot2, (64 - self.game.special_slot_animations["Reference slot"][2], 64 - self.game.special_slot_animations["Reference slot"][2])), (Width // 2 + math.cos((2 * math.pi * 5) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 4) / 6) * radius - 32))
				except: win.blit(Reference_slot2, (Width // 2 + math.cos((2 * math.pi * 5) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 5) / 6) * radius - 32))
			
			else:
				win.blit(Reference_slot1, (Width // 2 + math.cos((2 * math.pi * 5) / 6) * radius - 32, Height // 2 + math.sin((2 * math.pi * 5) / 6) * radius - 32))

			text(t("Reference"), Width // 2 + math.cos((2 * math.pi * 5) / 6) * radius, Height // 2 + math.sin((2 * math.pi * 5) / 6) * radius + 40, alignment=True)

			pygame.display.update()
			clock.tick(MAX_FPS)
