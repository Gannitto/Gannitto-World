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
		
		"Display": {
			"Brightness": 100,
			"Inventory transparency": 90,
			"Distance": 0,
			"Display hitboxes": False,
			"Shadows": True,
			"Inventory slots animation": True,
			"FPS": 60,
			"Mouse click display": True,
			"Description of the object on hover": True,
			"Dim screen when turned off": True,
			"Show intro": True
			},
		"User": {
			"Nickname": "Player",
			"Developer mode": False
			},
		"Sound": {
			"Music volume": 100,
			"Sound volume": 100
			},
		"Game": {
			"Automatically pick up items": True,
			"Telephone control": False,
			"Mouse wheel sensitivity": 100,
			"Cursor blink rate": 0.7
			},
		"Languages": [
			"English"
			],
		"Keys": ["a",
		   "s",
		   "w",
		   "d",
		   "e",
		   "c",
		   "TAB", "SPACE"
		   ],
		"Multiplayer": {
			"Соединение через интернет": True,
			"Порт": 5555,
			"Внешний порт": 5555,
			"IP хоста": "127.0.0.1",
			"Порт хоста": 5555
			},
		"Edit world": {
			"World name": "",
			"God mode": False
			}
		
		}

win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
Width, Height = pygame.display.get_surface().get_size()
text_color = (0, 180, 0)
menu_color_light = (192, 203, 220)
menu_color_medium = (139, 155, 180)
menu_color_dark = (58, 68, 102)
textInfo = pygame.font.Font(path + "Font.ttf", 18)
bigTextInfo = pygame.font.Font(path + "Font.ttf", 36)

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

clock = pygame.time.Clock()
colors = {
	"Normal": (39, 155, 80),
	"Normal2": (0, 255, 0),
	"Backrooms": (100, 100, 0),
	"Backrooms2": (100, 80, 0)
}

