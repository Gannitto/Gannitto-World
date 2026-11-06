import pygame
import math
import random
from Cache import load
from Assets import slime_types, slime_images, web_texture, butterfly_images
from Functions import check_collision
from Globals import Width, Height, win, Settings, path
from Classes.Particle import Particle

class Mob:
	def __init__(self, x, y, HP, speed, animation_frames):
		self.x = x
		self.y = y
		self.HP = HP
		self.max_hp = HP
		self.speed = speed
		self.animation_frames = animation_frames
		self.animation_timer = 0
		self.rect = animation_frames[0].get_rect()
		self.state = "Idle"  # Idle, Wonder, Jumping, Retreat
		self.attack_cooldown = 0
		self.detection_range = 1000
		self.attack_range = 200
		
	def update(self, game, dt):
		"""Обновляет состояние моба"""
		self._update_animation(dt)
		self._update_state(game.player)
		self._update_position(game.world)
		
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
			
	def _update_position(self, world):
		"""Обновляет позицию в зависимости от состояния"""
		if self.state == "chasing":
			self._move_towards_player(world)
		elif self.state == "idle":
			self._random_movement(world)
			
	def _move_towards_player(self, world, player):
		"""Движение к игроку с проверкой стен"""
		dx = player.x - self.x
		dy = player.y - self.y
		distance = math.dist((self.x, self.y), (player.x, player.y))
		
		if distance > 0:
			# Нормализуем вектор движения
			dx = dx / distance * self.speed
			dy = dy / distance * self.speed
			
			# Пробуем движение по X
			new_x = self.x + dx
			if not self._check_collision(new_x, self.y, world):
				self.x = new_x
				
			# Пробуем движение по Y
			new_y = self.y + dy
			if not self._check_collision(self.x, new_y, world):
				self.y = new_y

