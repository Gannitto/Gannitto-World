class GameTime:

	def __init__(self):

		self.day_duration = 1800  # длительность суток в секундах
		self.time_scale = 1.0	# множитель скорости времени (1=нормально)
		self.current_time = self.day_duration // 2
		self.day_phase = "Day"
		self.day_start = 0.15
		self.day_end = 0.75
		self.twilight_duration = 0.1
		
	def update(self, dt):

		"""Обновление игрового времени"""
		self.current_time += dt * self.time_scale
		if self.current_time >= self.day_duration:
			self.current_time -= self.day_duration
		self._update_day_phase()
	
	def _update_day_phase(self):

		"""Определение фазы дня на основе текущего времени"""

		progress = self.current_time / self.day_duration
		if progress < self.day_start or progress > self.day_end:
			self.day_phase = "night"
		elif progress < self.day_start + self.twilight_duration:
			self.day_phase = "sunrise"
		elif progress > self.day_end - self.twilight_duration:
			self.day_phase = "sunset"
		else:
			self.day_phase = "day"
	
	def get_brightness(self):
		"""Возвращает значение от 0 до 1 для плавного перехода день/ночь"""
		progress = self.current_time / self.day_duration
		
		if progress < self.day_start:
			# Ночь до восхода
			return 0.01
		elif progress < self.day_start + self.twilight_duration:
			# Восход (линейный рост)
			t = (progress - self.day_start) / self.twilight_duration
			return 0.01 + t * t	# квадратичный рост для красивого рассвета
		elif progress < self.day_end - self.twilight_duration:
			return 1
		elif progress < self.day_end:
			# Закат (линейное падение)
			t = (progress - (self.day_end - self.twilight_duration)) / self.twilight_duration
			return 0.01 + (1 - t) * (1 - t)	# квадратичное падение
		else:
			return 0.01
	
	def get_time_of_day(self):
		"""Возвращает строку с текущим временем суток"""
		progress = self.current_time / self.day_duration
		hour = int(progress * 24)  # 0-23 часа
		minute = int((progress * 24 - hour) * 60)
		return f"{hour:02d}:{minute:02d}"
	
	def set_time_speed(self, scale):
		"""Установка скорости времени"""
		self.time_scale = max(0, scale)
	
	def reset_to_day(self):
		"""Сброс времени на начало дня"""
		self.current_time = 0.0
	
	def skip_time(self, seconds):
		"""Добавление времени (для пропуска времени)"""
		self.current_time += seconds
		if self.current_time >= self.day_duration:
			self.current_time -= self.day_duration
