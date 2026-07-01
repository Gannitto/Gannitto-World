from Chunks import ChunkManager, Chunk
from NoiseGenerator import generator
from Biomes import BiomeManager

def quick_test():
	print("=== БЫСТРЫЙ ТЕСТ ГЕНЕРАЦИИ ===\n")
	
	# Создаем менеджеры
	biome_manager = BiomeManager()
	chunk_manager = ChunkManager()
	
	# Генерируем один чанк
	chunk = Chunk(0, 0)
	chunk_manager.generate_chunk(chunk)
	
	# Анализируем результаты
	print(f"Чанк (0,0):")
	print(f"  Биом: {chunk.biome.biome_type.value if chunk.biome else 'None'}")
	print(f"  Объектов: {len(chunk.objects)}")
	print(f"  Мобов: {len(chunk.mobs)}")
	print(f"  Блоков: {len(chunk.blocks)}")
	
	# Показываем первые 5 объектов
	if chunk.objects:
		print("\nПервые 5 объектов:")
		for i, obj in enumerate(chunk.objects[:5]):
			print(f"  {i+1}. {obj} (x={obj.x}, y={obj.y})")
	
	# Проверяем распределение биомов в нескольких точках
	print("\nРаспределение биомов в разных точках:")
	test_points = [(i, i*2) for i in range(-10000, 10000, 100)]
	v = []
	for x, y in test_points:
		height = generator.get_height(x, y)
		biome_value = generator.get_biome_value(x, y)
		biome = biome_manager.get_biome_at(height, biome_value)
		# print(f"  ({x}, {y}): {biome.biome_type.value} (height={height:.2f}) (biome value={biome_value:.2f})")
		# print(biome_value)
		v.append(biome_value)
	from collections import Counter

	# Найти самое часто встречающееся число
	while 0.0 in v: v.remove(0.0)
	while 0.03385313857086458 in v: v.remove(0.03385313857086458)
	while -0.03385313857086458 in v: v.remove(-0.03385313857086458)
	while 0.06770627714172917 in v: v.remove(0.06770627714172917)
	while -0.06770627714172917 in v: v.remove(-0.06770627714172917)
	counts = Counter(v)
	most_common = counts.most_common(1) 
	print(most_common[0][0])
	# for i in v: print(i)

if __name__ == "__main__":
	quick_test()
