from NoiseGenerator import generator
from itertools import product

chunk_size = 2048
tile_size = 256

biomes = ["Desert", "Field", "Forest", "Swamp", "Taiga"]

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

	def __init__(self):
		self.chunks = {}
		self.loaded_chunks = set()
		self.view_distance = 3
		
	def generate_chunk(self, chunk: Chunk):

		"""Генерация чанка с использованием шума Перлина"""
		# from Gannitto_world import Object
		bounds = chunk.get_world_bounds()
	
		value = generator.get_biome_at(chunk.chunk_x, chunk.chunk_y)
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
		chunk.is_generated = True

	def update_visible_chunks(self, player_x, player_y):

		"""Обновление видимых чанков вокруг игрока"""
		# Определяем центральный чанк, в котором находится игрок
		center_chunk_x = int(player_x // chunk_size)
		center_chunk_y = int(player_y // chunk_size)
		
		# Создаем множество для новых видимых чанков
		new_visible_chunks = set()
		
		# Перебираем все чанки в радиусе видимости
		for dx in range(-self.view_distance, self.view_distance + 1):
			for dy in range(-self.view_distance, self.view_distance + 1):
				chunk_x = center_chunk_x + dx
				chunk_y = center_chunk_y + dy
				
				# Проверяем, находится ли чанк в радиусе (круг вместо квадрата)
				if dx * dx + dy * dy <= self.view_distance * self.view_distance:
					chunk_key = (chunk_x, chunk_y)
					new_visible_chunks.add(chunk_key)
					
					# Если чанк еще не существует, создаем его
					if chunk_key not in self.chunks:
						new_chunk = Chunk(chunk_x, chunk_y)
						self.chunks[chunk_key] = new_chunk
					
					# Если чанк существует, но не сгенерирован, генерируем его
					chunk = self.chunks[chunk_key]
					if not chunk.is_generated:
						self.generate_chunk(chunk)
						chunk.is_loaded = True
		
		# Обновляем список загруженных чанков
		self.loaded_chunks = new_visible_chunks.copy()
		
		# Выгружаем чанки, которые больше не видны
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
