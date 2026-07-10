import Saver
import sys
import os
import pygame
from itertools import product
from Globals import *

def languages(Russian: str, English: str, Kazach: str) -> str:
	from Globals import changed_language
	if changed_language == "Russian": return Russian
	if changed_language == "English": return English
	if changed_language == "Kazach": return Kazach

def text(text: str, text_x: int, text_y: int, color: tuple=text_color, size: int=20, alignment: bool=False, letter_spasing: int=10, surface: pygame.Surface=win, max_width: int=0, max_height: int=0, return_surface: bool=False, spase_between_strings: int=10):
	pos = (text_x, text_y)
	text = text.replace("\t\t", "")
	X, Y = pos
	
	if max_width == 0:
		max_width = surface.get_size()[0] - 10
	if max_height == 0:
		max_height = surface.get_size()[1] - 10

	all_text_surface = pygame.Surface((max_width, max_height), pygame.SRCALPHA)

	temp_font = pygame.font.Font(path + "Font.ttf", size)

	for line in (word.split(" ") for word in text.splitlines()):
		
		line_surface = pygame.Surface((max_width, size), pygame.SRCALPHA)
		TextX = 0

		for word in line:

			word_surface = temp_font.render(word, True, color)
			word_width, word_height = word_surface.get_size()
			if TextX + word_width >= max_width:
				surface.blit(line_surface, (X - TextX // 2 if alignment else X, Y))
				line_surface = pygame.Surface((max_width, size), pygame.SRCALPHA)
				TextX = 0
				Y += word_height + spase_between_strings
			
			line_surface.blit(word_surface, (TextX, 0))
			TextX += word_width + letter_spasing
		if return_surface:
			all_text_surface.blit(line_surface, (X - TextX // 2 if alignment else X, Y))

		else:
			surface.blit(line_surface, (X - TextX // 2 if alignment else X, Y))
		Y += word_height + spase_between_strings

	return all_text_surface

def shadow(
		surface: pygame.Surface,
		name: str,
		len_shadow: int=1,
		intensity: int=100
		) -> pygame.Surface:
	
	"""
	Показывает на изображении его тень.
	surface - Изображение, на котором нужно показать тень
	name - Имя изображение, по которому оно сохранится в кеш
	len_shadow - Длина тени
	intensity - Интенсивность тени
	"""
	
	from Globals import Settings
	
	if Settings["Display"][4]:
		if not os.path.exists(path + "Cache"):
			os.mkdir(path + "Cache")

		if os.path.exists(path + "Cache/" + name + ".png"):
			return pygame.image.load(path + "Cache/" + name + ".png")

		else:
			
			new_surface = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
			new_surface.blit(surface, (0, 0))
			shadow_surface = pygame.Surface((new_surface.get_width(), new_surface.get_height()), pygame.SRCALPHA)

			for _ in range(len_shadow):

				for X, Y in product(range(new_surface.get_width() - 1), range(new_surface.get_height() - 1)):

					try:

						if 0 < new_surface.get_at((X, Y)).a and new_surface.get_at((X + 1, Y + 1)).a < 100:
							shadow_surface.set_at((X + 1, Y + 1), (0, 0, 150, 1))

					except IndexError:

						temp = new_surface.copy()
						new_surface.blit(shadow_surface, (0, 0))
						new_surface = pygame.transform.scale(new_surface, (new_surface.get_width() + 1, new_surface.get_height() + 1))
						shadow_surface = pygame.Surface((new_surface.get_width(), new_surface.get_height()), pygame.SRCALPHA)
						shadow_surface.set_at((X + 1, Y + 1), (0, 0, 150, 1))

				new_surface.blit(shadow_surface, (0, 0))
			
			shadow_surface.set_alpha(intensity)
			pygame.image.save(new_surface, path + "Cache/" + name + ".png")
			
			return new_surface
	else:

		return surface
	
def win_fill(fill_colour=(0, 0, 0), alpha: int=90, rect: tuple=(0, 0, Width, Height)):

	"""
	Заливка экрана, которая может работать с альфа каналом
	
	fill_colour - Цвет, которым заливается экран
	alpha - Прозрачность заливки
	rect - Квадрат заливки, по умолчанию весь экран
	"""
	
	from Globals import win
	
	a = pygame.Surface(rect[2:4])
	a.fill(fill_colour)
	a.set_alpha(alpha)
	win.blit(a, rect[0:2])
	
def win_darken(screen: pygame.Surface):
	
	"""
	Затемнить экран. Используется для переходов между окнами
	screen - Изображение экрана
	"""
	from Globals import win, clock
	from main import save
	tick = 0
	display_speed = 7
	dark = 0
	
	while tick < 12:
		
		tick += 1
		display_speed += 7
		dark += display_speed

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				save()
				sys.exit()

		win.blit(screen, (0, 0))
		win_fill(alpha=dark)
		pygame.display.update()
		clock.tick(30)
	

def win_lighten(screen: pygame.Surface, start_dark: int=300):
	
	"""
	Осветлить экран. Используется для переходов между окнами
	screen - Изображение экрана
	start_dark - Значение темноты в начале, если сделать её больше, то задержка будет больше
	"""
	
	from Globals import clock, win
	from main import save

	dark = start_dark
	display_speed = 7

	while dark > 1:
		
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				save()
				sys.exit()
		
		display_speed += 7
		dark -= display_speed
		win.blit(screen, (0, 0))
		win_fill(alpha=dark)
		
		pygame.display.update()
		clock.tick(30)

def draw_key(key: str, X: int, Y: int):
	
	"""
	Отображает клавишу на экране. Используется для клавиши alt
	key - Имя клавиши
	X - x клавиши
	Y - y клавиши
	"""
	from Globals import win, bigTextInfo
	pygame.draw.rect(win, (192, 203, 220), (X - bigTextInfo.size(key)[0] / 2, Y, bigTextInfo.size(key)[0] + 10, 45))
	pygame.draw.rect(win, (139, 155, 180), (X - bigTextInfo.size(key)[0] / 2, Y, bigTextInfo.size(key)[0] + 10, 45), 3)
	win.blit(bigTextInfo.render(key, True, (139, 155, 180)), (X - bigTextInfo.size(key)[0] / 2 + 5, Y + 5))

def show_error_window(error_message: str):

	"""
	Показывает окно об ошибке
	error_message - Имя ошибки
	"""

	import pyperclip
	import traceback
	from main import text

	pyperclip.copy(traceback.format_exc())

	# Параметры окна
	pygame.init()
	Width, Height = 600, 400
	win = pygame.display.set_mode((Width, Height))
	pygame.display.set_caption("Error")

	# Основной цикл окна ошибки
	running = True
	while running:

		win.fill((0, 0, 255))
		
		text(":(", 10, 10, (255, 255, 255), 60)
		text(f"""Во время игры произошла ошибка.
		Её текст был скопирован в буфер обмена

		Далее следуйте по этому плану:
		1. Скажите разработчику игры о найденной ошибке, он не кусается
		ТГ Gannitto, gmail danilaserezhin@gmail.com
		2. Расскажите о том, что вы только что делали в игре
		3. Сообщите саму ошибку
		""", 10, 80, (255, 255, 255))

		pygame.display.flip()

		# Обработка событий
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		
		# Для выхода из программы при возникновении ошибки
		if running == False:
			pygame.quit()
			sys.exit()

mouse_click_images = (
	 pygame.transform.scale(pygame.image.load(path + "Images/Mouse click 1.png"), (128, 128)),
	 pygame.transform.scale(pygame.image.load(path + "Images/Mouse click 2.png"), (128, 128)),
	 pygame.transform.scale(pygame.image.load(path + "Images/Mouse click 3.png"), (128, 128)),
	 pygame.transform.scale(pygame.image.load(path + "Images/Mouse click 4.png"), (128, 128)),
	 pygame.transform.scale(pygame.image.load(path + "Images/Mouse click 5.png"), (128, 128))
	 )

mouse_click_image = None

def animate_click(Settings, win, mouse_x, mouse_y):

	global mouse_click_image

	if Settings["Display"][7]:

		if pygame.mouse.get_pressed()[0] == 1:
			mouse_click_image = 1
		try:
			win.blit(mouse_click_images[mouse_click_image - 1], (mouse_x - 64, mouse_y - 64))
			if mouse_click_image == 5:
				mouse_click_image = None
			else:
				mouse_click_image += 1
		except TypeError:
			pass


