from Chunks import chunk_size, Chunk
import math
from itertools import product

def create_light_circle(chunk_manager, world_x, world_y, radius, brightness, falloff_type="linear"):
	"""
	Создает круг освещения на карте света с центром в указанных мировых координатах.
	
	Args:
		chunk_manager: экземпляр ChunkManager
		world_x, world_y: мировые координаты центра круга (в пикселях)
		radius: радиус круга в тайлах (ячейках по 64 пикселя)
		brightness: максимальная яркость в центре (0-15)
		falloff_type: тип затухания ('linear' - линейное, 'quadratic' - квадратичное)
	"""
	
	# Размер тайла в пикселях
	tile_pixel_size = 64
	
	# Переводим мировые координаты в тайловые
	tile_x = int(world_x // tile_pixel_size)
	tile_y = int(world_y // tile_pixel_size)
	
	# Определяем, какой чанк содержит центр
	chunk_x = int(world_x // chunk_size)
	chunk_y = int(world_y // chunk_size)
	
	# Вычисляем локальные координаты центра в тайлах внутри чанка
	local_center_x = tile_x - (chunk_x * chunk_size // tile_pixel_size)
	local_center_y = tile_y - (chunk_y * chunk_size // tile_pixel_size)
	
	# Количество тайлов в чанке (32x32)
	tiles_per_chunk = chunk_size // tile_pixel_size
	
	# Проходим по всем тайлам в радиусе
	for dx in range(-radius, radius + 1):
		for dy in range(-radius, radius + 1):
			# Расстояние от центра в тайлах
			distance = math.sqrt(dx**2 + dy**2)
			
			# Если тайл вне радиуса - пропускаем
			if distance > radius:
				continue
			
			# Вычисляем яркость в зависимости от типа затухания
			if falloff_type == "linear":
				# Линейное затухание: от центра к краям
				brightness_value = brightness * (1 - distance / radius)
			elif falloff_type == "quadratic":
				# Квадратичное затухание: более резкое падение у краев
				brightness_value = brightness * (1 - (distance / radius)**2)
			elif falloff_type == "gaussian":
				# Гауссовское затухание: плавное, колоколообразное
				sigma = radius / 2.5  # Параметр для регулировки ширины
				brightness_value = brightness * math.exp(-(distance**2) / (2 * sigma**2))
			else:
				# По умолчанию линейное
				brightness_value = brightness * (1 - distance / radius)
			
			# Округляем и ограничиваем значения 0-15
			brightness_value = max(0, min(15, round(brightness_value)))
			
			# Если яркость равна 0, пропускаем (не добавляем в карту)
			if brightness_value == 0:
				continue
			
			# Определяем чанк для текущего тайла
			target_chunk_x = chunk_x
			target_chunk_y = chunk_y
			local_x = local_center_x + dx
			local_y = local_center_y + dy
			
			# Корректируем координаты, если выходим за пределы чанка
			if local_x < 0:
				target_chunk_x -= 1
				local_x += tiles_per_chunk
			elif local_x >= tiles_per_chunk:
				target_chunk_x += 1
				local_x -= tiles_per_chunk
				
			if local_y < 0:
				target_chunk_y -= 1
				local_y += tiles_per_chunk
			elif local_y >= tiles_per_chunk:
				target_chunk_y += 1
				local_y -= tiles_per_chunk
			
			# Проверяем, существует ли целевой чанк
			chunk_key = (target_chunk_x, target_chunk_y)
			if chunk_key not in chunk_manager.chunks:
				# Если чанка нет - создаем его
				new_chunk = Chunk(target_chunk_x, target_chunk_y)
				chunk_manager.chunks[chunk_key] = new_chunk
				# Если чанк не сгенерирован - генерируем
				if not new_chunk.is_generated:
					chunk_manager.generate_chunk(new_chunk)
				new_chunk.is_loaded = True
			
			target_chunk = chunk_manager.chunks[chunk_key]
			
			# Добавляем освещение в карту света
			# Если уже есть значение, берем максимальное (самое яркое)
			current_light = target_chunk.light_map.get((local_x, local_y), 0)
			if brightness_value > current_light:
				target_chunk.light_map[(local_x, local_y)] = brightness_value
	
	# Отмечаем чанки как измененные для сохранения
	for dx, dy in product(range(-1, 2), range(-1, 2)):
		chunk_key = (chunk_x + dx, chunk_y + dy)
		if chunk_key in chunk_manager.chunks:
			chunk_manager.chunks[chunk_key].modified = True

def create_light_circle_with_falloff(chunk_manager, world_x, world_y, radius, brightness, 
								   inner_radius=None, falloff_type="linear"):
	"""
	Создает круг освещения с возможностью указать внутренний радиус, 
	где яркость максимальна.
	
	Args:
		chunk_manager: экземпляр ChunkManager
		world_x, world_y: мировые координаты центра круга (в пикселях)
		radius: максимальный радиус круга в тайлах
		brightness: максимальная яркость (0-15)
		inner_radius: радиус полной яркости (по умолчанию 0)
		falloff_type: тип затухания ('linear' или 'quadratic')
	"""
	
	if inner_radius is None:
		inner_radius = 0
	
	tile_pixel_size = 64
	tile_x = int(world_x // tile_pixel_size)
	tile_y = int(world_y // tile_pixel_size)
	
	chunk_x = int(world_x // chunk_size)
	chunk_y = int(world_y // chunk_size)
	
	local_center_x = tile_x - (chunk_x * chunk_size // tile_pixel_size)
	local_center_y = tile_y - (chunk_y * chunk_size // tile_pixel_size)
	
	tiles_per_chunk = chunk_size // tile_pixel_size
	
	for dx in range(-radius, radius + 1):
		for dy in range(-radius, radius + 1):
			distance = math.sqrt(dx**2 + dy**2)
			
			if distance > radius:
				continue
			
			# Если внутри внутреннего радиуса - максимальная яркость
			if distance <= inner_radius:
				brightness_value = brightness
			else:
				# Вычисляем затухание от внутреннего радиуса до внешнего
				normalized_distance = (distance - inner_radius) / (radius - inner_radius)
				
				if falloff_type == "linear":
					brightness_value = brightness * (1 - normalized_distance)
				elif falloff_type == "quadratic":
					brightness_value = brightness * (1 - normalized_distance**2)
				else:
					brightness_value = brightness * (1 - normalized_distance)
			
			brightness_value = max(0, min(15, round(brightness_value)))
			
			if brightness_value == 0:
				continue
			
			target_chunk_x = chunk_x
			target_chunk_y = chunk_y
			local_x = local_center_x + dx
			local_y = local_center_y + dy
			
			if local_x < 0:
				target_chunk_x -= 1
				local_x += tiles_per_chunk
			elif local_x >= tiles_per_chunk:
				target_chunk_x += 1
				local_x -= tiles_per_chunk
				
			if local_y < 0:
				target_chunk_y -= 1
				local_y += tiles_per_chunk
			elif local_y >= tiles_per_chunk:
				target_chunk_y += 1
				local_y -= tiles_per_chunk
			
			chunk_key = (target_chunk_x, target_chunk_y)
			if chunk_key not in chunk_manager.chunks:
				new_chunk = Chunk(target_chunk_x, target_chunk_y)
				chunk_manager.chunks[chunk_key] = new_chunk
				if not new_chunk.is_generated:
					chunk_manager.generate_chunk(new_chunk)
				new_chunk.is_loaded = True
			
			target_chunk = chunk_manager.chunks[chunk_key]
			current_light = target_chunk.light_map.get((local_x, local_y), 0)
			if brightness_value > current_light:
				target_chunk.light_map[(local_x, local_y)] = brightness_value
	
	# Отмечаем чанки как измененные
	for dx in product(range(-1, 2), range(-1, 2)):
		chunk_key = (chunk_x + dx, chunk_y + dy)
		if chunk_key in chunk_manager.chunks:
			chunk_manager.chunks[chunk_key].modified = True

def remove_light_circle(chunk_manager, world_x, world_y, radius):
	"""
	Удаляет освещение в круге (для динамических источников света).
	"""
	tile_pixel_size = 64
	tile_x = int(world_x // tile_pixel_size)
	tile_y = int(world_y // tile_pixel_size)
	
	chunk_x = int(world_x // chunk_size)
	chunk_y = int(world_y // chunk_size)
	
	local_center_x = tile_x - (chunk_x * chunk_size // tile_pixel_size)
	local_center_y = tile_y - (chunk_y * chunk_size // tile_pixel_size)
	
	tiles_per_chunk = chunk_size // tile_pixel_size
	
	for dx in range(-radius, radius + 1):
		for dy in range(-radius, radius + 1):
			distance = math.sqrt(dx**2 + dy**2)
			if distance > radius:
				continue
			
			target_chunk_x = chunk_x
			target_chunk_y = chunk_y
			local_x = local_center_x + dx
			local_y = local_center_y + dy
			
			if local_x < 0:
				target_chunk_x -= 1
				local_x += tiles_per_chunk
			elif local_x >= tiles_per_chunk:
				target_chunk_x += 1
				local_x -= tiles_per_chunk
				
			if local_y < 0:
				target_chunk_y -= 1
				local_y += tiles_per_chunk
			elif local_y >= tiles_per_chunk:
				target_chunk_y += 1
				local_y -= tiles_per_chunk
			
			chunk_key = (target_chunk_x, target_chunk_y)
			if chunk_key in chunk_manager.chunks:
				target_chunk = chunk_manager.chunks[chunk_key]
				if (local_x, local_y) in target_chunk.light_map:
					del target_chunk.light_map[(local_x, local_y)]
					target_chunk.modified = True

