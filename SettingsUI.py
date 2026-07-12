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
		
		# Менеджер страниц
		self.page_manager = PageManager(1, 3)
		
	def create_elements(self):
		# Страница 1
		self.page1_elements = []
		
		# Поля ввода для яркости, прозрачности, дистанции
		self.brightness_input = InputField(
			405, 113, "Brightness",
			lambda: self.settings["Display"][0],
			lambda v: self.settings["Display"].__setitem__(0, v),
			self.font, unit="%"
		)
		self.alpha_input = InputField(
			405, 199, "Inventory transparency",
			lambda: self.settings["Display"][1],
			lambda v: self.settings["Display"].__setitem__(1, v),
			self.font, unit="%"
		)
		self.distance_input = InputField(
			405, 285, "Distance",
			lambda: self.settings["Display"][2],
			lambda v: self.settings["Display"].__setitem__(2, v),
			self.font, unit="%"
		)
		
		# Переключатели
		self.hitboxes_toggle = ToggleButton(
			405, 371, "Display hitboxes",
			lambda: self.settings["Display"][3],
			lambda v: self.settings["Display"].__setitem__(3, v),
			self.font
		)
		self.shadows_toggle = ToggleButton(
			405, 457, "Shadows",
			lambda: self.settings["Display"][4],
			lambda v: self.settings["Display"].__setitem__(4, v),
			self.font
		)
		
		self.page1_elements = [
			self.brightness_input, self.alpha_input, self.distance_input,
			self.hitboxes_toggle, self.shadows_toggle
		]
		
		# Страница 2
		self.page2_elements = []
		
		self.slots_animation_toggle = ToggleButton(
			405, 113, "Inventory slots animation",
			lambda: self.settings["Display"][5],
			lambda v: self.settings["Display"].__setitem__(5, v),
			self.font
		)
		self.fps_input = InputField(
			405, 199, "FPS",
			lambda: self.settings["Display"][6],
			lambda v: self.settings["Display"].__setitem__(6, v),
			self.font
		)
		self.mouse_click_toggle = ToggleButton(
			405, 285, "Mouse click display",
			lambda: self.settings["Display"][7],
			lambda v: self.settings["Display"].__setitem__(7, v),
			self.font
		)
		self.object_description_toggle = ToggleButton(
			405, 371, "Description of the object on hover",
			lambda: self.settings["Display"][8],
			lambda v: self.settings["Display"].__setitem__(8, v),
			self.font
		)
		self.dim_screen_toggle = ToggleButton(
			405, 457, "Dim screen when turned off",
			lambda: self.settings["Display"][9],
			lambda v: self.settings["Display"].__setitem__(9, v),
			self.font
		)
		
		self.page2_elements = [
			self.slots_animation_toggle, self.fps_input,
			self.mouse_click_toggle, self.object_description_toggle,
			self.dim_screen_toggle
		]
		
		# Страница 3
		self.page3_elements = []
		
		self.intro_toggle = ToggleButton(
			405, 113, "Show intro",
			lambda: self.settings["Display"][10],
			lambda v: self.settings["Display"].__setitem__(10, v),
			self.font
		)
		
		self.page3_elements = [self.intro_toggle]

	def _set_display_value(self, index: int, value):
		"""Вспомогательный метод для установки значения в списке настроек"""
		self.settings["Display"][index] = value
	
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
		
		# Обработка навигации по страницам
		# Добавьте кнопки "Назад" и "Вперед"
	
	def get_current_page_elements(self):
		page = self.page_manager.get_page()
		if page == 1:
			return self.page1_elements
		elif page == 2:
			return self.page2_elements
		elif page == 3:
			return self.page3_elements
		return []
	
	def draw(self):
		# Отрисовка заголовков для текущей страницы
		self.draw_labels()
		
		# Отрисовка элементов текущей страницы
		for element in self.get_current_page_elements():
			element.draw(self.win)
		
		# Отрисовка номера страницы
		page_text = self.font.render(str(self.page_manager.get_page()), True, (139, 155, 180))
		self.win.blit(page_text, ((self.win.get_width() - 415) // 2 + 391, self.win.get_height() - 96))
	
	def draw_labels(self):
		# Отрисовка текстовых меток для элементов
		# Используй свою функцию text() здесь
		pass

