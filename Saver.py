import pickle

def save_objects(file_path, objects):
	with open(file_path, 'wb') as file:
		pickle.dump(objects, file)

def load_objects(file_path):
	with open(file_path, 'rb') as file:
		return pickle.load(file)
