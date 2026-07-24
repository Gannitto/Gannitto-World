import Saver
import sys
import os
import pygame
from itertools import product
import numpy as np
from PIL import Image
from Globals import Width, Height, path

changed_language = "Russian"
def languages(Russian: str, English: str, Kazach: str) -> str:
	"""Переводит текст на выбранный язык. Эта функция устарела и нужно постепенно от неё отказываться."""
	if changed_language == "Russian": return Russian
	if changed_language == "English": return English
	if changed_language == "Kazach": return Kazach

def shadow(
		surface: pygame.Surface,
		name: str,
		len_shadow: int = 20,
		intensity: int = 100,
		x_bias: int=1,
		y_bias: int=1
		) -> pygame.Surface:
	
	from Globals import Settings
	
	if not Settings["Display"][4]:
		return surface
	
	cache_path = path + "Cache/"
	if not os.path.exists(cache_path):
		os.mkdir(cache_path)
	
	cache_file = cache_path + name + ".png"
	if os.path.exists(cache_file):
		return pygame.image.load(cache_file)
	
	# Конвертируем pygame surface в PIL Image
	width, height = surface.get_width(), surface.get_height()
	
	# Получаем данные поверхности
	data = pygame.image.tostring(surface, "RGBA")
	img = Image.frombytes("RGBA", (width, height), data)
	
	# Создаем массив numpy из PIL Image
	img_array = np.array(img)
	
	# Создаем тень
	shadow_array = np.zeros_like(img_array)
	
	# Проверяем границы
	for y, x in product(range(height - 1), range(width - 1)):
		if img_array[y, x, 3] > 0 and img_array[y + 1, x + 1, 3] < 100:
			for bias in range(len_shadow):
				if not (0 <= x + 1 + bias * x_bias < width and 0 <= y + 1 + bias * y_bias < height) or img_array[y + 1 + bias * y_bias, x + 1 + bias * x_bias, 3] == 255:
					break
				shadow_array[y + 1 + bias * y_bias, x + 1 + bias * x_bias] = [0, 0, 10, intensity * (len_shadow - bias) // len_shadow]
	
	# Комбинируем
	result_array = np.where(shadow_array[:, :, 3:4] > 0, shadow_array, img_array)
	
	# Конвертируем обратно в PIL Image
	result_img = Image.fromarray(result_array, "RGBA")
	
	# Сохраняем в pygame surface
	result_data = result_img.tobytes()
	result_surface = pygame.image.fromstring(result_data, (width, height), "RGBA")
	
	pygame.image.save(result_surface, cache_file)
	return result_surface

def win_fill(fill_colour=(0, 0, 0), alpha: int=90, rect: tuple=(0, 0, Width, Height)):

	"""
	Заливка экрана, которая может работать с альфа каналом
	
	fill_colour - Цвет, которым заливается экран
	alpha - Прозрачность заливки
	rect - Квадрат заливки, по умолчанию весь экран
	"""
	if alpha > 0:
		from Globals import win
		
		a = pygame.Surface(rect[2:4], pygame.SRCALPHA)
		a.fill(fill_colour)
		a.set_alpha(alpha)
		win.blit(a, rect[0:2])
	
def win_darken(screen: pygame.Surface):
	
	"""
	Затемнить экран. Используется для переходов между окнами
	screen - Изображение экрана
	"""
	from Globals import win, clock
	from Gannitto_world import save
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
	from Gannitto_world import save

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
	from Gannitto_world import text

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

