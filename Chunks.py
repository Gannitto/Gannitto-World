from NoiseGenerator import generator
from itertools import product
import random

chunk_size = 2048
tile_size = 256

biomes = ["Desert", "Field", "Forest", "Swamp", "Taiga"]

# Частота появления, (имя, путь к изображению, твёрдый ли)
biomes_objects = {

		"Desert": (
			(1, {
				"name": "Cactus",
				"image_path": "Gannitto world/files/Images/Objects/Cactus.png",
				"scale_x": (256, 256),
				"is_solid": True,
				"rect": (-80, 116, 160, 232)
				}),
			(0.5, {
				"name": "Pile of sand",
				"image_path": "Gannitto world/files/Images/Objects/Pile of sand.png",
				"scale_x": (256, 256),
				})
			),

		"Field": (),

		"Forest": (
			(3, {
				"name": "Tree",
				"image_path": "Gannitto world/files/Images/Objects/Tree.png",
				"scale_x": (256, 256),
				"special_flags": 100,
				"is_solid": True}),
			(3, {
				"name": "Birch",
				"image_path": "Gannitto world/files/Images/Objects/Birch.png",
				"scale_x": (256, 256),
				"special_flags": 100,
				"is_solid": True
				})
			),

		"Swamp": (
			(2, {
				"name": "Dark tree",
				"image_path": "Gannitto world/files/Images/Objects/Dark tree.png",
				"scale_x": (256, 256),
				"special_flags": 100,
				"is_solid": True}),
			),
		"Taiga": (
			(3, {
				"name": "Spruce",
				"image_path": "Gannitto world/files/Images/Objects/Spruce.png",
				"scale_x": (512, 512),
				"special_flags": 100,
				"is_solid": True
				}),
			(2, {
				"name": "Dark bush",
				"image_path": "Gannitto world/files/Images/Objects/Dark bush.png",
				"scale_x": (128, 128),
				"is_solid": True
				})
			)
		}

class Chunk:

	def __init__(self, X, Y):
		self.x = X
		self.y = Y
		self.blocks = []
		self.mobs = []
		self.objects = []
		self.items = []
		self.particles = []
		self.caves = []
		self.biome = None
		self.objects = []
		self.is_loaded = False
		self.is_generated = False
		
	def get_world_bounds(self):
		return {
			"x1": self.x * chunk_size,
			"y1": self.y * chunk_size,
			"x2": (self.x + 1) * chunk_size,
			"y2": (self.y + 1) * chunk_size
		}

class ChunkManager:

	def __init__(self):
		self.chunks = {}
		self.loaded_chunks = set()
		self.view_distance = 3
		
	def generate_chunk(self, chunk: Chunk):

		"""Генерация чанка с использованием шума Перлина"""
		from Gannitto_world import Object
		bounds = chunk.get_world_bounds()
	
		value = generator.get_biome_at(chunk.x, chunk.y)
		index = int(value * len(biomes))
		if index >= len(biomes):
			index = len(biomes) - 1
		biome = biomes[index]
		# Добавление игровых объектов через шум Перлина (будет в будущем)
		# for x, y in product(range(int(bounds["x1"]), int(bounds["x2"]), tile_size), range(int(bounds["y1"]), int(bounds["y2"]), tile_size)):
			# height = generator.get_height(x, y)
			# Для теста взята текстура цветка
			# if height > 0.5:
			#	chunk.objects.append(Object("Orange tulip", x, y, "Gannitto world/files/Images/Items/Orange tulip.png"))

		# Сохраняем биом для этого чанка
		chunk.biome = biome

		# Генерация объектов в чанке
		rng = random.Random((chunk.x * 100000 + chunk.y * 77777) ^ 0x9e3779b9)
		
		objects = []
		for object in biomes_objects[chunk.biome]:
			if rng.random() <= object[0]:
				for _ in range(rng.randint(1, int(object[0] * 3) + 1)):
					X = chunk.x * chunk_size + rng.randint(0, chunk_size - 1)
					Y = chunk.y * chunk_size + rng.randint(0, chunk_size - 1)
					objects.append(Object(object_x=X, object_y=Y, **object[1]))

		# for _ in range(rng.randint(5, 10)):
			
		# 	local_x = chunk.x * chunk_size + rng.randint(0, chunk_size - 1)
		# 	local_y = chunk.y * chunk_size + rng.randint(0, chunk_size - 1)	
		# 	objects.append(Object("Orange tulip", local_x, local_y, "Gannitto world/files/Images/Items/Orange tulip.png"))
			
		# for _ in range(rng.randint(5, 10)):
			
		# 	local_x = chunk.x * chunk_size + rng.randint(0, chunk_size - 1)
		# 	local_y = chunk.y * chunk_size + rng.randint(0, chunk_size - 1)
		# 	objects.append(Object("Cactus", local_x, local_y, "Gannitto world/files/Images/Objects/Cactus.png", (256, 256), is_solid=True, rect=(local_x - 80, local_y + 116, 160, 232)))


		
		chunk.objects = objects
		chunk.is_generated = True
	
	def get_chunk_at(self, X, Y):
		chunk_pos = (int(X // chunk_size), int(Y // chunk_size))
		if chunk_pos in self.chunks: return self.chunks[chunk_pos]
		return None

	def update_visible_chunks(self, player_x, player_y):

		"""Обновление видимых чанков вокруг игрока"""

		center_chunk_x = int(player_x // chunk_size)
		center_chunk_y = int(player_y // chunk_size)
		new_visible_chunks = set()
		
		# Перебираем все чанки в радиусе видимости
		for dx in range(-self.view_distance, self.view_distance + 1):
			for dy in range(-self.view_distance, self.view_distance + 1):
				chunk_x = center_chunk_x + dx
				chunk_y = center_chunk_y + dy
				
				# Находится ли чанк в радиусе прорисовки
				if dx * dx + dy * dy <= self.view_distance * self.view_distance:
					chunk_key = (chunk_x, chunk_y)
					new_visible_chunks.add(chunk_key)
					
					# Если чанк еще не существует, то создаётся
					if chunk_key not in self.chunks:
						new_chunk = Chunk(chunk_x, chunk_y)
						self.chunks[chunk_key] = new_chunk
					
					# Если чанк существует, но не сгенерирован, то он генерируется
					chunk = self.chunks[chunk_key]
					if not chunk.is_generated:
						self.generate_chunk(chunk)
						chunk.is_loaded = True
		
		self.loaded_chunks = new_visible_chunks.copy()
		
		# Выгрузка чанков, которые больше не видны
		chunks_to_unload = []
		for chunk_key, chunk in self.chunks.items():
			if chunk_key not in new_visible_chunks and chunk.is_loaded:
				chunks_to_unload.append(chunk_key)
				chunk.is_loaded = False
				# Здесь можно добавить очистку данных чанка для экономии памяти
				# chunk.blocks.clear()
				# chunk.objects.clear()
				# chunk.mobs.clear()
				# chunk.particles.clear()
		
		# Удаляем выгруженные чанки из словаря (опционально)
		# for chunk_key in chunks_to_unload:
		#	  del self.chunks[chunk_key]
