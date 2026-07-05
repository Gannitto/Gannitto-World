from NoiseGenerator import NoiseGenerator
from itertools import product
import random
from Saver import save_chunk, load_chunk, chunk_exists

chunk_size = 2048
tile_size = 256

biomes = ["Desert", "Field", "Forest", "Swamp", "Taiga"]

# Частота появления, параметры
biomes_objects = {

		"Desert": ((
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
				})),
			()),

		"Field": ((), ()),

		"Forest": ((
			(2, {
				"name": "Tree",
				"image_path": "Gannitto world/files/Images/Objects/Tree.png",
				"scale_x": (256, 256),
				"special_flags": 100,
				"is_solid": True}),
			(2, {
				"name": "Birch",
				"image_path": "Gannitto world/files/Images/Objects/Birch.png",
				"scale_x": (256, 256),
				"special_flags": 100,
				"is_solid": True
				}),
			(0.5, {
				"name": "Bush",
				"image_path": "Gannitto world/files/Images/Objects/Bush.png",
				"scale_x": (128, 128),
				"is_solid": True
				})),
			(
			(0.5, {
				"name": "Stone",
				"image_path": "Gannitto world/files/Images/Items/Stone.png",
				}),
			(0.1, {
				"name": "Mushroom",
				"image_path": "Gannitto world/files/Images/Items/Mushroom.png",
				}),
			(0.1, {
				"name": "Red mushroom",
				"image_path": "Gannitto world/files/Images/Items/Red mushroom.png",
				}))),

		"Swamp": ((
			(2, {
				"name": "Dark tree",
				"image_path": "Gannitto world/files/Images/Objects/Dark tree.png",
				"scale_x": (256, 256),
				"special_flags": 100,
				"is_solid": True}),),
			(
			(0.5, {
				"name": "Cotton grass",
				"image_path": "Gannitto world/files/Images/Items/Cotton grass.png",
				}),
			(0.5, {
				"name": "Mushroom",
				"image_path": "Gannitto world/files/Images/Items/Mushroom.png",
				}),
			(0.5, {
				"name": "Red mushroom",
				"image_path": "Gannitto world/files/Images/Items/Red mushroom.png",
				}))),


		"Taiga": ((
			(2, {
				"name": "Spruce",
				"image_path": "Gannitto world/files/Images/Objects/Spruce.png",
				"scale_x": (512, 512),
				"special_flags": 100,
				"is_solid": True
				}),
			(0.5, {
				"name": "Dark bush",
				"image_path": "Gannitto world/files/Images/Objects/Dark bush.png",
				"scale_x": (128, 128),
				"is_solid": True
				})),
			())
			
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
		self.modified = True # TODO изменён ли чанк игроком
		
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
		self.view_distance = 1
		self.generator = NoiseGenerator()
		self.save_directory = ""
		
	def generate_chunk(self, chunk: Chunk):

		"""Генерация чанка"""
		from Gannitto_world import Object
		bounds = chunk.get_world_bounds()
	
		value = self.generator.get_biome_at(chunk.x, chunk.y)
		index = int(value * len(biomes))
		if index >= len(biomes):
			index = len(biomes) - 1
		biome = biomes[index]
		# Добавление некоторых игровых объектов через шум Перлина (будет в будущем)
		# for x, y in product(range(int(bounds["x1"]), int(bounds["x2"]), tile_size), range(int(bounds["y1"]), int(bounds["y2"]), tile_size)):
			# height = self.generator.get_height(x, y)
			# if height > 0.5: ...

		# Сохраняем биом для этого чанка
		chunk.biome = biome

		# Генерация объектов в чанке
		rng = random.Random((chunk.x * 100000 + chunk.y * 77777) ^ 0x9e3779b9)
		
		objects = []
		for object in biomes_objects[chunk.biome][0]:
			if rng.random() <= object[0]:
				for _ in range(rng.randint(1, int(object[0] * 3) + 1)):
					X = chunk.x * chunk_size + rng.randint(0, chunk_size - 1)
					Y = chunk.y * chunk_size + rng.randint(0, chunk_size - 1)
					objects.append(Object(object_x=X, object_y=Y, **object[1]))
		
		items = []
		for item in biomes_objects[chunk.biome][1]:
			if rng.random() <= item[0]:
				for _ in range(rng.randint(1, int(item[0] * 3) + 1)):
					X = chunk.x * chunk_size + rng.randint(0, chunk_size - 1)
					Y = chunk.y * chunk_size + rng.randint(0, chunk_size - 1)
					items.append(Object(object_x=X, object_y=Y, **item[1]))

		chunk.objects = objects
		chunk.items = items
		chunk.is_generated = True
	
	def get_chunk_at(self, X, Y):
		chunk_pos = (int(X // chunk_size), int(Y // chunk_size))
		if chunk_pos in self.chunks: return self.chunks[chunk_pos]
		return None

	def _load_chunk_from_disk(self, chunk_x, chunk_y):
		"""Загружает чанк с диска, если он существует"""
		if chunk_exists(chunk_x, chunk_y, self.save_directory):
			chunk = load_chunk(chunk_x, chunk_y, self.save_directory)
			if chunk:
				return chunk
		return None

	def _unload_chunk(self, chunk_key):
		"""Выгружает чанк из памяти, сохраняя если нужно"""
		chunk = self.chunks.get(chunk_key)
		if chunk and chunk.is_loaded:
			# Сохраняем чанк, если он был изменен
			if chunk.modified:
				save_chunk(chunk, self.save_directory)
			
			# Очищаем данные для экономии памяти
			chunk.blocks.clear()
			chunk.objects.clear()
			chunk.mobs.clear()
			chunk.items.clear()
			chunk.particles.clear()
			chunk.caves.clear()
			
			chunk.is_loaded = False
			chunk.is_generated = True
			
			if chunk_key in self.chunks:
				del self.chunks[chunk_key]

	def update_visible_chunks(self, player_x, player_y):

		"""Обновление видимых чанков вокруг игрока"""

		center_chunk_x = int(player_x // chunk_size)
		center_chunk_y = int(player_y // chunk_size)
		new_visible_chunks = set()
		
		for dx, dy in product(range(-self.view_distance, self.view_distance + 1), range(-self.view_distance, self.view_distance + 1)):
			chunk_x = center_chunk_x + dx
			chunk_y = center_chunk_y + dy
			
			chunk_key = (chunk_x, chunk_y)
			new_visible_chunks.add(chunk_key)
			
			# Если чанк еще не существует, то создаётся
			if chunk_key not in self.chunks:
				new_chunk = self._load_chunk_from_disk(chunk_x, chunk_y)
				if new_chunk is None:
					new_chunk = Chunk(chunk_x, chunk_y)
				self.chunks[chunk_key] = new_chunk
				new_chunk.is_loaded = True
			
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
		
		for chunk_key in chunks_to_unload:
			self._unload_chunk(chunk_key)
		
		self.loaded_chunks = new_visible_chunks.copy()

	def save_all_loaded_chunks(self):
		"""Сохраняет все загруженные в данный момент чанки"""
		for chunk_key, chunk in self.chunks.items():
			if chunk.is_loaded and chunk.modified:
				save_chunk(chunk, self.save_directory)
	
	def force_save_chunk(self, chunk_x, chunk_y):
		"""Принудительно сохраняет конкретный чанк"""
		chunk_key = (chunk_x, chunk_y)
		if chunk_key in self.chunks:
			chunk = self.chunks[chunk_key]
			if chunk.is_loaded:
				save_chunk(chunk, self.save_directory)
				return True
		return False

	def delete_chunk_save(self, chunk_x, chunk_y):
		"""Удаляет сохраненный файл чанка (для перегенерации)"""
		from Saver import delete_chunk
		return delete_chunk(chunk_x, chunk_y, self.save_directory)
