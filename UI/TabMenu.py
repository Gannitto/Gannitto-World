import pygame
import math
import sys
import time
from Translator import t
from Assets import (Craft_list_slot1, Craft_list_slot2, Game_menu_slot1, Game_menu_slot2, 
					Menu_slot1, Menu_slot2, Multiplayer_slot1, Multiplayer_slot2, 
					Close_slot1, Close_slot2, Reference_slot1, Reference_slot2)
from Functions import text, win_darken
from Globals import win, Width, Height, hot_keys, MAX_FPS, clock, Settings

class TabMenu:
	def __init__(self, game, save, music_channel):
		self.game = game
		self.save = save
		self.music_channel = music_channel
		
		# Группируем данные кнопок: (Имя в анимациях, Текст, Итоговый угол/индекс, Иконка1, Иконка2, Действие)
		# Углы распределяем равномерно от 0 до 5 (шаг 60 градусов)
		self.buttons_config = [
			("Craft list slot", "Craft list", 0, Craft_list_slot1, Craft_list_slot2, self._action_craft),
			("Game menu slot", "Game menu", 1, Game_menu_slot1, Game_menu_slot2, self._action_game_menu),
			("Menu slot", "Extra info menu", 2, Menu_slot1, Menu_slot2, self._action_menu), # судя по коду, открывает multiplayer
			("Multiplayer slot", "Multiplayer menu", 3, Multiplayer_slot1, Multiplayer_slot2, self._action_multiplayer),
			("Close slot", "Close", 4, Close_slot1, Close_slot2, self._action_close),
			("Reference slot", "Reference", 5, Reference_slot1, Reference_slot2, self._action_reference)
		]

	# Блок функций-действий для кнопок
	def _action_craft(self):
		self.game.inventory_open = True
		self.game.craft_list_open = True
		return "close_menu"

	def _action_game_menu(self):
		self.save(False)
		if self.game.multiplayer:
			self.game.net.disconnect()
		win_darken(win)
		self.game.does_lighten = False
		return self.game.main_menu.main_menu

	def _action_menu(self):
		self.game.menu_open = not self.game.menu_open
		return "close_menu"

	def _action_multiplayer(self):
		self.game.multiplayer_menu_open = True
		return "close_menu"

	def _action_close(self):
		return "close_menu"

	def _action_reference(self):
		self.music_channel.stop()
		self.game.clear_world_data()
		self.game.statistics[1] += (time.time() - self.game.start_time) / 3600
		self.save()
		self.game.does_lighten = False
		return self.game.settings_menu.help

	def tab_menu(self):
		radius = 0		   # Расстояние от центра экрана
		display_speed = 7  # Скорость изменения радиуса
		is_opening = True  # Флаг фазы открытия
		is_closing = False # Флаг фазы закрытия
		win_copy = win.copy()

		while True:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			click = pygame.mouse.get_pressed()
			release = False
			dt = clock.tick(MAX_FPS) / 1000.0

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.save()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONUP:
					release = True
				if event.type == pygame.KEYUP and event.key == hot_keys["Close"]:
					is_closing = True
					display_speed = 7

			# Логика анимации раскрытия / закрытия меню
			if is_closing:
				display_speed += 4
				radius -= display_speed * dt * 50
				if display_speed > 45:
					break
			else:
				if radius < 200:
					display_speed += 4
					radius += display_speed * dt * 50
				elif radius < 270 and is_opening:
					display_speed -= 5
					radius += display_speed * dt * 50
				elif 270 < radius < 300:
					radius -= (display_speed // 3) * dt * 50
					is_opening = False

			win.blit(win_copy, (0, 0))

			# Центр экрана
			center_x, center_y = Width // 2, Height // 2

			# Общий цикл для отрисовки и обработки кнопок
			for slot_name, text_key, angle_idx, img1, img2, action in self.buttons_config:
				# Вычисляем угол для текущей кнопки (в радианах)
				angle = (2 * math.pi * angle_idx) / 6
				
				# Координаты центра текущей кнопки
				btn_x = center_x + math.cos(angle) * radius
				btn_y = center_y + math.sin(angle) * radius

				# Проверка наведения мыши (хитбокс 64x64 вокруг btn_x, btn_y)
				is_hovered = (btn_x - 32 < mouse_x < btn_x + 32) and (btn_y - 32 < mouse_y < btn_y + 32)

				# Управление состояниями анимации слота
				anim_data = self.game.special_slot_animations.get(slot_name, [False, 0, 10])
				
				if is_hovered:
					if anim_data[0]: # Если уже наведены
						if anim_data[1] < dt * 150:
							anim_data[1] += dt * 30
							anim_data[2] = abs(anim_data[2] - dt * 90)
					else:
						anim_data = [True, 0, 10]
					
					# Проверяем условия клика / релиза (для Craft list нужен release, для остальных click[0])
					trigger = release if slot_name == "Craft list slot" else click[0]
					if trigger:
						result = action()
						if result == "close_menu":
							is_closing = True
							display_speed = 7
						elif result is not None:
							return result # Возвращаем метод переключения меню (например, main_menu)
				else:
					if anim_data[0]:
						anim_data[0] = False
						anim_data[1] = 0
					elif anim_data[1] < dt * 250:
						anim_data[1] += dt * 30

				# Сохраняем обновленные данные анимации обратно в объект игры
				self.game.special_slot_animations[slot_name] = anim_data

				# Отрисовка иконки кнопки
				if anim_data[0] and Settings["Display"][5]:
					size = max(1, int(64 - anim_data[2])) # Защита от нулевого/отрицательного размера scale
					try:
						scaled_img = pygame.transform.scale(img2, (size, size))
						win.blit(scaled_img, (btn_x - size // 2, btn_y - size // 2))
					except pygame.error:
						win.blit(img2, (btn_x - 32, btn_y - 32))
				else:
					win.blit(img1, (btn_x - 32, btn_y - 32))

				# Отрисовка подписи к кнопке
				text(t(text_key), btn_x, btn_y + 40, alignment=True)

			pygame.display.update()

