import pygame
from Assets import wall_images
from Globals import win, Settings

# Смещения и битовые веса соседей: (dx, dy, bit_weight)
NEIGHBOR_BITS = (
    (0, 256, 1),   # Верх
    (256, 0, 2),   # Право
    (0, -256, 4),  # Низ
    (-256, 0, 8)   # Лево
)

# Хитбоксы
WALL_RECTS = (
    (-24, -128, 48, 256),   # 0: одиночная
    (-24, -128, 48, 256),   # 1: верх
    (-24, -128, 152, 256),  # 2: право
    (-24, -128, 152, 256),  # 3: верх + право
    (-24, -128, 48, 256),   # 4: низ
    (-24, -128, 48, 256),   # 5: верх + низ
    (-24, -128, 152, 256),  # 6: право + низ
    (-24, -128, 152, 256),  # 7: верх + право + низ
    (-128, -128, 152, 256), # 8: лево
    (-128, -128, 152, 256), # 9: верх + лево
    (-128, -128, 256, 256), # 10: право + лево
    (-128, -128, 256, 256), # 11: верх + право + лево
    (-128, -128, 152, 256), # 12: низ + лево
    (-128, -128, 152, 256), # 13: верх + низ + лево
    (-128, -128, 256, 256), # 14: право + низ + лево
    (-128, -128, 256, 256)  # 15: все стороны
)
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

		mask = 0
		for dx, dy, bit in NEIGHBOR_BITS:
			nx, ny = self.x + dx, self.y + dy
			chunk = world.chunk_manager.get_chunk_at(nx, ny)
			if chunk is not None and (nx, ny) in chunk.walls:
				mask |= bit  # Побитовое ИЛИ добавляет вес соседа к маске

		self.image = self.images[mask]
		rx, ry, rw, rh = WALL_RECTS[mask]
		self.rect = pygame.Rect(self.x + rx, self.y + ry, rw, rh)		

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

