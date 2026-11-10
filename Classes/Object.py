import pygame
import random
import time
from Cache import load
from Functions import crack_surface, destroy_object
from Globals import Width, Height, path, win
from Config import Settings
from Classes.Particle import Particle

class Object:

	def __init__(self,
			  name: str,
			  object_x: int,
			  object_y: int,
			  image_path: str,
			  scale: tuple[int, int] = (64, 64),
			  image = None,
			  special_flags: str = None,
			  add_path=True,
			  start_time=None,
			  is_solid=False,
			  rect=(),
			  pickable=False,
			  breakable=False,
			  max_break=1,
			  breakable_by_hammer=False,
			  drop_items=()):

		"""
		Класс основного объекта игры. Такого, как например дерево.
		Аргументы:
		name - Имя объекта
		object_x - X объекта
		object_y - Y объекта
		image_path - Путь к изображению объекта
		scale - На сколько нужно изменить размер изображения объекта
		image - Изображение объекта
		special_flags - Специальные флаги объекта
		add_path - Добавлять ли путь до папки игры к путю до изображения
		start_time - Время, когда был создан объект
		rect - Хитбокс объекта
		pickable - Можно ли подобрать объект
		breakable - Можно ли сломать объект
		max_break - Сколько нужно ударов чтобы сломать
		breakable_by_hammer - Можно ли моментально сломать объект молотом
		drop_items - Предметы, которые дропаются из объекта (название, мин количество, макс количество)
		"""

		if start_time is None:
			self.start_time = time.time()
		else:
			self.start_time = start_time

		self.name = name
		self.x = object_x
		self.y = object_y

		if image is None:
			if add_path:
				self.image = load(path + image_path, *scale)
			else:
				self.image = load(image_path, *scale)
		else:
			self.image = pygame.transform.scale(image, (scale[0], scale[1]))

		self.image_path = image_path
		self.w = self.image.get_width()
		self.h = self.image.get_height()
		self.special_flags = special_flags
		self.add_path = add_path
		self.scale = scale
		self.is_solid = is_solid
		self.pickable = pickable
		self.breakable = breakable
		self.max_break = max_break
		self.breaked = max_break
		self.breakable_by_hammer = breakable_by_hammer
		self.drop_items = drop_items

		if rect == ():
			self.rect = pygame.Rect(self.x - self.w / 2, self.y - self.h / 2, self.w, self.h)
		else:
			self.rect = pygame.Rect(rect[0] + self.x, rect[1] + self.y, rect[2], rect[3])
	
	def main(self, game, dt):
			
		player = game.player

		if player.hovered_object is None and self.get_hovered(game):
			player.hovered_object = self
			if self.breakable and pygame.mouse.get_pressed()[0]:

				player.breaking_object = self
				if not player.started_break and game.multiplayer:
					game.events.append({"event_type": "object_started_breaking", "x": self.x, "y": self.y, "name": self.name})
				player.started_break = True
				player.breaking_object_info = (self.x, self.y, self.name)
				self.breaked -= dt * 100
				self.image = crack_surface(game.world, Particle, self, (self.max_break - self.breaked) // self.max_break, 8)

				if self.breaked < 1:

					destroy_object(self.image, self.x, self.y, game.world, Particle)
					if game.multiplayer:
						game.events.append({"event_type": "object_removed", "x": self.x, "y": self.y, "name": self.name})
					game.world.chunk_manager.get_chunk_at(self.x, self.y).objects.remove(self)
					
					game.statistics[2] += 1
					for item_name, min_amount, max_amount in self.drop_items:
						for _ in range(random.randint(min_amount, max_amount)):
							rand_x, rand_y = self.x + random.randint(-self.w // 2, self.w // 2), self.y + random.randint(-self.h // 2, self.h // 2)
							game.world.chunk_manager.get_chunk_at(rand_x, rand_y).items.append(Object(item_name, rand_x, rand_y, f"Images/Items/{item_name}.png", pickable=True))
					return

		if player.x - Width // 2 - self.w // 2 <= self.x <= player.x + Width // 2 + self.w // 2 and player.y - Height // 2 - self.h // 2 <= self.y <= player.y + Height // 2 + self.h // 2:
			win.blit(self.image, game.world_to_screen(self.x, self.y, self.w, self.h, player))
		if Settings["Display"]["Display hitboxes"]:
			pygame.draw.rect(win, (0, 0, 0), (*game.world_to_screen(self.rect[0] + self.w // 2, self.rect[1] + self.h // 2, self.rect[2], self.rect[3], player), self.rect[2], self.rect[3]), 3)

	def get_left_pressed(self, mouse_x, mouse_y, player):

		click = pygame.mouse.get_pressed()
		if click[0] and self.x - player.x + Width // 2 - self.image.get_width() // 2 <= mouse_x <= self.x - player.x + Width // 2 + self.w // 2 and player.y - self.y + Height // 2 - self.h // 2 <= mouse_y <= player.y - self.y + Height // 2 + self.h // 2:
			return True
		else:
			return False

	def get_right_pressed(self, mouse_x, mouse_y, player):

		click = pygame.mouse.get_pressed()
		if click[2] == 1 and self.x - player.x + Width // 2 - self.image.get_width() // 2 <= mouse_x <= self.x - player.x + Width // 2 + self.w // 2 and player.y - self.y + Height // 2 - self.h // 2 <= mouse_y <= player.y - self.y + Height // 2 + self.h // 2:
			return True
		else:
			return False

	def get_hovered(self, game):
		return pygame.Rect((*game.world_to_screen(self.rect[0] + self.w // 2, self.rect[1] + self.h // 2, self.rect[2], self.rect[3], game.player), self.rect[2], self.rect[3])).collidepoint(pygame.mouse.get_pos())

	def copy(self):
		return Object(self.name, self.x, self.y, self.image_path, self.scale, self.image, self.special_flags, self.add_path, self.start_time, self.is_solid, self.rect, self.is_solid, self.breakable, self.max_break, self.breakable_by_hammer, self.drop_items)
	
	def __getstate__(self):
		
		state = self.__dict__.copy()
		del state["image"]
		rect = state["rect"]
		state["rect"] = (rect[0], rect[1], rect[2], rect[3])
		return state

	def __setstate__(self, state):
		
		self.__dict__.update(state)
		if self.add_path:
			self.image = load(path + self.image_path, *self.scale)
		else:
			self.image = load(self.image_path, *self.scale)

		self.rect = pygame.Rect(state["rect"][0], state["rect"][1], state["rect"][2], state["rect"][3])
		
