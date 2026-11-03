import Saver
import sys
import os
import time
import pygame
import random
import math
import pygame.surfarray as surfarray
from subprocess import check_output
import numpy as np
from itertools import product
from PIL import Image
from Globals import MAX_FPS, Width, Height, path, win, clock, Settings, bigTextInfo, text_color
from Cache import load

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
	
	cache_path = path + "/Saves/Cache/"
	if not os.path.exists(cache_path):
		os.mkdir(cache_path)
	
	cache_file = cache_path + name + ".png"
	if os.path.exists(cache_file):
		return load(cache_file, surface.get_width(), surface.get_height())
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

def win_darken(win: pygame.Surface, screen: pygame.Surface=None, duration: float=0.3):
	"""
	Затемнить экран. Используется для переходов между окнами
	win - Экран
	screen - Изображение экрана
	duration - Длительность перехода в секундах
	"""
	if screen is None:
		screen = win.copy()
	
	start_time = time.time()
	total_alpha = 255  # Максимальная темнота
	current_alpha = 0
	
	while current_alpha < total_alpha:
		elapsed = time.time() - start_time
		progress = min(elapsed / duration, 1.0)
		
		current_alpha = int(total_alpha * progress)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		
		win.blit(screen, (0, 0))
		win_fill(alpha=current_alpha)
		pygame.display.update()
		clock.tick(60)

def win_lighten(win: pygame.Surface, screen: pygame.Surface=None, duration: float=0.3):
	"""
	Осветлить экран. Используется для переходов между окнами
	win - Экран
	screen - Изображение экрана
	duration - Длительность перехода в секундах
	"""
	if screen is None:
		screen = win.copy()
	
	start_time = time.time()
	total_alpha = 300  # Максимальная темнота
	current_alpha = total_alpha
	
	while current_alpha > 1:
		elapsed = time.time() - start_time
		progress = min(elapsed / duration, 1.0)
		
		current_alpha = int(total_alpha * (1 - progress))
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		
		win.blit(screen, (0, 0))
		win_fill(alpha=max(current_alpha, 0))
		pygame.display.update()
		clock.tick(60)

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
	 load(path + "Images/Mouse click 1.png", 128),
	 load(path + "Images/Mouse click 2.png", 128),
	 load(path + "Images/Mouse click 3.png", 128),
	 load(path + "Images/Mouse click 4.png", 128),
	 load(path + "Images/Mouse click 5.png", 128)
	 )

mouse_click_image = None
mouse_click_timer = None

def animate_click(dt, mouse_x, mouse_y):

	global mouse_click_timer

	if Settings["Display"][7]:

		if pygame.mouse.get_pressed()[0] == 1:
			mouse_click_timer = 0
		if mouse_click_timer is not None:
			if mouse_click_timer >= 5:
				mouse_click_timer = None
			else:
				win.blit(mouse_click_images[int(mouse_click_timer)], (mouse_x - 64, mouse_y - 64))
				mouse_click_timer += dt * 40

def crack_surface(world, Particle, object, damage_level, scale=1):
	
	w, h = object.w, object.h
	w //= scale
	h //= scale
	result = object.image.copy()
	pixels = pygame.PixelArray(result)
	temp_surface = pygame.Surface((scale, scale))

	# Количество трещин зависит от damage
	crack_count = int(3 + 30 * damage_level)
	
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
				r, g, b, a = result.get_at((x * scale, y * scale))
				dark = int(40 + 120 * damage_level)
				new_color = (max(0, r - dark), max(0, g - dark), max(0, b - dark), a)
				pixels[x * scale : (x + 1) * scale, y * scale : (y + 1) * scale] = new_color

			x += random.choice([-1, 0, 1])
			y += random.choice([-1, 0, 1])
	
	pixels.close()
	del pixels
	
	return result

def destroy_object(image, x, y, world, Particle):
	world.particles.append(Particle(x, y, image, y_bias=-image.get_height() / 4, twisting_in_height=image.get_height() / 16, increased_transparency=20))

