import pygame
import time
from typing import Callable, Any, Optional
from Translator import translator
from Globals import cursor_speed, bigTextInfo, win

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
				 font=bigTextInfo, color=(139, 155, 180)):
		self.get_value = get_value
		self.set_value = set_value
		self.font = font
		self.color = color
		super().__init__(x, y, 71, 71, label)
	
	def draw(self):

		text_surface = self.font.render(t(self.label), True, self.color)
		win.blit(text_surface, (self.x, self.y + 10))
		
		# Отрисовка рамки
		pygame.draw.rect(win, self.color, self.rect, 5)
		
		# Отрисовка значения (✓ или x)
		value = " ✓" if self.get_value() else " x"
		text_surface = self.font.render(value, True, self.color)
		win.blit(text_surface, (self.x + self.label_width + 10, self.y + 10))
	
	def handle_click(self, mouse_x: int, mouse_y: int, release: bool) -> bool:
		if super().handle_click(mouse_x, mouse_y, release):
			self.set_value(not self.get_value())
			return True
		return False

class InputField(UIElement):
	"""Поле ввода текста или числа"""
	def __init__(self, x: int, y: int, label: str, get_value: Callable, set_value: Callable, font=bigTextInfo, color=(139, 155, 180), width=None, unit="", can_write_text=False, max_len=3):
		self.get_value = get_value
		self.set_value = set_value
		self.font = font
		self.color = color
		self.is_active = False
		self.input_text = ""
		self.unit = unit
		self.can_write_text = can_write_text
		self.max_len = max_len
		self.width = (font.size("a" * max_len)[0] + 20) or width
		self.cursor_timer = 0
		self.show_cursor = False
		super().__init__(x, y, self.width, 71, label)
	
	def draw(self):

		text_surface = self.font.render(t(self.label), True, self.color)
		win.blit(text_surface, (self.x, self.y + 10))

		# Отрисовка рамки
		pygame.draw.rect(win, self.color, self.rect, 5)
		
		# Отрисовка значения или вводимого текста
		if self.is_active:
			text = self.input_text
			if time.time() - self.cursor_timer >= cursor_speed:
				self.cursor_timer = time.time()
				self.show_cursor = not self.show_cursor
			if self.show_cursor:
				text += "|"
		else:
			text = str(self.get_value())
		
		text_surface = self.font.render(text, True, self.color)
		win.blit(text_surface, (self.x + self.label_width + 10, self.y + 10))
		
		# Отрисовка знака для некоторых полей
		if self.unit != "":
			percent = self.font.render(self.unit, True, self.color)
			win.blit(percent, (self.x + self.label_width + self.width + 5, self.y + 10))
	
	def handle_click(self, mouse_x: int, mouse_y: int, release: bool) -> bool:
		if super().handle_click(mouse_x, mouse_y, release):
			self.is_active = not self.is_active
			if self.is_active:
				self.cursor_timer = time.time()
				self.input_text = str(self.get_value())
			elif self.input_text:
				try:
					self.set_value(self.input_text)
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
						self.set_value(self.input_text if self.can_write_text else int(self.input_text))
					except ValueError:
						pass
				self.input_text = ""
				return True
			elif event.key == pygame.K_BACKSPACE:
				self.input_text = self.input_text[:-1]
				return True
			elif (self.can_write_text or event.unicode in "0123456789") and len(self.input_text) < self.max_len:
				self.input_text += event.unicode
				return True
		return False

class Button(UIElement):
	"""Обычная кнопка"""
	def __init__(self, x: int, y: int, width: int, height: int, label: str, 
				 callback: Callable, font=bigTextInfo, color=(139, 155, 180)):
		super().__init__(x, y, width, height)
		self.label = label
		self.callback = callback
		self.font = font
		self.color = color
	
	def draw(self):
		pygame.draw.rect(self.color, self.rect, 2)
		text_surface = self.font.render(t(self.label), True, self.color)
		text_rect = text_surface.get_rect(center=self.rect.center)
		win.blit(text_surface, text_rect)
	
	def handle_click(self, mouse_x: int, mouse_y: int, release: bool) -> bool:
		if super().handle_click(mouse_x, mouse_y, release):
			self.callback()
			return True
		return False

