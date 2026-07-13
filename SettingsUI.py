import pygame
from UI import ToggleButton, InputField, Button, PageManager

class SettingsUI:

	def __init__(self, win, settings, font, path):

		self.win = win
		self.settings = settings
		self.font = font
		self.path = path
		
		# Создаем все элементы интерфейса
		self.create_elements()
		
	def create_elements(self):
		
		self.display_elements = [
		
			InputField(
				405, 113, "Brightness",
				lambda: self.settings["Display"][0],
				lambda v: self.settings["Display"].__setitem__(0, v),
				self.font, unit="%"
			),
			InputField(
				405, 199, "Inventory transparency",
				lambda: self.settings["Display"][1],
				lambda v: self.settings["Display"].__setitem__(1, v),
				self.font, unit="%"
			),
			InputField(
				405, 285, "Distance",
				lambda: self.settings["Display"][2],
				lambda v: self.settings["Display"].__setitem__(2, v),
				self.font, unit="%"
			),
			ToggleButton(
				405, 371, "Display hitboxes",
				lambda: self.settings["Display"][3],
				lambda v: self.settings["Display"].__setitem__(3, v),
				self.font
			),
			ToggleButton(
				405, 457, "Shadows",
				lambda: self.settings["Display"][4],
				lambda v: self.settings["Display"].__setitem__(4, v),
				self.font
			),
			ToggleButton(
				405, 113, "Inventory slots animation",
				lambda: self.settings["Display"][5],
				lambda v: self.settings["Display"].__setitem__(5, v),
				self.font
			),
			InputField(
				405, 199, "FPS",
				lambda: self.settings["Display"][6],
				lambda v: self.settings["Display"].__setitem__(6, v),
				self.font
			),
			ToggleButton(
				405, 285, "Mouse click display",
				lambda: self.settings["Display"][7],
				lambda v: self.settings["Display"].__setitem__(7, v),
				self.font
			),
			ToggleButton(
				405, 371, "Description of the object on hover",
				lambda: self.settings["Display"][8],
				lambda v: self.settings["Display"].__setitem__(8, v),
				self.font
			),
			ToggleButton(
				405, 457, "Dim screen when turned off",
				lambda: self.settings["Display"][9],
				lambda v: self.settings["Display"].__setitem__(9, v),
				self.font
			),
			ToggleButton(
				405, 113, "Show intro",
				lambda: self.settings["Display"][10],
				lambda v: self.settings["Display"].__setitem__(10, v),
				self.font
			)
		]

		self._set_positions(0)

	def _set_display_value(self, index: int, value):
		"""Вспомогательный метод для установки значения в списке настроек"""
		self.settings["Display"][index] = value

	def _set_positions(self, bias, get_max_bias=False):
		
		y = 0
		for element in self.display_elements:
			y += 80
			element.y = 50 + bias + y
			element.rect.y = 50 + bias + y

		if get_max_bias:
			return y
		return
		
	def handle_events(self, events, mouse_x, mouse_y, release):

		"""Обработка событий"""

		current_elements = self.get_current_page_elements()
		
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
	
	def get_current_page_elements(self):
		return self.display_elements
	
	def draw(self):
		# Отрисовка заголовков для текущей страницы
		self.draw_labels()
		
		# Отрисовка элементов текущей страницы
		for element in self.get_current_page_elements():
			element.draw(self.win)
	
	def draw_labels(self):
		# Отрисовка текстовых меток для элементов
		pass

