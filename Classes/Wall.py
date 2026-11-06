import pygame
from Assets import wall_images
from Globals import win, Settings

class Wall:

	def __init__(self, world, wall_type: str, X, Y, is_door: bool=False):

		self.x = X
		self.y = Y

		self.wall_type = wall_type
		self.neigbords = []
		self.is_door = is_door
		self.open = False
		self.rect = pygame.Rect(self.x - 24, self.y - 128, 48, 256)
		self.images = wall_images[self.wall_type]

		self.image = self.images[0]
		self.update_neigboors(world)

	def update_neigboors(self, world):

		self.neigbords = []
		for wall in ((self.x - 256, self.y), (self.x + 256, self.y), (self.x, self.y - 256), (self.x, self.y + 256)):
			chunk = world.chunk_manager.get_chunk_at(*wall)
			if chunk is not None and wall in chunk.walls:
				self.neigbords.append(wall)

		if self.is_door:

			if len(self.neigbords) == 0:
				if self.open:
					self.image = self.images[2]
				else:
					self.image = self.images[0]

			if len(self.neigbords) == 1:

				if self.neigbords[0][0] == self.x:
					if self.open:
						self.image = self.images[3]
					else:
						self.image = self.images[1]
				else:
					if self.open:
						self.image = self.images[2]
					else:
						self.image = self.images[0]

			elif len(self.neigbords) == 2:

				if self.neigbords[0][0] == self.x == self.neigbords[1][0]:
					if self.open:
						self.image = self.images[3]
					else:
						self.image = self.images[1]
				elif self.neigbords[0][1] == self.y == self.neigbords[1][1]:
					if self.open:
						self.image = self.images[2]
					else:
						self.image = self.images[0]

		else:

			if len(self.neigbords) == 1:

				if self.neigbords[0][0] < self.x:
					self.image = self.images[3]
					self.rect = pygame.Rect(self.x - 128, self.y - 128, 152, 256)
				elif self.neigbords[0][0] > self.x:
					self.image = self.images[4]
					self.rect = pygame.Rect(self.x - 24, self.y - 128, 152, 256)
				else:
					self.image = self.images[2]
					self.rect = pygame.Rect(self.x - 24, self.y - 128, 48, 256)

			elif len(self.neigbords) == 2:

				if self.neigbords[0][0] == self.x == self.neigbords[1][0]:
					self.image = self.images[2]
					self.rect = pygame.Rect(self.x - 24, self.y - 128, 48, 256)
				elif self.neigbords[0][1] == self.y == self.neigbords[1][1]:
					self.image = self.images[1]
					self.rect = pygame.Rect(self.x - 128, self.y - 128, 256, 256)
				elif (self.neigbords[0][0] == self.x - 256 and self.neigbords[1][1] == self.y + 256) or (self.neigbords[1][0] == self.x - 256 and self.neigbords[0][1] == self.y + 256):
					self.image = self.images[5]
					self.rect = pygame.Rect(self.x - 128, self.y - 128, 152, 256)
				elif (self.neigbords[0][0] == self.x + 256 and self.neigbords[1][1] == self.y + 256) or (self.neigbords[1][0] == self.x + 256 and self.neigbords[0][1] == self.y + 256):
					self.image = self.images[6]
					self.rect = pygame.Rect(self.x - 24, self.y - 128, 152, 256)
				elif (self.neigbords[0][0] == self.x + 256 and self.neigbords[1][1] == self.y - 256) or (self.neigbords[1][0] == self.x + 256 and self.neigbords[0][1] == self.y - 256):
					self.image = self.images[7]
					self.rect = pygame.Rect(self.x - 24, self.y - 128, 152, 256)
				elif (self.neigbords[0][0] == self.x - 256 and self.neigbords[1][1] == self.y - 256) or (self.neigbords[1][0] == self.x - 256 and self.neigbords[0][1] == self.y - 256):
					self.image = self.images[8]
					self.rect = pygame.Rect(self.x - 128, self.y - 128, 152, 256)

			elif len(self.neigbords) == 3:

				if self.neigbords[0][1] != self.y + 256 and self.neigbords[1][1] != self.y + 256 and self.neigbords[2][1] != self.y + 256:
					self.image = self.images[9]
					self.rect = pygame.Rect(self.x - 128, self.y - 128, 256, 256)
				if self.neigbords[0][1] != self.y - 256 and self.neigbords[1][1] != self.y - 256 and self.neigbords[2][1] != self.y - 256:
					self.image = self.images[10]
					self.rect = pygame.Rect(self.x - 128, self.y - 128, 256, 256)
				if self.neigbords[0][0] != self.x + 256 and self.neigbords[1][0] != self.x + 256 and self.neigbords[2][0] != self.x + 256:
					self.image = self.images[11]
					self.rect = pygame.Rect(self.x - 128, self.y - 128, 152, 256)
				if self.neigbords[0][0] != self.x - 256 and self.neigbords[1][0] != self.x - 256 and self.neigbords[2][0] != self.x - 256:
					self.image = self.images[12]
					self.rect = pygame.Rect(self.x - 24, self.y - 128, 152, 256)

			elif len(self.neigbords) == 4:
				self.image = self.images[12]
				self.rect = pygame.Rect(self.x - 128, self.y - 128, 256, 256)
		
	def main(self, release, mouse_x, mouse_y, game):
		screen_x, screen_y = game.world_to_screen(self.x, self.y, 256, 256)
		if self.is_door and release and screen_x <= mouse_x <= screen_x + 256 and screen_y <= mouse_y <= screen_y + 256:
			self.open = not self.open
			self.update_neigboors(game.world)
			if game.multiplayer:
				game.game_events.append({"event_type": "wall_interaction", "wall_pos": (self.x, self.y)})
		win.blit(self.image, game.world_to_screen(self.x, self.y, 256, 256))
		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), game.world_rect_to_screen(self.rect[0] + self.rect[2] // 2, self.rect[1] + self.rect[3] // 2, self.rect[2], self.rect[3]), 3)
		
	def __getstate__(self):
		
		state = self.__dict__.copy()
		state["image"] = self.images.index(self.image)
		del state["images"]
		if "world" in state:
			del state["world"]
		rect = state["rect"]
		state["rect"] = (rect[0], rect[1], rect[2], rect[3])
		return state

	def __setstate__(self, state):
		
		self.__dict__.update(state)
		self.images = wall_images[self.wall_type]
		self.image = self.images[self.image]

		self.rect = pygame.Rect(state["rect"][0], state["rect"][1], state["rect"][2], state["rect"][3])

