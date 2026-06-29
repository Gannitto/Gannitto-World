#import noise
import random
from dataclasses import dataclass
from typing import Tuple, Dict

@dataclass
class WorldConfig:
	seed: int = 42
	world_scale: float = 0.005	# Масштаб для шума (чем меньше, тем плавнее)
	biome_scale: float = 0.002	# Для биомов (крупнее)
	detail_scale: float = 0.02	# Для деталей внутри биомов
	
class WorldGenerator:
	def __init__(self, seed=None):
		self.seed = seed or random.randint(0, 2**31 - 1)
		self.config = WorldConfig(seed=self.seed)
		
	def get_height(self, x: float, y: float) -> float:
		"""Основная карта высот (для рельефа)"""
		return noise.pnoise2(
			x * self.config.world_scale,
			y * self.config.world_scale,
			octaves=6,
			persistence=0.5,
			lacunarity=2.0,
			repeatx=1024,
			repeaty=1024,
			base=self.seed
		)
	
	def get_biome_value(self, x: float, y: float) -> float:
		"""Определяет тип биома"""
		return noise.pnoise2(
			x * self.config.biome_scale,
			y * self.config.biome_scale,
			octaves=4,
			persistence=0.7,
			lacunarity=2.5,
			repeatx=1024,
			repeaty=1024,
			base=self.seed + 1000
		)
	
	def get_detail_value(self, x: float, y: float) -> float:
		"""Мелкие детали для объектов внутри биома"""
		return noise.pnoise2(
			x * self.config.detail_scale,
			y * self.config.detail_scale,
			octaves=3,
			persistence=0.4,
			lacunarity=3.0,
			repeatx=1024,
			repeaty=1024,
			base=self.seed + 2000
		)
