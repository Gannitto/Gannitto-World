import random
from dataclasses import dataclass
from typing import Tuple, Dict
import vnoise  # Перешли на vnoise

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
		
		return raw#max(0.0, min(1.0, result))

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
