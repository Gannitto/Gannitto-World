import os
import time
import pygame
import Saver
import sys

if getattr(sys, "frozen", False):
	path = sys._MEIPASS
else:
	path = os.path.dirname(os.path.abspath(__file__)) + os.sep

default_settings = {
		
		"Display": [100, 90, 0, False, True, True, 30, True, True, True, True],
		"Languages": ["English"],
		"User": ["Player"],
		"Sound": [100, 100],
		"Keys": ["a", "s", "w", "d", "e", "c", "TAB", "SPACE"],
		"Game": [True, False]
		
		}

try:
	Settings = Saver.load_objects(path + "Settings/Settings.save")
except FileNotFoundError:
	Settings = default_settings
	Saver.save_objects(path + "Settings/Settings.save", Settings)

changed_slot = 0
animation = [None, 0]
player_bullets = []
craft_items_list = [None] * 7
craft_amounts_list = [None] * 7
craft_images_list = [None] * 7
does_lighten = False
alt_pressed = False
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
start_time = time.time()
world_name = None
MAX_FPS = Settings["Display"][6]
FPS = MAX_FPS - 1
page = 1
Width, Height = pygame.display.get_surface().get_size()
screenmode = "FULLSCREEN"
text_color = (0, 180, 0)
menu_color_light = (192, 203, 220)
menu_color_medium = (139, 155, 180)
menu_color_dark = (58, 68, 102)
menu_open = False
multiplayer_menu_open = False
textInfo = pygame.font.Font(path + "Font.ttf", 18)
bigTextInfo = pygame.font.Font(path + "Font.ttf", 36)
mouse_x, mouse_y = pygame.mouse.get_pos()
inventory_open = False
hold_left = False
backrooms_objects = []
screenshot_num = 1
bullet_num = 0
item_settings_open = False
craft_list_open = False
craft_list_page = 1
craft_list_offset = 0
craft_list_max_offset = -10000
multiplayer = False
multiplayer_role = None
host_net = None
client_net = None
slot_animations = [[False, 15] for _ in range(30)]   # Используется для анимации при наведении на слот
special_slot_animations = {"Craft list slot": [False, 0.6], "Game menu slot": [False, 0.6], "Menu slot": [False, 0.6], "Multiplayer slot": [False, 0.6], "Close slot": [False, 0.6], "Reference slot": [False, 0.6], "Close slot": [False, 0.6], "Split items slot": [False, 0.6], "Compact inventory slot": [False, 0.6]}   # Используется для анимации при наведении на слот, который выполняет какое-либо действие

try:
	statistics = Saver.load_objects(path + "Settings/Statistics.save")
except FileNotFoundError:
	statistics = [0, 0, 0]   # Заходы в игру, срублено деревьев

default_hot_keys = {
	
		"Multiplayer menu": pygame.K_m,
		"TAB menu": pygame.K_TAB,
		"Help": pygame.K_F1,
		"Menu": pygame.K_F2,
		"Screenshot": pygame.K_F3,
		"Change screen": pygame.K_F11,
		"Throw away the item": pygame.K_e,
		"Use item": pygame.K_SPACE,
		"Inventory": pygame.K_i,
		"Set Ron home": pygame.K_HOME,
		"Open chat": pygame.K_c,
		"Execute command": pygame.K_SLASH,
		"Noclip in backrooms": pygame.K_n,
		"Show keys": pygame.K_LALT,
		"Close": pygame.K_ESCAPE,
		"Plugin manager": pygame.K_p,
		"Move left": pygame.K_a,
		"Move right": pygame.K_d,
		"Move down": pygame.K_s,
		"Move up": pygame.K_w,
		
		}

try:
	
	hot_keys = Saver.load_objects(path + "Settings/Hot keys.save")
	
except FileNotFoundError:
	
	hot_keys = default_hot_keys
	Saver.save_objects(path + "Settings/Hot keys.save", hot_keys)

clock = pygame.time.Clock()
chat = []
main_chat = []
chat_tick = 0
in_motherboard = None
click = pygame.mouse.get_pressed()
screen_rect = pygame.Rect((0, 0, Width, Height))
