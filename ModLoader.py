import os
import importlib.util
from Globals import path

class ModAPI:
	def __init__(self, game):
		self.game = game
		self.hooks = {
			"on_tick": [],
			"on_world_load": []
		}

	def on(self, event_name, callback):
		"""Регистрация функции мода на событие игры"""
		if event_name in self.hooks:
			self.hooks[event_name].append(callback)

	def trigger(self, event_name, *args, **kwargs):
		"""Вызов всех подписанных функций из основного цикла игры"""
		for callback in self.hooks.get(event_name, []):
			callback(self.game, *args, **kwargs)

class ModLoader:
	def __init__(self, game):
		self.api = ModAPI(game)
		self.mods_folder = path + "Mods/"
		self.load_mods()

	def load_mods(self):
		if not os.path.exists(self.mods_folder):
			os.makedirs(self.mods_folder)
			return

		for filename in os.listdir(self.mods_folder):
			if filename.endswith(".py") and not filename.startswith("_"):
				mod_path = os.path.join(self.mods_folder, filename)
				spec = importlib.util.spec_from_file_location(filename[:-3], mod_path)
				module = importlib.util.module_from_spec(spec)
				spec.loader.exec_module(module)
				# Запускаем точку входа мода
				if hasattr(module, "setup"):
					module.setup(self.api)

