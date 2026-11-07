import os
import time
import pygame
import Saver
import sys

pygame.init()

if getattr(sys, "frozen", False):
	path = sys._MEIPASS
else:
	path = os.path.dirname(os.path.abspath(__file__)) + os.sep

default_settings = {
		
		"Display": [100, 90, 0, False, True, True, 60, True, True, True, True],
		"Languages": ["English"],
		"User": ["Player", False],
		"Sound": [100, 100],
		"Keys": ["a", "s", "w", "d", "e", "c", "TAB", "SPACE"],
		"Game": [True, False, 100, 0.7],
		"Multiplayer": [True, 5555, 5555, "127.0.0.1", 5555],
		"Edit world": ["", False]
		
		}

try:
	Settings = Saver.load_objects(path + "Saves/Settings/Settings.save")
except FileNotFoundError:
	Settings = default_settings
	Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)

win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
MAX_FPS = Settings["Display"][6]
FPS = MAX_FPS - 1
Width, Height = pygame.display.get_surface().get_size()
text_color = (0, 180, 0)
menu_color_light = (192, 203, 220)
menu_color_medium = (139, 155, 180)
menu_color_dark = (58, 68, 102)
textInfo = pygame.font.Font(path + "Font.ttf", 18)
bigTextInfo = pygame.font.Font(path + "Font.ttf", 36)

try:
	statistics = Saver.load_objects(path + "Saves/Settings/Statistics.save")
except FileNotFoundError:
	statistics = [0, 0, 0]   # Заходы в игру, срублено деревьев

default_hot_keys = {
	
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
		"Move left": pygame.K_a,
		"Move right": pygame.K_d,
		"Move down": pygame.K_s,
		"Move up": pygame.K_w,
		
		}

try:
	
	hot_keys = Saver.load_objects(path + "Saves/Settings/Hot keys.save")
	
except FileNotFoundError:
	
	hot_keys = default_hot_keys
	Saver.save_objects(path + "Saves/Settings/Hot keys.save", hot_keys)

clock = pygame.time.Clock()
colors = {
	"Normal": (39, 155, 80),
	"Normal2": (0, 255, 0),
	"Backrooms": (100, 100, 0),
	"Backrooms2": (100, 80, 0)
}
