import pygame

class TextureCache:
	_textures = {}
	
	@classmethod
	def get(cls, path, scale=None):
		key = (path, scale)
		if key not in cls._textures:
			image = pygame.image.load(path)
			if scale:
				image = pygame.transform.scale(image, scale)
			cls._textures[key] = image
		return cls._textures[key]

class BaseEnemy:
	def __init__(self, x, y, HP, speed, animation_frames):
		self.x = x
		self.y = y
		self.HP = HP
		self.max_hp = HP
		self.speed = speed
		self.animation_frames = animation_frames
		self.animation_count = 0
		self.rect = animation_frames[0].get_rect()
		self.state = "Idle"  # Idle, Wonder, Jumping, Retreat
		self.attack_cooldown = 0
		self.detection_range = 1000
		self.attack_range = 200
		
	def update(self, player, world):
		"""Обновляет состояние моба"""
		self._update_animation()
		self._update_state(player, world)
		self._update_position(world)
		
	def _update_animation(self):
		self.animation_count = (self.animation_count + 1) % 20
		
	def _update_state(self, player, world):
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
			
	def _move_towards_player(self, player, world):
		"""Движение к игроку с проверкой стен"""
		dx = player.x - self.x
		dy = player.y - self.y
		distance = sqrt(dx**2 + dy**2)
		
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

