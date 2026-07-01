import random
from Biomes import BiomeManager
from NoiseGenerator import generator
from itertools import product

chunk_size = 2048
tile_size = 512

class Chunk:

	def __init__(self, chunk_x, chunk_y):
		self.chunk_x = chunk_x
		self.chunk_y = chunk_y
		self.blocks = []
		self.mobs = []
		self.objects = []
		self.particles = []
		self.biome = None
		self.objects = []
		self.is_loaded = False
		self.is_generated = False
		# self.tiles = []
		
	def get_world_bounds(self):
		return {
			"x1": self.chunk_x * chunk_size,
			"y1": self.chunk_y * chunk_size,
			"x2": (self.chunk_x + 1) * chunk_size,
			"y2": (self.chunk_y + 1) * chunk_size
		}

class ChunkManager:

	def __init__(self, view_distance=3):
		self.view_distance = view_distance
		self.chunks = {}
		self.loaded_chunks = set()
		self.biome_manager = BiomeManager()
		
	def generate_chunk(self, chunk: Chunk):
		"""Генерация чанка с использованием шума Перлина"""
		# from Gannitto_world import Object
		bounds = chunk.get_world_bounds()
	
		biome_value = generator.get_biome_value(bounds["x1"], bounds["y1"])
		height = generator.get_height(bounds["x1"], bounds["y1"])
		biome = self.biome_manager.get_biome_at(height, biome_value)
		# Добавление игровых объектов через шум Перлина
		for x, y in product(range(int(bounds["x1"]), int(bounds["x2"]), tile_size), range(int(bounds["y1"]), int(bounds["y2"]), tile_size)):
			# Получаем значения шума
			height = generator.get_height(x, y)
			b = generator.get_biome_value(x, y)
		
			# Генерация объектов
			# Для теста взята текстура цветка
			# if height > 0.5:
			# 	chunk.objects.append(Object("Orange tulip", x, y, "Gannitto world/files/Images/Items/Orange tulip.png"))

		# Сохраняем биом для этого чанка
		chunk.biome = biome
		chunk.is_generated = True

