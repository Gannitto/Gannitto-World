import pygame
import math
import random
from itertools import product
from Cache import load
from Assets import slime_types, slime_images, red_slime_images, web_texture, butterfly_images, spider_animation_images, spider_red_animation_images
from Functions import check_collision, check_projectiles_collision, text
from Globals import Width, Height, win, path
from Config import Settings
from Classes.Particle import Particle
from Classes.Object import Object

class Mob:
	def __init__(self, x, y, HP, speed, animation_frames, red_animation_frames, drop_items):
		self.x = x
		self.y = y
		self.HP = HP
		self.max_hp = HP
		self.speed = speed
		self.animation_frames = animation_frames
		self.red_animation_frames = red_animation_frames
		self.animation_timer = 0
		self.rect = animation_frames[0].get_rect()
		self.state = "Idle"  # Idle, Wonder, Jumping, Retreat
		self.attack_cooldown = 0
		self.detection_range = 1000
		self.attack_range = 200
		self.damage_cooldown = 0.1
		self.damage_timer = 0
		self.drop_items = drop_items
		
	def update(self, game, dt):
		"""Обновляет состояние моба"""
		self._update_animation(dt)
		self._update_state(game.player)
		self._update_position(game)
		
	def _update_animation(self, dt):
		self.animation_timer += dt * 5
		if self.animation_timer >= 4:
			self.animation_timer = 0
		
	def _update_state(self, player):
		"""Определяет текущее состояние на основе расстояния до игрока"""
		distance = self._get_distance_to(player)
		
		if self.HP <= 0:
			self.state = "Dead"
		elif distance < self.attack_range:
			self.state = "Attacking"
			self._attack(player)
		elif distance < self.detection_range:
			self.state = "Chasing"
		else:
			self.state = "Idle"
			
	def _update_position(self, game):
		"""Обновляет позицию в зависимости от состояния"""
		if self.state == "chasing":
			self._move_towards_player(game)
		elif self.state == "idle":
			self._random_movement(game.world)
			
	def _move_towards_player(self, game):
		"""Движение к игроку с проверкой стен"""
		dx = game.player.x - self.x
		dy = game.player.y - self.y
		distance = math.dist((self.x, self.y), (game.player.x, game.player.y))
		
		if distance > 0:
			# Нормализуем вектор движения
			dx = dx / distance * self.speed
			dy = dy / distance * self.speed
			
			# Пробуем движение по X
			new_x = self.x + dx
			if not self._check_collision(new_x, self.y, game):
				self.x = new_x
				
			# Пробуем движение по Y
			new_y = self.y + dy
			if not self._check_collision(self.x, new_y, game):
				self.y = new_y

	def damage(self, game, HP):

		self.HP -= HP
		self.damage_timer = self.damage_cooldown

		game.world.particles.append(Particle(self.x + random.randint(-64, 64), self.y + random.randint(-64, 64), text(str(-HP), 0, 0, (180, 10, 10), max_width=44, max_height=50, return_surface=True), y_bias=3, increased_transparency=30, end_time=0.5))

		if self.HP < 1:
			
			for item_name, min_amount, max_amount in self.drop_items:
				for _ in range(random.randint(min_amount, max_amount)):
					rand_x, rand_y = self.x + random.randint(-self.rect[2] // 2, self.rect[2] // 2), self.y + random.randint(-self.rect[3] // 2, self.rect[3] // 2)
					game.world.chunk_manager.get_chunk_at(rand_x, rand_y).items.append(Object(item_name, rand_x, rand_y, f"Images/Items/{item_name}.png", pickable=True))
			game.world.mobs.remove(self)

class Slime(Mob):
	
	def __init__(self, x, y):

		self.slime_type = random.choice(slime_types)
		self.name = "Slime"
		
		super().__init__(
			x=x, y=y,
			HP=50,
			speed=random.randint(300, 400),
			animation_frames=slime_images[self.slime_type],
			red_animation_frames=red_slime_images[self.slime_type],
			drop_items=(("Blue slime" if self.slime_type == 1 else "Pink slime", 1, 3),)
		)

		self.state = "Wander"

		self.wander_radius = 1000
		self.wander_angle = random.uniform(0, 2 * math.pi)
		self.wander_distance = random.uniform(100, self.wander_radius)
		self.wander_timer = 0
		self.wander_change_interval = 1
		self.rect = pygame.Rect(self.x - 50, self.y - 50, 100, 100)

		# Параметры атаки
		self.attack_cooldown = 0
		self.attack_charge_time = 30
		self.charge_timer = 0
		self.jump_speed = 3000  # Скорость прыжка
		self.retreat_speed = 3000	# Скорость отскока
		self.attack_range = 150  # Дистанция атаки
		self.detection_range = 1000	# Дистанция обнаружения
		
		# Состояние прыжка
		self.start_x = x
		self.start_y = y
		self.target_x = x
		self.target_y = y
		
		# Флаг урона
		self.damage_dealt = False
	
	def update(self, game, dt):

		self._update_animation(dt)
		
		if self.HP < 16 and self.speed < 8:
			self.speed += 10  # Ускорение при низком HP
	
		self.attack_cooldown = max(0, self.attack_cooldown - dt * 30)
		self.damage_timer = max(0, self.damage_timer - dt)
		self.check_projectiles(game)

		match self.state:
			case "Wander": self._handle_wander(game, dt)
			case "Prepare attak": self._handle_prepare_attack(game.player, game.world, dt)
			case "Jumping": self._handle_jumping(game, dt)
			case "Retreat": self._handle_retreat(game, dt)
	
	def check_projectiles(self, game):

		self.rect = pygame.Rect((self.x, self.y - 64, 128, 128))

		if check_projectiles_collision(self.rect, game.world):
			self.damage(game, 15)

	def _handle_wander(self, game, dt):

		"""Блуждание вокруг игрока"""

		distance = math.dist((self.x, self.y), (game.player.x, game.player.y))
		if (distance < self.detection_range and 
			self.attack_cooldown <= 0 and
			random.random() < 0.02):  # 2% шанс начать атаку
			self.state = "Prepare attak"
			self.charge_timer = self.attack_charge_time
			self.start_x = self.x
			self.start_y = self.y
			return
			
		# Случайное блуждание по окружности вокруг игрока
		self.wander_timer += dt
		
		# Меняем направление через определенные интервалы
		if self.wander_timer >= self.wander_change_interval:
			self.wander_timer = 0
			self.wander_angle += random.uniform(-math.pi/4, math.pi/4)
			self.wander_distance = random.uniform(150, self.wander_radius)
			
		# Целевая точка для блуждания
		target_x = game.player.x + math.cos(self.wander_angle) * self.wander_distance
		target_y = game.player.y + math.sin(self.wander_angle) * self.wander_distance
		
		# Движение к целевой точке
		dx = target_x - self.x
		dy = target_y - self.y
		dist = math.dist((self.x, self.y), (target_x, target_y))
		
		if dist > 10:  # Если не достигли цели
			move_x = dx / dist * self.speed * dt
			move_y = dy / dist * self.speed * dt
			
			# Проверка стен
			if not self._check_collision(self.x + move_x, self.y, game):
				self.x += move_x
			if not self._check_collision(self.x, self.y + move_y, game):
				self.y += move_y
				
	def _handle_prepare_attack(self, player, world, dt):
		"""Подготовка к прыжку (прицеливание)"""
		self.charge_timer -= dt * 60
		
		# Слизень слегка дрожит в процессе подготовки
		if int(self.charge_timer) % 4 < 2:
			self.y -= 3
		else:
			self.y += 3
			
		if self.charge_timer <= 0:
			self.state = "Jumping"
			self.target_x = player.x
			self.target_y = player.y
			self.damage_dealt = False
			self.start_x = self.x
			self.start_y = self.y
			
	def _handle_jumping(self, game, dt):
		"""Прыжок на игрока"""
		# Движение к цели
		dx = self.target_x - self.x
		dy = self.target_y - self.y
		dist = math.dist((self.x, self.y), (self.target_x, self.target_y))
		
		if dist > 1:
			# Движение к цели
			move_x = dx / dist * self.jump_speed * dt
			move_y = dy / dist * self.jump_speed * dt
			
			# Проверяем стены
			if not self._check_collision(self.x + move_x, self.y, game):
				self.x += move_x
			if not self._check_collision(self.x, self.y + move_y, game):
				self.y += move_y
				
			# Эффект прыжка - немного подпрыгиваем вверх
			jump_height = math.sin((1 - dist / (math.sqrt((self.x - self.target_x)**2 + (self.y - self.target_y)**2))) * math.pi) * 20
			self._jump_offset = -jump_height
			
			# Наносим урон, если достигли игрока
			if dist < 50 and not self.damage_dealt:
				self._attack(game.player)
				self.damage_dealt = True
				self.state = "Retreat"
				
		else:
			# Достигли цели - отскок назад
			self.state = "Retreat"
			self._jump_offset = 0
			
			# TODO Создать частицы при столкновении
			
	def _handle_retreat(self, game, dt):
		"""Отскок на начальную позицию"""
		# Движение обратно к начальной позиции
		dx = self.start_x - self.x
		dy = self.start_y - self.y
		dist = math.dist((self.x, self.y), (self.start_x, self.start_y))
		
		if dist > 10:
			move_x = dx / dist * self.retreat_speed * dt
			move_y = dy / dist * self.retreat_speed * dt
			
			if not self._check_collision(self.x + move_x, self.y, game):
				self.x += move_x
			if not self._check_collision(self.x, self.y + move_y, game):
				self.y += move_y
		else:
			# Вернулись на место
			self.x = self.start_x
			self.y = self.start_y
			self.state = "Wander"

	def _attack(self, player):
		"""Атака игрока"""
		if not player.god_mode and self.attack_cooldown <= 0:
			if pygame.Rect(self.x - 50, self.y + 50, 100, 100).colliderect(pygame.Rect(player.x - 100, player.y + 100, 200, 200)):
				player.damage(10)
		self.attack_cooldown = 100

	def _check_collision(self, x, y, game):
		"""Проверка столкновения со стенами"""
		self.rect = pygame.Rect(x - 50, y - 50, 100, 100)
		return check_collision(self.rect, game)

	def draw(self, game):
		"""Отрисовка слизня"""
		screen_x = self.x - game.player.x + Width // 2 - 64
		screen_y = game.player.y - self.y + Height // 2 - 64
		
		frame_index = int(self.animation_timer) % 5
		frame = self.red_animation_frames[frame_index] if self.damage_timer > 0 else self.animation_frames[frame_index]
		
		win.blit(frame, (screen_x, screen_y))
		
		if Settings["Display"]["Display hitboxes"]:
			pygame.draw.rect(win, (0, 0, 0), (screen_x, screen_y - 8, 128, 128), 3)

	def __getstate__(self):
		
		state = self.__dict__.copy()
		del state["animation_frames"]
		del state["red_animation_frames"]
		return state

	def __setstate__(self, state):
		
		self.__dict__.update(state)
		self.animation_frames = slime_images[self.slime_type]
		self.red_animation_frames = red_slime_images[self.slime_type]

class Spider(Mob):
	
	def __init__(self, x, y):

		self.name = "Spider"
		self.direction = "Right"
		self.x = x
		self.y = y
		self.rect = pygame.Rect(self.x - 50, self.y - 50, 100, 100)
		
		super().__init__(
			x=x, y=y,
			HP=50,
			speed=random.randint(500, 1000),
			animation_frames=list(spider_animation_images.values()),
			red_animation_frames=list(spider_red_animation_images.values()),
			drop_items=(("Thread", 1, 2),)
		)
		
		self.animation_images = spider_animation_images
		self.red_animation_images = spider_red_animation_images
		self.state = "Going towards player"

		# Параметры атаки
		self.attack_cooldown = 0
		self.attack_charge_time = 1
		self.attack_range = 150  # Дистанция атаки
		self.shoot_range = 900
		self.shoot_cooldown = 0
		self.shoot_charge_time = 3
		self.shoot_prepare_charge_time = 0.5
		self.shoot_charge_timer = 0
		self.detection_range = 1000	# Дистанция обнаружения
		
		# Флаг урона
		self.damage_dealt = False
	
	def update(self, game, dt):

		if self.HP < 16 and self.speed < 8:
			self.speed += 10  # Ускорение при низком HP
		
		self.attack_cooldown = max(0, self.attack_cooldown - dt)
		self.shoot_cooldown = max(0, self.shoot_cooldown - dt)
		self.damage_timer = max(0, self.damage_timer - dt)
		self.check_projectiles(game)

		distance = math.dist((self.x, self.y), (game.player.x, game.player.y))

		match self.state:
			case "Attacking": self.state = "Going towards player"
			case "Prepare shoot": self._handle_prepare_shoot(game.player, game.world, dt)
			case "Going towards player": self._handle_go_towards_player(game, dt)
		
	def check_projectiles(self, game):

		self.rect = pygame.Rect((self.x, self.y - 128, 256, 256))

		if check_projectiles_collision(self.rect, game.world):
			self.damage(game, 15)

	def _handle_prepare_shoot(self, player, world, dt):
		"""Подготовка к атаке паутиной (прицеливание)"""
		self.shoot_charge_timer -= dt
		
		# Паук слегка дрожит в процессе подготовки
		if self.shoot_charge_timer % 4 < 2:
			self.y -= 2
		else:
			self.y += 2
			
		if self.shoot_charge_timer <= 0:
			self.shoot_cooldown = self.shoot_charge_time
			dx = player.x - self.x
			dy = player.y - self.y
			dist = math.dist((self.x, self.y), (player.x, player.y))
			move_x = dx / dist * 100
			move_y = dy / dist * 100
			world.particles.append(Particle(self.x, self.y, pygame.transform.rotate(web_texture, -math.degrees(math.atan2(-move_y, move_x))), move_x, move_y, del_self_condition=lambda particle: (pygame.Rect(particle.x - 32, particle.y + 32, 64, 64).colliderect(pygame.Rect(player.x - 100, player.y + 100, 200, 200))), end_time=1)) # TODO наложить эффект замедления
			self.state = "Attacking"

	def _handle_go_towards_player(self, game, dt):
		
		dx = game.player.x - self.x
		dy = game.player.y - self.y
		dist = math.dist((self.x, self.y), (game.player.x, game.player.y))

		if dist <= self.detection_range:
			if dist > 100:
				# Движение к цели
				move_x = dx / dist * self.speed * dt
				move_y = dy / dist * self.speed * dt
				if not self._check_collision(self.x + move_x, self.y, game):
					self.x += move_x
					if move_x > 0: self.direction = "Right"
					else: self.direction = "Left"
				if not self._check_collision(self.x, self.y + move_y, game):
					self.y += move_y

			else:
				self._attack(game.player)
			
			if dist <= self.shoot_range and self.shoot_cooldown <= 0:
				self.shoot_charge_timer = self.shoot_prepare_charge_time
				self.state = "Prepare shoot"
			
	def _attack(self, player):
		"""Атака игрока"""
		if not player.god_mode and self.attack_cooldown <= 0:
			self.state = "Attacking"
			if pygame.Rect(self.x - 50, self.y + 50, 100, 100).colliderect(pygame.Rect(player.x - 100, player.y + 100, 200, 200)):
				player.damage(10)
			self.attack_cooldown = self.attack_charge_time

	def _check_collision(self, x, y, game):
		"""Проверка столкновения со стенами"""
		self.rect = pygame.Rect(x - 50, y - 50, 100, 100)
		return check_collision(self.rect, game)
		
	def draw(self, game, show_hitbox=False):
		"""Отрисовка паука"""
		screen_x = self.x - game.player.x + Width // 2 - 128
		screen_y = game.player.y - self.y + Height // 2 - 128
		
		if self.state == "Attacking":
			frame = self.red_animation_images[self.direction + " attack"] if self.damage_timer > 0 else self.animation_images[self.direction + " attack"]
		else:
			frame = self.red_animation_images[self.direction] if self.damage_timer > 0 else self.animation_images[self.direction]

		win.blit(frame, (screen_x, screen_y))
		
		if show_hitbox:
			pygame.draw.rect(win, (0, 0, 0), (screen_x, screen_y - 8, 128, 128), 3)

	def __getstate__(self):
		
		state = self.__dict__.copy()
		del state["animation_frames"]
		del state["red_animation_frames"]
		del state["animation_images"]
		del state["red_animation_images"]
		return state

	def __setstate__(self, state):
		
		self.__dict__.update(state)
		self.animation_frames = list(spider_animation_images.values())
		self.red_animation_frames = list(spider_red_animation_images.values())
		self.animation_images = spider_animation_images
		self.red_animation_images = spider_red_animation_images

class Butterfly:

	def __init__(self, mob_x: int, mob_y: int):

		self.name = "Butterfly"
		self.x = mob_x
		self.y = mob_y
		self.rand_mob = random.randint(1, 2)
		self.animation_images = butterfly_images
		self.HP = 10
		self.animation_count = -1
		self.reset_offset = 0
		self.offset_x = random.randint(-3000, 3000)
		self.offset_y = random.randint(-3000, 3000)
	
	def main(self, player, world):

		self.animation_count += 1
		if self.animation_count == 8:
			self.animation_count = 0
		
		if self.reset_offset == 0:
			self.reset_offset = random.randint(120, 150)
			self.offset_x = random.randint(-3000, 3000)
			self.offset_y = random.randint(-3000, 3000)
		else:
			self.reset_offset -= 1
		
		if player.x + self.offset_x > self.x:

			a = True
			for i in world.visible_walls.values():
				if i.x - 300 < self.x < i.x + 256 and i.y - 256 < self.y < i.y + 256:
					a = False
					break
			   
				if a:
					self.x += 1

		elif player.x + self.offset_x < self.x:

			a = True
			for i in world.visible_walls.values():
				if i.x - 256 < self.x < i.x + 300 and i.y - 256 < self.y < i.y + 256:
					a = False
					break

			if a:
				self.x -= 1
		
		if player.y + self.offset_y > self.y:

			a = True
			for i in world.visible_walls.values():
				if i.x - 256 < self.x < i.x + 256 and i.y - 300 < self.y < i.y + 256:
					a = False
					break

			if a:
				self.y += 1

		elif player.y + self.offset_y < self.y - player.y:

			a = True
			for i in world.visible_walls.values():
				if i.x - 256 < self.x < i.x + 256 and i.y - 256 < self.y < i.y + 300:
					a = False
					break

			if a:
				self.y -= 1
		
		win.blit(self.animation_images[(self.animation_count - self.animation_count % 2) // 2], (self.x - player.x + Width // 2 - 64, player.y - self.y + Height // 2 - 32))
		if Settings["Display"]["Display hitboxes"]:
			pygame.draw.rect(win, (0, 0, 0), (self.x - player.x + Width // 2 - 32, player.y - self.y + Height // 2 - 32, 64, 64), 3)
