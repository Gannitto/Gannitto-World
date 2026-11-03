import pygame
import time
from Cache import load
from Assets import no_file_texture
from Globals import win, Settings

class Particle:

	def __init__(self,
				 start_x: int=0,
				 start_y: int=0,
				 image: pygame.Surface=no_file_texture.copy(),
				 x_bias=0, y_bias=0,
				 rotate: int=None,
				 display_mode=None,
				 tick_command=None,
				 increased_transparency: int=0,
				 twisting_in_width: int=0, twisting_in_height: int=0,
				 remove_particle_after_twisting: bool=True,
				 track_ticks: bool=False,
				 del_self_condition=None,
				 can_interfere_with_placing: bool=False,
				 save_particle: bool=False,
				 save_start_time: bool=True,
				 start_time: float|None=None,
				 end_x: int=None, end_y: int=None,
				 end_zone: int=0, end_time: float=None,
				 end_command=None,
				 special_flags: list=[]):

		"""
		Частицы, с помощью которых можно сделать много всего
		
		Аргументы:
		start_x - Координата X, где появится частица
		start_y - Координата Y, где появится частица
		image - Изображение частицы, по умолчанию иконка файла без текстуры
		x_bias - Смещение по оси X
		y_bias - Смещение по оси Y
		rotate - Поворот частцы на каждом тике
		display_mode - Режим отображения частицы
		tick_command - Код, который будет срабатывать при каждом тике часлицы
		increased_transparency - Число, на которое будет уменьшаться прозрачность частицы, если нужно
		twisting_in_width - Сжимает изображение цастицы по длине
		twisting_in_height - Сжимает изображение частицы по ширине
		remove_particle_after_twisting - Удалить частицу после после полного скручивания
		track_ticks - Слитать ли каждый тик в переменную ticks после создания частицы
		del_self_condition - Условие, при котором удалится частица
		can_interfere_with_placing - Может ли частица мешать ставить объекты
		save_particle - Сохранять ли частицу после выхода из мира
		save_start_time - Сохранять ли параметр start_time после выхода из мира, если включён save_particle
		start_time - Время создания частицы. По умолчанию выставляется автоматически
		end_x - Координата X, при достижении которой частица пропадёт
		end_y - Координата Y, при достижении которой частица пропадёт
		end_zone - Если нужно, чтобы частица пропадала, когда она находится не именно на end_x и/или end_y, а на определённом растоянии или ближе, то можно использовать end_zone. За это расстояние этот аргумент и отвечает.
		end_time - Время, после которого частица пропадает
		end_command - Команда, которая будет срабатывать после удаления частицы
		special_flags - Специальные флаги частицы, с помощью которых можно реализовать её механики
		"""

		self.x = start_x
		self.y = start_y

		self.image = image
		self.w = self.image.get_width()
		self.h = self.image.get_height()
		self.x_bias = x_bias
		self.y_bias = y_bias
		self.rotate = rotate
		if display_mode is None:
			import sys
			main_module = sys.modules.get("__main__")
			if main_module and hasattr(main_module, "world_to_screen"):
				self.display_mode = main_module.world_to_screen
			else:
				# Безопасный дефолтный вариант (на случай тестов без главного файла)
				self.display_mode = lambda X, Y, W, H: (X - start_x, Y - start_y)
		else:
			self.display_mode = display_mode
		
		self.tick_command = tick_command

		self.special_flags = special_flags
		self.increased_transparency = increased_transparency
		if self.increased_transparency > 0:
			self.image = self.image.convert_alpha()
		self.can_interfere_with_placing = can_interfere_with_placing
		
		self.twisting_in_width = twisting_in_width
		self.twisting_in_height = twisting_in_height
		self.remove_particle_after_twisting = remove_particle_after_twisting

		self.track_ticks = track_ticks
		self.ticks = -1

		self.del_self_condition = del_self_condition
		
		self.save_particle = save_particle
		self.save_start_time = start_time

		self.end_x = end_x
		self.end_y = end_y
		self.end_zone = end_zone
		self.end_time = end_time
		self.end_command = end_command

		self.start_time = time.time()

		self.w, self.h = self.image.get_size()
	
	def __getstate__(self):
		
		state = self.__dict__.copy()
		del state["image"]
		return state

	def __setstate__(self, state):
		
		self.__dict__.update(state)
		self.image = load(self.image_path, self.w, self.h)
	
	def main(self, dt, world):
		
		self.dt = dt
		if self.tick_command is not None:
			self.tick_command(self)

		if self.track_ticks: self.ticks += 1
		if self.increased_transparency != 0:
			self.image.set_alpha(self.image.get_alpha() - self.increased_transparency * dt * 25)
		
		if self.twisting_in_width or self.twisting_in_height:
			try:
				self.image = pygame.transform.scale(
						self.image,
						(self.image.get_width() - self.twisting_in_width * dt * 100,
						self.image.get_height() - self.twisting_in_height * dt * 100)
						)
			except:
				if self.remove_particle_after_twisting:
					if self.end_command is not None: self.end_command(self)
					world.particles.remove(self)
					return
		if self.x_bias:
			self.x += dt * 25 * self.x_bias if self.x_bias.__class__ in (int, float) else self.x_bias(self)
		if self.y_bias:
			self.y += dt * 25 * self.y_bias if self.y_bias.__class__ in (int, float) else self.y_bias(self)

		if self.rotate is not None:
			image_rect = self.image.get_rect()
			rotated_image = pygame.transform.rotate(self.image, self.rotate)
			rect_copy = image_rect.copy()
			rect_copy.center = rotated_image.get_rect().center
			self.image = rotated_image.subsurface(rect_copy).copy()
			
		if (self.end_x is not None and self.end_y is None and self.end_x - self.end_zone <= self.x <= self.end_x + self.end_zone) or (self.end_y is not None and self.end_x is None and self.end_y - self.end_zone <= self.y <= self.end_y + self.end_zone) or (self.end_x is not None and self.end_y is not None and self.end_x - self.end_zone <= self.x <= self.end_x + self.end_zone and self.end_y - self.end_zone <= self.y <= self.end_y + self.end_zone):
			if self.end_command is not None: self.end_command(self)
			world.particles.remove(self)

		win.blit(self.image, (self.display_mode(self.x, self.y, self.w, self.h)))

		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), (self.display_mode(self.x, self.y, self.w, self.h)[0], self.display_mode(self.x, self.y, self.w, self.h)[1], self.w, self.h), 3)
