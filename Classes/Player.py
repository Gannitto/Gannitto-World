import pygame
import random
from Assets import Heart
from Cache import load
import PlayerAnimator
from Translator import t
from Functions import shadow, text, check_collision
from Globals import path, Width, Height, win
from Config import Settings
from Classes.Particle import Particle
from Classes.Object import Object
from PlayerAnimator import PlayerAnimator

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
		self.animation = [None, 0]
		self.changed_character = "Hiro"
		self.animator = PlayerAnimator(self)

		# Игровые параметры
		self.HP = 100
		self.HP_TICK = 90
		self.god_mode = False
		self.pass_through_walls = False # TODO
		self.is_moving = False
		self.rect = pygame.Rect(self.x - 25, self.y - 112, 50, 224)
		self.hovered_object = None
		self.started_break = False
		self.breaking_object_info = None
		self.breaking_object = None
		self.changed_item = None
		self.changed_item_x = 0
		self.changed_item_y = 0
		self.damage_cooldown = 0.3
		self.damage_timer = 0
		
		# Спрайт
		self.load_frames()
		self.image = self.get_current_frame()

		# Цвета для анимаций
		self.eye_color = self.animations["Down"][0].get_at((112, 88))
		
	def load_frames(self):

		directions = ("Down", "Up", "Left", "Right", "Down-left", "Down-right", "Up-left", "Up-right")
		self.animations = {}

		for direction in directions:

			frames = []
			for frame_num in range(1, 7):
				path_to_image = f"{path}Images/Players/{self.changed_character}/Normal/{direction}/{frame_num}.png"
				frame = load(path_to_image, 256)
				if Settings["Display"]["Shadows"]:
					frame = shadow(frame, f"Player {direction} {frame_num}")
				frames.append(frame)
			self.animations[direction] = frames

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

	def collides_with_walls(self, game):
		"""Проверяет, пересекается ли игрок с какой-либо стеной."""
		if self.pass_through_walls:
			return False
		self.rect = pygame.Rect(self.x - 25, self.y - 112, 50, 224)
		return check_collision(self.rect, game)
	
	def update_rect(self):
		self.rect = pygame.Rect(self.x - 25, self.y - 112, 50, 224)

	def move(self, dx, dy, dt, game):
		"""Двигает игрока и обновляет направление"""

		self.is_moving = True

		# Обновление позиции

		self.x += dx * self.speed * dt * 30
		if self.collides_with_walls(game):
			self.x -= dx * self.speed * dt * 30

		self.y += dy * self.speed * dt * 30
		if self.collides_with_walls(game):
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

		self.update_rect()
	
	def stop(self):
		"""Останавливает движение"""
		self.is_moving = False
		self.frame_index = 0
		self.animation_timer = 0
		self.move_timer = 0

	def handle_animations(self, game):

		if self.animation[0] is None:
			
			if random.randint(1, 300) == 1:
				self.animation = ["Close eyes", 0, 16]

		elif self.animation[1] <= self.animation[2]:
			self.animation[1] += 1
		else:
			self.animation = [None, 0]

		self.changed_item_x = 0
		self.changed_item_y = 0
		frame = self.frame_index % len(self.animations[self.direction])

		match self.direction:

			case "Down":

				match frame:
					# 97, 209
					case 0 | 1 | 3 | 4 | 6 | 7:

						self.changed_item_x = -80
						self.changed_item_y = 0

						match self.animation[0]:

							case "Close eyes":

								if self.animation[1] < 9:
									win.fill(self.eye_color, (Width // 2 - 24, Height / 2 - 32, 8, self.animation[1] * 2))
									win.fill(self.eye_color, (Width // 2 + 16, Height / 2 - 32, 8, self.animation[1] * 2))
								else:
									win.fill(self.eye_color, (Width // 2 - 24, Height / 2 - 32, 8, (8 - self.animation[1] + 8) * 2))
									win.fill(self.eye_color, (Width // 2 + 16, Height / 2 - 32, 8, (8 - self.animation[1] + 8) * 2))

						match frame:

							case 1 | 3:
								
								a = pygame.Surface((16, 24))
								a.fill((0, 0, 0))
								a.set_alpha(90)
								# game.world.particles.append(Particle(self.x + 16, self.y + 96, a, end_time=3))

							case 4 | 6:

								a = pygame.Surface((16, 24))
								a.fill((0, 0, 0))
								a.set_alpha(90)
								# game.world.particles.append(Particle(self.x - 32, self.y + 96, a, end_time=3))

					case 2:

						self.changed_item_x = -74
						self.changed_item_y = -16

						match self.animation[0]:

							case "Close eyes":

								if self.animation[1] < 9:
									win.fill(self.eye_color, (Width // 2 - 24, Height / 2 - 24, 8, self.animation[1] * 2))
									win.fill(self.eye_color, (Width // 2 + 16, Height / 2 - 24, 8, self.animation[1] * 2))
								else:
									win.fill(self.eye_color, (Width // 2 - 24, Height / 2 - 24, 8, (8 - self.animation[1] + 8) * 2))
									win.fill(self.eye_color, (Width // 2 + 16, Height / 2 - 24, 8, (8 - self.animation[1] + 8) * 2))

					case 5:

						self.changed_item_x = -94
						self.changed_item_y = -16

						match self.animation[0]:

							case "Close eyes":

								if self.animation[1] < 9:
									win.fill(self.eye_color, (Width // 2 - 24, Height / 2 - 24, 8, self.animation[1] * 2))
									win.fill(self.eye_color, (Width // 2 + 16, Height / 2 - 24, 8, self.animation[1] * 2))
								else:
									win.fill(self.eye_color, (Width // 2 - 24, Height / 2 - 24, 8, (8 - self.animation[1] + 8) * 2))
									win.fill(self.eye_color, (Width // 2 + 16, Height / 2 - 24, 8, (8 - self.animation[1] + 8) * 2))

			case "Left":

				match frame:

					case 0 | 1 | 3 | 4 | 6 | 7:

						self.changed_item_x = -84
						self.changed_item_y = -16

						match self.animation[0]:

							case "Close eyes":

								if self.animation[1] < 9:
									win.fill(self.eye_color, (Width // 2 - 24, Height / 2 - 32, 8, self.animation[1] * 2))
								else:
									win.fill(self.eye_color, (Width // 2 - 24, Height / 2 - 32, 8, (8 - self.animation[1] + 8) * 2))

					case 2:

						self.changed_item_x = -104
						self.changed_item_y = 0

						match self.animation[0]:

							case "Close eyes":

								if self.animation[1] < 9:
									win.fill(self.eye_color, (Width // 2 - 24, Height / 2 - 24, 8, self.animation[1] * 2))
								else:
									win.fill(self.eye_color, (Width // 2 - 24, Height / 2 - 24, 8, (8 - self.animation[1] + 8) * 2))

					case 5:

						self.changed_item_x = -70
						self.changed_item_y = 0

						match self.animation[0]:

							case "Close eyes":

								if self.animation[1] < 9:
									win.fill(self.eye_color, (Width // 2 - 24, Height / 2 - 24, 8, self.animation[1] * 2))
								else:
									win.fill(self.eye_color, (Width // 2 - 24, Height / 2 - 24, 8, (8 - self.animation[1] + 8) * 2))

			case "Right":

				match frame:

					case 0 | 1 | 3 | 4:

						self.changed_item_x = -20
						self.changed_item_y = 0

						match self.animation[0]:

							case "Close eyes":

								if self.animation[1] < 9:
									win.fill(self.eye_color, (Width // 2 + 16, Height / 2 - 32, 8, self.animation[1] * 2))
								else:
									win.fill(self.eye_color, (Width // 2 + 16, Height / 2 - 32, 8, (8 - self.animation[1] + 8) * 2))

					case 2:

						self.changed_item_x = -32
						self.changed_item_y = 0

						match self.animation[0]:

							case "Close eyes":

								if self.animation[1] < 9:
									win.fill(self.eye_color, (Width // 2 + 16, Height / 2 - 24, 8, self.animation[1] * 2))
								else:
									win.fill(self.eye_color, (Width // 2 + 16, Height / 2 - 24, 8, (8 - self.animation[1] + 8) * 2))

					case 5 | 6 | 7:

						self.changed_item_x = -16
						self.changed_item_y = 16

						match self.animation[0]:

							case "Close eyes":

								if self.animation[1] < 9:
									win.fill(self.eye_color, (Width // 2 + 16, Height / 2 - 24, 8, self.animation[1] * 2))
								else:
									win.fill(self.eye_color, (Width // 2 + 16, Height / 2 - 24, 8, (8 - self.animation[1] + 8) * 2))

	def render(self, game, dt):
		frame = self.frame_index % len(self.animations[self.direction])

		center = (Width // 2, Height // 2)
		win.blit(self.image, (center[0] - 128, center[1] - 128))

		# 2. Офсет предмета
		offset = self.animator.item_offset(frame)
		if self.changed_item and offset is not None:
			dx, dy = offset
			win.blit(
				game.inventory.resources[self.changed_item].image,
				(center[0] + dx, center[1] + dy),
			)

		# 3. Анимации
		self.animator.update(dt)
		self.animator.draw_blink(win, frame, center)

		# 4. Отладка
		if Settings["Display"]["Display hitboxes"]:
			pygame.draw.rect(win, (0, 255, 0), (center[0] - 128, center[1] - 128, 256, 256), 2)
			self._draw_debug_rect()

	def _draw_debug_rect(self):
		x = self.rect[0] - self.x + Width // 2
		y = self.y - self.rect[1] - self.rect[3] + Height // 2
		pygame.draw.rect(win, (0, 0, 0), (x, y, self.rect[2], self.rect[3]), 3)

	def damage(self, HP):
		self.HP -= HP
		self.damage_timer = self.damage_cooldown

	def update_health_and_death(self, game, mouse_x, mouse_y):

		if self.god_mode:
			return

		self.HP_TICK += 1
		if self.HP_TICK == 300:
			self.HP_TICK = 0
			if self.HP < 100:
				self.HP += 10

		if self.HP > 100:
			self.HP = 100

		if self.HP < 1:
			self.death(game)

	def death(self, game):

			for item in game.inventory.whole_inventory:
				if item is not None:
					for _ in range(item.amount):
						rand_x, rand_y = self.x + random.randint(-300, 300), self.y + random.randint(-300, 300)
						game.world.chunk_manager.get_chunk_at(rand_x, rand_y).items.append(Object(item.name, rand_x, rand_y, item.image_path, add_path=False, pickable=True))
			game.inventory.whole_inventory = [None] * 30
			self.HP = 100
			self.x = 0
			self.y = 0

class Peer(Player):

	def __init__(self, id: str, address: tuple, name: str, last_seen: float, X: int = 0, Y: int = 0, view_distance: int = 1):
		super().__init__()
		self.address = address
		self.name = name
		self.last_seen = last_seen
		self.x = X
		self.y = Y
		self.view_distance = view_distance

	def update_rect(self):
		self.rect = pygame.Rect(self.x - 25, self.y - 112, 50, 224)
	
	def render(self, game, dt):
		"""Отрисовывает игрока на экране"""
		frames = self.animations[self.direction]
		win.blit(self.image, game.world_to_screen(self.x, self.y, 256, 256))
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
			win.blit(game.inventory.resources[self.changed_item].image, game.world_to_screen(self.x + changed_item_x + 128, self.y + changed_item_y - 128, 256, 256))
		text_x, text_y = game.world_to_screen(self.x + 128, self.y + 32, 256, 256)
		text(self.name, text_x, text_y, (255, 255, 255), alignment=True)
		
		if Settings["Display"]["Display hitboxes"]:
			pygame.draw.rect(win, (0, 255, 0), game.world_rect_to_screen(self.x, self.y, 256, 256), 2)
			pygame.draw.rect(win, (0, 0, 0), (self.rect[0] - self.x + Width // 2, self.y - self.rect[1] - self.rect[3] + Height // 2, self.rect[2], self.rect[3]), 3)

