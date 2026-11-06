from itertools import product
from Chunks import ChunkManager
from Assets import biome_textures
from Globals import Width, Height, win

class World:

	def __init__(self, game):
		
		from Classes.Object import Object
		self.game = game
		self.chunk_manager = ChunkManager(Object, game.world_rect_to_screen)
		self.current_cave = None

		self.visible_objects = []
		self.visible_items = []
		self.visible_walls = {}
		self.visible_farmlands = {}
		self.visible_caves = []

		self.mobs = []
		self.particles = []
		self.mechanisms = []
		self.projectiles = []
		self.backrooms_objects = []
		
	def update(self):

		chunks_to_get = self.chunk_manager.update_visible_chunks(self.game.player.x, self.game.player.y, self.game.multiplayer and self.game.multiplayer_role == "Client")
		if self.game.multiplayer and self.game.multiplayer_role == "Client":
			for chunk_key in chunks_to_get:
				self.game.net._send_packet({"type": "get_chunk", "player_id": self.game.net.player_id, "chunk_key": chunk_key}, self.game.net.host_address)
				self.chunk_manager.chunks_to_get.append(chunk_key)
		# Сборка объектов из загруженных чанков
		self.visible_objects.clear()
		self.visible_items.clear()
		self.visible_walls.clear()
		self.visible_farmlands.clear()
		self.visible_caves.clear()
		for chunk_key in self.chunk_manager.loaded_chunks:
			chunk = self.chunk_manager.chunks[chunk_key]
			self.visible_objects.extend(chunk.objects)
			self.visible_items.extend(chunk.items)
			self.visible_walls.update(chunk.walls)
			self.visible_farmlands.update(chunk.farmlands)
			self.visible_caves.extend(chunk.caves)

	def render_loaded_chunks(self):

		"""Отрисовка загруженных чанков с их биомами"""

		for chunk_key in self.chunk_manager.loaded_chunks:
			chunk = self.chunk_manager.chunks.get(chunk_key)
			if chunk and chunk.is_generated:
				bounds = chunk.get_world_bounds()
				
				# Проверка, виден ли чанк на экране
				if (bounds["x2"] > self.game.player.x - Width // 2 and 
					bounds["x1"] < self.game.player.x + Width // 2 and
					bounds["y2"] > self.game.player.y - Height // 2 and 
					bounds["y1"] < self.game.player.y + Height):
					
					biome_texture = biome_textures.get(chunk.biome)
					if biome_texture:
						# Смещение чанка относительно игрока
						offset_x = bounds["x1"] - self.game.player.x + Width // 2
						offset_y = self.game.player.y - bounds["y1"] + Height // 2
						
						# Отрисовка тайлов чанка
						tiles_per_chunk = 2048 // 256
						for tile_x, tile_y in product(range(tiles_per_chunk), range(tiles_per_chunk)):
							tile_screen_x = offset_x + tile_x * 256
							tile_screen_y = offset_y - tile_y * 256
							if (tile_screen_x > -256 and 
								tile_screen_x < Width and
								tile_screen_y > -256 and 
								tile_screen_y < Height):
								win.blit(biome_texture, (tile_screen_x, tile_screen_y))

					if chunk.transition_image is not None:
						win.blit(chunk.transition_image, (bounds["x1"] - self.game.player.x + Width // 2, self.game.player.y - bounds["y2"] + Height // 2 + 256))


