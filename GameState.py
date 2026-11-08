import pygame
from Globals import Width, Height

class GameState:

	def __init__(self):

		self.difficulty = "norm"
		self.shadow_surface = pygame.Surface((Width, Height), pygame.SRCALPHA)
		self.shadow_surface.fill((0, 0, 0, 90))
		self.chat = []
		self.main_chat = []
		self.chat_tick = 0
		self.chat_open = False
		self.events = []
		self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
		self.does_lighten = False
		self.in_motherboard = None

		self.item_settings_open = False
		self.craft_list_open = False
		self.inventory_open = False
		self.menu_open = False
		self.alt_pressed = False
		self.start_time = 0
		self.hold_left = False
		self.world_name = None
		self.current_biome = None
		self.night_playing = False
		self.release = False
		self.use_item_pressed = False

		self.multiplayer = False
		self.multiplayer_role = None
		self.net = None

		self.craft_list_offset = 0
		self.craft_list_max_offset = -1

	def close_sub_menus(self):
		
		if self.item_settings_open:
			self.item_settings_open = False
		elif self.ron.window[0]:
			self.ron.window[0] = False
		elif self.in_motherboard is not None:
			self.in_motherboard = None
		elif self.craft_list_open:
			self.craft_list_open = False
		elif self.inventory_open:
			self.inventory_open = False
		else:
			return True
		return False

	def clear_world_data(self):
		
		self.world.chunk_manager.chunks = {}
		self.world.mobs = []
		self.effects.effects = []
		self.world.particles = []
		self.chat = []
		self.main_chat = []
		self.chat_tick = 0
		self.inventory.whole_inventory = [None] * 30
		self.world_name = None

