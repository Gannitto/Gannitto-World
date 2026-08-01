import Saver
import sys
import os
import pygame
import random
import pygame.surfarray as surfarray
import numpy as np
from itertools import product
from PIL import Image
from Globals import Width, Height, path, win, clock, Settings, bigTextInfo

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

default_fill_surface = pygame.Surface((Width, Height), pygame.SRCALPHA)
default_fill_surface.fill((0, 0, 0))
default_fill_surface.set_alpha(90)

def win_fill(fill_color=(0, 0, 0), alpha: int=90, rect: tuple=(0, 0, Width, Height)):

	"""
	Заливка экрана, которая может работать с альфа каналом
	
	fill_color - Цвет, которым заливается экран
	alpha - Прозрачность заливки
	rect - Квадрат заливки, по умолчанию весь экран
	"""

	if alpha > 0:
		if fill_color == (0, 0, 0) and alpha == 90 and rect == (0, 0, Width, Height):
			win.blit(default_fill_surface, (0, 0))
		else:
			temp_surface = pygame.Surface(rect[2:4], pygame.SRCALPHA)
			temp_surface.fill(fill_color)
			temp_surface.set_alpha(alpha)
			win.blit(temp_surface, rect[0:2])

def get_shadow(alpha: int):

	"""
	Функция для наложения естественной тени
	alpha - Прозрачность заливки
	"""

	temp_surface = pygame.Surface((Width, Height), pygame.SRCALPHA)
	temp_surface.fill((0, 0, 0))
	temp_surface.set_alpha(alpha)
	return temp_surface

def reverse_fill_area(rect, fill_color=(0, 0, 0), alpha=90):

	"""
	Создаёт освещение на области экрана с помощью numpy и pygame.surfarray
	"""

	x, y, w, h = rect
	a = alpha / 255.0
	
	if a >= 1.0:
		return
	
	# Подповерхность
	area = win.subsurface(rect)
	mult = 1.0 - a
	
	pixels = pygame.surfarray.array3d(area).astype(np.float32)
	
	if fill_color[0] == fill_color[1] == fill_color[2]:
		# Серый - 1 канал
		pixels = (pixels - fill_color[0] * a) / mult
	else:
		# Цветной - 3 канала
		fill_array = np.array(fill_color, dtype=np.float32)
		pixels = (pixels - fill_array * a) / mult
		
	final_pixels = np.clip(pixels, 0, 255).astype(np.uint8)
	
	del pixels
	pygame.surfarray.blit_array(area, final_pixels)

def win_darken(win: pygame.Surface, screen: pygame.Surface=None):
	
	"""
	Затемнить экран. Используется для переходов между окнами
	win - Экран
	screen - Изображение экрана
	"""
	if screen is None:
		screen = win.copy()
	tick = 0
	display_speed = 7
	dark = 0
	
	while tick < 12:
		
		tick += 1
		display_speed += 7
		dark += display_speed

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		win.blit(screen, (0, 0))
		win_fill(alpha=dark)
		pygame.display.update()
		clock.tick(30)
	

def win_lighten(win: pygame.Surface, screen: pygame.Surface=None, start_dark: int=300):
	
	"""
	Осветлить экран. Используется для переходов между окнами
	win - Экран
	screen - Изображение экрана
	start_dark - Значение темноты в начале, если сделать её больше, то задержка будет больше
	"""
	if screen is None:
		screen = win.copy()

	dark = start_dark
	display_speed = 7

	while dark > 1:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
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

def crack_surface(world, Particle, object, damage_level, scale=1):
	
	w, h = object.w, object.h
	w //= scale
	h //= scale
	result = object.image.copy()
	pixels = pygame.PixelArray(result)
	temp_surface = pygame.Surface((scale, scale))

	# Количество трещин зависит от damage
	crack_count = int(3 + 45 * damage_level)
	
	for _ in range(crack_count):

		x = random.randint(0, w-1)
		y = random.randint(0, h-1)
		length = random.randint(5, int(10 + 12 * damage_level))
		color_at_pos = object.image.get_at((x * scale, y * scale))
		if color_at_pos != (0, 0, 0, 255):
			temp_surface.fill(color_at_pos)
			world.particles.append(Particle(object.x - object.w // 2 + x * scale, object.y - object.h // 2 + y * scale, temp_surface, 5, -16, end_time=0.5))
		
		for _ in range(length):
			if 0 <= x < w and 0 <= y < h:
				r, g, b, _ = result.get_at((x * scale, y * scale))
				dark = int(40 + 120 * damage_level)
				pixels[x * scale : (x + 1) * scale, y * scale : (y + 1) * scale] = (max(0, r-dark), max(0, g-dark), max(0, b-dark))
			
			x += random.choice([-1, 0, 1])
			y += random.choice([-1, 0, 1])
	
	del pixels
	
	return result
