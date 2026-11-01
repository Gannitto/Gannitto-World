import pygame
import time
import pyperclip
import re
from Globals import win, menu_color_medium, Settings

pygame.key.set_repeat(500, 50) 

class InputSystem:
	def __init__(self, text):
		self.text = text
		self.input_text = ""
		self.stop_input()
		
	def start_input(self,
				 input_name,
				 text_x=0,
				 text_y=0,
				 text_color_=menu_color_medium,
				 text_size=20,
				 text_alignment=False,
				 text_letter_spacing=10,
				 text_surface=win,
				 text_max_width=0,
				 text_max_height=0,
				 text_space_between_strings=10
				 ):

		self.input_text = ""
		self.inputting = True
		self.input_name = input_name
		self.cursor_position = 0
		self.cursor_timer = time.time()
		self.show_cursor = False
		self.text_x = text_x
		self.text_y = text_y
		self.text_color = text_color_
		self.text_size = text_size
		self.text_alignment = text_alignment
		self.text_letter_spacing = text_letter_spacing
		self.text_surface = text_surface
		self.text_max_width = text_max_width
		self.text_max_height = text_max_height
		self.text_space_between_strings = text_space_between_strings

	def stop_input(self):

		self.last_text = self.input_text
		self.input_text = ""
		self.inputting = False
		self.input_name = None
		self.cursor_position = 0
		self.cursor_timer = 0
		self.show_cursor = False
		self.text_x = 0
		self.text_y = 0
		self.text_color = menu_color_medium
		self.text_size = 20
		self.text_alignment = False
		self.text_letter_spacing = 10
		self.text_surface = win
		self.text_max_width = 0
		self.text_max_height = 0
		self.text_space_between_strings = 10

	def _find_word_start(self):
		"""Ищет индекс начала слова слева от курсора (для Ctrl+Left и Ctrl+Backspace)"""
		if self.cursor_position == 0:
			return 0
		
		# Берем текст слева от курсора
		left_text = self.input_text[:self.cursor_position]
		
		# Пропускаем пробелы непосредственно перед курсором
		stripped = left_text.rstrip()
		if not stripped:
			return 0
			
		# Находим границу между пробелом и словом (или начало строки)
		# Ищет последний переход от пробельного символа к непробельному
		matches = list(re.finditer(r"\s\S", stripped))
		if matches:
			return matches[-1].start() + 1
		return 0

	def _find_word_end(self):
		"""Ищет индекс конца слова справа от курсора (для Ctrl+Right и Ctrl+Delete)"""
		if self.cursor_position >= len(self.input_text):
			return len(self.input_text)
			
		# Берем текст справа от курсора
		right_text = self.input_text[self.cursor_position:]
		
		# Пропускаем пробелы непосредственно перед следующим словом
		stripped = right_text.lstrip()
		if not stripped:
			return len(self.input_text)
			
		# Находим первый пробел после букв в правой части
		match = re.search(r"\s", stripped)
		if match:
			# Складываем: текущая позиция + сколько скипнули пробелов + длина слова до пробела
			spaces_skipped = len(right_text) - len(stripped)
			return self.cursor_position + spaces_skipped + match.start()
		return len(self.input_text)

	def handle_input(self, events):
		if self.inputting:
			current_time = time.time() * 1000

			for event in events:
				if event.type == pygame.KEYDOWN:
					self.holding_key = event.key
					self.key_timer = current_time + 500
					self.trigger_key_action(event.key)

				elif event.type == pygame.KEYUP:
					if hasattr(self, "holding_key") and event.key == self.holding_key:
						self.holding_key = None

				elif event.type == pygame.TEXTINPUT:
					# Игнорируем ввод текста, если зажат Ctrl (чтобы при Ctrl+V или Ctrl+Backspace не вводились символы "v" и т.д.)
					if not (pygame.key.get_mods() & pygame.KMOD_CTRL):
						self.input_text = self.input_text[:self.cursor_position] + event.text + self.input_text[self.cursor_position:]
						self.cursor_position += len(event.text)

			if hasattr(self, "holding_key") and self.holding_key is not None:
				keys_pressed = pygame.key.get_pressed()
				if keys_pressed[self.holding_key]:
					if current_time >= self.key_timer:
						self.trigger_key_action(self.holding_key)
						self.key_timer = current_time + 25
				else:
					self.holding_key = None

			if time.time() - self.cursor_timer >= Settings["Game"][3]:
				self.cursor_timer = time.time()
				self.show_cursor = not self.show_cursor
			text = self.input_text
			if self.show_cursor:
				text = text[:self.cursor_position] + "|" + text[self.cursor_position:]
			self.text(text, self.text_x, self.text_y, self.text_color, self.text_size, self.text_alignment, self.text_letter_spacing, self.text_surface, self.text_max_width, self.text_max_height, False, self.text_space_between_strings)

	def trigger_key_action(self, key):
		"""Вспомогательный метод для выполнения действия клавиши"""
		ctrl_pressed = pygame.key.get_mods() & pygame.KMOD_CTRL

		if key == pygame.K_RETURN:
			self.stop_input()
			
		elif key == pygame.K_BACKSPACE:
			if self.cursor_position > 0:
				if ctrl_pressed:
					# Удаление слова целиком (влево)
					start_pos = self._find_word_start()
					self.input_text = self.input_text[:start_pos] + self.input_text[self.cursor_position:]
					self.cursor_position = start_pos
				else:
					# Обычное удаление символа
					self.input_text = self.input_text[:self.cursor_position - 1] + self.input_text[self.cursor_position:]
					self.cursor_position -= 1
				
		elif key == pygame.K_DELETE:
			if self.cursor_position < len(self.input_text):
				if ctrl_pressed:
					# Удаление слова целиком (вправо)
					end_pos = self._find_word_end()
					self.input_text = self.input_text[:self.cursor_position] + self.input_text[end_pos:]
				else:
					# Обычное удаление символа справа
					self.input_text = self.input_text[:self.cursor_position] + self.input_text[self.cursor_position + 1:]
				
		elif key == pygame.K_LEFT:
			if ctrl_pressed:
				self.cursor_position = self._find_word_start()
			else:
				self.cursor_position = max(0, self.cursor_position - 1)
			self.show_cursor = True
			
		elif key == pygame.K_RIGHT:
			if ctrl_pressed:
				self.cursor_position = self._find_word_end()
			else:
				self.cursor_position = min(len(self.input_text), self.cursor_position + 1)
			self.show_cursor = True

		elif key == pygame.K_HOME:
			self.cursor_position = 0

		elif key == pygame.K_END:
			self.cursor_position = len(self.input_text)
			
		elif key == pygame.K_v and ctrl_pressed:
			clipboard_text = pyperclip.paste()
			if clipboard_text:
				self.input_text = self.input_text[:self.cursor_position] + clipboard_text + self.input_text[self.cursor_position:]
				self.cursor_position += len(clipboard_text)

