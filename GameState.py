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
		self.slot_animations = [[False, 15] for _ in range(30)]   # Используется для анимации при наведении на слот
		self.special_slot_animations = {"Craft list slot": [False, 0.6], "Game menu slot": [False, 0.6], "Menu slot": [False, 0.6], "Multiplayer slot": [False, 0.6], "Close slot": [False, 0.6], "Reference slot": [False, 0.6], "Close slot": [False, 0.6], "Split items slot": [False, 0.6], "Compact inventory slot": [False, 0.6]}   # Используется для анимации при наведении на слот, который выполняет какое-либо действие

		self.item_settings_open = False
		self.craft_list_open = False
		self.inventory_open = False
		self.menu_open = False
		self.multiplayer_menu_open = False
		self.alt_pressed = False
		self.start_time = 0
		self.hold_left = False
		self.world_name = None
		self.current_biome = None
		self.night_playing = False
		self.release = False

		self.multiplayer = False
		self.multiplayer_role = None
		self.net = None

		self.craft_list_offset = 0
		self.craft_list_max_offset = -1
