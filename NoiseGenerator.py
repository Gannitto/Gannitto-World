import random
from dataclasses import dataclass
from typing import Tuple, Dict
import vnoise
import math

@dataclass
class WorldConfig:
	seed: int = 42
	world_scale: float = 0.005	# Масштаб для шума
	biome_scale: float = 0.005	# Для биомов
	detail_scale: float = 0.02	# Для деталей
	
class NoiseGenerator:
	def __init__(self, seed=None):
		self.seed = seed or random.randint(0, 2**31 - 1)
		self.config = WorldConfig(seed=self.seed)
		
		# Создаем отдельные генераторы с разным сидом вместо параметра base
		self.height_noise = vnoise.Noise(seed=self.seed)
		self.biome_noise = vnoise.Noise(seed=self.seed + 1000)
		self.detail_noise = vnoise.Noise(seed=self.seed + 2000)
		
	def get_height(self, x: float, y: float) -> float:
		"""Основная карта высот (для рельефа)"""
		return self.height_noise.noise2(
			x * self.config.world_scale,
			y * self.config.world_scale,
			octaves=6,
			persistence=0.5,
			lacunarity=2.0
		)
	
	def get_biome_value(self, x: float, y: float) -> float:
		"""Определяет тип биома"""
		raw = self.biome_noise.noise2(
			x * self.config.biome_scale,
			y * self.config.biome_scale,
			octaves=4,
			persistence=0.7,
			lacunarity=2.5
		)

		normalized = (raw + 0.4) / 0.74
		normalized = max(0.0, min(1.0, normalized))
		
		# Чем меньше степень, тем сильнее растягиваются значения около 0.5
		power = 0.7  # Экспериментируйте с этим параметром
		if normalized < 0.5:
			result = 0.5 * (normalized / 0.5) ** power
		else:
			result = 1.0 - 0.5 * ((1.0 - normalized) / 0.5) ** power
		
		result = max(0.0, min(1.0, result))
		return normalized

	def get_detail_value(self, x: float, y: float) -> float:
		"""Мелкие детали для объектов внутри биома"""
		return self.detail_noise.noise2(
			x * self.config.detail_scale,
			y * self.config.detail_scale,
			octaves=3,
			persistence=0.4,
			lacunarity=3.0
		)

class ValueNoiseBiome:
	def __init__(self, seed, grid_size=3):
		self.seed = seed
		self.grid_size = grid_size
		self.grid = {}	# Кэш для значений в узлах сетки
	
	def _get_grid_value(self, gx, gy):
		"""Получает случайное равномерное значение для узла сетки"""
		key = (gx, gy)
		if key not in self.grid:
			# Детерминированное случайное значение для узла
			local_seed = self.seed + gx * 1000003 + gy * 1000033
			random.seed(local_seed)
			self.grid[key] = random.random()  # Равномерное [0, 1)
		return self.grid[key]
	
	def _smoothstep(self, t):
		"""Плавная интерполяция"""
		return t * t * (3 - 2 * t)
	
	def get_biome_value(self, x, y):
		# Масштабируем координаты
		sx = x / self.grid_size * 0.05
		sy = y / self.grid_size * 0.05
		
		# Находим узлы сетки
		gx0 = math.floor(sx)
		gx1 = gx0 + 1
		gy0 = math.floor(sy)
		gy1 = gy0 + 1
		
		# Интерполяционные коэффициенты
		fx = self._smoothstep(sx - gx0)
		fy = self._smoothstep(sy - gy0)
		
		# Получаем значения в узлах (равномерно распределённые)
		v00 = self._get_grid_value(gx0, gy0)
		v01 = self._get_grid_value(gx0, gy1)
		v10 = self._get_grid_value(gx1, gy0)
		v11 = self._get_grid_value(gx1, gy1)
		
		# Билинейная интерполяция
		v0 = v00 + (v10 - v00) * fx
		v1 = v01 + (v11 - v01) * fx
		
		return v0 + (v1 - v0) * fy

biomes = ["Desert", "Field", "Forest", "Swamp", "Taiga"]
biome_noise = ValueNoiseBiome(random.randint(0, 99999))
def get_biome_name(x, y):
	value = biome_noise.get_biome_value(x, y)
	index = int(value * len(biomes))
	if index >= len(biomes):
		index = len(biomes) - 1
	return biomes[index]

generator = NoiseGenerator()
