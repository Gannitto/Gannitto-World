from Globals import *
from core.texture_cache import TextureCache
import pygame



class Object:

	def __init__(self,
			  name: str,
			  object_x: int,
			  object_y: int,
			  image_path: str,
			  scale_x: list = (64, 64),
			  image = None,
			  special_flags: str = None,
			  add_path=True,
			  start_time=None,
			  is_solid=False,
			  rect=(),
			  pickable=False):

		"""
		Класс основного объекта игры. Такого, как например дерево.
		Аргументы:
		name - Имя объекта
		object_x - X объекта
		object_y - Y объекта
		image_path - Путь к изображению объекта
		scale_x - На сколько нужно изменить размер изображения объекта
		image - Изображение объекта
		special_flags - Специальные флаги объекта
		add_path - Добавлять ли путь до папки игры к путю до изображения
		start_time - Время, когда был создан объект
		rect - Хитбокс объекта
		"""

		self.object_class = "Object"

		if start_time is None:
			self.start_time = time.time()
		else:
			self.start_time = start_time

		self.name = name
		self.x = object_x
		self.y = object_y

		if image is None:
			if add_path:
				self.image = TextureCache.get(path + image_path, scale_x)
			else:
				self.image = TextureCache.get(image_path, scale_x)
		else:
			self.image = pygame.transform.scale(image, (scale_x[0], scale_x[1]))
		self.image_path = image_path
		self.w = self.image.get_width()
		self.h = self.image.get_height()
		self.special_flags = special_flags
		self.add_path = add_path
		self.scale_x = scale_x
		self.is_solid = is_solid
		self.pickable = pickable

		if rect == ():
			self.rect = pygame.Rect(self.x - self.w / 2, self.y + self.h / 2, self.w, self.h)
		else:
			self.rect = (rect[0] + self.x, rect[1] + self.y, rect[2], rect[3])
	
	def main(self, X, Y):

		if X - Width // 2 - self.w // 2 <= self.x <= X + Width // 2 + self.w // 2 and Y - Height // 2 <= Y + Height // 2:
			win.blit(self.image, (self.x - X + Width // 2 - self.w // 2, Y - self.y + Height // 2 - self.h // 2))

		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), (self.rect[0] - X + Width // 2, Y - self.rect[1] + Height // 2, self.rect[2], self.rect[3]), 3)

	def get_left_pressed(self, player):

		click = pygame.mouse.get_pressed()
		if click[0] and self.x - player.x + Width // 2 - self.image.get_width() // 2 <= mouse_x <= self.x - player.x + Width // 2 + self.w // 2 and player.y - self.y + Height // 2 - self.h // 2 <= mouse_y <= player.y - self.y + Height // 2 + self.h // 2:
			return True
		else:
			return False

	def get_right_pressed(self, player):

		click = pygame.mouse.get_pressed()
		if click[2] == 1 and self.x - player.x + Width // 2 - self.image.get_width() // 2 <= mouse_x <= self.x - player.x + Width // 2 + self.w // 2 and player.y - self.y + Height // 2 - self.h // 2 <= mouse_y <= player.y - self.y + Height // 2 + self.h // 2:
			return True
		else:
			return False
	
	def __getstate__(self):
		
		state = self.__dict__.copy()
		del state["image"]
		return state

	def __setstate__(self, state):
		
		self.__dict__.update(state)
		if self.add_path:
			self.image = TextureCache.get(path + self.image_path, self.scale_x)
		else:
			self.image = TextureCache.get(self.image_path, self.scale_x)

