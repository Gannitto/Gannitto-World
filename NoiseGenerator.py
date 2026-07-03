import random
from dataclasses import dataclass
from typing import Tuple, Dict
import vnoise
import math

@dataclass
class WorldConfig:
	seed: int = 42
	world_scale: float = 0.005	# Масштаб для шума
	biome_size: float = 3    	# Для биомов
	detail_scale: float = 0.02	# Для деталей
	
class NoiseGenerator:

	def __init__(self, seed=None):
		self.seed = seed or random.randint(0, 2**31 - 1)
		self.config = WorldConfig(seed=self.seed)
		
		# Отдельные генераторы с разным сидом вместо параметра base
		self.height_noise = vnoise.Noise(seed=self.seed)
		self.detail_noise = vnoise.Noise(seed=self.seed + 1000)

		self.biome_grid = {}
		
	def get_height(self, x: float, y: float) -> float:
		"""Основная карта высот (для рельефа)"""
		return self.height_noise.noise2(
			x * self.config.world_scale,
			y * self.config.world_scale,
			octaves=6,
			persistence=0.5,
			lacunarity=2.0
		)
	
	def get_biome_grid_value(self, gx, gy):
		"""Получает случайное равномерное значение для узла сетки"""
		key = (gx, gy)
		if key not in self.biome_grid:
			random.seed(self.seed + gx * 1000003 + gy * 1000033)
			self.biome_grid[key] = random.random()
		return self.biome_grid[key]
	
	def smoothstep(self, t):
		"""Плавная интерполяция"""
		return t * t * (3 - 2 * t)

	def get_biome_at(self, x, y):
		# Масштабируем координаты
		sx = x / self.config.biome_size * 0.05
		sy = y / self.config.biome_size * 0.05
		
		# Находим узлы сетки
		gx0 = math.floor(sx)
		gx1 = gx0 + 1
		gy0 = math.floor(sy)
		gy1 = gy0 + 1
		
		# Интерполяционные коэффициенты
		fx = self.smoothstep(sx - gx0)
		fy = self.smoothstep(sy - gy0)
		
		# Получаем значения в узлах (равномерно распределённые)
		v00 = self.get_biome_grid_value(gx0, gy0)
		v01 = self.get_biome_grid_value(gx0, gy1)
		v10 = self.get_biome_grid_value(gx1, gy0)
		v11 = self.get_biome_grid_value(gx1, gy1)
		
		# Билинейная интерполяция
		v0 = v00 + (v10 - v00) * fx
		v1 = v01 + (v11 - v01) * fx
		
		return v0 + (v1 - v0) * fy

	def get_detail_value(self, x: float, y: float) -> float:
		"""Мелкие детали для объектов внутри биома"""
		return self.detail_noise.noise2(
			x * self.config.detail_scale,
			y * self.config.detail_scale,
			octaves=3,
			persistence=0.4,
			lacunarity=3.0
		)

generator = NoiseGenerator()

