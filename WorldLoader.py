import os
import Saver
from Assets import load
from Globals import path
from Classes import Object

class WorldLoader:

	def __init__(self, game, save):
		self.game = game
		self.save = save

	def load_world(self):
		self.game.world.chunk_manager.save_directory = path + "Saves/Worlds/" + self.game.world_name + "/Chunks/"

		if os.path.exists(path + "Saves/Worlds/" + self.game.world_name):
			
			self.game.world.mobs = Saver.load_objects(path + "Saves/Worlds/" + self.game.world_name + "/Mobs.save")
			self.game.player.x, self.game.player.y, self.game.Backrooms.InBackrooms, self.game.Backrooms.Level, self.game.world.current_cave, self.game.player.speed, self.game.player.HP, self.game.start_time, self.game.ron.x, self.game.ron.y, self.game.ron.home, self.game.ron.inventory, self.game.world.chunk_manager.generator.seed, self.game.time_system.current_time = Saver.load_objects(path + "Saves/Worlds/" + self.game.world_name + "/Info.save")
			self.game.world.chunk_manager.update_seed()
			self.game.difficulty, self.game.player.god_mode = Saver.load_objects(path + "Saves/Worlds/" + self.game.world_name + "/Settings.save")
			self.game.inventory.whole_inventory = Saver.load_objects(path + "Saves/Worlds/" + self.game.world_name + "/Inventory.save")
			self.game.effects.effects = Saver.load_objects(path + "Saves/Worlds/" + self.game.world_name + "/Effects.save")
			self.game.player.update_rect()
			
			if self.game.multiplayer:
				self.game.net.peers[self.game.net.player_id].x = self.game.player.x
				self.game.net.peers[self.game.net.player_id].y = self.game.player.y
				self.game.net.peers[self.game.net.player_id].direction = self.game.player.direction
			
		else:
			
			if not os.path.exists(path + "Saves/Worlds/"):
				os.mkdir(cache_path + "Saves/Worlds/")

			os.mkdir(path + "Saves/Worlds/" + self.game.world_name)
			os.mkdir(path + "Saves/Worlds/" + self.game.world_name + "/Images")

			self.save(False, True)
			