class Slime(Mob):
	
	def __init__(self, x, y):

		slime_type = random.choice(slime_types)
		self.name = "Slime"
		
		super().__init__(
			x=x, y=y,
			HP=50,
			speed=random.randint(10, 20),
			animation_frames=slime_images[slime_type]
		)
		
		self.slime_type = slime_type
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
		self.jump_speed = 50  # Скорость прыжка
		self.retreat_speed = 50	# Скорость отскока
		self.attack_range = 150  # Дистанция атаки
		self.detection_range = 1000	# Дистанция обнаружения
		
		# Состояние прыжка
		self.start_x = x
		self.start_y = y
		self.target_x = x
		self.target_y = y
		
		# Флаг урона
		self.damage_dealt = False
	
	def update(self, player, world, dt):

		self._update_animation(dt)
		
		if self.HP < 16 and self.speed < 8:
			self.speed += 10  # Ускорение при низком HP
	
		self.attack_cooldown = max(0, self.attack_cooldown - dt * 30)

		match self.state:
			case "Wander": self._handle_wander(player, world, dt)
			case "Prepare attak": self._handle_prepare_attack(player, world, dt)
			case "Jumping": self._handle_jumping(player, world)
			case "Retreat": self._handle_retreat(player, world)
	
	def _handle_wander(self, player, world, dt):

		"""Блуждание вокруг игрока"""

		distance = math.dist((self.x, self.y), (player.x, player.y))
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
		target_x = player.x + math.cos(self.wander_angle) * self.wander_distance
		target_y = player.y + math.sin(self.wander_angle) * self.wander_distance
		
		# Движение к целевой точке
		dx = target_x - self.x
		dy = target_y - self.y
		dist = math.dist((self.x, self.y), (target_x, target_y))
		
		if dist > 10:  # Если не достигли цели
			move_x = dx / dist * self.speed
			move_y = dy / dist * self.speed
			
			# Проверка стен
			if not self._check_collision(self.x + move_x, self.y, world):
				self.x += move_x
			if not self._check_collision(self.x, self.y + move_y, world):
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
			
	def _handle_jumping(self, player, world):
		"""Прыжок на игрока"""
		# Движение к цели
		dx = self.target_x - self.x
		dy = self.target_y - self.y
		dist = math.dist((self.x, self.y), (self.target_x, self.target_y))
		
		if dist > 5:
			# Движение к цели
			move_x = dx / dist * self.jump_speed
			move_y = dy / dist * self.jump_speed
			
			# Проверяем стены
			if not self._check_collision(self.x + move_x, self.y, world):
				self.x += move_x
			if not self._check_collision(self.x, self.y + move_y, world):
				self.y += move_y
				
			# Эффект прыжка - немного подпрыгиваем вверх
			jump_height = math.sin((1 - dist / (math.sqrt((self.x - self.target_x)**2 + (self.y - self.target_y)**2))) * math.pi) * 20
			self._jump_offset = -jump_height
			
			# Наносим урон, если достигли игрока
			if dist < 50 and not self.damage_dealt:
				self._attack(player)
				self.damage_dealt = True
				self.state = "Retreat"
				
		else:
			# Достигли цели - отскок назад
			self.state = "Retreat"
			self._jump_offset = 0
			
			# TODO Создать частицы при столкновении
			
	def _handle_retreat(self, player, world):
		"""Отскок на начальную позицию"""
		# Движение обратно к начальной позиции
		dx = self.start_x - self.x
		dy = self.start_y - self.y
		dist = math.dist((self.x, self.y), (self.start_x, self.start_y))
		
		if dist > 10:
			move_x = dx / dist * self.retreat_speed
			move_y = dy / dist * self.retreat_speed
			
			if not self._check_collision(self.x + move_x, self.y, world):
				self.x += move_x
			if not self._check_collision(self.x, self.y + move_y, world):
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
				player.HP -= 10
				player.HP_animation_tick = 1
		self.attack_cooldown = 100

	def _check_collision(self, x, y, world):
		"""Проверка столкновения со стенами"""
		self.rect = pygame.Rect(x - 50, y - 50, 100, 100)
		return check_collision(self.rect, world)

	def draw(self, player):
		"""Отрисовка слизня"""
		screen_x = self.x - player.x + Width // 2 - 64
		screen_y = player.y - self.y + Height // 2 - 64
		
		frame_index = int(self.animation_timer) % 5
		frame = self.animation_frames[frame_index]
		
		win.blit(frame, (screen_x, screen_y))
		
		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), (screen_x, screen_y - 8, 128, 128), 3)

	def __getstate__(self):
		
		state = self.__dict__.copy()
		del state["animation_frames"]
		return state

	def __setstate__(self, state):
		
		self.__dict__.update(state)
		self.animation_frames = slime_images[self.slime_type]

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
			animation_frames=[
				load(path + "Images/Mobs/Spider.png", 256),
				load(path + "Images/Mobs/Spider 2.png", 256)]
		)
		
		self.animation_images = {
				"Left": load(path + "Images/Mobs/Spider.png", 256),
				"Left attack": load(path + "Images/Mobs/Spider attack.png", 256),
				"Right": load(path + "Images/Mobs/Spider 2.png", 256),
				"Right attack": load(path + "Images/Mobs/Spider 2 attack.png", 256)
				}
		
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
	
	def update(self, player, world, dt):

		if self.HP < 16 and self.speed < 8:
			self.speed += 10  # Ускорение при низком HP
		
		self.attack_cooldown = max(0, self.attack_cooldown - dt)
		self.shoot_cooldown = max(0, self.shoot_cooldown - dt)

		distance = math.dist((self.x, self.y), (player.x, player.y))

		match self.state:
			case "Attacking": self.state = "Going towards player"
			case "Prepare shoot": self._handle_prepare_shoot(player, world)
			case "Going towards player": self._handle_go_towards_player(player, world, dt)
		
	def _handle_prepare_shoot(self, player, world):
		"""Подготовка к атаке паутиной (прицеливание)"""
		self.shoot_charge_timer -= 1
		
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

	def _handle_go_towards_player(self, player, world, dt):
		
		dx = player.x - self.x
		dy = player.y - self.y
		dist = math.dist((self.x, self.y), (player.x, player.y))

		if dist <= self.detection_range:
			if dist > 100:
				# Движение к цели
				move_x = dx / dist * self.speed * dt
				move_y = dy / dist * self.speed * dt
				if not self._check_collision(self.x + move_x, self.y, world):
					self.x += move_x
					if move_x > 0: self.direction = "Right"
					else: self.direction = "Left"
				if not self._check_collision(self.x, self.y + move_y, world):
					self.y += move_y

			else:
				self._attack(player)
			
			if dist <= self.shoot_range and self.shoot_cooldown <= 0:
				self.shoot_charge_timer = self.shoot_prepare_charge_time
				self.state = "Prepare shoot"
			
	def _attack(self, player):
		"""Атака игрока"""
		if not player.god_mode and self.attack_cooldown <= 0:
			self.state = "Attacking"
			if pygame.Rect(self.x - 50, self.y + 50, 100, 100).colliderect(pygame.Rect(player.x - 100, player.y + 100, 200, 200)):
				player.HP -= 10
				player.HP_animation_tick = 1
			self.attack_cooldown = self.attack_charge_time

	def _check_collision(self, x, y, world):
		"""Проверка столкновения со стенами"""
		self.rect = pygame.Rect(x - 50, y - 50, 100, 100)
		return check_collision(self.rect, world)
		
	def draw(self, player, show_hitbox=False):
		"""Отрисовка паука"""
		screen_x = self.x - player.x + Width // 2 - 128
		screen_y = player.y - self.y + Height // 2 - 128
		
		if self.state == "Attacking":
			frame = self.animation_images[self.direction + " attack"]
		else:
			frame = self.animation_images[self.direction]

		win.blit(frame, (screen_x, screen_y))
		
		if show_hitbox:
			pygame.draw.rect(win, (0, 0, 0), (screen_x, screen_y - 8, 128, 128), 3)

	def __getstate__(self):
		
		state = self.__dict__.copy()
		del state["animation_frames"]
		del state["animation_images"]
		return state

	def __setstate__(self, state):
		
		self.__dict__.update(state)
		self.animation_frames=(
			load(path + "Images/Mobs/Spider.png", 256),
			load(path + "Images/Mobs/Spider 2.png", 256)
		)
		self.animation_images = {
				"Left": load(path + "Images/Mobs/Spider.png", 256),
				"Left attack": load(path + "Images/Mobs/Spider attack.png", 256),
				"Right": load(path + "Images/Mobs/Spider 2.png", 256),
				"Right attack": load(path + "Images/Mobs/Spider 2 attack.png", 256)
				}

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
		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), (self.x - player.x + Width // 2 - 32, player.y - self.y + Height // 2 - 32, 64, 64), 3)
