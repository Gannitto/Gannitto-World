import random
from Biomes import BiomeManager, BiomeType
from WorldGenerator import WorldGenerator
chunk_size = 2048

class Chunk:
	def __init__(self, chunk_x, chunk_y):
		self.chunk_x = chunk_x
		self.chunk_y = chunk_y
		chunk_size = chunk_size
		self.platforms = []
		self.objects = []
		self.mobs = []
		self.biome_map = {}  # Карта биомов внутри чанка
		self.is_loaded = False
		self.is_generated = False
		
	def get_world_bounds(self):
		return {
			"x1": self.chunk_x * chunk_size,
			"y1": self.chunk_y * chunk_size,
			"x2": (self.chunk_x + 1) * chunk_size,
			"y2": (self.chunk_y + 1) * chunk_size
		}

class ChunkManager:
	def __init__(self, chunk_size=256, view_distance=3):
		chunk_size = chunk_size
		self.view_distance = view_distance
		self.chunks = {}
		self.loaded_chunks = set()
		self.generator = WorldGenerator(seed=12345)
		self.biome_manager = BiomeManager()
		
	def generate_chunk(self, chunk: Chunk):
		"""Генерация чанка с использованием шума Перлина"""
		bounds = chunk.get_world_bounds()
		
		# Определяем шаг дискретизации (чем меньше, тем детальнее)
		step = 16  # пикселей на точку выборки
		
		# Проходим по всем точкам в чанке
		for x in range(int(bounds["x1"]), int(bounds["x2"]), step):
			for y in range(int(bounds["y1"]), int(bounds["y2"]), step):
				# Получаем значения шума
				height = self.generator.get_height(x, y)
				biome_value = self.generator.get_biome_value(x, y)
				
				# Определяем биом
				biome = self.biome_manager.get_biome_at(height, biome_value)
				chunk.biome_map[(x, y)] = biome
				
				# Генерируем объекты в зависимости от биома
				self._generate_objects_in_area(chunk, x, y, step, biome, height)
		
		chunk.is_generated = True
	
def _generate_objects_in_area(self, chunk, x, y, step, biome, height):
	"""Генерирует объекты на основе биома"""
	# Используем детальный шум для размещения объектов внутри биома
	detail = self.generator.get_detail_value(x, y)
	
	# Платформы (земля)
	if biome.platform_density > 0 and detail > 0.3:
		# Создаем платформу с учетом высоты
		platform_x = x + step/2
		platform_y = y + step/2
		
		# Корректируем высоту в зависимости от биома
		if biome.biome_type == BiomeType.WATER:
			# Пропускаем воду
			return
		
		elif biome.biome_type == BiomeType.MOUNTAIN:
			platform_y = y + height * 100  # Горы выше
		else:
			platform_y = y + height * 30  # Обычный рельеф
		
		# Используем детальный шум для определения точного места
		if detail > 0.4:  # Только некоторые точки становятся платформами
			platform = self._create_platform(
				platform_x, 
				platform_y, 
				biome,
				detail
			)
			chunk.platforms.append(platform)
	
	# Деревья/объекты
	if "tree" in biome.objects and detail > 0.7:
		# Генерируем дерево
		tree_x = x + step/2
		tree_y = y + step/2 + self.generator.get_height(x, y) * 30
		if biome.biome_type not in [BiomeType.WATER, BiomeType.MOUNTAIN]:
			chunk.objects.append(self._create_tree(tree_x, tree_y))
	
	# Мобы
	if random.random() < biome.mob_spawn_chance and detail > 0.8:
		mob_x = x + step/2
		mob_y = y + step/2 + self.generator.get_height(x, y) * 30
		chunk.mobs.append(self._create_mob(mob_x, mob_y, biome))
	
	def _create_platform(self, x, y, biome, detail):
		"""Создание платформы с параметрами биома"""
		# Здесь ваша существующая логика создания платформы
		# но с цветом и свойствами из биома
		from Gannitto_world import Platform  # адаптируйте импорт
		
		size = 32 + detail * 30  # Размер зависит от шума
		return Platform(
			x=x, 
			y=y, 
			width=size, 
			height=10,
			color=biome.color
		)
