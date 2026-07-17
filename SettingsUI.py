import pygame
from UI import ToggleButton, InputField, Button, PageManager

class SettingsUI:

	def __init__(self, win, settings, statistics, font, path):

		self.win = win
		self.settings = settings
		self.statistics = statistics
		self.font = font
		self.path = path
		
		# Создаем все элементы интерфейса
		self.create_elements()
		
	def create_elements(self):

		self.elements = {

			"Display": [
				
				InputField(
					400, 0, "Brightness",
					lambda: self.settings["Display"][0],
					lambda v: self.settings["Display"].__setitem__(0, v),
					self.font, unit="%"
				),
				InputField(
					400, 0, "Inventory transparency",
					lambda: self.settings["Display"][1],
					lambda v: self.settings["Display"].__setitem__(1, v),
					self.font, unit="%"
				),
				InputField(
					400, 0, "Distance",
					lambda: self.settings["Display"][2],
					lambda v: self.settings["Display"].__setitem__(2, v),
					self.font, unit="%"
				),
				ToggleButton(
					400, 0, "Display hitboxes",
					lambda: self.settings["Display"][3],
					lambda v: self.settings["Display"].__setitem__(3, v),
					self.font
				),
				ToggleButton(
					400, 0, "Shadows",
					lambda: self.settings["Display"][4],
					lambda v: self.settings["Display"].__setitem__(4, v),
					self.font
				),
				ToggleButton(
					400, 0, "Inventory slots animation",
					lambda: self.settings["Display"][5],
					lambda v: self.settings["Display"].__setitem__(5, v),
					self.font
				),
				InputField(
					400, 0, "FPS",
					lambda: self.settings["Display"][6],
					lambda v: self.settings["Display"].__setitem__(6, v),
					self.font
				),
				ToggleButton(
					400, 0, "Mouse click display",
					lambda: self.settings["Display"][7],
					lambda v: self.settings["Display"].__setitem__(7, v),
					self.font
				),
				ToggleButton(
					400, 0, "Description of the object on hover",
					lambda: self.settings["Display"][8],
					lambda v: self.settings["Display"].__setitem__(8, v),
					self.font
				),
				ToggleButton(
					400, 0, "Dim screen when turned off",
					lambda: self.settings["Display"][9],
					lambda v: self.settings["Display"].__setitem__(9, v),
					self.font
				),
				ToggleButton(
					400, 0, "Show intro",
					lambda: self.settings["Display"][10],
					lambda v: self.settings["Display"].__setitem__(10, v),
					self.font
				)
			],
		"User": [
				InputField(
					400, 0, "Nickname",
					lambda: self.settings["User"][0],
					lambda v: self.settings["User"].__setitem__(0, v),
					self.font, can_write_text=True, max_len=10
				)
			],
		"Sound": [
				InputField(
					400, 0, "Music volume",
					lambda: self.settings["Sound"][0],
					lambda v: self.settings["Sound"].__setitem__(0, min(v, 100)),
					self.font, unit="%"
				),
				InputField(
					400, 0, "Sound volume",
					lambda: self.settings["Sound"][1],
					lambda v: self.settings["Sound"].__setitem__(1, min(v, 100)),
					self.font, unit="%"
				)
			],
		"Statistics": [
				InputField(
					400, 0, "Visits to the game",
					lambda: self.statistics[0],
					lambda v: ...,
					self.font
				),
				InputField(
					400, 0, "Hours played",
					lambda: int(self.statistics[1]),
					lambda v: ...,
					self.font
				),
				InputField(
					400, 0, "Trees felled",
					lambda: self.statistics[2],
					lambda v: ...,
					self.font
				)
				],
		"Game": [
				ToggleButton(
					400, 0, "Automatically pick up items",
					lambda: self.settings["Game"][0],
					lambda v: self.settings["Game"].__setitem__(0, v),
					self.font
				),
				ToggleButton(
					400, 0, "Telephone control",
					lambda: self.settings["Game"][1],
					lambda v: self.settings["Game"].__setitem__(1, v),
					self.font
				),
			]
		}

	def _set_positions(self, bias, section, get_max_bias=False, start_y=50):
		
		y = 0
		for element in self.elements[section]:
			y += 80
			element.y = start_y + bias + y
			element.rect.y = start_y + bias + y

		if get_max_bias:
			return y
		return
		
	def handle_events(self, events, mouse_x, mouse_y, release, section):

		"""Обработка событий"""

		current_elements = self.elements[section]
		
		for event in events:
			# Обработка клавиатуры для всех input полей
			if event.type == pygame.KEYDOWN:
				for element in current_elements:
					if hasattr(element, "handle_keyboard"):
						element.handle_keyboard(event)
			
			# Обработка кликов
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				for element in current_elements:
					element.handle_click(mouse_x, mouse_y, release)
	
	def draw(self, section, win, Width, Height, bias, max_bias):

		self.draw_labels()
		
		# Отрисовка элементов текущей страницы
		for element in self.elements[section]:
			element.draw(self.win)
	
		self.show_settings_elements(win, Width, Height, bias, max_bias)

	def draw_labels(self):
		# Отрисовка текстовых меток для элементов TODO
		pass

	def show_settings_elements(self, win, Width, Height, bias, max_bias):
		
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

