import pygame
from Sound import play_sound
from Globals import win, textInfo, menu_color_medium, menu_color_light

class Button:

	def __init__(self, X: int, Y: int, image1: pygame.Surface, image2: pygame.Surface, surface=win, alignment=False, sound=True, cooldown=0.15, info=None, action=None):

		"""
		Кнопка.
		Аргементы:
		x - Координата x, на которой появится кнопка
		y - Координата y, на которой появится кнопка
		image1 - Изображение кнопки
		image2 - Изображение кнопки, когда на неё навели
		surface - Плоскость, на которой появится кнопка
		aligment - Выравнивание кнопки по центру своих координат
		sound - Будет ли раздаваться звук при нажатии на кнопку, или нет
		cooldown - Задержка в секундах между срабатываниями (защита от спама)
		info - Текст всплывающей подсказки
		action - Функция, которая выполняется после нажатия
		"""

		self.w = image1.get_width()
		self.h = image2.get_height()

		self.x = X
		self.y = Y

		self.image = image1
		self.image1 = image1
		self.image2 = image2

		self.surface = surface
		self.alignment = alignment

		self.sound = sound
		self.cooldown = cooldown

		self.info = info
		self.hold = 0
		self.info_y = 0
		self.info_speed = 3
		self.info_forward = True
		self.info_back = False

		self.action = action

		self.is_pressed = False
		self.is_activated = False
		self.last_trigger_time = 0
	
	def main(self, action=None):

		"""Главная функция кнопки, которая её показывает и работает с её механикой"""

		mouse_x, mouse_y = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		current_time = pygame.time.get_ticks()
		
		if self.info_back:

			if self.info_y <= 0:
				self.info_back = False
				self.info_y = 0
				self.info_speed = 3
				self.info_forward = True
			else:
				self.info_speed += 2
				self.info_y -= self.info_speed

		elif self.hold > 20:

			if self.info_y < 60:
				self.info_speed += 7
				self.info_y += self.info_speed

			elif self.info_y < 100 and self.info_forward:
				self.info_speed -= 4
				self.info_y += self.info_speed

			elif 100 < self.info_y < 130:
				self.info_y -= self.info_speed // 4
				self.info_forward = False

		if self.info is not None and self.info_y != 0:

			if self.alignment:
				pygame.draw.rect(self.surface, menu_color_medium, (self.x - textInfo.size(self.info)[0] // 2 - 5, self.y - self.h / 2 - self.info_y - 5, textInfo.size(self.info)[0] + 10, 28))
				self.surface.blit(textInfo.render(self.info, True, menu_color_medium, menu_color_light), (self.x - textInfo.size(self.info)[0] // 2, self.y - self.h / 2 - self.info_y))
			else:
				pygame.draw.rect(self.surface, menu_color_medium, (self.x - self.w // 2 - textInfo.size(self.info)[0] // 2 - 5, self.y - self.h / 2 - self.info_y - 5, textInfo.size(self.info)[0] + 10, 28))
				self.surface.blit(textInfo.render(self.info, True, menu_color_medium, menu_color_light), (self.x - self.w // 2 - textInfo.size(self.info)[0] // 2, self.y - self.info_y))

		hovered = self.alignment and (self.x - self.w / 2 < mouse_x < self.x + self.w / 2 and self.y - self.h / 2 < mouse_y < self.y + self.h / 2) or not self.alignment and (self.x < mouse_x < self.x + self.w and self.y < mouse_y < self.y + self.h)
		if hovered:

			self.image = self.image2
			self.hold += 1

			#if self.info_back:   # Очень необычная механика

			#	self.info_speed += 2
			#	self.info_y -= self.info_speed

			#elif self.hold > 50:

			#	if self.info_y < 50:
			#		self.info_speed += 4
			#		self.info_y += self.info_speed

			#	elif self.info_y >= 50 and self.info_forward:
			#		self.info_speed -= 5
			#		self.info_y += self.info_speed

			#	elif 27 < self.info_y < 30:
			#		self.info_y -= self.info_speed // 3
			#		self.info_forward = False
			
			#if self.alignment:
			#	self.surface.blit(bigTextInfo.render(self.info, True, (139, 105, 180)), (self.x - bigTextInfo.size(self.info)[0] // 2, self.y - self.h / 2 - self.info_y))
			#else:
			#	self.surface.blit(bigTextInfo.render(self.info, True, (139, 105, 180)), (self.x - self.w // 2 - bigTextInfo.size(self.info)[0] // 2, self.y - self.info_y))

		else:

			self.image = self.image1
			self.hold = 0
			if self.info_y > 0: self.info_back = True

		if hovered and click[0]:
			self.is_pressed = True
		else:
			if not click[0]:
				if self.is_pressed and hovered:
					if current_time - self.last_trigger_time > self.cooldown * 1000:
						if self.sound:
							play_sound("Button click")
						self.last_trigger_time = current_time
						self.is_activated = True

						if self.action is not None:
							self.action()
						if action is not None:
							action()
		
		if not click[0]:
			self.is_pressed = False
		
		if self.alignment:
			self.surface.blit(self.image, (self.x - self.w / 2, self.y - self.h / 2))
		else:
			self.surface.blit(self.image, (self.x, self.y))

	def get_pressed(self) -> bool:

		"Проверяет, нажата ли кнопка. Устаревший метод, оставлен для совместимости"

		mouse_x, mouse_y = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		if self.alignment and (self.x - self.w / 2 < mouse_x < self.x + self.w / 2 and self.y - self.h / 2 < mouse_y < self.y + self.h / 2) or not self.alignment and (self.x < mouse_x < self.x + self.w and self.y < mouse_y < self.y + self.h):
			self.image = self.image2
			if click[0]:
				return True
		else:
			self.image = self.image1
			return False
