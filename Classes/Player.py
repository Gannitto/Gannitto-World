import pygame
from Cache import load
from Inventory import inventory
from Functions import shadow, text
from Globals import path, Settings, Width, Height, win

class Player:

	def __init__(self, X=0, Y=0):

		self.x = X
		self.y = Y
		self.speed = 50
		
		# Анимация
		self.direction = "Down"
		self.frame_index = 0
		self.animation_speed = 0.05  # Скорость анимации (секунды между кадрами)
		self.animation_timer = 0
		self.move_timer = 0
		self.costum = 0
		directions = ("Down", "Up", "Left", "Right", "Down-left", "Down-right", "Up-left", "Up-right")
		self.animations = {}
		self.animation = [None, 0]
		
		for direction in directions:

			frames = []
			for frame_num in range(1, 7):
				path_to_image = f"{path}Images/Players/Hiro/Normal/{direction}/{frame_num}.png"
				frames.append(load(path_to_image, 256))	
			self.animations[direction] = frames

		# Игровые параметры
		self.HP = 100
		self.HP_TICK = 90
		self.HP_animation_tick = 0
		self.effects = []
		self.god_mode = False
		self.pass_through_walls = False # TODO
		self.is_moving = False
		self.rect = pygame.Rect(self.x - 25, self.y - 112, 50, 224)
		self.hovered_object = None
		self.started_break = False
		self.breaking_object_info = None
		self.breaking_object = None
		self.changed_item = None
		
		# Текущий спрайт
		self.image = self.get_current_frame()
		
	def get_current_frame(self):
		"""Возвращает текущий кадр анимации"""
		frames = self.animations[self.direction]
		return frames[self.frame_index % len(frames)]
	
	def update_animation(self, dt):
		"""Обновляет анимацию на основе времени"""
		if self.is_moving:
			self.animation_timer += dt
			
			# Если прошло достаточно времени, кадр меняется
			if self.animation_timer >= self.animation_speed:
				self.animation_timer = 0
				self.frame_index += 1
		
		self.image = self.get_current_frame()

	def collides_with_walls(self, check_collision, world):
		"""Проверяет, пересекается ли игрок с какой-либо стеной."""
		if self.pass_through_walls:
			return False
		self.rect = pygame.Rect(self.x - 25, self.y - 112, 50, 224)
		return check_collision(self.rect, world)

	def move(self, dx, dy, dt, check_collision, world):
		"""Двигает игрока и обновляет направление"""

		self.is_moving = True

		# Обновление позиции

		self.x += dx * self.speed * dt * 30
		if self.collides_with_walls(check_collision, world):
			self.x -= dx * self.speed * dt * 30

		self.y += dy * self.speed * dt * 30
		if self.collides_with_walls(check_collision, world):
			self.y -= dy * self.speed * dt * 30
		
		# Определение направления
		if dx > 0 and dy == 0:
			self.direction = "Right"
		elif dx < 0 and dy == 0:
			self.direction = "Left"
		elif dy > 0 and dx == 0:
			self.direction = "Up"
		elif dy < 0 and dx == 0:
			self.direction = "Down"
		elif dx > 0 and dy > 0:
			self.direction = "Up-right"
		elif dx < 0 and dy > 0:
			self.direction = "Up-left"
		elif dx > 0 and dy < 0:
			self.direction = "Down-right"
		elif dx < 0 and dy < 0:
			self.direction = "Down-left"
	
	def stop(self):
		"""Останавливает движение"""
		self.is_moving = False
		self.frame_index = 0
		self.animation_timer = 0
		self.move_timer = 0
	
	def render(self):
		"""Отрисовывает игрока на экране"""
		frames = self.animations[self.direction]
		win.blit(shadow(self.image, f"Player {self.direction} {self.frame_index % len(frames)}"), (Width / 2 - 128, Height / 2 - 128))
		
		if Settings["Display"][3]:
			self.rect = pygame.Rect(self.x - 25, self.y - 112, 50, 224)
			pygame.draw.rect(win, (0, 255, 0), (Width / 2 - 128, Height / 2 - 128, 256, 256), 2)
			pygame.draw.rect(win, (0, 0, 0), (self.rect[0] - self.x + Width // 2, self.y - self.rect[1] - self.rect[3] + Height // 2, self.rect[2], self.rect[3]), 3)

class Peer(Player):

	def __init__(self, id: str, address: tuple, name: str, last_seen: float, X: int = 0, Y: int = 0, view_distance: int = 1):
		super().__init__()
		self.address = address
		self.name = name
		self.last_seen = last_seen
		self.x = X
		self.y = Y
		self.view_distance = view_distance
	
	def render(self, world_to_screen, world_rect_to_screen):
		"""Отрисовывает игрока на экране"""
		frames = self.animations[self.direction]
		win.blit(shadow(self.image, f"Player {self.direction} {self.frame_index % len(frames)}"), world_to_screen(self.x, self.y, 256, 256))
		if self.changed_item is not None and self.direction != "Up":
			changed_item_x = 0
			changed_item_y = 0
			match self.direction:
				case "Down":
					changed_item_x = -80
					changed_item_y = 0
				case "Left":
					changed_item_x = -84
					changed_item_y = 0
				case "Right":
					changed_item_x = -20
					changed_item_y = 0
			win.blit(inventory.resources[self.changed_item].image, world_to_screen(self.x + changed_item_x + 128, self.y + changed_item_y - 128, 256, 256))
		text_x, text_y = world_to_screen(self.x + 128, self.y + 32, 256, 256)
		text(self.name, text_x, text_y, (255, 255, 255), alignment=True)
		
		if Settings["Display"][3]:
			self.rect = pygame.Rect(self.x - 25, self.y - 112, 50, 224)
			pygame.draw.rect(win, (0, 255, 0), world_rect_to_screen(self.x, self.y, 256, 256), 2)
			pygame.draw.rect(win, (0, 0, 0), (self.rect[0] - self.x + Width // 2, self.y - self.rect[1] - self.rect[3] + Height // 2, self.rect[2], self.rect[3]), 3)
