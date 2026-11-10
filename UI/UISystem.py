import pygame
from UI.ElementsUI import ToggleButton, InputField, Button
from Globals import win, Width, Height
from Config import Settings, statistics

class UISystem:

	def __init__(self):

		# Создаем все элементы интерфейса
		self.create_elements()
		
	def create_elements(self):

		self.elements = {

			"Display": [
				
				InputField(
					400, 0, "Brightness",
					lambda: Settings["Display"]["Brightness"],
					lambda v: Settings["Display"].__setitem__(0, v),
					unit="%"
				),
				InputField(
					400, 0, "Inventory transparency",
					lambda: Settings["Display"]["Inventory transparency"],
					lambda v: Settings["Display"].__setitem__(1, v),
					unit="%"
				),
				InputField(
					400, 0, "Distance",
					lambda: Settings["Display"]["Distance"],
					lambda v: Settings["Display"].__setitem__(2, v),
					unit="%"
				),
				ToggleButton(
					400, 0, "Display hitboxes",
					lambda: Settings["Display"]["Display hitboxes"],
					lambda v: Settings["Display"].__setitem__(3, v)
				),
				ToggleButton(
					400, 0, "Shadows",
					lambda: Settings["Display"]["Shadows"],
					lambda v: Settings["Display"].__setitem__(4, v)
				),
				ToggleButton(
					400, 0, "Inventory slots animation",
					lambda: Settings["Display"]["Inventory slots animation"],
					lambda v: Settings["Display"].__setitem__(5, v)
				),
				InputField(
					400, 0, "FPS",
					lambda: Settings["Display"]["FPS"],
					lambda v: Settings["Display"].__setitem__(6, v)
				),
				ToggleButton(
					400, 0, "Mouse click display",
					lambda: Settings["Display"]["Mouse click display"],
					lambda v: Settings["Display"].__setitem__(7, v)
				),
				ToggleButton(
					400, 0, "Description of the object on hover",
					lambda: Settings["Display"]["Description of the object on hover"],
					lambda v: Settings["Display"].__setitem__(8, v)
				),
				ToggleButton(
					400, 0, "Dim screen when turned off",
					lambda: Settings["Display"]["Dim screen when turned off"],
					lambda v: Settings["Display"].__setitem__(9, v)
				),
				ToggleButton(
					400, 0, "Show intro",
					lambda: Settings["Display"]["Show intro"],
					lambda v: Settings["Display"].__setitem__(10, v)
				)
			],
		"User": [
				InputField(
					400, 0, "Nickname",
					lambda: Settings["User"]["Nickname"],
					lambda v: Settings["User"].__setitem__(0, v),
					can_write_text=True, max_len=10
				),
				ToggleButton(
					400, 0, "Developer mode",
					lambda: Settings["User"]["Developer mode"],
					lambda v: Settings["User"].__setitem__(1, v)
				)
			],
		"Sound": [
				InputField(
					400, 0, "Music volume",
					lambda: Settings["Sound"]["Music volume"],
					lambda v: Settings["Sound"].__setitem__(0, min(v, 100)),
					unit="%"
				),
				InputField(
					400, 0, "Sound volume",
					lambda: Settings["Sound"]["Sound volume"],
					lambda v: Settings["Sound"].__setitem__(1, min(v, 100)),
					unit="%"
				)
			],
		"Statistics": [
				InputField(
					400, 0, "Visits to the game",
					lambda: statistics[0],
					lambda v: ...
				),
				InputField(
					400, 0, "Hours played",
					lambda: int(statistics[1]),
					lambda v: ...
				),
				InputField(
					400, 0, "Trees felled",
					lambda: statistics[2],
					lambda v: ...
				)
				],
		"Game": [
				ToggleButton(
					400, 0, "Automatically pick up items",
					lambda: Settings["Game"]["Automatically pick up items"],
					lambda v: Settings["Game"].__setitem__(0, v)
				),
				ToggleButton(
					400, 0, "Telephone control",
					lambda: Settings["Game"]["Telephone control"],
					lambda v: Settings["Game"].__setitem__(1, v)
				),
				InputField(
					400, 0, "Mouse wheel sensitivity",
					lambda: Settings["Game"]["Mouse wheel sensitivity"],
					lambda v: Settings["Game"].__setitem__(2, int(v))
				),
				InputField(
					400, 0, "Cursor blink rate",
					lambda: int(Settings["Game"]["Cursor blink rate"] * 1000),
					lambda v: Settings["Game"].__setitem__(3, int(v) / 1000)
				)
			],
		"World settings": [
				InputField(
					50, 60, "World name",
					lambda: Settings["Edit world"]["World name"],
					lambda v: Settings["Edit world"].__setitem__(0, v),
					can_write_text=True, max_len=50
				),
				ToggleButton(
					50, 520, "God mode",
					lambda: Settings["Edit world"]["God mode"],
					lambda v: Settings["Edit world"].__setitem__(1, v)
				)
			],
		"Multiplayer settings menu": [
				ToggleButton(
					10, 0, "Соединение через интернет",
					lambda: Settings["Multiplayer"]["Соединение через интернет"],
					lambda v: Settings["Multiplayer"].__setitem__(0, v)
				),
				ToggleButton(
					10, 0, "Соединение по локальной сети",
					lambda: not Settings["Multiplayer"]["Соединение через интернет"],
					lambda v: Settings["Multiplayer"].__setitem__(0, not v)
				),
				InputField(
					10, 0, "Порт",
					lambda: Settings["Multiplayer"]["Порт"],
					lambda v: Settings["Multiplayer"].__setitem__(1, v),
					max_len=5
				),
				InputField(
					10, 0, "Внешний порт",
					lambda: Settings["Multiplayer"]["Внешний порт"],
					lambda v: Settings["Multiplayer"].__setitem__(2, v),
					max_len=10
				),
				InputField(
					10, 0, "IP хоста",
					lambda: Settings["Multiplayer"]["IP хоста"],
					lambda v: Settings["Multiplayer"].__setitem__(3, v),
					can_write_text=True, max_len=15
				),
				InputField(
					10, 0, "Порт хоста",
					lambda: Settings["Multiplayer"]["Порт хоста"],
					lambda v: Settings["Multiplayer"].__setitem__(4, v),
					max_len=10
				)
			]
		}

	def _set_positions(self, bias, section, start_y=50):
		
		y = 0
		for element in self.elements[section]:
			y += 80
			element.y = start_y + bias + y
			element.rect.y = start_y + bias + y
			if hasattr(element, "handle_keyboard") and element.is_active:
				element.update_text_pos()

		return y
		
	def handle_events(self, events, mouse_x, mouse_y, release, section):

		"""Обработка событий"""

		current_elements = self.elements[section]
		for element in current_elements:
			if hasattr(element, "handle_keyboard"):
				element.handle_keyboard(events)
		
		for event in events:
			
			# Обработка кликов
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				for element in current_elements:
					element.handle_click(mouse_x, mouse_y, release)
	
	def draw(self, section, bias: int = 0, max_bias: int = 0, show_settings_lines: bool = True):

		self.draw_labels()
		
		# Отрисовка элементов текущей страницы
		for element in self.elements[section]:
			element.draw()
		if show_settings_lines:
			self.show_settings_elements(bias, max_bias)

	def draw_labels(self):
		# Отрисовка текстовых меток для элементов TODO
		pass

	def show_settings_elements(self, bias, max_bias):
		
		pygame.draw.rect(win, (192, 203, 220), (0, 0, Width, 103))
		pygame.draw.rect(win, (139, 155, 180), (-8, 100, 373, Height), 8)
		pygame.draw.line(win, (139, 155, 180), (307, 103), (Width, 103), 8)

		visible_height = Height - 103
		content_height = visible_height + abs(max_bias)
		scrollbar_height = Height - 103

		bar_height = max(scrollbar_height * (visible_height / content_height), 20)
		max_scroll = content_height - visible_height
		scroll_rel = abs(bias) / max_scroll if max_scroll > 0 else 0
		bar_y = 103 + scroll_rel * (scrollbar_height - bar_height)
		
		pygame.draw.rect(win, (139, 155, 180), (Width - 10, bar_y, 10, bar_height))

