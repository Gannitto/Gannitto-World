import pygame
import vnoise
import numpy as np
import random

class CaveGenerator:
	def __init__(self, width=800, height=600, seed=None):
		"""
		Инициализация генератора пещер
		
		Args:
			width: ширина карты в пикселях
			height: высота карты в пикселях
			seed: сид для генерации (если None, используется случайный)
			cell_size: размер одного "пикселя" карты
		"""
		self.cell_size = 10
		self.width = width // self.cell_size
		self.height = height // self.cell_size
		self.seed = seed if seed is not None else random.randint(0, 1000000)
		self.scale = 60
		
		# Инициализация шума
		self.noise = vnoise.Noise(seed=self.seed)
		
		# Параметры шума для пещер
		self.frequency = 0.08
		self.octaves = 4
		self.lacunarity = 2.0
		self.gain = 0.5
		self.threshold = 0  # Порог для разделения стены/пустота
		
		# Карта пещеры (True - стена, False - пустота)
		self.cave_map = None
		
	def generate_map(self):
		"""Генерация карты пещеры"""
		self.cave_map = np.zeros((self.height, self.width), dtype=bool)
		# self.cave_map_copy = np.zeros((self.height, self.width), dtype=float)
		
		for y in range(0, self.height):
			for x in range(0, self.width):
				# Нормализованные координаты
				nx = x / self.width * self.scale
				ny = y / self.height * self.scale
				
				# Генерация шума
				value = self.noise.noise2(
					nx * self.frequency,
					ny * self.frequency,
					octaves=self.octaves,
					lacunarity=self.lacunarity,
					# gain=self.gain
				)
				
				# Применение порога
				self.cave_map[y][x] = value > self.threshold
				# self.cave_map_copy[y][x] = value
		# print(self.cave_map_copy.min(), self.cave_map_copy.max())
		return self.cave_map
	
	def apply_smoothing(self, iterations=2):
		"""Применение сглаживания для улучшения формы пещер"""
		for _ in range(iterations):
			new_map = np.copy(self.cave_map)
			
			for y in range(1, self.height - 1):
				for x in range(1, self.width - 1):
					# Подсчет соседей-стен
					wall_count = 0
					for dy in [-1, 0, 1]:
						for dx in [-1, 0, 1]:
							if dy == 0 and dx == 0:
								continue
							if self.cave_map[y + dy][x + dx]:
								wall_count += 1
					
					# Если больше 3 соседей - стена, иначе пустота
					new_map[y][x] = wall_count >= 4
			
			self.cave_map = new_map
			
		return self.cave_map
	
	def remove_isolated_cells(self):
		"""Удаление изолированных клеток"""
		new_map = np.copy(self.cave_map)
		
		for y in range(1, self.height - 1):
			for x in range(1, self.width - 1):
				# Для пустых клеток
				if not self.cave_map[y][x]:
					wall_count = 0
					for dy in [-1, 0, 1]:
						for dx in [-1, 0, 1]:
							if dy == 0 and dx == 0:
								continue
							if self.cave_map[y + dy][x + dx]:
								wall_count += 1
					
					# Если у пустой клетки 7 или 8 соседей-стен - превращаем в стену
					if wall_count >= 7:
						new_map[y][x] = True
				
				# Для стен
				else:
					wall_count = 0
					for dy in [-1, 0, 1]:
						for dx in [-1, 0, 1]:
							if dy == 0 and dx == 0:
								continue
							if self.cave_map[y + dy][x + dx]:
								wall_count += 1
					
					# Если у стены 0 или 1 сосед-стена - превращаем в пустоту
					if wall_count <= 1:
						new_map[y][x] = False
		
		self.cave_map = new_map
		return self.cave_map
	
	def render(self, screen):
		"""Отрисовка карты на экране"""
		colors = {
			True: (40, 40, 40),   # Стены - темно-серые
			False: (200, 180, 150)	# Пустота - песочные
		}
		
		for y in range(self.height):
			for x in range(self.width):
				color = colors[self.cave_map[y][x]]
				pygame.draw.rect(
					screen,
					color,
					(x * self.cell_size, y * self.cell_size, 
					 self.cell_size, self.cell_size)
				)
	
	def get_cave_regions(self):
		"""Нахождение областей пещеры (для возможного использования)"""
		visited = np.zeros((self.height, self.width), dtype=bool)
		regions = []
		
		for y in range(self.height):
			for x in range(self.width):
				if not self.cave_map[y][x] and not visited[y][x]:
					# BFS для поиска связной области
					region = []
					queue = [(y, x)]
					visited[y][x] = True
					
					while queue:
						cy, cx = queue.pop(0)
						region.append((cx, cy))
						
						for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
							ny, nx = cy + dy, cx + dx
							if (0 <= ny < self.height and 0 <= nx < self.width and 
								not self.cave_map[ny][nx] and not visited[ny][nx]):
								visited[ny][nx] = True
								queue.append((ny, nx))
					
					if len(region) > 50:  # Игнорируем слишком маленькие области
						regions.append(region)
		
		return regions

def main():
	# Инициализация Pygame
	pygame.init()
	
	# Параметры окна
	WINDOW_WIDTH = 800
	WINDOW_HEIGHT = 600
	win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption("Генерация пещер")
	
	# Создание генератора с заданным сидом
	seed = 12345  # Измените для разных пещер
	generator = CaveGenerator(
		width=WINDOW_WIDTH,
		height=WINDOW_HEIGHT,
		seed=seed,
	)
	
	# Генерация пещеры
	print(f"Генерация пещеры с сидом {seed}...")
	generator.generate_map()
	print("Применение сглаживания...")
	generator.apply_smoothing(iterations=3)
	print("Удаление изолированных клеток...")
	generator.remove_isolated_cells()
	
	# Дополнительное сглаживание для более естественного вида
	generator.apply_smoothing(iterations=1)
	
	# Получение областей пещеры (информативно)
	regions = generator.get_cave_regions()
	print(f"Найдено {len(regions)} областей пещеры")
	if regions:
		total_cells = sum(len(r) for r in regions)
		print(f"Всего клеток в пещерах: {total_cells}")
	
	clock = pygame.time.Clock()
	running = True
	
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:  # Регенерация с новым сидом
					new_seed = random.randint(0, 1000000)
					print(f"\nРегенерация с сидом {new_seed}...")
					generator = CaveGenerator(
						width=WINDOW_WIDTH,
						height=WINDOW_HEIGHT,
						seed=new_seed,
					)
					generator.generate_map()
					generator.apply_smoothing(iterations=3)
					generator.remove_isolated_cells()
					generator.apply_smoothing(iterations=1)
					
					regions = generator.get_cave_regions()
					print(f"Найдено {len(regions)} областей пещеры")
					if regions:
						print(f"Всего клеток в пещерах: {sum(len(r) for r in regions)}")
		
		# Отрисовка
		win.fill((0, 0, 0))
		generator.render(win)
		
		# Отображение информации
		font = pygame.font.Font(None, 24)
		info_text = f"Seed: {generator.seed} | R - регенерация"
		text_surface = font.render(info_text, True, (255, 255, 255))
		win.blit(text_surface, (10, 10))
		
		pygame.display.flip()
		clock.tick(60)
	
	pygame.quit()

if __name__ == "__main__":
	main()
