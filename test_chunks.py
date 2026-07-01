import pygame
import sys
from Chunks import ChunkManager, Chunk, chunk_size, tile_size
from Biomes import BiomeManager
from NoiseGenerator import NoiseGenerator
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Тест генерации чанков")

# Цвета
COLORS = {
	"background": (30, 30, 40),
	"grid": (60, 60, 70),
	"chunk_border": (100, 100, 150),
	"object": (255, 200, 50),
}

# Масштаб для отображения (1 пиксель = сколько игровых пикселей)
VIEW_SCALE = 10.0  # 1:1 для начала, можно уменьшить для обзора

class ChunkViewer:
	def __init__(self):
		self.chunk_manager = ChunkManager(view_distance=3)
		self.generator = NoiseGenerator(seed=12345)
		self.biome_manager = self.chunk_manager.biome_manager
		
		# Камера для перемещения по миру
		self.camera_x = 0
		self.camera_y = 0
		self.camera_speed = 20
		
		# Загруженные чанки
		self.loaded_chunks = {}
		
		# Мини-карта для отображения
		self.minimap_scale = 4	# 1 пиксель = 4 игровых пикселя
		
	def generate_visible_chunks(self, center_x=0, center_y=0):
		"""Генерирует чанки вокруг центральной точки"""
		# Определяем, какие чанки должны быть видны
		view_distance = 3
		
		for dx in range(-view_distance, view_distance + 1):
			for dy in range(-view_distance, view_distance + 1):
				chunk_x = int(center_x // chunk_size) + dx
				chunk_y = int(center_y // chunk_size) + dy
				chunk_key = (chunk_x, chunk_y)
				
				if chunk_key not in self.loaded_chunks:
					chunk = Chunk(chunk_x, chunk_y)
					self.chunk_manager.generate_chunk(chunk)
					self.loaded_chunks[chunk_key] = chunk
	
	def draw_minimap(self, surface, offset_x=0, offset_y=0):
		"""Рисует мини-карту всех загруженных чанков"""
		if not self.loaded_chunks:
			return
			
		# Определяем границы для отображения
		min_x = min(chunk.chunk_x for chunk in self.loaded_chunks.values())
		max_x = max(chunk.chunk_x for chunk in self.loaded_chunks.values())
		min_y = min(chunk.chunk_y for chunk in self.loaded_chunks.values())
		max_y = max(chunk.chunk_y for chunk in self.loaded_chunks.values())
		
		# Рисуем сетку чанков
		for chunk in self.loaded_chunks.values():
			# Позиция чанка на мини-карте
			map_x = (chunk.chunk_x - min_x) * 50 + 10 + offset_x
			map_y = (chunk.chunk_y - min_y) * 50 + 10 + offset_y
			
			# Цвет биома (упрощенно)
			if chunk.biome:
				color = chunk.biome.color
			else:
				color = (100, 100, 100)
			
			# Рисуем прямоугольник чанка
			pygame.draw.rect(surface, color, (map_x, map_y, 48, 48))
			pygame.draw.rect(surface, COLORS["chunk_border"], (map_x, map_y, 48, 48), 1)
			
			# Количество объектов в чанке
			obj_count = len(chunk.objects)
			if obj_count > 0:
				font = pygame.font.Font(None, 16)
				text = font.render(str(obj_count), True, (255, 255, 255))
				surface.blit(text, (map_x + 20, map_y + 15))
			
			# Отображаем координаты чанка
			font = pygame.font.Font(None, 12)
			text = font.render(f"({chunk.chunk_x},{chunk.chunk_y})", True, (200, 200, 200))
			surface.blit(text, (map_x + 2, map_y + 30))
	
	def draw_world_view(self, surface):
		"""Рисует вид мира в выбранном масштабе"""
		# Получаем все объекты из загруженных чанков
		all_objects = []
		for chunk in self.loaded_chunks.values():
			all_objects.extend(chunk.objects)
		
		# Рисуем объекты
		for obj in all_objects:
			# Преобразуем координаты в экранные с учетом камеры
			screen_x = (obj.x - self.camera_x) / VIEW_SCALE + WINDOW_WIDTH // 2
			screen_y = (obj.y - self.camera_y) / VIEW_SCALE + WINDOW_HEIGHT // 2
			
			# Проверяем, виден ли объект
			if 0 <= screen_x <= WINDOW_WIDTH and 0 <= screen_y <= WINDOW_HEIGHT:
				pygame.draw.circle(surface, COLORS["object"], 
								 (int(screen_x), int(screen_y)), 3)
		
		# Отображаем информацию о чанках
		font = pygame.font.Font(None, 24)
		info_text = f"Загружено чанков: {len(self.loaded_chunks)} | Объектов: {len(all_objects)}"
		text = font.render(info_text, True, (255, 255, 255))
		surface.blit(text, (10, 10))
		
		# Отображаем позицию камеры
		cam_text = f"Камера: ({int(self.camera_x)}, {int(self.camera_y)})"
		text = font.render(cam_text, True, (255, 255, 255))
		surface.blit(text, (10, 40))
	
	def handle_events(self):
		"""Обработка событий клавиатуры"""
		keys = pygame.key.get_pressed()
		
		# Движение камеры
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			self.camera_x -= self.camera_speed
		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			self.camera_x += self.camera_speed
		if keys[pygame.K_UP] or keys[pygame.K_w]:
			self.camera_y -= self.camera_speed
		if keys[pygame.K_DOWN] or keys[pygame.K_s]:
			self.camera_y += self.camera_speed
	
	def run(self):
		"""Главный цикл"""
		clock = pygame.time.Clock()
		running = True
		
		# Генерируем начальные чанки
		self.generate_visible_chunks(0, 0)
		
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_r:
						# Перегенерация
						self.loaded_chunks.clear()
						self.generate_visible_chunks(self.camera_x, self.camera_y)
					elif event.key == pygame.K_SPACE:
						# Загрузить еще чанки вокруг камеры
						self.generate_visible_chunks(self.camera_x, self.camera_y)
					elif event.key == pygame.K_ESCAPE:
						running = False
			
			# Обработка движения
			self.handle_events()
			
			# Загружаем чанки вокруг камеры
			self.generate_visible_chunks(self.camera_x, self.camera_y)
			
			# Отрисовка
			screen.fill(COLORS["background"])
			
			# Рисуем основное поле
			self.draw_world_view(screen)
			
			# Рисуем мини-карту в правом верхнем углу
			minimap_offset_x = WINDOW_WIDTH - 350
			minimap_offset_y = 10
			self.draw_minimap(screen, minimap_offset_x, minimap_offset_y)
			
			# Информация об управлении
			font = pygame.font.Font(None, 16)
			controls = [
				"WASD - Движение камеры",
				"SPACE - Загрузить больше чанков",
				"R - Перегенерировать",
				"ESC - Выход"
			]
			y_pos = WINDOW_HEIGHT - 100
			for control in controls:
				text = font.render(control, True, (200, 200, 200))
				screen.blit(text, (10, y_pos))
				y_pos += 20
			
			pygame.display.flip()
			clock.tick(60)
		
		pygame.quit()
		sys.exit()

def test_noise_generator():
	"""Тест генератора шума"""
	generator = NoiseGenerator(seed=12345)
	print("Тестирование генератора шума:")
	print(f"Height в (0,0): {generator.get_height(0, 0)}")
	print(f"Biome value в (0,0): {generator.get_biome_value(0, 0)}")
	print(f"Height в (100,100): {generator.get_height(100, 100)}")
	print(f"Biome value в (100,100): {generator.get_biome_value(100, 100)}")

def test_biome_detection():
	"""Тест определения биомов"""
	generator = NoiseGenerator(seed=12345)
	biome_manager = BiomeManager()
	
	print("\nТестирование определения биомов:")
	test_points = [(0, 0), (100, 100), (-50, 50), (200, -100)]
	
	for x, y in test_points:
		height = generator.get_height(x, y)
		biome_value = generator.get_biome_value(x, y)
		biome = biome_manager.get_biome_at(height, biome_value)
		print(f"Точка ({x}, {y}): height={height:.3f}, value={biome_value:.3f} -> {biome.biome_type.value}")

if __name__ == "__main__":
	# Запускаем тесты
	print("=== ТЕСТИРОВАНИЕ ГЕНЕРАЦИИ МИРА ===\n")
	test_noise_generator()
	test_biome_detection()
	
	print("\nЗапуск визуализатора...")
	print("Управление:")
	print("  WASD - движение камеры")
	print("  SPACE - загрузить больше чанков")
	print("  R - перегенерировать")
	print("  ESC - выход\n")
	
	# Запускаем визуализатор
	viewer = ChunkViewer()
	viewer.run()
