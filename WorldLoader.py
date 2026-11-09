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

			os.mkdir(path + "Saves/Worlds/" + self.game.world_name)
			os.mkdir(path + "Saves/Worlds/" + self.game.world_name + "/Images")

			self.save(False, True)
		
		# Старая система плагинов, которая уже толком не работает. От неё нужно отказываться в пользу модов (которые ещё не созданы)
		plugins = []
		for _, _, files in os.walk(os.path.dirname(path) + "/Plugins/"):
			plugins = files
			break
		
		for plugin in plugins:

			for i in Saver.load_objects(os.path.dirname(path) + "/Plugins/" + plugin):

				match i[0]:

					case "Item":
						
						from Inventory import Resource
						try:
							self.game.inventory.resources[i[1]] = Resource(i[1], i[2], [i[3], i[4]], [i[5], i[6]], i[7])
						except FileNotFoundError:
							self.game.inventory.resources[i[1]] = Resource(i[1], path + "Images/No-file texture.png", [i[3], i[4]], [i[5], i[6]], i[7])

					case "Recipe":

						from Inventory import Recipe
						a = []
						for ii in i[2]: a.append(str(ii))
						self.game.inventory.recipes.append(Recipe(i[1], a, i[3], i[4], i[5], i[6]))
						del Recipe
			
					case "Object":

						try:
							a = Object(i[1], i[3], i[4], i[2], (load(i[2]).get_width(), load(i[2]).get_height()), special_flags=i[5], add_path=False)
						except FileNotFoundError:
							a = Object(i[1], i[3], i[4], "Images/No-file texture.png", special_flags=i[5])
						b = True
						for object in self.game.world.visible_objects:
							if a == object:
								b = False
						if b and self.game.world_name == i[6]:
							self.game.world.visible_objects.append(a)

					case "Command":

						if i[2] == "1":
							try:
								eval(i[1])
							except:
								pass
	
