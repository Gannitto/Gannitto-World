import pygame
import sys
from Translator import translator, t
import Saver
from Assets import load, arrow_down, arrow_left, arrow_right, arrow_up, Inventory_slot, Changed_inventory_slot
from Functions import text, win_darken, win_lighten, languages, draw_key, animate_click, win_fill
from UI.UISystem import UISystem
from Globals import path, Width, Height, win, textInfo, bigTextInfo, menu_color_dark, menu_color_medium, menu_color_light, default_settings, default_hot_keys, clock, MAX_FPS
from Classes import Button

ui_system = UISystem()

class SettingsMenu():

	def __init__(self, game, save, music_channel, set_sound_volume, Settings, hot_keys):

		self.game = game
		self.game.does_lighten = False
		self.page = 1
		self.init_buttons()
		self.save = save 
		self.music_channel = music_channel
		self.set_sound_volume = set_sound_volume
		self.Settings = Settings
		self.hot_keys = hot_keys

	def open_settings(self):
		win_darken(win)
		self.game.does_lighten = False
		current_screen = self.help
		while current_screen is not None:
			current_screen = current_screen()

	def page_back(self):
		self.page = max(1, self.page - 1)
	def next_page(self):
		self.page += 1

	def init_buttons(self):

		self.back_button = Button(-20, -20, load(path + "Images/Buttons/Back.png", 128), load(path + "Images/Buttons/Back 2.png", 128))

		self.help_button = Button(10, 117, load(path + "Images/Buttons/Help.png", 132, 64), load(path + "Images/Buttons/Help 2.png", 132, 64))
		self.display_button = Button(10, 192, load(path + "Images/Buttons/Display.png", 222, 64), load(path + "Images/Buttons/Display 2.png", 222, 64))
		self.languages_button = Button(10, 267, load(path + "Images/Buttons/Languages.png", 272, 64), load(path + "Images/Buttons/Languages 2.png", 272, 64))
		self.user_button = Button(10, 342, load(path + "Images/Buttons/User.png", 132, 64), load(path + "Images/Buttons/User 2.png", 132, 64))
		self.sound_button = Button(10, 417, load(path + "Images/Buttons/Sound.png", 160, 64), load(path + "Images/Buttons/Sound 2.png", 160, 64))
		self.statistics_button = Button(10, 492, load(path + "Images/Buttons/Statistics.png", 300, 64), load(path + "Images/Buttons/Statistics 2.png", 300, 64))
		self.keys_button = Button(10, 567, load(path + "Images/Buttons/Keys.png", 132, 64), load(path + "Images/Buttons/Keys 2.png", 132, 64))
		self.game_button = Button(10, 642, load(path + "Images/Buttons/Game.png", 132, 64), load(path + "Images/Buttons/Game 2.png", 132, 64))
		
		self.english_button = Button(385, 198, load(path + "Images/Buttons/English.png", 220, 64), load(path + "Images/Buttons/English 2.png", 220, 64))
		self.russian_button = Button(385, 267, load(path + "Images/Buttons/Russian.png", 220, 64), load(path + "Images/Buttons/Russian 2.png", 220, 64))
		self.kazach_button = Button(385, 336, load(path + "Images/Buttons/Kazach.png", 188, 64), load(path + "Images/Buttons/Kazach 2.png", 188, 64))

		self.page_back_button = Button(361, Height - 138, load(path + "Images/Buttons/Back.png", 128), load(path + "Images/Buttons/Back 2.png", 128), action=self.page_back)
		self.page_next_button = Button(Width - 138, Height - 138, pygame.transform.flip(load(path + "Images/Buttons/Back.png", 128), True, False), pygame.transform.flip(load(path + "Images/Buttons/Back 2.png", 128), True, False), action=self.next_page)
	
	def show_reset_settings(self):
		
		if Width - 30 - bigTextInfo.size(t("Reset settings"))[0] < self.game.mouse_x < Width - 30 and 30 < self.game.mouse_y < 60:
			win.blit(bigTextInfo.render(t("Reset settings"), True, menu_color_dark), (Width - 30 - bigTextInfo.size(t("Reset settings"))[0], 30))
			if pygame.mouse.get_pressed()[0]:
				self.Settings = default_settings
		else:
			win.blit(bigTextInfo.render(t("Reset settings"), True, menu_color_medium), (Width - 30 - bigTextInfo.size(t("Reset settings"))[0], 30))

	def help(self):

		while True:

			self.game.mouse_x, self.game.mouse_y = pygame.mouse.get_pos()
			dt = clock.tick(MAX_FPS) / 1000.0

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.save()
					sys.exit()
				if event.type == pygame.KEYUP:
					if event.key == self.hot_keys["Show keys"]:
						self.game.alt_pressed = not self.game.alt_pressed

					if event.key == self.hot_keys["Close"]:
						Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
						win_darken(win)
						return

			win.fill(menu_color_light)
			pygame.draw.rect(win, menu_color_medium, (-8, 100, 373, Height), 8)
			pygame.draw.line(win, menu_color_medium, (307, 103), (Width, 103), 8)
			self.back_button.main()
			self.show_reset_settings()
			
			if self.back_button.is_released:
				Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
				win_darken(win)
				return
				
			self.page_back_button.main()
			self.page_next_button.main()
			self.page = min(self.page, 2)

			win.blit(bigTextInfo.render(str(self.page), True, menu_color_medium), ((Width - 415) // 2 + 391, Height - 96))
			win.blit(load(path + "Images/Buttons/Help 2.png", 132, 64), (10, 117))
			self.display_button.main()
			if self.display_button.is_released: return self.display
			self.languages_button.main()
			if self.languages_button.is_released: return self.display
			self.user_button.main()
			if self.user_button.is_released: return self.User
			self.sound_button.main()
			if self.sound_button.is_released: return self.Sound
			self.statistics_button.main()
			if self.statistics_button.is_released: return self.Statistics
			self.keys_button.main()
			if self.keys_button.is_released: return self.Keys
			self.game_button.main()
			if self.game_button.is_released: return self.Game

			if self.page == 1:
				
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
				
			elif self.page == 2:
				
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
			

			if self.game.alt_pressed:
				
				draw_key("ESC", 44, 108)
				draw_key("<-", 425, Height - 168)
				draw_key("->", Width - 74, Height - 168)

			animate_click(dt, self.game.mouse_x, self.game.mouse_y)

			win_fill(alpha=100 - self.Settings["Display"][0])	# Если в настройках установлена яркость ниже 100, то экран становится темнее
			
			if not self.game.does_lighten:
				win_lighten(win)
				self.game.does_lighten = True

			pygame.display.update()

	def display(self):

		bias = 0
		max_bias = -ui_system._set_positions(bias, "Display")
		max_bias = (max_bias + Height - 103) * max_bias > Height - 103

		while True:
			
			click = pygame.mouse.get_pressed()
			self.game.mouse_x, self.game.mouse_y = pygame.mouse.get_pos()
			release = False
			events = pygame.event.get()
			dt = clock.tick(MAX_FPS) / 1000.0
			
			for event in events:
				if event.type == pygame.QUIT:
					Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
					self.save()
					sys.exit()
				
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					release = True
				
				elif event.type == pygame.KEYUP:
					if event.key == self.hot_keys["Show keys"]:
						self.game.alt_pressed = not self.game.alt_pressed
					if event.key == self.hot_keys["Close"]:
						Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
						win_darken(win)
						return
				elif event.type == pygame.MOUSEWHEEL:
					bias = max((min(bias + event.y * self.Settings["Game"][2], 0)), max_bias)
					ui_system._set_positions(bias, "Display")
			
			# Очистка экрана
			win.fill(menu_color_light)
			
			# Обработка UI
			ui_system.handle_events(events, self.game.mouse_x, self.game.mouse_y, release, "Display")
			ui_system.draw("Display", bias, max_bias)

			self.back_button.main()
			self.show_reset_settings()
			
			if self.back_button.is_released:
				Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
				win_darken(win)
				return

			self.help_button.main()
			if self.help_button.is_released: return self.help
			win.blit(load(path + "Images/Buttons/Display 2.png", 222, 64), (10, 192))
			self.languages_button.main()
			if self.languages_button.is_released: return self.Languages
			self.user_button.main()
			if self.user_button.is_released: return self.User
			self.sound_button.main()
			if self.sound_button.is_released: return self.Sound
			self.statistics_button.main()
			if self.statistics_button.is_released: return self.Statistics
			self.keys_button.main()
			if self.keys_button.is_released: return self.Keys
			self.game_button.main()
			if self.game_button.is_released: return self.Game
			
			if self.game.alt_pressed:
				draw_key("ESC", 44, 108)

			if self.back_button.is_released:
				Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
				win_darken(win)
				return
				
			# Анимация и эффекты
			animate_click(dt, self.game.mouse_x, self.game.mouse_y)
			win_fill(alpha=100 - self.Settings["Display"][0])
			
			pygame.display.update()

	def Languages(self):

		while True:
			
			self.game.mouse_x, self.game.mouse_y = pygame.mouse.get_pos()
			dt = clock.tick(MAX_FPS) / 1000.0

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.save()
					sys.exit()
				if event.type == pygame.KEYUP:
					if event.key == self.hot_keys["Show keys"]:
						self.game.alt_pressed = not self.game.alt_pressed
					if event.key == self.hot_keys["Close"]:
						Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
						win_darken(win)
						return

					if event.key == pygame.K_1:
						self.Settings["Languages"][0] = "English"
						translator.load_language("English")
						for element_list in ui_system.elements.values():
							for element in element_list:
								element.label_width = element.font.size(t(element.label))[0] + 10
								element.rect = pygame.Rect(element.x + element.label_width, element.y, element.width, element.height)

					if event.key == pygame.K_2:
						self.Settings["Languages"][0] = "Russian"
						translator.load_language("Russian")
						for element_list in ui_system.elements.values():
							for element in element_list:
								element.label_width = element.font.size(t(element.label))[0] + 10
								element.rect = pygame.Rect(element.x + element.label_width, element.y, element.width, element.height)

					if event.key == pygame.K_3:
						self.Settings["Languages"][0] = "Kazach"
						translator.load_language("Kazach")
						for element_list in ui_system.elements.values():
							for element in element_list:
								element.label_width = element.font.size(t(element.label))[0] + 10
								element.rect = pygame.Rect(element.x + element.label_width, element.y, element.width, element.height)

			win.fill(menu_color_light)
			pygame.draw.rect(win, menu_color_medium, (-8, 100, 373, Height), 8)
			pygame.draw.line(win, menu_color_medium, (307, 103), (Width, 103), 8)
			self.back_button.main()
			if self.back_button.is_released:
				Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
				win_darken(win)
				return
			self.show_reset_settings()

			win.blit(bigTextInfo.render(t("You can choose one of these"), True, menu_color_medium), (385, 123))
			win.blit(bigTextInfo.render(t("languages:"), True, menu_color_medium), (385, 153))

			self.english_button.main()
			if self.english_button.is_released:
				self.Settings["Languages"][0] = "English"
				translator.load_language("English")
				for element_list in ui_system.elements.values():
					for element in element_list:
						element.label_width = element.font.size(t(element.label))[0] + 10
						element.rect = pygame.Rect(element.x + element.label_width, element.y, element.width, element.height)

			self.russian_button.main()
			if self.russian_button.is_released:
				self.Settings["Languages"][0] = "Russian"
				translator.load_language("Russian")
				for element_list in ui_system.elements.values():
					for element in element_list:
						element.label_width = element.font.size(t(element.label))[0] + 10
						element.rect = pygame.Rect(element.x + element.label_width, element.y, element.width, element.height)

			self.kazach_button.main()
			if self.kazach_button.is_released:
				self.Settings["Languages"][0] = "Kazach"
				translator.load_language("Kazach")
				for element_list in ui_system.elements.values():
					for element in element_list:
						element.label_width = element.font.size(t(element.label))[0] + 10
						element.rect = pygame.Rect(element.x + element.label_width, element.y, element.width, element.height)

			self.help_button.main()
			if self.help_button.is_released: return self.help
			self.display_button.main()
			if self.display_button.is_released: return self.display
			win.blit(load(path + "Images/Buttons/Languages 2.png", 272, 64), (10, 267))
			self.user_button.main()
			if self.user_button.is_released: return self.User
			self.sound_button.main()
			if self.sound_button.is_released: return self.Sound
			self.statistics_button.main()
			if self.statistics_button.is_released: return self.Statistics
			self.keys_button.main()
			if self.keys_button.is_released: return self.Keys
			self.game_button.main()
			if self.game_button.is_released: return self.Game
			
			if self.game.alt_pressed:
				
				draw_key("ESC", 44, 108)

			animate_click(dt, self.game.mouse_x, self.game.mouse_y)
			win_fill(alpha=100 - self.Settings["Display"][0])	# Если в настройках установлена яркость ниже 100, то экран становится темнее

			if not self.game.does_lighten:
				win_lighten(win)
				self.game.does_lighten = True

			pygame.display.update()

	def User(self):

		bias = 0
		max_bias = -ui_system._set_positions(bias, "User")
		max_bias = (max_bias + Height - 103) * max_bias > Height - 103

		while True:
			
			click = pygame.mouse.get_pressed()
			self.game.mouse_x, self.game.mouse_y = pygame.mouse.get_pos()
			release = False
			dt = clock.tick(MAX_FPS) / 1000.0
			
			events = pygame.event.get()
			
			for event in events:
				if event.type == pygame.QUIT:
					Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
					self.save()
					sys.exit()
				
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					release = True
				
				elif event.type == pygame.KEYUP:
					if event.key == self.hot_keys["Show keys"]:
						self.game.alt_pressed = not self.game.alt_pressed
					if event.key == self.hot_keys["Close"]:
						Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
						win_darken(win)
						return
				elif event.type == pygame.MOUSEWHEEL:
					bias = max((min(bias + event.y * self.Settings["Game"][2], 0)), max_bias)
					ui_system._set_positions(bias, "User")
			
			# Очистка экрана
			win.fill(menu_color_light)
			
			# Обработка UI
			ui_system.handle_events(events, self.game.mouse_x, self.game.mouse_y, release, "User")
			ui_system.draw("User", bias, max_bias)
			
			self.back_button.main()
			self.show_reset_settings()
			
			if self.back_button.is_released:
				Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
				win_darken(win)
				return

			self.help_button.main()
			if self.help_button.is_released: return self.help
			self.display_button.main()
			if self.display_button.is_released: return self.display
			self.languages_button.main()
			if self.languages_button.is_released: return self.Languages
			win.blit(load(path + "Images/Buttons/User 2.png", 132, 64), (10, 342))
			self.sound_button.main()
			if self.sound_button.is_released: return self.Sound
			self.statistics_button.main()
			if self.statistics_button.is_released: return self.Statistics
			self.keys_button.main()
			if self.keys_button.is_released: return self.Keys
			self.game_button.main()
			if self.game_button.is_released: return self.Game

			if self.game.alt_pressed:
				draw_key("ESC", 44, 108)

			if self.back_button.is_released:
				Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
				win_darken(win)
				return
				
			# Анимация и эффекты
			animate_click(dt, self.game.mouse_x, self.game.mouse_y)
			win_fill(alpha=100 - self.Settings["Display"][0])
			
			pygame.display.update()

	def Sound(self):

		bias = 0
		max_bias = -ui_system._set_positions(bias, "Sound")
		max_bias = (max_bias + Height - 103) * max_bias > Height - 103

		while True:
			
			click = pygame.mouse.get_pressed()
			self.game.mouse_x, self.game.mouse_y = pygame.mouse.get_pos()
			release = False
			dt = clock.tick(MAX_FPS) / 1000.0
			
			events = pygame.event.get()
			
			for event in events:
				if event.type == pygame.QUIT:
					Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
					self.save()
					sys.exit()
				
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					release = True
				
				elif event.type == pygame.KEYUP:
					if event.key == self.hot_keys["Show keys"]:
						self.game.alt_pressed = not self.game.alt_pressed
					if event.key == self.hot_keys["Close"]:
						Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
						win_darken(win)
						return
					if event.key == pygame.K_RETURN:

						self.music_channel.set_volume(self.Settings["Sound"][0], self.Settings["Sound"][0] / 100)
						self.set_sound_volume(self.Settings["Sound"][1] / 100)

				elif event.type == pygame.MOUSEWHEEL:
					bias = max((min(bias + event.y * self.Settings["Game"][2], 0)), max_bias)
					ui_system._set_positions(bias, "Sound")
			
			# Очистка экрана
			win.fill(menu_color_light)
			
			# Обработка UI
			ui_system.handle_events(events, self.game.mouse_x, self.game.mouse_y, release, "Sound")
			ui_system.draw("Sound", bias, max_bias)
			
			self.back_button.main()
			self.show_reset_settings()
			
			if self.back_button.is_released:
				Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
				win_darken(win)
				return

			self.help_button.main()
			if self.help_button.is_released: return self.help
			self.display_button.main()
			if self.display_button.is_released: return self.display
			self.languages_button.main()
			if self.languages_button.is_released: return self.Languages
			self.user_button.main()
			if self.user_button.is_released: return self.User
			win.blit(load(path + "Images/Buttons/Sound 2.png", 160, 64), (10, 417))
			self.statistics_button.main()
			if self.statistics_button.is_released: return self.Statistics
			self.keys_button.main()
			if self.keys_button.is_released: return self.Keys
			self.game_button.main()
			if self.game_button.is_released: return self.Game

			if self.game.alt_pressed:
				draw_key("ESC", 44, 108)

			if self.back_button.is_released:
				Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
				win_darken(win)
				return
				
			# Анимация и эффекты
			animate_click(dt, self.game.mouse_x, self.game.mouse_y)
			win_fill(alpha=100 - self.Settings["Display"][0])
			
			pygame.display.update()

	def Statistics(self):

		bias = 0
		max_bias = -ui_system._set_positions(bias, "Statistics")
		max_bias = (max_bias + Height - 103) * max_bias > Height - 103

		while True:
			
			click = pygame.mouse.get_pressed()
			self.game.mouse_x, self.game.mouse_y = pygame.mouse.get_pos()
			release = False
			dt = clock.tick(MAX_FPS) / 1000.0
			
			events = pygame.event.get()
			
			for event in events:
				if event.type == pygame.QUIT:
					Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
					self.save()
					sys.exit()
				
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					release = True
				
				elif event.type == pygame.KEYUP:
					if event.key == self.hot_keys["Show keys"]:
						self.game.alt_pressed = not self.game.alt_pressed
					if event.key == self.hot_keys["Close"]:
						Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
						win_darken(win)
						return
				elif event.type == pygame.MOUSEWHEEL:
					bias = max((min(bias + event.y * self.Settings["Game"][2], 0)), max_bias)
					ui_system._set_positions(bias, "Statistics")
			
			# Очистка экрана
			win.fill(menu_color_light)
			
			# Обработка UI
			ui_system.draw("Statistics", bias, max_bias)
			
			self.back_button.main()
			self.show_reset_settings()
			
			if self.back_button.is_released:
				Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
				win_darken(win)
				return

			self.help_button.main()
			if self.help_button.is_released: return self.help
			self.display_button.main()
			if self.display_button.is_released: return self.display
			self.languages_button.main()
			if self.languages_button.is_released: return self.Languages
			self.user_button.main()
			if self.user_button.is_released: return self.User
			self.sound_button.main()
			if self.sound_button.is_released: return self.Sound
			win.blit(load(path + "Images/Buttons/Statistics 2.png", 300, 64), (10, 492))
			self.keys_button.main()
			if self.keys_button.is_released: return self.Keys
			self.game_button.main()
			if self.game_button.is_released: return self.Game

			if self.game.alt_pressed:
				draw_key("ESC", 44, 108)

			if self.back_button.is_released:
				Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
				win_darken(win)
				return
				
			# Анимация и эффекты
			animate_click(dt, self.game.mouse_x, self.game.mouse_y)
			win_fill(alpha=100 - self.Settings["Display"][0])
			
			pygame.display.update()

	def Keys(self):

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
		check_keys = lambda key: key_values_combined[key] in self.hot_keys.values() # Эта lambda-функция выясняет, является ли данная клавиша одной из горячих клавиш игры
		check_blocked_keys = lambda key: key in ("prt sc", "super", "off")

		while True:

			changed_key = ""
			click = pygame.mouse.get_pressed()
			self.game.mouse_x, self.game.mouse_y = pygame.mouse.get_pos()
			release = False
			dt = clock.tick(MAX_FPS) / 1000.0
			
			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					Saver.save_objects(path + "Saves/Settings/Hot keys.save", self.hot_keys)
					self.save()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					release = True
				if event.type == pygame.KEYUP:
					if event.key == self.hot_keys["Show keys"]:
						self.game.alt_pressed = not self.game.alt_pressed
					if event.key == self.hot_keys["Close"]:
						if looked_key is not None:
							looked_key = None
						else:
							Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
							Saver.save_objects(path + "Saves/Settings/Hot keys.save", self.hot_keys)
							win_darken(win)
							return

			self.back_button.main()
			if self.back_button.is_released:
				if looked_key is not None:
					looked_key = None
				else:
					Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
					Saver.save_objects(path + "Saves/Settings/Hot keys.save", self.hot_keys)
					win_darken(win)
					return
				
			win.fill(menu_color_light)
			pygame.draw.rect(win, menu_color_medium, (-8, 100, 373, Height), 8)
			pygame.draw.line(win, menu_color_medium, (307, 103), (Width, 103), 8)
			
			self.back_button.main()
			self.show_reset_settings()
			
			if self.back_button.is_released:
				Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
				win_darken(win)
				return

			self.help_button.main()
			if self.help_button.is_released: return self.help
			self.display_button.main()
			if self.display_button.is_released: return self.display
			self.languages_button.main()
			if self.languages_button.is_released: return self.Languages
			self.user_button.main()
			if self.user_button.is_released: return self.User
			self.sound_button.main()
			if self.sound_button.is_released: return self.Sound
			self.statistics_button.main()
			if self.statistics_button.is_released: return self.Statistics
			self.keys_button.main()
			win.blit(load(path + "Images/Buttons/Keys 2.png", 132, 64), (10, 567))
			self.game_button.main()
			if self.game_button.is_released: return self.Game

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
					if key_values_combined[key] == self.hot_keys["Close"]: close_key = key
					if key_rect.collidepoint((self.game.mouse_x, self.game.mouse_y)): changed_key = key
					
					pygame.draw.rect(win, key_color, (X, Y, key_size, 40), 6 if changed_key == key else 3)
					win.blit(littleTextInfo.render(key, True, key_color), (X + 5, Y + 7))
					X += key_size + 10
				X = 385
				Y += 50
			
			text(t("Hotkeys are highlighted in dark blue"), 385, 440, menu_color_dark)
			text(t("Locked keys are highlighted in white"), 385, 470, (255, 255, 255))
			text(t("To change the hot key, click on it"), 385, 500, menu_color_medium)

			if Width - 30 - textInfo.size(t("Reset key settings"))[0] < self.game.mouse_x < Width - 30 and 420 < self.game.mouse_y < 450:
				win.blit(textInfo.render(t("Reset key settings"), True, menu_color_dark), (Width - 30 - textInfo.size(t("Reset key settings"))[0], 420))
				if click[0]:
					self.hot_keys = default_hot_keys
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
				for key, val in self.hot_keys.items():
					if val == changed_key_value:
						text("\n" + key, 400, 575, menu_color_dark)
						break

			if changed_key != "" and release:
				
				if looked_key is None:
					if changed_key != "" and check_keys(changed_key) and not check_blocked_keys(key):
						looked_key = changed_key
				elif changed_key != looked_key and looked_key is not None and not check_blocked_keys(changed_key) and not check_keys(changed_key):
					for key, val in self.hot_keys.items():
						if val == key_values_combined[looked_key]:
							self.hot_keys[key] = changed_key_value
							break
					looked_key = None

			if self.game.alt_pressed:
				draw_key("ESC", 44, 108)

			animate_click(dt, self.game.mouse_x, self.game.mouse_y)

			win_fill(alpha=100 - self.Settings["Display"][0])	# Если в настройках установлена яркость ниже 100, то экран становится темнее
			
			if not self.game.does_lighten:
				win_lighten(win)
				self.game.does_lighten = True

			pygame.display.update()

	def Game(self):

		bias = 0
		max_bias = -ui_system._set_positions(bias, "Game")
		max_bias = (max_bias + Height - 103) * max_bias > Height - 103

		while True:
			
			click = pygame.mouse.get_pressed()
			self.game.mouse_x, self.game.mouse_y = pygame.mouse.get_pos()
			release = False
			dt = clock.tick(MAX_FPS) / 1000.0
			
			events = pygame.event.get()
			
			for event in events:
				if event.type == pygame.QUIT:
					Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
					self.save()
					sys.exit()
				
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					release = True
				
				elif event.type == pygame.KEYUP:
					if event.key == self.hot_keys["Show keys"]:
						self.game.alt_pressed = not self.game.alt_pressed
					if event.key == self.hot_keys["Close"]:
						Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
						win_darken(win)
						return
				elif event.type == pygame.MOUSEWHEEL:
					bias = max((min(bias + event.y * self.Settings["Game"][2], 0)), max_bias)
					ui_system._set_positions(bias, "Game")
			
			# Очистка экрана
			win.fill(menu_color_light)
			
			# Обработка UI
			ui_system.handle_events(events, self.game.mouse_x, self.game.mouse_y, release, "Game")
			ui_system.draw("Game", bias, max_bias)
			
			self.back_button.main()
			self.show_reset_settings()
			
			if self.back_button.is_released:
				Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
				win_darken(win)
				return

			self.help_button.main()
			if self.help_button.is_released: return self.help
			self.display_button.main()
			if self.display_button.is_released: return self.display
			self.languages_button.main()
			if self.languages_button.is_released: return self.Languages
			self.user_button.main()
			if self.user_button.is_released: return self.User
			self.sound_button.main()
			if self.sound_button.is_released: return self.Sound
			self.statistics_button.main()
			if self.statistics_button.is_released: return self.Statistics
			self.keys_button.main()
			if self.keys_button.is_released: return self.Keys
			win.blit(load(path + "Images/Buttons/Game 2.png", 132, 64), (10, 642))

			if self.game.alt_pressed:
				draw_key("ESC", 44, 108)

			if self.back_button.is_released:
				Saver.save_objects(path + "Saves/Settings/Settings.save", self.Settings)
				win_darken(win)
				return
				
			# Анимация и эффекты
			animate_click(dt, self.game.mouse_x, self.game.mouse_y)
			win_fill(alpha=100 - self.Settings["Display"][0])
			
			pygame.display.update()
	
