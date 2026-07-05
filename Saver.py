import pickle
import os

def save_objects(file_path, objects):
	with open(file_path, "wb") as file:
		pickle.dump(objects, file)

def load_objects(file_path):
	with open(file_path, "rb") as file:
		return pickle.load(file)

def save_chunk(chunk, save_directory="Gannitto world/saves/chunks/"):
	"""Сохраняет отдельный чанк в файл"""
	if not os.path.exists(save_directory):
		os.makedirs(save_directory)
	
	# Имя файла по координатам чанка
	filename = f"chunk_{chunk.x}_{chunk.y}.dat"
	filepath = os.path.join(save_directory, filename)
	
	# Сохраняем только необходимые данные
	chunk_data = {
		"x": chunk.x,
		"y": chunk.y,
		"biome": chunk.biome,
		"objects": chunk.objects,
		"mobs": chunk.mobs,
		"items": chunk.items,
		"blocks": chunk.blocks,
		"caves": chunk.caves,
		"is_generated": chunk.is_generated,
		"is_loaded": False
	}
	
	with open(filepath, "wb") as file:
		pickle.dump(chunk_data, file)

def load_chunk(chunk_x, chunk_y, save_directory):
	"""Загружает чанк из файла"""
	filename = f"chunk_{chunk_x}_{chunk_y}.dat"
	filepath = os.path.join(save_directory, filename)
	
	if not os.path.exists(filepath):
		return None
	
	with open(filepath, "rb") as file:
		chunk_data = pickle.load(file)
	
	from Chunks import Chunk
	chunk = Chunk(chunk_data["x"], chunk_data["y"])
	chunk.biome = chunk_data["biome"]
	chunk.objects = chunk_data["objects"]
	chunk.mobs = chunk_data["mobs"]
	chunk.items = chunk_data["items"]
	chunk.blocks = chunk_data["blocks"]
	chunk.caves = chunk_data["caves"]
	chunk.is_generated = chunk_data["is_generated"]
	chunk.is_loaded = False
	
	return chunk

def chunk_exists(chunk_x, chunk_y, save_directory):
	"""Проверяет, существует ли сохраненный чанк"""
	filename = f"chunk_{chunk_x}_{chunk_y}.dat"
	filepath = os.path.join(save_directory, filename)
	return os.path.exists(filepath)

def delete_chunk(chunk_x, chunk_y, save_directory):
	"""Удаляет файл чанка"""
	filename = f"chunk_{chunk_x}_{chunk_y}.dat"
	filepath = os.path.join(save_directory, filename)
	if os.path.exists(filepath):
		os.remove(filepath)
		return True
	return False