def create_throw_particle(Object, Particle, player, world, multiplayer, game_events, item_image, item_name):
	
	# Векторы направления
	dir_map = {
		"Down": (0, -1), "Up": (0, 1),
		"Left": (-1, 0), "Right": (1, 0),
		"Up-right": (1, 1), "Up-left": (-1, 1),
		"Down-right": (1, -1), "Down-left": (-1, -1)
	}
	
	dx, dy = dir_map.get(player.direction, (0, 1))
	norm = math.sqrt(dx*dx + dy*dy)
	if norm > 0:
		dx, dy = dx/norm, dy/norm
	
	# Скорость
	vx = dx * 2000
	vy = dy * 2000
	
	# Состояние для физики
	physics_state = {"vx": vx, "vy": vy, "start_x": player.x, "start_y": player.y}
	
	def tick_command(p):
		dt = p.dt
		p.x += physics_state["vx"] * dt
		p.y += physics_state["vy"] * dt
		physics_state["vx"] *= 0.0001 ** dt
		physics_state["vy"] *= 0.0001 ** dt
	
	def del_condition(p):
		# return abs(p.x - physics_state["start_x"]) > 200 or abs(p.y - physics_state["start_y"]) > 200
		return abs(physics_state["vx"]) < 64 and abs(physics_state["vy"]) < 64
	
	def end_command(p):
		chunk = world.chunk_manager.get_chunk_at(p.x, p.y)
		obj = Object(p.special_flags, p.x, p.y, f"Images/Items/{p.special_flags}.png", pickable=True)
		chunk.items.append(obj)
		if multiplayer:
			game_events.append({
				"event_type": "item_added",
				"item": obj.__getstate__()
			})
	
	return Particle(
		player.x, player.y,
		item_image,
		x_bias=0, y_bias=0,
		end_time=None,
		end_command=end_command,
		special_flags=item_name,
		tick_command=tick_command,
		del_self_condition=del_condition
	)

def text(
		text: str,
		text_x: int,
		text_y: int,
		color: tuple=text_color,
		size: int=20,
		alignment: bool=False,
		letter_spasing: int=10,
		surface: pygame.Surface=win,
		max_width: int=0,
		max_height: int=0,
		return_surface: bool=False,
		space_between_strings: int=10
		):
	
	"""
	Выводит текст на экран
	Аргументы:
	text - Сам текст
	text_x, text_y - Координаты текста
	color - Цвет текста
	size - Размер шрифта
	alignment - Выравнивание текста по центру
	letter_spasing - Размер пробела
	surface - Поверхность, на которой будет текст
	max_width - Максимальная длина текста
	return_surface - Выводить ли текст на экран или методом return
	"""
	
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
				Y += word_height + space_between_strings
			
			line_surface.blit(word_surface, (TextX, 0))
			TextX += word_width + letter_spasing

		if return_surface:
			all_text_surface.blit(line_surface, (X - TextX // 2 if alignment else X, Y))
		else:
			surface.blit(line_surface, (X - TextX // 2 if alignment else X, Y))
		Y += word_height + space_between_strings

	return all_text_surface

def get_text_height(
		text: str,
		size: int=20,
		letter_spasing: int=10,
		max_width: int=0,
		space_between_strings: int=10
		) -> int:
	
	"""
	Возвращает ширину текста
	Аргументы:
	text - Сам текст
	size - Размер шрифта
	letter_spasing - Размер пробела
	max_width - Максимальная длина текста
	space_between_strings - Расстояние между строками
	"""
	
	text = text.replace("\t\t", "")
	tempTextInfo = pygame.font.Font(path + "Font.ttf", size)
	text_height = 0

	for line in (word.split(" ") for word in text.splitlines()):
		TextX = 0
		text_height += size - 2 + space_between_strings
		for word in line:
			word_width = tempTextInfo.size(word)[0]
			if TextX + word_width >= Width // 3:
				TextX = 0
				text_height += size - 2 + space_between_strings
			TextX += word_width + 10

	return text_height

def check_collision(rect: pygame.Rect, world, only_solid=True, check_walls=True):
	"""Проверяет столкновение с твёрдыми объектами"""
	if check_walls:
		for wall in world.visible_walls.values():
			if (not wall.is_door or not wall.open) and rect.colliderect(wall.rect):
				return True
	for object in world.visible_objects:
		if (not only_solid or object.is_solid) and rect.colliderect(object.rect):
			return True
	return False

def check_projectiles_collision(rect: pygame.Rect, world, remove_projectile=True):

	for projectile in world.projectiles:
		if rect.collidepoint((projectile.x, projectile.y)):
			if remove_projectile:
				world.projectiles.remove(projectile)
			return True
	return False

def get_build_number():
	try:
		build_num = int(check_output(("git", "rev-list", "--count", "HEAD"), text=True).strip())
	except:
		build_num = "Error"
	return build_num

