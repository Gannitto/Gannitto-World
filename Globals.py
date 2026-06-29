import os
import time
import pygame
import Saver

path = __file__[:-31]
if not os.path.exists(path):
	path = __file__[:-26] + "\\"

try:

	Settings = Saver.load_objects(path + "Gannitto world/files/Settings/Settings.save")

except FileNotFoundError:

	# После изменения настроек тут, надо бы изменить их и во вкладке настроек в функции show_reset_settings

	Settings = {
		
		"Display": [100, 90, 0, False, True, True, 30, True, True, True, True],
		"User": ["Gannitto"],
		"Sound": [1, 1],
		"Keys": ["a", "s", "w", "d", "e", "c", "TAB", "SPACE"],
		"Game": [True, False]
		
		}
	
	Saver.save_objects(path + "Gannitto world/files/Settings/Settings.save", Settings)

costum = 0
changed_slot = 0
animation = [None, 0]
player_bullets = []
craft_items_list = [None] * 7
craft_amounts_list = [None] * 7
craft_images_list = [None] * 7
in_cave = None
difficulty = None
does_lighten = False
alt_pressed = False
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
multyplayer_panel = pygame.surface.Surface((500, 250))
start_time = time.time()
world_name = None
from Inventory import inventory
FPS = Settings["Display"][6]
page = 1
weather = "Clear"
Width, Height = pygame.display.get_surface().get_size()
screenmode = "FULLSCREEN"
green_color = (87, 245, 66)
text_color = (0, 180, 0)
blue_color = (139, 155, 180)
menu_open = False
wall_list = []
multyplayer_menu_open = False
textInfo = pygame.font.Font(path + "Gannitto world/files/Font.ttf", 18)
bigTextInfo = pygame.font.Font(path + "Gannitto world/files/Font.ttf", 36)
changed_language = "Russian"
mouse_x, mouse_y = pygame.mouse.get_pos()
inventory_open = False
hold_left = False
# TODO возможность в настройках очистить кеш, переделать кнопку display,           реки, ачивки, берёзовый сок, стена из тёмной древесины, стол из тёмной древесины, музыкальные инструменты, падающие листья, кукуруза в полях, враги вороны, обвал в шахте, летучие мыши, таблички, забор, броня, хвощ(растение), песчаные бури в пустыне
backrooms_objects = []
screenshot_num = 1
bullet_num = 0
game_time = 0
item_settings_open = False
craft_list_open = False
craft_list_page = 1
multyplayer_mode = None
mobs = []
mechanisms = []
particles = []
slot_animations = [[False, 15] for _ in range(30)]   # Используется для анимации при наведении на слот
special_slot_animations = {"Craft list slot": [False, 0.6], "Game menu slot": [False, 0.6], "Menu slot": [False, 0.6], "Multyplayer slot": [False, 0.6], "Close slot": [False, 0.6], "Reference slot": [False, 0.6], "Close slot": [False, 0.6], "Split items slot": [False, 0.6]}   # Используется для анимации при наведении на слот, который выполняет какое-либо действие

try:

	statistics = Saver.load_objects(path + "Gannitto world/files/Settings/Statistics.save")

except FileNotFoundError:

	statistics = [0, 0, 0]   # Заходы в игру, срублено деревьев

# После изменения hot_keys'ов, надо обязательно изменить их и во вкладке keys в настройках
	
try:
	
	hot_keys = Saver.load_objects(path + "Gannitto world/files/Settings/Hot keys.save")
	
except FileNotFoundError:
	
	hot_keys = {
	
		"Multyplayer menu": pygame.K_m,
		"TAB menu": pygame.K_TAB,
		"Help": pygame.K_F1,
		"Menu": pygame.K_F2,
		"Screenshot": pygame.K_F3,
		"Change screen": pygame.K_F11,
		"Throw away the item": pygame.K_e,
		"Use item": pygame.K_SPACE,
		"Inventory": pygame.K_i,
		"Set Ron home": pygame.K_HOME
	
		}

	Saver.save_objects(path + "Gannitto world/files/Settings/Hot keys.save", hot_keys)

clock = pygame.time.Clock()
chat = []
main_chat = []
chat_tick = 0
in_motherboard = None
click = pygame.mouse.get_pressed()
mouse_click_image = None
