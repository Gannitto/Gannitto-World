from enum import Enum
from typing import Dict, List, Tuple
from dataclasses import dataclass

class BiomeType(Enum):
	FOREST = "Forest"
	DESERT = "Desert"
	FIELD = "Field"
	TAIGA = "Taiga"
	SWAMP = "Swamp"
@dataclass
class Biome:

	biome_type: BiomeType
	height_range: Tuple[float, float]  # диапазон высот
	biome_value_range: Tuple[float, float]	# диапазон для biome_value
	color: Tuple[int, int, int]
	mob_spawn_chance: float
	objects: Dict[str, float]  # шансы спавна разных объектов
	
	def contains_point(self, biome_value: float) -> bool:
		"""Проверяет, принадлежит ли точка этому биому"""
		return (self.biome_value_range[0] <= biome_value <= self.biome_value_range[1])

class BiomeManager:

	def __init__(self):
		self.biomes: List[Biome] = []
		self._initialize_biomes()
	
	def _initialize_biomes(self):

		"""Инициализация всех биомов"""

		self.biomes = [
			Biome(
				biome_type=BiomeType.FOREST,
				height_range=(0.0, 0.4),
				biome_value_range=(0.4, 0.8),
				color=(50, 150, 50),
				mob_spawn_chance=0.05,
				objects={"tree": 0.7, "bush": 0.3}
			),
			Biome(
				biome_type=BiomeType.DESERT,
				height_range=(-0.1, 0.2),
				biome_value_range=(-0.8, -0.4),
				color=(200, 180, 100),
				mob_spawn_chance=0.01,
				objects={"cactus": 0.2, "sand": 0.8}
			),
			Biome(
				biome_type=BiomeType.FIELD,
				height_range=(0.0, 0.4),
				biome_value_range=(0.4, 0.8),
				color=(50, 150, 50),
				mob_spawn_chance=0.05,
				objects={}
			),
			Biome(
				biome_type=BiomeType.TAIGA,
				height_range=(0.6, 1.0),
				biome_value_range=(0.6, 1.0),
				color=(220, 230, 240),
				mob_spawn_chance=0.005,
				objects={"Spruce": 0.9}
			),
			Biome(
				biome_type=BiomeType.SWAMP,
				height_range=(0.6, 1.0),
				biome_value_range=(0.6, 1.0),
				color=(220, 230, 240),
				mob_spawn_chance=0.005,
				objects={}
			)
		]
	
	def get_biome_at(self, height: float, biome_value: float) -> Biome:
		"""Находит биом в точке"""
		for biome in self.biomes:
			if biome.contains_point(biome_value):
				return biome
		
		# Если ничего не подошло, то возвращаем лес как дефолтный
		return self.biomes[0]

