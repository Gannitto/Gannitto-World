from enum import Enum
from typing import Dict, List, Tuple
from dataclasses import dataclass

class BiomeType(Enum):
	GRASSLAND = "grassland"
	FOREST = "forest"
	DESERT = "desert"
	MOUNTAIN = "mountain"
	WATER = "water"
	SWAMP = "swamp"
	SNOW = "snow"
	CAVE = "cave"

@dataclass
class Biome:
	biome_type: BiomeType
	height_range: Tuple[float, float]  # диапазон высот для этого биома
	biome_value_range: Tuple[float, float]	# диапазон для biome_value
	color: Tuple[int, int, int]
	platform_density: float  # плотность платформ
	mob_spawn_chance: float
	objects: Dict[str, float]  # шансы спавна разных объектов
	
	def contains_point(self, height: float, biome_value: float) -> bool:
		"""Проверяет, принадлежит ли точка этому биому"""
		return (self.height_range[0] <= height <= self.height_range[1] and
				self.biome_value_range[0] <= biome_value <= self.biome_value_range[1])

class BiomeManager:
	def __init__(self):
		self.biomes: List[Biome] = []
		self._initialize_biomes()
	
	def _initialize_biomes(self):
		"""Инициализация всех биомов"""
		self.biomes = [
			Biome(
				biome_type=BiomeType.GRASSLAND,
				height_range=(-0.1, 0.3),
				biome_value_range=(-0.2, 0.4),
				color=(100, 200, 100),
				platform_density=0.3,
				mob_spawn_chance=0.02,
				objects={"tree": 0.3, "flower": 0.2, "grass": 0.5}
			),
			Biome(
				biome_type=BiomeType.FOREST,
				height_range=(0.0, 0.4),
				biome_value_range=(0.4, 0.8),
				color=(50, 150, 50),
				platform_density=0.1,
				mob_spawn_chance=0.05,
				objects={"tree": 0.7, "bush": 0.3}
			),
			Biome(
				biome_type=BiomeType.MOUNTAIN,
				height_range=(0.5, 1.0),
				biome_value_range=(-0.5, 0.5),
				color=(150, 150, 150),
				platform_density=0.05,
				mob_spawn_chance=0.01,
				objects={"rock": 0.5, "ore": 0.1}
			),
			Biome(
				biome_type=BiomeType.DESERT,
				height_range=(-0.1, 0.2),
				biome_value_range=(-0.8, -0.4),
				color=(200, 180, 100),
				platform_density=0.15,
				mob_spawn_chance=0.01,
				objects={"cactus": 0.2, "sand": 0.8}
			),
			Biome(
				biome_type=BiomeType.WATER,
				height_range=(-1.0, -0.1),
				biome_value_range=(-1.0, 1.0),
				color=(50, 100, 200),
				platform_density=0.0,
				mob_spawn_chance=0.03,
				objects={}
			),
			Biome(
				biome_type=BiomeType.SNOW,
				height_range=(0.6, 1.0),
				biome_value_range=(0.6, 1.0),
				color=(220, 230, 240),
				platform_density=0.08,
				mob_spawn_chance=0.005,
				objects={"snow": 0.9}
			),
		]
	
	def get_biome_at(self, height: float, biome_value: float) -> Biome:
		"""Находит биом в точке"""
		# Сначала проверяем специальные биомы (вода, снег)
		for biome in self.biomes:
			if biome.contains_point(height, biome_value):
				return biome
		
		# Если ничего не подошло — возвращаем траву как дефолтный
		return self.biomes[0]  # GRASSLAND
