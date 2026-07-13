import pygame
from typing import Callable, Any, Optional
from Translator import translator

t = translator.get

class UIElement:
	"""Базовый класс для всех UI элементов"""
	def __init__(self, x: int, y: int, width: int, height: int, label: str=""):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.label = label
		if label == "":
			self.label_width = 0
		else:
			self.label_width = self.font.size(t(self.label))[0] + 10
		self.rect = pygame.Rect(x + self.label_width, y, width, height)
	
	def handle_click(self, mouse_x: int, mouse_y: int, release: bool) -> bool:
		"""Обрабатывает клик по элементу. Возвращает True если клик был внутри"""
		return self.rect.collidepoint(mouse_x, mouse_y) and release
	
	def draw(self, surface: pygame.Surface):
		"""Отрисовывает элемент"""
		pass

class ToggleButton(UIElement):
	"""Переключатель (вкл/выкл)"""
	def __init__(self, x: int, y: int, label: str, get_value: Callable, set_value: Callable, 
				 font, color=(139, 155, 180)):
		self.get_value = get_value
		self.set_value = set_value
		self.font = font
		self.color = color
		super().__init__(x, y, 71, 71, label)
	
	def draw(self, surface: pygame.Surface):

		text_surface = self.font.render(t(self.label), True, self.color)
		surface.blit(text_surface, (self.x, self.y + 10))
		
		# Отрисовка рамки
		pygame.draw.rect(surface, self.color, self.rect, 5)
		
		# Отрисовка значения (✓ или x)
		value = " ✓" if self.get_value() else " x"
		text_surface = self.font.render(value, True, self.color)
		surface.blit(text_surface, (self.x + self.label_width + 10, self.y + 10))
	
	def handle_click(self, mouse_x: int, mouse_y: int, release: bool) -> bool:
		if super().handle_click(mouse_x, mouse_y, release):
			self.set_value(not self.get_value())
			return True
		return False

class InputField(UIElement):
	"""Поле ввода текста или числа"""
	def __init__(self, x: int, y: int, label: str, get_value: Callable, set_value: Callable, font, color=(139, 155, 180), width: int = 120, unit=""):
		self.get_value = get_value
		self.set_value = set_value
		self.font = font
		self.color = color
		self.is_active = False
		self.input_text = ""
		self.unit = unit
		super().__init__(x, y, width, 71, label)
	
	def draw(self, surface: pygame.Surface):

		text_surface = self.font.render(t(self.label), True, self.color)
		surface.blit(text_surface, (self.x, self.y + 10))

		# Отрисовка рамки
		pygame.draw.rect(surface, self.color, self.rect, 5)
		
		# Отрисовка значения или вводимого текста
		if self.is_active:
			text = self.input_text
		else:
			text = str(self.get_value())
		
		text_surface = self.font.render(text, True, self.color)
		surface.blit(text_surface, (self.x + self.label_width + 10, self.y + 10))
		
		# Отрисовка процента для некоторых полей
		if self.unit != "":
			percent = self.font.render(self.unit, True, self.color)
			surface.blit(percent, (self.x + self.label_width + self.width + 5, self.y + 10))
	
	def handle_click(self, mouse_x: int, mouse_y: int, release: bool) -> bool:
		if super().handle_click(mouse_x, mouse_y, release):
			self.is_active = not self.is_active
			if not self.is_active and self.input_text:
				try:
					self.set_value(int(self.input_text))
				except ValueError:
					pass
			return True
		return False
	
	def handle_keyboard(self, event):
		if not self.is_active:
			return False
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				self.is_active = False
				if self.input_text:
					try:
						self.set_value(int(self.input_text))
					except ValueError:
						pass
				self.input_text = ""
				return True
			elif event.key == pygame.K_BACKSPACE:
				self.input_text = self.input_text[:-1]
				return True
			elif event.unicode in "0123456789" and len(self.input_text) < 3:
				self.input_text += event.unicode
				return True
		return False

class Button(UIElement):
	"""Обычная кнопка"""
	def __init__(self, x: int, y: int, width: int, height: int, label: str, 
				 callback: Callable, font, color=(139, 155, 180)):
		super().__init__(x, y, width, height)
		self.label = label
		self.callback = callback
		self.font = font
		self.color = color
	
	def draw(self, surface: pygame.Surface):
		pygame.draw.rect(surface, self.color, self.rect, 2)
		text_surface = self.font.render(t(self.label), True, self.color)
		text_rect = text_surface.get_rect(center=self.rect.center)
		surface.blit(text_surface, text_rect)
	
	def handle_click(self, mouse_x: int, mouse_y: int, release: bool) -> bool:
		if super().handle_click(mouse_x, mouse_y, release):
			self.callback()
			return True
		return False

class PageManager:
	"""Управление страницами настроек"""
	def __init__(self, initial_page: int = 1, max_page: int = 3):
		self.current_page = initial_page
		self.max_page = max_page
	
	def next_page(self):
		self.current_page = min(self.current_page + 1, self.max_page)
	
	def prev_page(self):
		self.current_page = max(self.current_page - 1, 1)
	
	def get_page(self) -> int:
		return self.current_page
