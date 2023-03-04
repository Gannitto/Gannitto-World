import pygame
from pygame.locals import *
import time
import random
from SaveLoadMananger import SaveLoadSystem
import Big_rect
from math import atan2, cos, sin, atan
import Backrooms
import socket
import getpass
from screen_brightness_control import get_brightness, set_brightness
import os
pygame.init()



# Переменные

x = 0
y = 0
speed = 128
HP = 50
costum = 0
changed_slot = 0
player_bullets = []
craft_items_list = [None] * 7
craft_amounts_list = [None] * 7
craft_images_list = [None] * 7
in_cave = None

num = 1

win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
multyplayer_panel = pygame.surface.Surface((500, 250))
world_name = None
from Inventory import inventory, Resourse
FPS = 30
page = 1
Width, Height = pygame.display.get_surface().get_size()
screenmode = "FULLSCREEN"
color = 87, 245, 66
text_color = 0, 180, 0
menu_open = 0
multyplayer_panel_open = 0
textInfo = pygame.font.Font("Font.ttf", 18)
changed_laungvege = "Russian"
path = os.path.abspath(__file__)[:os.path.abspath(__file__).index("Gannitto world")]
Save_load_mananger = SaveLoadSystem(".save", path + "Gannitto world/files/Worlds")
mouse_x, mouse_y = pygame.mouse.get_pos()
inventory_open = 0
hold_left = False
objects = [] # TODO ачивки, берёза, берёзовый сок, граната, порох, тёмная древесина, стена из тёмной древесины, стол из тёмной древесины, золотая руда, музыкальные инструменты
object_to_remove = None
backrooms_objects = []
backrooms_object_to_remove = None
screenshot_num = 1
bullet_num = 0
item_settings_open = False
craft_list_open = False
craft_list_page = 1
mobs = []
bioms = []
mechanisms = []
try:
    Settings = SaveLoadSystem(".save", path + "Gannitto world/files/").load_data("Settings")
    Settings[0] = get_brightness()[0]
except FileNotFoundError:
    Settings = [get_brightness()[0], 90, "Gannitto", 0, False]   # яркость экрана, прозрачность инвентаря, ник, отдаление, показать хитбоксы
screenmode == "FULLSCREEN"
clock = pygame.time.Clock()
chat = []
chat_tick = 0
in_motherboard = None
click = pygame.mouse.get_pressed()
mouse_click_image = None



# запуск игры

pygame.display.set_icon(pygame.image.load(path + "Gannitto world/files/Images/Icon.png"))
pygame.display.set_caption("Gannitto world")

Hiro_down_run_1 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Down/1.png")
Hiro_down_run_2 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Down/2.png")
Hiro_down_run_3 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Down/3.png")
Hiro_down_run_4 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Down/4.png")
Hiro_down_run_5 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Down/5.png")
Hiro_down_run_6 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Down/6.png")

Hiro_down_left = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Down-left/1.png")
Hiro_down_right = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Down-right/1.png")

Hiro_left_run_1 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Left/1.png")
Hiro_left_run_2 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Left/2.png")
Hiro_left_run_3 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Left/3.png")
Hiro_left_run_4 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Left/4.png")
Hiro_left_run_5 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Left/5.png")
Hiro_left_run_6 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Left/6.png")

Hiro_right_run_1 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Right/1.png")
Hiro_right_run_2 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Right/2.png")
Hiro_right_run_3 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Right/3.png")
Hiro_right_run_4 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Right/4.png")
Hiro_right_run_5 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Right/5.png")
Hiro_right_run_6 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Right/6.png")

Hiro_up_run_1 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Up/1.png")
Hiro_up_run_2 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Up/2.png")
Hiro_up_run_3 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Up/3.png")
Hiro_up_run_4 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Up/4.png")
Hiro_up_run_5 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Up/5.png")
Hiro_up_run_6 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Up/6.png")

Hiro_up_left = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Up-left/1.png")

Hiro_up_right_run_1 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Up-right/1.png")
Hiro_up_right_run_2 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Up-right/2.png")
Hiro_up_right_run_3 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Up-right/3.png")
Hiro_up_right_run_4 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Up-right/4.png")
Hiro_up_right_run_5 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Up-right/5.png")
Hiro_up_right_run_6 = pygame.image.load(path + "Gannitto world/files/Images/Players/Hiro/Normal/Up-right/6.png")

Hiro = Hiro_down_run_1
Hiro_run = "Down"
Hiro_rect = Hiro.get_rect(center=(Width / 2, Height / 2))

arrow_down = pygame.image.load(path + "Gannitto world/files/Phone Version Components/DOWN.png")
arrow_down = pygame.transform.scale(arrow_down, (64, 64))
arrow_left = pygame.image.load(path + "Gannitto world/files/Phone Version Components/LEFT.png")
arrow_left = pygame.transform.scale(arrow_left, (64, 64))
arrow_right = pygame.image.load(path + "Gannitto world/files/Phone Version Components/RIGHT.png")
arrow_right = pygame.transform.scale(arrow_right, (64, 64))
arrow_up = pygame.image.load(path + "Gannitto world/files/Phone Version Components/UP.png")
arrow_up = pygame.transform.scale(arrow_up, (64, 64))

PlayButton = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Play.png")
PlayButton = pygame.transform.scale(PlayButton, (256, 128))
PlayButton2 = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Play 2.png")
PlayButton2 = pygame.transform.scale(PlayButton2, (256, 128))
SettingsButton = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Settings.png")
SettingsButton = pygame.transform.scale(SettingsButton, (480, 128))
SettingsButton2 = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Settings 2.png")
SettingsButton2 = pygame.transform.scale(SettingsButton2, (480, 128))
ChangeACharacterButton = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Change a character.png")
ChangeACharacterButton = pygame.transform.scale(ChangeACharacterButton, (960, 128))
ChangeACharacterButton2 = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Change a character 2.png")
ChangeACharacterButton2 = pygame.transform.scale(ChangeACharacterButton2, (960, 128))
BackButton = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Back.png")
BackButton = pygame.transform.scale(BackButton, (128, 128))
BackButton2 = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Back 2.png")
BackButton2 = pygame.transform.scale(BackButton2, (128, 128))
CharacterButton = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Character.png")
CharacterButton = pygame.transform.scale(CharacterButton, (278, 64))
CharacterButton2 = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Character 2.png")
CharacterButton2 = pygame.transform.scale(CharacterButton2, (278, 64))
PetsButton = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Pets.png")
PetsButton = pygame.transform.scale(PetsButton, (132, 64))
PetsButton2 = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Pets 2.png")
PetsButton2 = pygame.transform.scale(PetsButton2, (132, 64))
HelpButton = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Help.png")
HelpButton = pygame.transform.scale(HelpButton, (132, 64))
HelpButton2 = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Help 2.png")
HelpButton2 = pygame.transform.scale(HelpButton2, (132, 64))
DisplayButton = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Display.png")
DisplayButton = pygame.transform.scale(DisplayButton, (222, 64))
DisplayButton2 = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Display 2.png")
DisplayButton2 = pygame.transform.scale(DisplayButton2, (222, 64))
LaungvegesButton = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Laungveges.png")
LaungvegesButton = pygame.transform.scale(LaungvegesButton, (336, 64))
LaungvegesButton2 = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Laungveges 2.png")
LaungvegesButton2 = pygame.transform.scale(LaungvegesButton2, (336, 64))
EnglishButton = pygame.image.load(path + "Gannitto world/files/Images/Buttons/English.png")
EnglishButton = pygame.transform.scale(EnglishButton, (228, 64))
EnglishButton2 = pygame.image.load(path + "Gannitto world/files/Images/Buttons/English 2.png")
EnglishButton2 = pygame.transform.scale(EnglishButton2, (228, 64))
RussianButton = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Russian.png")
RussianButton = pygame.transform.scale(RussianButton, (228, 64))
RussianButton2 = pygame.image.load(path + "Gannitto world/files/Images/Buttons/Russian 2.png")
RussianButton2 = pygame.transform.scale(RussianButton2, (228, 64))
UserButton = pygame.image.load(path + "Gannitto world/files/Images/Buttons/User.png")
UserButton = pygame.transform.scale(UserButton, (132, 64))
UserButton2 = pygame.image.load(path + "Gannitto world/files/Images/Buttons/User 2.png")
UserButton2 = pygame.transform.scale(UserButton2, (132, 64))

Inventory_slot = pygame.image.load(path + "Gannitto world/files/Images/Inventory slot.png")
Inventory_slot = pygame.transform.scale(Inventory_slot, (64, 64))

Changed_inventory_slot = pygame.image.load(path + "Gannitto world/files/Images/Changed inventory slot.png")
Changed_inventory_slot = pygame.transform.scale(Changed_inventory_slot, (64, 64))

Object_inventory_slot = pygame.image.load(path + "Gannitto world/files/Images/Object inventory slot.png")
Object_inventory_slot = pygame.transform.scale(Object_inventory_slot, (64, 64))

Tool_inventory_slot = pygame.image.load(path + "Gannitto world/files/Images/Tool inventory slot.png")
Tool_inventory_slot = pygame.transform.scale(Tool_inventory_slot, (64, 64))

Split_items1 = pygame.image.load(path + "Gannitto world/files/Images/Split_items1.png")
Split_items1 = pygame.transform.scale(Split_items1, (64, 64))
Split_items2 = pygame.image.load(path + "Gannitto world/files/Images/Split_items2.png")
Split_items2 = pygame.transform.scale(Split_items2, (64, 64))

Inventory_slot.set_alpha(Settings[1])
Changed_inventory_slot.set_alpha(Settings[1])
Object_inventory_slot.set_alpha(Settings[1])
Tool_inventory_slot.set_alpha(Settings[1])
Split_items1.set_alpha(Settings[1])
Split_items2.set_alpha(Settings[1])

Table = pygame.image.load(path + "Gannitto world/files/Images/Objects/Table.png")
Table = pygame.transform.scale(Table, (256, 256))

Wall_table = pygame.image.load(path + "Gannitto world/files/Images/Objects/Wall table.png")
Wall_table = pygame.transform.scale(Wall_table, (256, 256))

Pot = pygame.image.load(path + "Gannitto world/files/Images/Objects/Pot.png")
Pot = pygame.transform.scale(Pot, (64, 64))

cave = pygame.image.load(path + "Gannitto world/files/Images/Objects/Cave.png")
cave = pygame.transform.scale(cave, (128, 128))

Furnace = pygame.image.load(path + "Gannitto world/files/Images/Items/Furnace.png")
Furnace = pygame.transform.scale(Furnace, (256, 256))

Portal_1 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Portal 1.png")
Portal_1 = pygame.transform.scale(Portal_1, (128, 256))
Portal_2 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Portal 2.png")
Portal_2 = pygame.transform.scale(Portal_2, (128, 256))

Vending_machine_image = pygame.image.load(path + "Gannitto world/files/Images/Objects/Vending machine.png")

Wire_1 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Wire 1.png")
Wire_1 = pygame.transform.scale(Wire_1, (64, 64))
Wire_2 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Wire 2.png")
Wire_2 = pygame.transform.scale(Wire_2, (64, 64))
Wire_3 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Wire 3.png")
Wire_3 = pygame.transform.scale(Wire_3, (64, 64))
Wire_4 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Wire 4.png")
Wire_4 = pygame.transform.scale(Wire_4, (64, 64))
Wire_5 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Wire 5.png")
Wire_5 = pygame.transform.scale(Wire_5, (64, 64))
Wire_6 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Wire 6.png")
Wire_6 = pygame.transform.scale(Wire_6, (64, 64))
Wire_7 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Wire 7.png")
Wire_7 = pygame.transform.scale(Wire_7, (64, 64))
Wire_8 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Wire 8.png")
Wire_8 = pygame.transform.scale(Wire_8, (64, 64))
Wire_9 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Wire 9.png")
Wire_9 = pygame.transform.scale(Wire_9, (64, 64))
Wire_10 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Wire 10.png")
Wire_10 = pygame.transform.scale(Wire_10, (64, 64))
Wire_11 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Wire 11.png")
Wire_11 = pygame.transform.scale(Wire_11, (64, 64))

Random_box_1 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Random Box 1.png")
Random_box_1 = pygame.transform.scale(Random_box_1, (64, 64))
Random_box_2 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Random Box 2.png")
Random_box_2 = pygame.transform.scale(Random_box_2, (64, 64))
Random_box_3 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Random Box 3.png")
Random_box_3 = pygame.transform.scale(Random_box_3, (64, 64))
Random_box_4 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Random Box 4.png")
Random_box_4 = pygame.transform.scale(Random_box_4, (64, 64))

Slime1 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Blue Slime 1.png")
Slime1 = pygame.transform.scale(Slime1, (128, 128))
Slime1_2 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Blue Slime 2.png")
Slime1_2 = pygame.transform.scale(Slime1_2, (128, 128))
Slime1_3 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Blue Slime 3.png")
Slime1_3 = pygame.transform.scale(Slime1_3, (128, 128))
Slime1_4 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Blue Slime 4.png")
Slime1_4 = pygame.transform.scale(Slime1_4, (128, 128))
Slime2 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Pink Slime 1.png")
Slime2 = pygame.transform.scale(Slime2, (128, 128))
Slime2_2 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Pink Slime 2.png")
Slime2_2 = pygame.transform.scale(Slime2_2, (128, 128))
Slime2_3 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Pink Slime 3.png")
Slime2_3 = pygame.transform.scale(Slime2_3, (128, 128))
Slime2_4 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Pink Slime 4.png")
Slime2_4 = pygame.transform.scale(Slime2_4, (128, 128))

Butterfly1 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Butterfly 1 1.png")
Butterfly1 = pygame.transform.scale(Butterfly1, (32, 32))
Butterfly1_2 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Butterfly 1 2.png")
Butterfly1_2 = pygame.transform.scale(Butterfly1_2, (32, 32))
Butterfly1_3 = pygame.image.load(path + "Gannitto world/files/Images/Objects/Butterfly 1 3.png")
Butterfly1_3 = pygame.transform.scale(Butterfly1_3, (32, 32))

Bacteria_walk_left = [

    pygame.image.load(path + "Gannitto world/files/Images/Objects/Bacteria 1.png"),
    pygame.image.load(path + "Gannitto world/files/Images/Objects/Bacteria 2.png"),
    pygame.image.load(path + "Gannitto world/files/Images/Objects/Bacteria 3.png"),
    pygame.image.load(path + "Gannitto world/files/Images/Objects/Bacteria 4.png"),
    pygame.image.load(path + "Gannitto world/files/Images/Objects/Bacteria 5.png"),
    pygame.image.load(path + "Gannitto world/files/Images/Objects/Bacteria 6.png")

    ]

Screensaver2 = pygame.image.load(path + "Gannitto world/files/Images/Screensavers/Screensaver 2.png")
Screensaver2 = pygame.transform.scale(Screensaver2, (Width + Height // 64, Height))

textures = {

    "Grass": pygame.image.load(path + "Gannitto world/files/Images/Bioms/Grass.png"),
    "Sand": pygame.image.load(path + "Gannitto world/files/Images/Bioms/Sand.png"),
    "Field": pygame.image.load(path + "Gannitto world/files/Images/Bioms/Field.png"),
    "Snow": pygame.image.load(path + "Gannitto world/files/Images/Bioms/Snow.png"),
    "Swamp": pygame.image.load(path + "Gannitto world/files/Images/Bioms/Swamp.png"),
    "Backrooms 0": pygame.image.load(path + "Gannitto world/files/Images/Bioms/Backrooms 0.png"),
    "Backrooms 0.2": pygame.image.load(path + "Gannitto world/files/Images/Bioms/Backrooms 0.2.png")
    }

Backrooms_portal_images = [
    pygame.image.load(path + "Gannitto world/files/Images/Objects/Backrooms portal 1.png"),
    pygame.image.load(path + "Gannitto world/files/Images/Objects/Backrooms portal 2.png"),
    pygame.image.load(path + "Gannitto world/files/Images/Objects/Backrooms portal 3.png"),
    pygame.image.load(path + "Gannitto world/files/Images/Objects/Backrooms portal 4.png"),
    pygame.image.load(path + "Gannitto world/files/Images/Objects/Backrooms portal 5.png"),
    pygame.image.load(path + "Gannitto world/files/Images/Objects/Backrooms portal 6.png"),
    pygame.image.load(path + "Gannitto world/files/Images/Objects/Backrooms portal 7.png"),
    pygame.image.load(path + "Gannitto world/files/Images/Objects/Backrooms portal 8.png"),
    pygame.image.load(path + "Gannitto world/files/Images/Objects/Backrooms portal 9.png"),
    pygame.image.load(path + "Gannitto world/files/Images/Objects/Backrooms portal 10.png")
]

mouse_click_images = [
     pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Mouse click 1.png"), (128, 128)),
     pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Mouse click 2.png"), (128, 128)),
     pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Mouse click 3.png"), (128, 128)),
     pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Mouse click 4.png"), (128, 128)),
     pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Mouse click 5.png"), (128, 128))
     ]

no_file_texture = pygame.image.load("Images/No-file texture.png")
no_file_texture = pygame.transform.scale(no_file_texture, (64, 64))

Button_click = pygame.mixer.Sound(path + "Gannitto world/files/sounds/Button Pressed.mp3")
Stone_breaking1 = pygame.mixer.Sound(path + "Gannitto world/files/sounds/Stone breaking 1.mp3")
Stone_breaking2 = pygame.mixer.Sound(path + "Gannitto world/files/sounds/Stone breaking 2.mp3")
Grass_walking1 = pygame.mixer.Sound(path + "Gannitto world/files/sounds/Grass walking 1.mp3")
Grass_walking2 = pygame.mixer.Sound(path + "Gannitto world/files/sounds/Grass walking 2.mp3")
Grass_walking3 = pygame.mixer.Sound(path + "Gannitto world/files/sounds/Grass walking 3.mp3")
Snow_walking1 = pygame.mixer.Sound(path + "Gannitto world/files/sounds/Snow walking 1.mp3")
Snow_walking2 = pygame.mixer.Sound(path + "Gannitto world/files/sounds/Snow walking 2.mp3")
Snow_walking3 = pygame.mixer.Sound(path + "Gannitto world/files/sounds/Snow walking 3.mp3")
Sand_walking1 = pygame.mixer.Sound(path + "Gannitto world/files/sounds/Sand walking 1.mp3")
Sand_walking2 = pygame.mixer.Sound(path + "Gannitto world/files/sounds/Sand walking 2.mp3")
Sand_walking3 = pygame.mixer.Sound(path + "Gannitto world/files/sounds/Sand walking 3.mp3")
Swamp_walking1 = pygame.mixer.Sound(path + "Gannitto world/files/sounds/Swamp walking 1.mp3")
Swamp_walking2 = pygame.mixer.Sound(path + "Gannitto world/files/sounds/Swamp walking 2.mp3")
Swamp_walking3 = pygame.mixer.Sound(path + "Gannitto world/files/sounds/Swamp walking 3.mp3")
Backrooms_lamps = pygame.mixer.Sound(path + "Gannitto world/files/sounds/Backrooms/1.mp3")
Backrooms_rand_sound_1 = pygame.mixer.Sound(path + "Gannitto world/files/sounds/Backrooms/Random Sounds/1.mp3")
Pick_an_item = pygame.mixer.Sound(path + "Gannitto world/files/Sounds/Pick an item.mp3")

music_1 = pygame.mixer.Sound(path + "Gannitto world/files/Soundtracks/1.mp3")

colors = {
    "Normal": (39, 155, 80),
    "Normal2": (0, 255, 0),
    "Backrooms": (100, 100, 0),
    "Backrooms2": (100, 80, 0)
}



for dirs, folder, files in os.walk(path + "Gannitto world/Plugins/"):
    inside_files = files
    break

for file in inside_files:
    for i in SaveLoadSystem(".save", path + "Gannitto world/Plugins").load_data(file[0:-5]):
        match i[0]:
            case "Item":
                try:
                    inventory.resourses[i[1]] = Resourse(i[1], i[2], [i[3], i[4]], [i[5], i[6]], i[7])
                except FileNotFoundError:
                    inventory.resourses[i[1]] = Resourse(i[1], path + "Gannitto world/files/Images/No-file texture.png", [i[3], i[4]], [i[5], i[6]], i[7])

            case "Recipe":
                from Inventory import Recipe
                a = []
                for ii in i[2]: a.append(str(ii))
                inventory.recipes.append(Recipe(i[1], a, i[3], i[4], i[5], i[6]))


def laungveges(Russian: str, English: str) -> str:
    return eval(changed_laungvege)

def save():
    global Save_load_mananger
    Save_load_mananger = SaveLoadSystem(".save", path + "Gannitto world/files/Worlds/" + world_name)
    mobs2 = []
    for mob in mobs:
        if mob.__class__ == SlimeEnemy:
            mobs2.append(["Slime", mob.x, mob.y,mob.rand_mob, mob.HP, mob.animation_count, mob.reset_offset, mob.offset_x, mob.offset_y])
        if mob.__class__ == ButterflyEnemy:
            mobs2.append(["Butterfly", mob.x, mob.y,mob.rand_mob, mob.HP, mob.animation_count, mob.reset_offset, mob.offset_x, mob.offset_y])
    Save_load_mananger.save_data(mobs2, "Mobs")
            
    big_rects2 = []
    for big_rect in big_rects:
        big_rects2.append([big_rect.x, big_rect.y, big_rect.biom])
    Save_load_mananger.save_data(big_rects2, "Rects")

    Save_load_mananger.save_data([x, y, Backrooms.InBackrooms, Backrooms.Level, in_cave, speed, HP], "Info")
    
    objects2 = []
    for object in objects:
        if object.__class__ == Object or "Gannitto_world.Object":
            objects2.append(["Object", object.name, object.x, object.y, object.image_path, [object.w, object.h], object.special_flags])
        else:
            print(object.__class__)
    Save_load_mananger.save_data(objects2, "Objects")

    inventory2 = []
    for item in inventory.whole_inventory:
        if item == None:
            inventory2.append(None)
        else:
            inventory2.append([item.name, item.info, item.purpose, item.type, item.amount, item.settings, item.image_path])
    Save_load_mananger.save_data(inventory2, "Inventory")

class Object:
    def __init__(self, name: str, object_x: int, object_y: int, image_path: str, scale_x: list = [64, 64], image = None, special_flags: str = None):
        self.name = name
        self.x = object_x
        self.y = object_y
        if image == None:
            self.image = pygame.transform.scale(pygame.image.load(path + image_path), (scale_x[0], scale_x[1]))
        else:
            self.image = pygame.transform.scale(image, (scale_x[0], scale_x[1]))
        self.image_path = image_path
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.special_flags = special_flags
        self.num = len(objects)
    
    def main(self, x, y):
        if x - Width // 2 <= self.x <= x + Width // 2 and y - Height // 2 <= self.y + Height // 2:
            win.blit(self.image, (self.x - x + Width // 2 - self.w // 2, y - self.y + Height // 2 - self.h // 2))
        if Settings[4]:
            pygame.draw.rect(win, (0, 0, 0), (self.x - x + Width // 2 - self.w // 2, y - self.y + Height // 2 - self.h // 2, self.w, self.h), 3)

    def get_left_pressed(self):
        click = pygame.mouse.get_pressed()
        if click[0] == 1 and self.x - x + Width // 2 - self.image.get_width() // 2 <= mouse_x <= self.x - x + Width // 2 + self.w // 2 and y - self.y + Height // 2 - self.h // 2 <= mouse_y <= y - self.y + Height // 2 + self.h // 2:
            return True
        else:
            return False

    def get_right_pressed(self):
        click = pygame.mouse.get_pressed()
        if click[2] == 1 and self.x - x + Width // 2 - self.image.get_width() // 2 <= mouse_x <= self.x - x + Width // 2 + self.w // 2 and y - self.y + Height // 2 - self.h // 2 <= mouse_y <= y - self.y + Height // 2 + self.h // 2:
            return True
        else:
            return False

class SlimeEnemy:
    def __init__(self, mob_x: int, mob_y: int):
        self.x = mob_x
        self.y = mob_y
        self.rand_mob = random.randint(1, 2)
        if self.rand_mob == 1: self.animation_images = [Slime1, Slime1_2, Slime1_3, Slime1_4]
        else: self.animation_images = [Slime2, Slime2_2, Slime2_3, Slime2_4]
        self.rect = self.animation_images[0].get_rect()   # Хитбокс моба
        self.HP = 50
        self.animation_count = -1
        self.reset_offset = 0
        self.offset_x = random.randint(-3000, 3000)
        self.offset_y = random.randint(-3000, 3000)
        self.speed = random.randint(1, 3)
    
    def main(self):
        self.animation_count += 1
        if self.animation_count == 20:
            self.animation_count = 0
        
        if self.reset_offset == 0:
            if self.HP < 16:
                self.reset_offset = random.randint(1200, 1500)
                self.offset_x = random.randint(-30000, 30000)
                self.offset_y = random.randint(-30000, 30000)
            else:
                self.reset_offset = random.randint(120, 150)
                self.offset_x = random.randint(-3000, 3000)
                self.offset_y = random.randint(-3000, 3000)
        else:
            self.reset_offset -= 1
        
        if x + self.offset_x > self.x:
            self.x += self.speed
        elif x + self.offset_x < self.x:
            self.x -= self.speed
        
        if y + self.offset_y > self.y:
            self.y += self.speed
        elif y + self.offset_y < self.y - y:
            self.y -= self.speed

        if self.HP < 16 and self.speed < 8:
            self.speed += 1
        
        win.blit(self.animation_images[(self.animation_count - self.animation_count % 5) // 5], (self.x - x + Width // 2 - 64, y - self.y + Height // 2 - 32))
        if Settings[4]:
            pygame.draw.rect(win, (0, 0, 0), (self.x - x + Width // 2 - 64, y - self.y + Height // 2 - 24, 128, 128), 3)

class ButterflyEnemy:
    def __init__(self, mob_x, mob_y):
        self.x = mob_x
        self.y = mob_y
        self.rand_mob = random.randint(1, 2)
        self.animation_images = [Butterfly1, Butterfly1_2, Butterfly1_3, Butterfly1_2]
        self.HP = 10
        self.animation_count = -1
        self.reset_offset = 0
        self.offset_x = random.randint(-3000, 3000)
        self.offset_y = random.randint(-3000, 3000)
    
    def main(self):
        self.animation_count += 1
        if self.animation_count == 8:
            self.animation_count = 0
        
        if self.reset_offset == 0:
            self.reset_offset = random.randint(120, 150)
            self.offset_x = random.randint(-3000, 3000)
            self.offset_y = random.randint(-3000, 3000)
        else:
            self.reset_offset -= 1
        
        if x + self.offset_x > self.x:
            self.x += 1
        elif x + self.offset_x < self.x:
            self.x -= 1
        
        if y + self.offset_y > self.y:
            self.y += 1
        elif y + self.offset_y < self.y - y:
            self.y -= 1
        
        win.blit(self.animation_images[(self.animation_count - self.animation_count % 2) // 2], (self.x - x + Width // 2 - 64, y - self.y + Height // 2 - 32))
        if Settings[4]:
            pygame.draw.rect(win, (0, 0, 0), (self.x - x + Width // 2 - 32, y - self.y + Height // 2 - 32, 64, 64), 3)

mobs = [ButterflyEnemy(0, 0)]



class Bullet():
    def __init__(self, bullet_x: int, bullet_y: int, mouse_x, mouse_y):
        from math import pi
        self.x = bullet_x
        self.y = bullet_y
        self.num = bullet_num
        self.angle = atan2(Height / 2 - mouse_y, Width / 2 - mouse_x)
        self.x_vel = cos(self.angle) * 15
        self.y_vel = sin(self.angle) * 15
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Items/Bullet.png"),
                                                                    (64, 64)), atan2(mouse_x - Width / 2, mouse_y - Height / 2) * 180 / pi + 180)
    def main(self):
        """Shows the bullet"""
        self.x -= int(self.x_vel)
        self.y += int(self.y_vel)

        if self.x_vel < 0:
            self.x += 30
        else:
            self.x -= 30

        if self.y_vel > 0:
            self.y += 30
        else:
            self.y -= 30
        
        win.blit(self.image, (self.x - x + Width // 2 - 32, y - self.y + Height // 2 - 32))
        if Settings[4]:
            pygame.draw.rect(win, (0, 0, 0), (self.x - x + Width // 2 - 32, y - self.y + Height // 2 - 32, 64, 64), 3)

class Button:
    def __init__(self, x: int, y: int, image1: pygame.surface, image2: pygame.surface, surface):
        self.w = image1.get_width()
        self.h = image2.get_height()
        self.x = x
        self.y = y
        self.image = image1
        self.image1 = image1
        self.image2 = image2
        self.surface = surface
    
    def main(self, action):
        """Shows the button"""

        mouse_x, mouse_y = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x - self.w / 2 < mouse_x < self.x + self.w / 2 and self.y - self.h / 2 < mouse_y < self.y + self.h / 2:
            self.image = self.image2
            if click[0] == 1:
                time.sleep(0.1)
                pygame.mixer.Sound.play(Button_click)
                if action is not None:
                    action()
        else:
            self.image = self.image1
        
        self.surface.blit(self.image, (self.x - self.w / 2, self.y - self.h / 2))
    def get_pressed(self) -> bool:

        mouse_x, mouse_y = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x - self.w / 2 < mouse_x < self.x + self.w / 2 and self.y - self.h / 2 < mouse_y < self.y + self.h / 2:
            self.image = self.image2
            if click[0] == 1:
                time.sleep(0.1)
                pygame.mixer.Sound.play(Button_click)
                return True
        else:
            self.image = self.image1
            return False

class BackroomsPortal:
    def __init__(self, X: int, Y: int):
        self.image = 0
        self.rect = Backrooms_portal_images[0].get_rect()
        self.x = X
        self.y = Y
    def main(self):
        win.blit(Backrooms_portal_images[self.image], (self.x - x + Width // 2 - 128, y - self.y + Height // 2 - 128))
        self.image += 1
        if self.image == 10:
            self.image = 0
        if Settings[4]:
            pygame.draw.rect(win, (0, 0, 0), (self.x - x + Width // 2 - 128, y - self.y + Height // 2 - 128, 256, 256), 3)

class Wire:
    def __init__(self, in_motherboard):
        self.in_motherboard = in_motherboard
        if self.in_motherboard is None:
            self.x = (x + mouse_x - Width // 2) // 64
            self.y = (y - mouse_y + Height // 2) // 64
        else:
            self.x = (mouse_x - Width // 2 - 300) // 18.75
            self.y = (mouse_y + Width // 2 - 300) // 18.75
        self.condition = "Off"
        self.image = Wire_1
        self.neigbords = []
        self.neigbords_on = 0
        self.neigbords_none = 0
        self.num = len(mechanisms)
    
    def main(self):
        self.neigbords = []
        self.neigbords_on = 0
        self.neigbords_none = 0
        if self.in_motherboard is None:
            for mechanism in mechanisms:
                if mechanism.__class__ in [Wire, Lever, Motherboard]:
                    if ((mechanism.x == self.x and mechanism.y in [self.y + 1, self.y - 1]) or (mechanism.x in [self.x - 1, self.x + 1] and mechanism.y == self.y)) and mechanism.num != self.num:
                        self.neigbords.append(mechanism)
                        if mechanism.__class__ == Motherboard:
                            if mechanism.left_condition == "On" and mechanism.x >= self.x:
                                self.neigbords_on += 1
                            if mechanism.left_condition is None and mechanism.x >= self.x:
                                self.neigbords_none += 1
                        else:
                            if mechanism.condition == "On":
                                self.neigbords_on += 1
                            elif mechanism.condition is None:
                                self.neigbords_none += 1

                elif mechanism.__class__ == Random_box:
                    if mechanism.x - self.x in [1, -1] and mechanism.y == self.y and mechanism.num != self.num:
                        self.neigbords.append(mechanism)
                        if mechanism.condition == "On":
                            self.neigbords_on += 1
                        elif mechanism.condition == None:
                            self.condition = None
        else:
            for mechanism in in_motherboard.objects:
                if mechanism.__class__ in [Wire, Lever, Motherboard]:
                    if ((mechanism.x == self.x and mechanism.y in [self.y + 1, self.y - 1]) or (mechanism.x in [self.x - 1, self.x + 1] and mechanism.y == self.y)) and mechanism.num != self.num:
                        self.neigbords.append(mechanism)
                        if mechanism.condition == "On":
                            self.neigbords_on += 1
                        elif mechanism.condition == None:
                            self.neigbords_none += 1

                elif mechanism.__class__ == Random_box:
                    if mechanism.x - self.x in [1, -1] and mechanism.y == self.y and mechanism.num != self.num:
                        self.neigbords.append(mechanism)
                        if mechanism.condition == "On":
                            self.neigbords_on += 1
                        elif mechanism.condition == None:
                            self.condition = None

        if len(self.neigbords) == 1:
            if self.neigbords[0].x == self.x:
                self.image = Wire_2
            else:
                self.image = Wire_1
        elif len(self.neigbords) == 2:
            if self.neigbords[0].x == self.x == self.neigbords[1].x:
                self.image = Wire_2
            elif self.neigbords[0].y == self.y == self.neigbords[1].y:
                self.image = Wire_1
            elif (self.neigbords[0].x == self.x - 1 and self.neigbords[1].y == self.y + 1) or (self.neigbords[1].x == self.x - 1 and self.neigbords[0].y == self.y + 1):
                self.image = Wire_3
            elif (self.neigbords[0].x == self.x + 1 and self.neigbords[1].y == self.y + 1) or (self.neigbords[1].x == self.x + 1 and self.neigbords[0].y == self.y + 1):
                self.image = Wire_4
            elif (self.neigbords[0].x == self.x + 1 and self.neigbords[1].y == self.y - 1) or (self.neigbords[1].x == self.x + 1 and self.neigbords[0].y == self.y - 1):
                self.image = Wire_5
            elif (self.neigbords[0].x == self.x - 1 and self.neigbords[1].y == self.y - 1) or (self.neigbords[1].x == self.x - 1 and self.neigbords[0].y == self.y - 1):
                self.image = Wire_6
        elif len(self.neigbords) == 3:
            if self.neigbords[0].y != self.y + 1 and self.neigbords[1].y != self.y + 1 and self.neigbords[2].y != self.y + 1:
                self.image = Wire_7
            if self.neigbords[0].y != self.y - 1 and self.neigbords[1].y != self.y - 1 and self.neigbords[2].y != self.y - 1:
                self.image = Wire_8
            if self.neigbords[0].x != self.x + 1 and self.neigbords[1].x != self.x + 1 and self.neigbords[2].x != self.x + 1:
                self.image = Wire_9
            if self.neigbords[0].x != self.x - 1 and self.neigbords[1].x != self.x - 1 and self.neigbords[2].x != self.x - 1:
                self.image = Wire_10
        if len(self.neigbords) == 4:
            self.image = Wire_11

        if self.neigbords_on != 0 and self.condition == "Off":
            self.condition = "On"
        if self.condition == None:
            self.condition = "Off"
        elif self.neigbords_none != 0:
            self.condition = None
        
        if self.in_motherboard is None:
            win.blit(textInfo.render(self.condition, True, (0, 0, 0)), (self.x * 64 + Width // 2 - x, y - self.y * 64 + Height // 2 - 16))
            win.blit(self.image, (self.x * 64 + Width // 2 - x, y - self.y * 64 + Height // 2 - 16))
        else:
            ...#win.blit(pygame.transform.scale(self.image, (18.75, 18.75)), (Width // 2 + 300 + self.x * 18.75, 0 - Height // 2 + self.y * 18.75 + 18.75 * 2 + 9.4))

class Lever:
    def __init__(self, in_motherboard):
        self.in_motherboard = in_motherboard
        self.x = (x + mouse_x - Width // 2) // 64
        self.y = (y - mouse_y + Height // 2) // 64
        self.condition = False
        self.image1 = pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Objects/Lever 1.png"), (64, 64))
        self.image2 = pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Objects/Lever 2.png"), (64, 64))
        self.image = self.image1
        self.neigbords = []
        self.num = len(mechanisms)
    def main(self):
        global click, mouse_x, mouse_y
        click = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.neigbords = []

        for mechanism in mechanisms:
            if mechanism.__class__ == Wire:
                if ((mechanism.x == self.x and mechanism.y in [self.y + 1, self.y - 1]) or (mechanism.x in [self.x - 1, self.x + 1] and mechanism.y == self.y)) and mechanism.num != self.num:
                    self.neigbords.append(mechanism)

            elif mechanism.__class__ == Random_box:
                if mechanism.x - self.x in [1, -1] and mechanism.y == self.y and mechanism.num != self.num:
                    self.neigbords.append(mechanism)

        if click[0] and self.x * 64 + Width // 2 - x <= mouse_x <= self.x * 64 + Width // 2 - x + 64 and y - self.y * 64 + Height // 2 - 16 <= mouse_y <= y - self.y * 64 + Height // 2 - 16 + 64:
            if self.image == self.image1:
                self.image = self.image2
                self.condition = "On"
            else:
                self.image = self.image1
                self.condition = None
            time.sleep(0.15)

        win.blit(self.image, (self.x * 64 + Width // 2 - x, y - self.y * 64 + Height // 2 - 16))

class Wall:
    def __init__(self, wall_type: str):
        self.x = (x + mouse_x - Width // 2) - (x + mouse_x - Width // 2) % 256
        self.y = (y - mouse_y + Height // 2) - (y - mouse_y + Height // 2) % 256
        self.wall_type = wall_type
        self.neigbords = []
        self.num = len(objects)
        for object in objects:
            if object.__class__ == Wall:
                if ((object.x == self.x and object.y in [self.y + 256, self.y - 256]) or (object.x in [self.x - 256, self.x + 256] and object.y == self.y)) and object.num != self.num:
                    self.neigbords.append(object)
        self.images = [
            pygame.image.load(path + "Gannitto world/files/Images/Objects/" + wall_type + " 1.png"),
            pygame.image.load(path + "Gannitto world/files/Images/Objects/" + wall_type + " 2.png"),
            pygame.image.load(path + "Gannitto world/files/Images/Objects/" + wall_type + " 3.png"),
            pygame.image.load(path + "Gannitto world/files/Images/Objects/" + wall_type + " 4.png"),
            pygame.image.load(path + "Gannitto world/files/Images/Objects/" + wall_type + " 5.png"),
            pygame.image.load(path + "Gannitto world/files/Images/Objects/" + wall_type + " 6.png"),
            pygame.image.load(path + "Gannitto world/files/Images/Objects/" + wall_type + " 7.png"),
            pygame.image.load(path + "Gannitto world/files/Images/Objects/" + wall_type + " 8.png"),
            pygame.image.load(path + "Gannitto world/files/Images/Objects/" + wall_type + " 9.png"),
            pygame.image.load(path + "Gannitto world/files/Images/Objects/" + wall_type + " 10.png"),
            pygame.image.load(path + "Gannitto world/files/Images/Objects/" + wall_type + " 11.png")
        ]
        self.image = self.images[0]
    
    def main(self):
        self.neigbords = []
        for object in objects:
            if object.__class__ == Wall:
                if ((object.x == self.x and object.y in [self.y + 256, self.y - 256]) or (object.x in [self.x - 256, self.x + 256] and object.y == self.y)) and object.num != self.num:
                    self.neigbords.append(object)
        
        if len(self.neigbords) == 1:
            if self.neigbords[0].x == self.x:
                self.image = self.images[1]
            else:
                self.image = self.images[0]
        elif len(self.neigbords) == 2:
            if self.neigbords[0].x == self.x == self.neigbords[1].x:
                self.image = self.images[1]
            elif self.neigbords[0].y == self.y == self.neigbords[1].y:
                self.image = self.images[0]
            elif (self.neigbords[0].x == self.x - 256 and self.neigbords[1].y == self.y + 256) or (self.neigbords[1].x == self.x - 256 and self.neigbords[0].y == self.y + 256):
                self.image = self.images[2]
            elif (self.neigbords[0].x == self.x + 256 and self.neigbords[1].y == self.y + 256) or (self.neigbords[1].x == self.x + 256 and self.neigbords[0].y == self.y + 256):
                self.image = self.images[3]
            elif (self.neigbords[0].x == self.x + 256 and self.neigbords[1].y == self.y - 256) or (self.neigbords[1].x == self.x + 256 and self.neigbords[0].y == self.y - 256):
                self.image = self.images[4]
            elif (self.neigbords[0].x == self.x - 256 and self.neigbords[1].y == self.y - 256) or (self.neigbords[1].x == self.x - 256 and self.neigbords[0].y == self.y - 256):
                self.image = self.images[5]
        elif len(self.neigbords) == 3:
            if self.neigbords[0].y != self.y + 256 and self.neigbords[1].y != self.y + 256 and self.neigbords[2].y != self.y + 256:
                self.image = self.images[6]
            if self.neigbords[0].y != self.y - 256 and self.neigbords[1].y != self.y - 256 and self.neigbords[2].y != self.y - 256:
                self.image = self.images[7]
            if self.neigbords[0].x != self.x + 256 and self.neigbords[1].x != self.x + 256 and self.neigbords[2].x != self.x + 256:
                self.image = self.images[8]
            if self.neigbords[0].x != self.x - 256 and self.neigbords[1].x != self.x - 256 and self.neigbords[2].x != self.x - 256:
                self.image = self.images[9]
        elif len(self.neigbords) == 4:
            self.image = self.images[10]
        
        win.blit(self.image, (self.x + Width // 2 - x, y - self.y + Height // 2 - 128))

class Random_box:
    def __init__(self, in_motherboard):
        self.in_motherboard = in_motherboard
        self.x = (x + mouse_x - Width // 2) // 64
        self.y = (y - mouse_y + Height // 2) // 64
        self.on = False
        self.image = Random_box_1
        self.neigbords = []
        self.neigbords_on = 0
        self.num = len(mechanisms)
    
    def main(self):
        self.neigbords = []
        self.neigbords_on = 0
        for mechanism in mechanisms:
            if mechanism.y == self.y and mechanism.x - self.x in [1, -1] and mechanism.num != self.num:
                self.neigbords.append(mechanism)
                if mechanism.on:
                    self.neigbords_on += 1
        
        if len(self.neigbords) == 1:
            if self.neigbords[0].x == self.x - 1:
                self.image = Random_box_2
            else:
                self.image = Random_box_3
        elif len(self.neigbords) == 2:
            self.image = Random_box_4
        else:
            self.image = Random_box_1
        
        
        win.blit(self.image, (self.x * 64 + Width // 2 - x, y - self.y * 64 + Height // 2 - 16))

class LogicGate:
    def __init__(self, in_motherboard):
        self.in_motherboard = in_motherboard
        self.x = (x + mouse_x - Width // 2) // 64
        self.y = (y - mouse_y + Height // 2) // 64
        self.image = Wire_11
        self.neigbords = []
        self.neigbords_on = 0
        self.num = len(mechanisms)
    
    def main(self):
        self.neigbords = []
        self.neigbords_on = 0
        for mechanism in mechanisms:
            if mechanism.__class__ in [Wire, Lever]:
                if ((mechanism.x == self.x and mechanism.y in [self.y + 1, self.y - 1]) or (mechanism.x in [self.x - 1, self.x + 1] and mechanism.y == self.y)) and mechanism.num != self.num:
                    self.neigbords.append(mechanism)
                    if mechanism.condition == "On":
                        self.neigbords_on += 1

            elif mechanism.__class__ == Random_box:
                if mechanism.x - self.x in [1, -1] and mechanism.y == self.y and mechanism.num != self.num:
                    self.neigbords.append(mechanism)
                    if mechanism.condition == "On":
                        self.neigbords_on += 1

        if len(self.neigbords) == 1:
            if self.neigbords[0].x == self.x:
                self.image = Wire_2
            else:
                self.image = Wire_1
        elif len(self.neigbords) == 2:
            if self.neigbords[0].x == self.x == self.neigbords[1].x:
                self.image = Wire_2
            elif self.neigbords[0].y == self.y == self.neigbords[1].y:
                self.image = Wire_1
            elif (self.neigbords[0].x == self.x - 1 and self.neigbords[1].y == self.y + 1) or (self.neigbords[1].x == self.x - 1 and self.neigbords[0].y == self.y + 1):
                self.image = Wire_3
            elif (self.neigbords[0].x == self.x + 1 and self.neigbords[1].y == self.y + 1) or (self.neigbords[1].x == self.x + 1 and self.neigbords[0].y == self.y + 1):
                self.image = Wire_4
            elif (self.neigbords[0].x == self.x + 1 and self.neigbords[1].y == self.y - 1) or (self.neigbords[1].x == self.x + 1 and self.neigbords[0].y == self.y - 1):
                self.image = Wire_5
            elif (self.neigbords[0].x == self.x - 1 and self.neigbords[1].y == self.y - 1) or (self.neigbords[1].x == self.x - 1 and self.neigbords[0].y == self.y - 1):
                self.image = Wire_6
        elif len(self.neigbords) == 3:
            if self.neigbords[0].y != self.y + 1 and self.neigbords[1].y != self.y + 1 and self.neigbords[2].y != self.y + 1:
                self.image = Wire_7
            if self.neigbords[0].y != self.y - 1 and self.neigbords[1].y != self.y - 1 and self.neigbords[2].y != self.y - 1:
                self.image = Wire_8
            if self.neigbords[0].x != self.x + 1 and self.neigbords[1].x != self.x + 1 and self.neigbords[2].x != self.x + 1:
                self.image = Wire_9
            if self.neigbords[0].x != self.x - 1 and self.neigbords[1].x != self.x - 1 and self.neigbords[2].x != self.x - 1:
                self.image = Wire_10
        if len(self.neigbords) == 4:
            self.image = Wire_11

        if self.neigbords_on != 0 and self.condition == "Off":
            self.condition = "On"
        if self.condition == None:
            self.condition = "Off"
        elif self.neigbords_none != 0:
            self.condition = None
        
        if self.in_motherboard:
            ...#win.blit(self.image, (self.x * 64 + Width // 2 - x, y - self.y * 64 + Height // 2 - 16))
        else:
            win.blit(self.image, (self.x * 64 + Width // 2 - x, y - self.y * 64 + Height // 2 - 16))

class Motherboard:
    def __init__(self, in_motherboard):
        self.in_motherboard = in_motherboard
        self.x = (x + mouse_x - Width // 2) // 64
        self.y = (y - mouse_y + Height // 2) // 64
        self.condition = "Off"
        self.image = pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Objects/Motherboard.png"), (64, 64))
        self.neigbords = []
        self.neigbords_on = 0
        self.neigbords_none = 0
        self.num = len(mechanisms)
        self.objects = [None] * 1024
        self.objects_left = []
        self.objects_left_xy = []
        self.left_condition = "Off"
        self.objects_right = []
        self.objects_right_xy = []
        self.right_condition = "Off"
        self.objects_up = []
        self.objects_up_xy = []
        self.up_condition = "Off"
        self.objects_down = []
        self.objects_down_xy = []
        self.down_condition = "Off"
    
    def main(self):
        self.neigbords = []
        self.neigbords_on = 0
        self.neigbords_none = 0
        self.objects_left = []
        self.objects_left_xy = []
        self.objects_right = []
        self.objects_right_xy = []
        self.objects_up = []
        self.objects_up_xy = []
        self.objects_down = []
        self.objects_down_xy = []
        for mechanism in mechanisms:
            if mechanism.__class__ in [Wire, Lever, Motherboard]:
                if ((mechanism.x == self.x and mechanism.y in [self.y + 1, self.y - 1]) or (mechanism.x in [self.x - 1, self.x + 1] and mechanism.y == self.y)) and mechanism.num != self.num:
                    self.neigbords.append(mechanism)
                    if mechanism.condition == "On" and mechanism.x <= self.x and self.left_condition == "Off":
                        self.left_condition = "On"
                    elif mechanism.condition is None and mechanism.x <= self.x:
                        self.left_condition = None

            elif mechanism.__class__ == Random_box:
                if mechanism.x - self.x in [1, -1] and mechanism.y == self.y and mechanism.num != self.num:
                    self.neigbords.append(mechanism)
                    if mechanism.condition == "On":
                        self.neigbords_on += 1
                    elif mechanism.condition == None:
                        self.condition = None

        for i in self.objects:
            if i is not None:
                if i.x + 32 == 0:
                    self.objects_left.append(i.condition)
                    self.objects_left_xy.append(i)
                elif i.x == -1:
                    self.objects_right.append(i.condition)
                    self.objects_right_xy.append(i)

                if i.y == 21:
                    self.objects_up.append(i.condition)
                    self.objects_up_xy.append(i)
                elif i.y == 52:
                    self.objects_down.append(i.condition)
                    self.objects_down_xy.append(i)
                    
        if (any(self.objects_left) and self.left_condition == "Off") or self.left_condition == "On":
            self.left_condition = "On"
            for i in self.objects_left_xy:
                if self.objects[self.objects.index(i)].condition == "Off":
                    self.objects[self.objects.index(i)].condition = "On"
        if self.left_condition is None:
            self.left_condition = "Off"
        elif None in self.objects_left:
            self.left_condition = None
            for i in self.objects_left_xy:
                self.objects[self.objects.index(i)].condition = None

        
        self.get_pressed()
        if self.in_motherboard:
            ...#win.blit(self.image, (self.x * 64 + Width // 2 - x, y - self.y * 64 + Height // 2 - 16))
        else:
            win.blit(self.image, (self.x * 64 + Width // 2 - x, y - self.y * 64 + Height // 2 - 16))

    def get_pressed(self):
        global in_motherboard, mouse_x, mouse_y, click
        mouse_x, mouse_y = pygame.mouse.get_pos()
        #click = pygame.mouse.get_pos()
        if self.in_motherboard is None:
            if self.x * 64 + Width // 2 - x <= mouse_x <= self.x * 64 + Width // 2 - x + 64 and y - self.y * 64 + Height // 2 - 16 <= mouse_y <= y - self.y * 64 + Height // 2 - 16 + 64 and in_motherboard is None and click[0]:
                in_motherboard = self
        else:
            ...


class Cave:
    def __init__(self, cave_x, cave_y, w, h):
        self.x = cave_x
        self.y = cave_y
        self.w = 128
        self.h = 128
        self.own_width = w
        self.own_height = h
        self.image = cave
        self.objects = []
        self.num = len(objects) - 1
        self.name = "Cave"
        self.generate()

    def generate(self):
        for _ in range(self.own_width // 100 + random.randint(-10, 10)):
            self.objects.append(Object("Stone", random.randint(self.own_width // 2 * -1, self.own_width // 2), random.randint(self.own_height // 2 * -1, self.own_height // 2), "Gannitto world/files/Images/Items/Stone.png", special_flags="Item"))

        for _ in range(self.own_width // 300 + random.randint(-10, 10)):
            self.objects.append(Object("Iron ore", random.randint(self.own_width // 2 * -1, self.own_width // 2), random.randint(self.own_height // 2 * -1, self.own_height // 2), "Gannitto world/files/Images/Objects/Iron ore.png", [256, 256], special_flags=100))

    def main(self):
        if x - Width // 2 <= self.x <= x + Width // 2 and y - Height // 2 <= self.y + Height // 2:
            win.blit(self.image, (self.x - x + Width // 2 - self.w // 2, y - self.y + Height // 2 - self.h // 2))
        
    def get_in(self):
        global mouse_x, mouse_y
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.x <= x <= self.x + 128 and self.y <= y <= self.y <= 128 and self.x - x + Width // 2 - self.w // 2 <= mouse_x <= self.x - x + Width // 2 - self.w // 2 + 128 and y - self.y + Height // 2 - self.h // 2 <= mouse_y <= y - self.y + Height // 2 - self.h // 2 + 128 and pygame.mouse.get_pressed()[0]:
            return self.num
        else:
            return None
            

#objects.append(Cave(0, -256, 10000, 10000))

class Portal:
    def __init__(self):
        self.x = (x + mouse_x - Width // 2) // 128
        self.y = (y + mouse_y - Height // 2) // 256
        self.num = len(objects)
        a = False
        for object in objects:
            if object.__class__ == Portal and object.num != self.num - 1:
                a = True
        if a:
            self.image = Portal_2
        else:
            self.image = Portal_1

    def main(self):
        global x, y
        for object in objects:
            if object.__class__ == Portal and object.num != self.num - 1:
                if self.x * 128 <= x <= self.x * 128 + 128 and self.y * 256 - 256 <= y <= self.y * 256:
                    x = object.x * 128
                    y = object.y * 256 - 257
        
        win.blit(self.image, (self.x * 128 + Width // 2 - x, y - self.y * 256 + Height // 2))

class Vending_machine:
    def __init__(self) -> None:
        self.x = (x + mouse_x - Width // 2) // 304
        self.y = (y + mouse_y - Height // 2) // 560
        self.owner = Settings[2]
        self.image = Vending_machine_image

def settings():

    back_button = Button(44, 44, BackButton, BackButton2, win)
    help_button = Button(76, 149, HelpButton, HelpButton2, win)
    display_button = Button(121, 224, DisplayButton, DisplayButton2, win)
    laungveges_button = Button(178, 299, LaungvegesButton, LaungvegesButton2, win)
    english_button = Button(499, 230, EnglishButton, EnglishButton2, win)
    russian_button = Button(499, 299, RussianButton, RussianButton2, win)
    user_button = Button(76, 374, UserButton, UserButton2, win)
    page_back_button = Button(425, Height - 74, BackButton, BackButton2, win)
    page_next_button = Button(Width - 74, Height - 74, pygame.transform.flip(BackButton, True, False), pygame.transform.flip(BackButton2, True, False), win)
    bigTextInfo = pygame.font.Font("Font.ttf", 36)
    
    def help():
        global win, screenmode, changed_laungvege, mouse_x, mouse_y, mouse_click_image
        def page_1():
            global page
            if page != 1:
                page -= 1
        def page_2():
            global page
            if page != 3:
                page += 1
        while 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_F11]:
                if screenmode == "FULLSCREEN":
                    win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
                    screenmode = "RESIZABLE"
                else:
                    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    screenmode = "FULLSCREEN"
                time.sleep(0.1)
            
            win.fill((192, 203, 220))
            pygame.draw.rect(win, (139, 155, 180), (-8, 100, 373, Height), 8)
            pygame.draw.line(win, (139, 155, 180), (307, 103), (Width, 103), 8)
            back_button.main(None)
            if back_button.get_pressed():
                SaveLoadSystem(".save", path + "Gannitto world/files/").save_data(Settings, "Settings")
                menu()
            page_back_button.main(page_1)
            page_next_button.main(page_2)
            win.blit(bigTextInfo.render(str(page), True, (139, 155, 180)), ((Width - 415) // 2 + 391, Height - 96))
            win.blit(HelpButton2, (10, 117))
            display_button.main(display)
            laungveges_button.main(Laungveges)
            user_button.main(User)

            if page == 1:
                win.blit(bigTextInfo.render(laungveges("Начао игры", "Start game"), True, (139, 155, 180)), (385, 123))
                win.blit(textInfo.render(laungveges(" • Чтобы ходить вы можете использовать как и стрелки, так и A, S, W, и D.", "   To move, you can use the arrows or A, S, W and D"), True, (139, 155, 180)), (385, 209)) # между строками 86 пикселей
                win.blit(arrow_up, (459, 239))
                win.blit(arrow_left, (385, 313))
                win.blit(arrow_down, (459, 313))
                win.blit(arrow_right, (533, 313))
                pygame.draw.rect(win, (139, 155, 180), (701, 239, 64, 64), 6)
                pygame.draw.rect(win, (139, 155, 180), (627, 313, 64, 64), 6)
                pygame.draw.rect(win, (139, 155, 180), (701, 313, 64, 64), 6)
                pygame.draw.rect(win, (139, 155, 180), (775, 313, 64, 64), 6)
                win.blit(bigTextInfo.render("W", True, (139, 155, 180)), (710, 247))
                win.blit(bigTextInfo.render("A", True, (139, 155, 180)), (640, 321))
                win.blit(bigTextInfo.render("S", True, (139, 155, 180)), (716, 321))
                win.blit(bigTextInfo.render("D", True, (139, 155, 180)), (790, 321))
                win.blit(textInfo.render(laungveges(" • Так же, вы можете положить предмет на землю, нажав E, а чтобы его потом", "  Also, you can put an item on the ground by pressing E, and to get it, just click"), True, (139, 155, 180)), (385, 381)) # между строками 30 пикселей
                win.blit(textInfo.render(laungveges("подобрать, просто нажмите на него!", "on it!"), True, (139, 155, 180)), (385, 411))
                win.blit(textInfo.render(laungveges(" • Если вы хотите узнать свой координаты, или что-нибудь ещё, нажмите F2.", " • If you want to know you coordinate, or anything more, press F2."), True, (139, 155, 180)), (385, 441))
                win.blit(textInfo.render(laungveges("для открытия меню.", "to open the menu"), True, (139, 155, 180)), (385, 471))
                win.blit(textInfo.render(laungveges(" • При нажатии на I откроется весь инвентарь, чтобы его закрыть, нажмите", " • Clicking on I will open the entire inventory, to close it, click again."), True, (139, 155, 180)), (385, 501))
                win.blit(textInfo.render(laungveges("ещё раз", None), True, (139, 155, 180)), (385, 531))
                win.blit(textInfo.render(laungveges(" • В верхнем правом углу есть пункт, в котором можно узнать информацию", " • In the upper right corner there is an item where you can find out"), True, (139, 155, 180)), (385, 561))
                win.blit(textInfo.render(laungveges("об объекте, на который вы навели.", "information about the object you hovered over"), True, (139, 155, 180)), (385, 591))
            elif page == 2:
                win.blit(bigTextInfo.render(laungveges("Крафт", "Craft"), True, (139, 155, 180)), (385, 123))
                win.blit(textInfo.render(laungveges("   Наверняка, тебе было интересно, что это за слоты под инвентарём. Это", "    Forsnre, you were interesting about the cells under the inventory. This is"), True, (139, 155, 180)), (385, 209))
                win.blit(textInfo.render(laungveges("система крафта", "crafting system"), True, (139, 155, 180)), (385, 239))
                win.blit(Changed_inventory_slot, (385, 269))
                win.blit(Changed_inventory_slot, (465, 269))
                win.blit(Inventory_slot, (545, 269))
                win.blit(textInfo.render(laungveges("   На первый взгляд, всё как-то уныло, но на самом деле, крафтить весело!", "  At first glance, everything is somehow dull, but in fact, crafting is fun!"), True, (139, 155, 180)), (385, 359))
                win.blit(textInfo.render(laungveges("Первый слот обозначает объект, который нужен для крафта, например стол.", "The first slot denotes an object that is needed for crafting, such as a table."), True, (139, 155, 180)), (385, 389))
                win.blit(textInfo.render(laungveges("Второй слот - инструмент, который тебе нужен, например молоток. Дальше", "The second slot is the tool you need, like a hammer. Еhen there are 7 slots"), True, (139, 155, 180)), (385, 419))
                win.blit(textInfo.render(laungveges("идут 7 слотов для предметов. Если положить предмет в первый, то", "for items. If you put an item in the first one, then the second one is"), True, (139, 155, 180)), (385, 449))
                win.blit(textInfo.render(laungveges("разблокируется второй, потом третий, и так далее.", "unlocked, then the third, and so on."), True, (139, 155, 180)), (385, 479))
                win.blit(Changed_inventory_slot, (385, 509))
                win.blit(pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Items/Furnace.png"), (64, 64)), (385, 509))
                win.blit(Changed_inventory_slot, (465, 509))
                win.blit(Inventory_slot, (545, 509))
                win.blit(pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Items/Clay.png"), (64, 64)), (545, 509))
                win.blit(Inventory_slot, (625, 509))
                win.blit(Changed_inventory_slot, (1185, 509))
                win.blit(pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Items/Brick.png"), (64, 64)), (1185, 509))
                win.blit(textInfo.render(laungveges("   Если положить определённую комбинацию предметов, то можно будет", ""), True, (139, 155, 180)), (385, 599))
                win.blit(textInfo.render(laungveges("получить что-либо. Например, если поставить печь и положить глину в ячейки", ""), True, (139, 155, 180)), (385, 629))
                win.blit(textInfo.render(laungveges("крафта, то можно будет получить кирпич, а чтобы его получить, нажми.", ""), True, (139, 155, 180)), (385, 659))
            
            if pygame.mouse.get_pressed()[0] == 1:
                mouse_click_image = 1
            try:
                win.blit(mouse_click_images[mouse_click_image - 1], (mouse_x - 64, mouse_y - 64))
                if mouse_click_image == 5:
                    mouse_click_image = None
                else:
                    mouse_click_image += 1
            except TypeError:
                pass

            pygame.display.update()
            clock.tick(FPS)

    def display():
        global win, screenmode, Settings, click, mouse_x, mouse_y, mouse_click_image
        mouse_x, mouse_y = pygame.mouse.get_pos()
        def page_1():
            global page
            if page != 1:
                page -= 1
        def page_2():
            global page
            if page != 3:
                page += 1
        Brightness = False
        Inventory_alpha = False
        Distance = False
        input_text = ""
        while 1:
            click = pygame.mouse.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                elif event.type == pygame.KEYDOWN and (Brightness or Inventory_alpha or Distance):
                    if event.key == pygame.K_RETURN or len(input_text) == 3:
                        if Brightness:
                            Brightness = False
                            Settings[0] = int(input_text)
                        elif Inventory_alpha:
                            Inventory_alpha = False
                            Settings[1] = int(input_text)
                        elif Distance:
                            Distance = False
                            Settings[3] = int(input_text)
                        input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                        input_text += event.unicode



            keys = pygame.key.get_pressed()
            if keys[pygame.K_F11]:
                if screenmode == "FULLSCREEN":
                    win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
                    screenmode = "RESIZABLE"
                else:
                    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    screenmode = "FULLSCREEN"
                time.sleep(0.1)

            if bigTextInfo.size(laungveges("Яркось", "Brightness"))[0] + 337 <= mouse_x <= bigTextInfo.size(laungveges("Яркось", "Brightness"))[0] + 467 + 120 and 113 <= mouse_y <= 184 and click[0] == 1:
                Brightness = True
            if bigTextInfo.size(laungveges("Прозрачность инвентаря", "Inventory transparency"))[0] + 337 <= mouse_x <= bigTextInfo.size(laungveges("Прозрачность инвентаря", "Inventory 123"))[0] + 467 + 120 and 199 <= mouse_y <= 270 and click[0] == 1:
                Inventory_alpha = True
            if bigTextInfo.size(laungveges("Отдаление", "Distance"))[0] + 337 <= mouse_x <= bigTextInfo.size(laungveges("Отдаление", "Distance"))[0] + 467 + 120 and 285 <= mouse_y <= 356 and click[0] == 1:
                Distance = True
            
            win.fill((192, 203, 220))
            pygame.draw.rect(win, (139, 155, 180), (-8, 100, 373, Height), 8)
            pygame.draw.line(win, (139, 155, 180), (307, 103), (Width, 103), 8)
            back_button.main(None)
            if back_button.get_pressed():
                SaveLoadSystem(".save", path + "Gannitto world/files/").save_data(Settings, "Settings")
                menu()
            page_back_button.main(page_1)
            page_next_button.main(page_2)
            win.blit(bigTextInfo.render(str(page), True, (139, 155, 180)), ((Width - 415) // 2 + 391, Height - 96))
            help_button.main(help)
            win.blit(DisplayButton2, (10, 192))
            laungveges_button.main(Laungveges)
            user_button.main(User)

            if page == 1:
                win.blit(bigTextInfo.render(laungveges("Яркось", "Brightness"), True, (139, 155, 180)), (385, 123))
                pygame.draw.rect(win, (139, 155, 180), (bigTextInfo.render(laungveges("Яркось", "Brightness"), True, (139, 155, 180)).get_width() + 395, 113, 120, 71), 5)
                win.blit(bigTextInfo.render("%", True, (139, 155, 180)), (bigTextInfo.render(laungveges("Яркось", "Brightness"), True, (139, 155, 180)).get_width() + 525, 123))
                if Brightness:
                    win.blit(bigTextInfo.render(input_text, True, (139, 155, 180)), (bigTextInfo.render(laungveges("Яркось", "Brightness"), True, (139, 155, 180)).get_width() + 405, 123))
                else:
                    win.blit(bigTextInfo.render(str(Settings[0]), True, (139, 155, 180)), (bigTextInfo.render(laungveges("Яркось", "Brightness"), True, (139, 155, 180)).get_width() + 405, 123))
                    if get_brightness() != Settings[0]:
                        set_brightness(Settings[0])
                
                win.blit(bigTextInfo.render(laungveges("Прозрачность инвентаря", "Inventory 123"), True, (139, 155, 180)), (385, 209))
                pygame.draw.rect(win, (139, 155, 180), (bigTextInfo.render(laungveges("Прозрачность инвентаря", "Inventory 123"), True, (139, 155, 180)).get_width() + 395, 199, 120, 71), 5)
                win.blit(bigTextInfo.render("%", True, (139, 155, 180)), (bigTextInfo.render(laungveges("Прозрачность инвентаря", "Inventory 123"), True, (139, 155, 180)).get_width() + 525, 209))
                if Inventory_alpha:
                    win.blit(bigTextInfo.render(input_text, True, (139, 155, 180)), (bigTextInfo.render(laungveges("Прозрачность инвентаря", "Inventory 123"), True, (139, 155, 180)).get_width() + 405, 209))
                else:
                    win.blit(bigTextInfo.render(str(Settings[1]), True, (139, 155, 180)), (bigTextInfo.render(laungveges("Прозрачность инвентаря", "Inventory 123"), True, (139, 155, 180)).get_width() + 405, 209))

                win.blit(bigTextInfo.render(laungveges("Отдаление", "Distance"), True, (139, 155, 180)), (385, 295))
                pygame.draw.rect(win, (139, 155, 180), (bigTextInfo.render(laungveges("Отдаление", "Distance"), True, (139, 155, 180)).get_width() + 395, 285, 120, 71), 5)
                if Distance:
                    win.blit(bigTextInfo.render(input_text, True, (139, 155, 180)), (bigTextInfo.render(laungveges("Отдаление", "Distance"), True, (139, 155, 180)).get_width() + 405, 295))
                else:
                    win.blit(bigTextInfo.render(str(Settings[3]), True, (139, 155, 180)), (bigTextInfo.render(laungveges("Отдаление", "Distance"), True, (139, 155, 180)).get_width() + 405, 295))

                win.blit(bigTextInfo.render(laungveges("Отображать хитбоксы", "Display hitboxes"), True, (139, 155, 180)), (385, 381))
                pygame.draw.rect(win, (139, 155, 180), (bigTextInfo.render(laungveges("Отображать хитбоксы", "Display hitboxes"), True, (139, 155, 180)).get_width() + 395, 371, 71, 71), 5)
                if Settings[4]:
                    win.blit(bigTextInfo.render(" ✓", True, (139, 155, 180)), (bigTextInfo.render(laungveges("Отображать хитбоксы", "Display hitboxes"), True, (139, 155, 180)).get_width() + 405, 381))
                    if bigTextInfo.render(laungveges("Отображать хитбоксы", "Display hitboxes"), True, (139, 155, 180)).get_width() + 395 <= mouse_x <= bigTextInfo.render(laungveges("Отображать хитбоксы", "Display hitboxes"), True, (139, 155, 180)).get_width() + 466 and 371 <= mouse_y <= 442 and click[0] == 1:
                        Settings[4] = False
                        time.sleep(0.15)
                else:
                    win.blit(bigTextInfo.render(" x", True, (139, 155, 180)), (bigTextInfo.render(laungveges("Отображать хитбоксы", "Display hitboxes"), True, (139, 155, 180)).get_width() + 405, 381))
                    if bigTextInfo.render(laungveges("Отображать хитбоксы", "Display hitboxes"), True, (139, 155, 180)).get_width() + 395 <= mouse_x <= bigTextInfo.render(laungveges("Отображать хитбоксы", "Display hitboxes"), True, (139, 155, 180)).get_width() + 466 and 371 <= mouse_y <= 442 and click[0] == 1:
                        Settings[4] = True
                        time.sleep(0.15)

            if pygame.mouse.get_pressed()[0] == 1:
                mouse_click_image = 1
            try:
                win.blit(mouse_click_images[mouse_click_image - 1], (mouse_x - 64, mouse_y - 64))
                if mouse_click_image == 5:
                    mouse_click_image = None
                else:
                    mouse_click_image += 1
            except TypeError:
                pass

            pygame.display.update()
            clock.tick(FPS)

    def Laungveges():
        global win, screenmode, changed_laungvege, mouse_click_image
        def page_1():
            global page
            if page != 1:
                page -= 1
        def page_2():
            global page
            if page != 3:
                page += 1
        while 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_F11]:
                if screenmode == "FULLSCREEN":
                    win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
                    screenmode = "RESIZABLE"
                else:
                    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    screenmode = "FULLSCREEN"
                time.sleep(0.1)
            
            win.fill((192, 203, 220))
            pygame.draw.rect(win, (139, 155, 180), (-8, 100, 373, Height), 8)
            pygame.draw.line(win, (139, 155, 180), (307, 103), (Width, 103), 8)
            back_button.main(None)
            if back_button.get_pressed():
                SaveLoadSystem(".save", path + "Gannitto world/files/").save_data(Settings, "Settings")
                menu()
            page_back_button.main(page_1)
            page_next_button.main(page_2)
            win.blit(bigTextInfo.render(laungveges("Ты можешь выбрать один из этих", "You can choose one of these"), True, (139, 155, 180)), (385, 123))
            win.blit(bigTextInfo.render(laungveges("языков:", "laungveges:"), True, (139, 155, 180)), (385, 153))
            english_button.main(None)
            if english_button.get_pressed():
                changed_laungvege = "English"
            russian_button.main(None)
            if russian_button.get_pressed():
                changed_laungvege = "Russian"
            win.blit(bigTextInfo.render(str(page), True, (139, 155, 180)), ((Width - 415) // 2 + 391, Height - 96))
            help_button.main(help)
            display_button.main(display)
            user_button.main(User)
            win.blit(LaungvegesButton2, (10, 267))
            
            if keys[pygame.K_1]:
                changed_laungvege = "Russian"
            if keys[pygame.K_2]:
                changed_laungvege = "English"

            if pygame.mouse.get_pressed()[0] == 1:
                mouse_click_image = 1
            try:
                win.blit(mouse_click_images[mouse_click_image - 1], (mouse_x - 64, mouse_y - 64))
                if mouse_click_image == 5:
                    mouse_click_image = None
                else:
                    mouse_click_image += 1
            except TypeError:
                pass

            pygame.display.update()
            clock.tick(FPS)
    def User():
        global win, screenmode, Settings, click, mouse_x, mouse_y, mouse_click_image
        mouse_x, mouse_y = pygame.mouse.get_pos()
        def page_1():
            global page
            if page != 1:
                page -= 1
        def page_2():
            global page
            if page != 3:
                page += 1
        Nick = False
        Inventory_alpha = False
        input_text = ""
        while 1:
            click = pygame.mouse.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                elif event.type == pygame.KEYDOWN and (Nick or Inventory_alpha):
                    if event.key == pygame.K_RETURN or len(input_text) == 3:
                        if Nick:
                            Nick = False
                            Settings[3] = input_text
                        elif Inventory_alpha:
                            Inventory_alpha = False
                            Settings[1] = int(input_text)
                        input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                        input_text += event.unicode



            keys = pygame.key.get_pressed()
            if keys[pygame.K_F11]:
                if screenmode == "FULLSCREEN":
                    win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
                    screenmode = "RESIZABLE"
                else:
                    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    screenmode = "FULLSCREEN"
                time.sleep(0.1)

            if bigTextInfo.render(laungveges("Ник", "Nickname"), True, (139, 155, 180)).get_width() + 337 <= mouse_x <= bigTextInfo.render(laungveges("Ник", "Nickname"), True, (139, 155, 180)).get_width() + 467 + 120 and 113 <= mouse_y <= 184 and click[0] == 1:
                Nick = True
            if bigTextInfo.render(laungveges("скоро появится", "comming soon"), True, (139, 155, 180)).get_width() + 337 <= mouse_x <= bigTextInfo.render(laungveges("скоро появится", "comming soon"), True, (139, 155, 180)).get_width() + 467 + 120 and 199 <= mouse_y <= 270 and click[0] == 1:
                Inventory_alpha = True
            
            win.fill((192, 203, 220))
            pygame.draw.rect(win, (139, 155, 180), (-8, 100, 373, Height), 8)
            pygame.draw.line(win, (139, 155, 180), (307, 103), (Width, 103), 8)
            back_button.main(None)
            if back_button.get_pressed():
                SaveLoadSystem(".save", path + "Gannitto world/files/").save_data(Settings, "Settings")
                menu()
            page_back_button.main(page_1)
            page_next_button.main(page_2)
            win.blit(bigTextInfo.render(str(page), True, (139, 155, 180)), ((Width - 415) // 2 + 391, Height - 96))
            help_button.main(help)
            display_button.main(display)
            laungveges_button.main(Laungveges)
            win.blit(UserButton2, (10, 342))

            if page == 1:
                win.blit(bigTextInfo.render(laungveges("Ник", "Nickname"), True, (139, 155, 180)), (385, 123))
                pygame.draw.rect(win, (139, 155, 180), (bigTextInfo.render(laungveges("Ник", "Nickname"), True, (139, 155, 180)).get_width() + 395, 113, 200, 71), 5)
                if Nick:
                    win.blit(bigTextInfo.render(input_text, True, (139, 155, 180)), (bigTextInfo.render(laungveges("Ник", "Nickname"), True, (139, 155, 180)).get_width() + 405, 123))
                else:
                    win.blit(bigTextInfo.render(Settings[2], True, (139, 155, 180)), (bigTextInfo.render(laungveges("Ник", "Nickname"), True, (139, 155, 180)).get_width() + 405, 123))
                
                win.blit(bigTextInfo.render(laungveges("скоро появится", "comming soon"), True, (139, 155, 180)), (385, 209))
                pygame.draw.rect(win, (139, 155, 180), (bigTextInfo.render(laungveges("скоро появится", "comming soon"), True, (139, 155, 180)).get_width() + 395, 199, 120, 71), 5)
                if Inventory_alpha:
                    win.blit(bigTextInfo.render(input_text, True, (139, 155, 180)), (bigTextInfo.render(laungveges("скоро появится", "comming soon"), True, (139, 155, 180)).get_width() + 405, 209))
                else:
                    win.blit(bigTextInfo.render(str(Settings[1]), True, (139, 155, 180)), (bigTextInfo.render(laungveges("скоро появится", "comming soon"), True, (139, 155, 180)).get_width() + 405, 209))
                    Inventory_slot.set_alpha(Settings[1])
                    Changed_inventory_slot.set_alpha(Settings[1])
                    Object_inventory_slot.set_alpha(Settings[1])
                    Tool_inventory_slot.set_alpha(Settings[1])
                    Split_items1.set_alpha(Settings[1])
                    Split_items2.set_alpha(Settings[1])

            if pygame.mouse.get_pressed()[0] == 1:
                mouse_click_image = 1
            try:
                win.blit(mouse_click_images[mouse_click_image - 1], (mouse_x - 64, mouse_y - 64))
                if mouse_click_image == 5:
                    mouse_click_image = None
                else:
                    mouse_click_image += 1
            except TypeError:
                pass

            pygame.display.update()
            clock.tick(FPS)
        
    help()

def change_a_character():

    back_button = Button(44, 44, BackButton, BackButton2, win)
    character_button = Button(149, 152, CharacterButton, CharacterButton2, win)
    pets_button = Button(76, 224, PetsButton, PetsButton2, win)
    page_back_button = Button(367, Height - 74, BackButton, BackButton2, win)
    page_next_button = Button(Width - 74, Height - 74, pygame.transform.flip(BackButton, True, False), pygame.transform.flip(BackButton2, True, False), win)
    bigTextInfo = pygame.font.Font(None, 36)

    def characters():
        global win, screenmode, mouse_click_image
        
        def page_1():
            global page
            if page != 1:
                page -= 1
        def page_2():
            global page
            if page != 3:
                page += 1
        
        class Character():
            def __init__(self, name: str, info: str, images_list: list):
                self.name = name
                self.info = info
                self.images_list = images_list
                self.image_num = 0
        
        characters_list = [
            Character("Hiro", "123", [
                Hiro_down_run_1,
                Hiro_down_left,
                Hiro_left_run_1,
                Hiro_up_left,
                Hiro_up_run_1,
                Hiro_up_right_run_1,
                Hiro_right_run_1,
                Hiro_down_right
            ])
        ]

        changed_character = characters_list[0]
        changed_character_num = 0

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_F11]:
                if screenmode == "FULLSCREEN":
                    win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
                    screenmode = "RESIZABLE"
                else:
                    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    screenmode = "FULLSCREEN"
                time.sleep(0.1)
            
            win.fill((192, 203, 220))
            pygame.draw.rect(win, (139, 155, 180), (-8, 100, 315, Height), 8)
            pygame.draw.rect(win, (139, 155, 180), (315, 100, Width - 325, 100), 8)
            pygame.draw.rect(win, (139, 155, 180), (316 + changed_character_num * 300, 210, 256, 256), 8)
            pygame.draw.rect(win, (139, 155, 180), (316, 476, 256, Height - 604), 8)
            pygame.draw.rect(win, (139, 155, 180), ((Width - 415) // 2 + 230, 476, 256, Height - 604), 8)
            pygame.draw.rect(win, (139, 155, 180), (Width - 266, 476, 256, Height - 604), 8)
            win.blit(textInfo.render(laungveges("Имя", "Name") + ":", True, (139, 155, 180)), (335, 120))
            win.blit(bigTextInfo.render(changed_character.name, True, (139, 155, 180)), (335, 140))
            pygame.draw.line(win, (139, 155, 180), (325 + len(changed_character.name) * 30, 100), (325 + len(changed_character.name) * 30, 198), 8)
            win.blit(textInfo.render(laungveges("Описание", "Info") + ":", True, (139, 155, 180)), (Width - len(changed_character.info) * 30 - 28, 120))
            win.blit(bigTextInfo.render(changed_character.info, True, (139, 155, 180)), (Width - len(changed_character.info) * 30 - 28, 140))
            back_button.main(menu)
            win.blit(CharacterButton2, (10, 120))
            pets_button.main(pets)
            page_back_button.main(page_1)
            page_next_button.main(page_2)
            win.blit(bigTextInfo.render(str(page), True, (139, 155, 180)), ((Width - 415) // 2 + 340, Height - 96))
            if keys[pygame.K_1]:
                changed_character_num = 0
            if keys[pygame.K_2]:
                changed_character_num = 1
            
            i = 0
            for character in characters_list:
                i += 1
                character.image_num += 1
                if character.image_num == 40:
                    character.image_num = 0
                if i // 3 == page - 1:
                    win.blit(character.images_list[character.image_num // 5], (316, 216))

            if pygame.mouse.get_pressed()[0] == 1:
                mouse_click_image = 1
            try:
                win.blit(mouse_click_images[mouse_click_image - 1], (mouse_x - 64, mouse_y - 64))
                if mouse_click_image == 5:
                    mouse_click_image = None
                else:
                    mouse_click_image += 1
            except TypeError:
                pass
            
            pygame.display.update()
            clock.tick(FPS)
    
    def pets():
        global win, screenmode, mouse_click_image
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_F11]:
                if screenmode == "FULLSCREEN":
                    win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
                    screenmode = "RESIZABLE"
                else:
                    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    screenmode = "FULLSCREEN"
                time.sleep(0.1)

            win.fill((192, 203, 220))
            pygame.draw.rect(win, (139, 155, 180), (-8, 100, 315, Height), 8)
            pygame.draw.rect(win, (139, 155, 180), (315, 100, Width - 325, 100), 8)
            back_button.main(menu)
            character_button.main(characters)
            win.blit(PetsButton2, (10, 192))
            
            if pygame.mouse.get_pressed()[0] == 1:
                mouse_click_image = 1
            try:
                win.blit(mouse_click_images[mouse_click_image - 1], (mouse_x - 64, mouse_y - 64))
                if mouse_click_image == 5:
                    mouse_click_image = None
                else:
                    mouse_click_image += 1
            except TypeError:
                pass

            pygame.display.update()
            clock.tick(FPS)
    characters()

def get_item(num: int):
    global object_to_remove
    inventory.increate("Almond whater", 1)
    object_to_remove = num



# Цикл проверки событий

backrooms_portal = BackroomsPortal(-500, 500)
multyplayer = False

def start_game():
    
    input_text = ""
    chat_input = False
    bigTextInfo = pygame.font.Font(None, 72)
    aaa = 0
    AA = 0

    global Hiro_run, win, Hiro_rect, changed_slot, x, y, menu_open, multyplayer_panel_open, screenmode, inventory_open, hold_left, backrooms, text_color, bullet_num, object_to_remove, craft_items_list, craft_amounts_list, craft_images_list, screenshot_num, mechanisms, mouse_x, mouse_y, item_settings_open, multyplayer_panel, big_rects, objects, mobs, speed, in_cave, chat_tick, craft_list_open, craft_list_page, click, in_motherboard, os, mouse_click_image, HP

    Save_load_mananger = SaveLoadSystem(".save", path + "Gannitto world/files/Worlds/" + world_name)
    pygame.mixer.Sound.play(music_1, -1)
    pygame.mixer.Sound.set_volume(music_1, 0.2)
    
    try:
        mobs = []
        mobs2 = Save_load_mananger.load_data("Mobs")
        for mob in mobs2:
            if mob[0] == "Slime":
                mobs.append(SlimeEnemy(mob[1], mob[2]))
                a = len(mobs) - 1
                if mob[3] == 1: mobs[a].animation_images = [Slime1, Slime1_2, Slime1_3, Slime1_4]
                else: mobs[a].animation_images = [Slime2, Slime2_2, Slime2_3, Slime2_4]
                mobs[a].HP = mob[4]
                mobs[a].animation_count = mob[5]
                mobs[a].reset_offset = mob[6]
                mobs[a].offset_x = mob[7]
                mobs[a].offset_y = mob[8]
            if mob[0] == "Butterfly":
                mobs.append(ButterflyEnemy(mob[1], mob[2]))
                a = len(mobs) - 1
                if mob[3] == 1: mobs[a].animation_images = [Butterfly1, Butterfly1_2, Butterfly1_3]
                mobs[a].HP = mob[4]
                mobs[a].animation_count = mob[5]
                mobs[a].reset_offset = mob[6]
                mobs[a].offset_x = mob[7]
                mobs[a].offset_y = mob[8]
        
        big_rects = []
        big_rects2 = Save_load_mananger.load_data("Rects")
        for big_rect in big_rects2:
            big_rects.append(Big_rect.BigRect(big_rect[0], big_rect[1]))
            big_rects[len(big_rects) - 1].biom = big_rect[2]
        
        x, y, Backrooms.InBackrooms, Backrooms.Level, in_cave, speed, HP = Save_load_mananger.load_data("Info")
        
        objects2 = Save_load_mananger.load_data("Objects")
        for object in objects2:
            if object[0] == "Object":
                a = pygame.transform.scale(pygame.image.load(path + object[4]), (object[5][0], object[5][1]))
                objects.append(Object(object[1], object[2], object[3], object[4], object[5], a, object[6]))
        
        inventory.whole_inventory = []
        inventory2 = Save_load_mananger.load_data("Inventory")
        from Inventory import Resourse
        for cell in inventory2:
            if cell == None:
                inventory.whole_inventory.append(None)
            else:
                inventory.whole_inventory.append(Resourse(cell[0], cell[6], cell[1], cell[2], cell[3]))
                inventory.whole_inventory[len(inventory.whole_inventory) - 1].amount = cell[4]
        del Resourse
    except FileNotFoundError:
        os.mkdir(path + "Gannitto world/files/Worlds/" + world_name)
        big_rects = [Big_rect.BigRect(0, 0)]
        objects = big_rects[0].generate(objects)
        save()
        
    while 1:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_object = None
        click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                quit()
            
            elif event.type == pygame.KEYDOWN and chat_input:
                if event.key == pygame.K_RETURN or len(input_text) == 20:
                    chat_input = False
                    if input_text[0] == "/":   # Команды
                        a = True
                        b = ""
                        c = 0
                        space = False
                        command = []
                        command_error = None
                        for i in input_text:
                            c += 1
                            if a:
                                if not i in ["/", " "]:
                                    a = False
                                    b = i
                            elif i != " ":
                                space = False
                                b += i
                            else:
                                space = True
                            if command == []:
                                if b in ["Tp", "tp", "Teleport", "teleport"]:
                                    command = ["tp"]

                                if b in ["Spawn", "spawn"]:
                                    command = ["spawn"]

                                elif space and not a:
                                    command = [b]

                            else:
                                if command[0] == "tp":
                                    if len(command) == 5:
                                        command_error = laungveges("Слишком много аргументов!", "Too many arguments!")
                                        break
                                    elif b != "" and (space or c == len(input_text)) and b != "tp":
                                        command.append(b)
                                        b = ""
                                    if b == "tp":
                                        b = ""
                                
                                if command[0] == "spawn":
                                    if len(command) == 3:
                                        command_error = laungveges("Слишком много аргументов!", "Too many arguments!")
                                        break
                                    elif b != "" and (space or c == len(input_text)) and b != "tp":
                                        command.append(b)
                                        b = ""
                                    if b == "spawn":
                                        b = ""
                                else:
                                    command_error = laungveges("Неправильная команда!", "Invalid command!")
                                    break
                        if command_error == None:
                            if command[0] == "tp":
                                x = int(command[2])
                                y = int(command[3])
                                input_text = "Вы были успешно телепортированы"
                            elif command[0] == "spawn":
                                a = None
                                for i in command:
                                    if "[" in i:
                                        a = i
                                        break
                                if a != None:
                                    b = False
                                    j = 0
                                    for i in a:
                                        j += 1
                                        if not b and a == "[":
                                            if a[len(a) - 1] == "]":
                                                c = a[j:len(a)].split(",")
                                                break
                                            else:
                                                input_text = laungveges('"[" не была закрыта', '"[" was not closed')
                                if input_text != laungveges('"[" не была закрыта', '"[" was not closed'):
                                    if a != None:
                                        if command[1] == "Bush":
                                            objects.append(Object("Bush", int(c[0]), int(c[1]), "Gannitto world/files/Images/Objects/Bush.png", c[2]))
                                    else:
                                        if command == "Bush":
                                            objects.append(Object("Bush", x, y, "Gannitto world/files/Images/Objects/Bush.png"))
                        else:
                            input_text = command_error
                        chat.append(laungveges("Игра", "Game") + ": " + input_text)
                    else:
                        chat.append(Settings[2] + ": " + input_text)
                    if len(input_text) <= 5:
                        chat_tick = 30
                    else:
                       chat_tick += len(input_text) // 5 * FPS
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
        
        if inventory_open == 1:
            if click[0] and not hold_left:
                inventory.set_start_cell(mouse_x, mouse_y)
                hold_left = True
            if hold_left and not click[0]:
                inventory.set_end_cell(mouse_x, mouse_y)
                hold_left = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_F11]:
            if screenmode == "FULLSCREEN":
                win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
                screenmode = "RESIZABLE"
                win.blit(Hiro, Hiro_rect)
                Hiro_rect = Hiro.get_rect(center=(500, 350))
            else:
                win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                screenmode = "FULLSCREEN"
                win.blit(Hiro, Hiro_rect)
                Hiro_rect = Hiro.get_rect(center=(Width / 2, Height / 2))
            time.sleep(0.1)

        if keys[pygame.K_F1]:
            save()
            settings()

        if keys[pygame.K_F2]:
            if menu_open == 0: menu_open = 1
            else: menu_open = 0
            time.sleep(0.1)

        if keys[pygame.K_c]:
            chat_input = True
        
        if keys[pygame.K_i] and not chat_input:
            if inventory_open == 0:
                inventory_open = 1
            else:
                inventory_open = 0
                i = -1
                if craft_items_list != [None] * 7:
                    i += 1
                    for item in craft_items_list:
                        if item != None:
                            inventory.increate(item, craft_amounts_list[i])
                craft_items_list = [None] * 7
                craft_amounts_list = [None] * 7
                craft_images_list = [None] * 7
            time.sleep(0.1)
        
        if keys[pygame.K_e] and inventory.whole_inventory[changed_slot] != None and not chat_input:
            if Backrooms.InBackrooms:
                backrooms_objects.append(Object(inventory.whole_inventory[changed_slot].name, x, y, "Gannitto world/files/Images/Items/" + inventory.whole_inventory[changed_slot].name + ".png", special_flags="Item"))
            else:
                objects.append(Object(inventory.whole_inventory[changed_slot].name, x, y, "Gannitto world/files/Images/Items/" + inventory.whole_inventory[changed_slot].name + ".png", special_flags="Item"))
            
            inventory.increate(inventory.whole_inventory[changed_slot].name, -1)
            if inventory.whole_inventory[changed_slot].amount == 0:
                inventory.whole_inventory[changed_slot] = None
        
        if keys[pygame.K_ESCAPE]:
            if multyplayer_panel_open == 1:
                multyplayer_panel_open = 0
                time.sleep(0.25)
            elif item_settings_open:
                item_settings_open = False
                time.sleep(0.25)
            elif in_motherboard is not None:
                in_motherboard = None
                time.sleep(0.25)
            elif craft_list_open:
                craft_list_open = False
                time.sleep(0.25)
            elif inventory_open:
                inventory_open = False
                time.sleep(0.25)
            else:
                save()
                menu()

        if keys[pygame.K_m] and not chat_input:
            if multyplayer_panel_open == 0:
                multyplayer_panel_open = 1
            else:
                multyplayer_panel_open = 0
            time.sleep(0.1)
            enable_multiplayer = Button(250, 50, textInfo.render("Enable multiplayer", True, (255, 255, 255)), textInfo.render("Enable multiplayer", True, text_color), multyplayer_panel)
            enter_another_game = Button(250, 210, textInfo.render("Enter another game", True, (255, 255, 255)), textInfo.render("Enter another game", True, text_color), multyplayer_panel)
           
        if keys[pygame.K_q]:
            pygame.mouse.set_pos(Width // 2, 0)
        if keys[pygame.K_SPACE] and inventory.whole_inventory[changed_slot] != None and inventory.whole_inventory[changed_slot].name == "Gun" and inventory.resourses["Bullet"].amount != 0 and not chat_input:
            i = -1
            for slot in inventory.whole_inventory:
                i += 1
                if slot != None and slot.name == "Bullet":
                    if inventory.whole_inventory[i].amount > 1:
                        inventory.increate("Bullet", -1)
                    else:
                        inventory.whole_inventory[i] = None
                    break
            player_bullets.append(Bullet(x, y, mouse_x, mouse_y))
            bullet_num += 1
            time.sleep(0.15)
        
        if keys[pygame.K_1]: changed_slot = 0
        if keys[pygame.K_2]: changed_slot = 1
        if keys[pygame.K_3]: changed_slot = 2
        if keys[pygame.K_4]: changed_slot = 3
        if keys[pygame.K_5]: changed_slot = 4
        if keys[pygame.K_6]: changed_slot = 5
        if keys[pygame.K_7]: changed_slot = 6
        if keys[pygame.K_8]: changed_slot = 7
        if keys[pygame.K_9]: changed_slot = 8
        if keys[pygame.K_0]: changed_slot = 9

        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            a = True
            if Backrooms.InBackrooms:
                for i in range(Width // 2 - 80, Width // 2 + 80):
                    if win.get_at((i, Height // 2 + 127)) == wall_color:
                        a = False
                        break
            if in_cave != None and y <= objects[in_cave + 1].own_height // 2 * -1 + 150:
                a = False
            if a:
                Hiro_run = "Down"
                if costum == 7: 
                    costum = 0
                costum += 1

                if costum == 1:
                    Hiro = Hiro_down_run_1
                elif costum == 2:
                    Hiro = Hiro_down_run_2
                elif costum == 3:
                    Hiro = Hiro_down_run_3
                elif costum == 4:
                    Hiro = Hiro_down_run_4
                elif costum == 5:
                    Hiro = Hiro_down_run_5
                elif costum == 6:
                    Hiro = Hiro_down_run_6
                time.sleep(0.08)
                y -= speed
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            a = True
            if Backrooms.InBackrooms:
                for i in range(Width // 2 - 80, Width // 2 + 80):
                    if win.get_at((i, Height // 2 - 127)) == wall_color:
                        a = False
                        break
            if in_cave != None and y >= objects[in_cave + 1].own_height // 2 - 100:
                a = False
            if a:
                Hiro_run = "Up"
                if costum == 7:
                    costum = 0
                costum += 1

                if costum == 1:
                    Hiro = Hiro_up_run_1
                elif costum == 2:
                    Hiro = Hiro_up_run_2
                elif costum == 3:
                    Hiro = Hiro_up_run_3
                elif costum == 4:
                    Hiro = Hiro_up_run_4
                elif costum == 5:
                    Hiro = Hiro_up_run_5
                elif costum == 6:
                    Hiro = Hiro_up_run_6
                time.sleep(0.08)
                y += speed
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            a = True
            if Backrooms.InBackrooms:
                for i in range(Height // 2 - 100, Height // 2 + 100):
                    if win.get_at((Width // 2 - 100, i)) in [Color(180, 160, 50), Color(50, 50, 50)]:
                        a = False
                        break
            if in_cave != None and x <= objects[in_cave + 1].own_width // 2 * -1 + 150:
                a = False
            if a:
                Hiro_run = "Left"
                if costum == 7:
                    costum = 0
                costum += 1

                if costum == 1:
                    Hiro = Hiro_left_run_1
                elif costum == 2:
                    Hiro = Hiro_left_run_2
                elif costum == 3:
                    Hiro = Hiro_left_run_3
                elif costum == 4:
                    Hiro = Hiro_left_run_4
                elif costum == 5:
                    Hiro = Hiro_left_run_5
                elif costum == 6:
                    Hiro = Hiro_left_run_6
                time.sleep(0.08)
                x -= speed
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            a = True
            if Backrooms.InBackrooms:
                for i in range(Height // 2 - 100, Height // 2 + 100):
                    if win.get_at((Width // 2 + 107, i)) == wall_color:
                        a = False
                        break
            if in_cave != None and x >= objects[in_cave + 1].own_width // 2 - 150:
                a = False
            if a:
                Hiro_run = "Right"
                if costum == 7:
                    costum = 0
                costum += 1

                if costum == 1:
                    Hiro = Hiro_right_run_1
                elif costum == 2:
                    Hiro = Hiro_right_run_2
                elif costum == 3:
                    Hiro = Hiro_right_run_3
                elif costum == 4:
                    Hiro = Hiro_right_run_4
                elif costum == 5:
                    Hiro = Hiro_right_run_5
                elif costum == 6:
                    Hiro = Hiro_right_run_6
                time.sleep(0.08)
                x += speed
        else:
            costum = 0
            if Hiro_run == "Down-left":
                Hiro = Hiro_down_left
            elif Hiro_run == "Down-right":
                Hiro = Hiro_down_right
            elif Hiro_run == "Down":
                Hiro = Hiro_down_run_1
            elif Hiro_run == "Up-left":
                Hiro = Hiro_up_left
            elif Hiro_run == "Up-right":
                Hiro = Hiro_up_right_run_1
            elif Hiro_run == "Up":
                Hiro = Hiro_up_run_1
            elif Hiro_run == "Left":
                Hiro = Hiro_left_run_1
            elif Hiro_run == "Right":
                Hiro = Hiro_right_run_1
        
        if screenmode == "FULLSCREEN":
            if Width // 2 - 100 <= mouse_x <= Width // 2 + 100 and Height // 2 - 100 <= mouse_y <= Height // 2 + 100:
                mouse_object = "It's you"
        else:
            if 400 <= mouse_x <= 600 and 250 <= mouse_y <=  450:
                mouse_object = "It's you"

        if not Backrooms.InBackrooms:
            biom_name = None
            for big_rect in big_rects:
                if big_rect.main() is not None:
                    biom_name = big_rect.main()
            for i in range(-6, 6):
                for ii in range(-3, 3):
                    if biom_name != None:
                        win.blit(textures[biom_name], (Width - x % 256 + i * 256, y % 256 + ii * 256))
                        if in_cave != None:
                            ... #шаги по пещере
                        elif any([keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s]]):
                            if biom_name in ["Grass", "Field"] and random.randint(1, 150) == 1:
                                pygame.mixer.Sound.play(random.choice([Grass_walking1, Grass_walking2, Grass_walking3]), maxtime=1000)

                            if biom_name == "Sand" and random.randint(1, 230) == 1:
                                pygame.mixer.Sound.play(random.choice([Sand_walking1, Sand_walking2, Sand_walking3]), maxtime=1000)

                            if biom_name == "Snow" and random.randint(1, 120) == 1:
                                pygame.mixer.Sound.play(random.choice([Snow_walking1, Snow_walking2, Snow_walking3]), maxtime=1000)

                            if biom_name == "Swamp" and random.randint(1, 120) == 1:
                                pygame.mixer.Sound.play(random.choice([Swamp_walking1, Swamp_walking2, Swamp_walking3]), maxtime=1000)
                    else:
                        win.blit(textInfo.render(laungveges("Пожалуйста, подождите, биом ещё генерируется...", "Please, wait, the biom is still genegating..."), True, (0, 0, 0)), (Width - x % 512 + i * 512, y % 256 + ii * 256))
            if biom_name == None:
                big_rects.append(Big_rect.BigRect(x - x % 100000, y - y % 100000))
                objects = big_rects[len(big_rects) - 1].generate(objects)

        else:
            for i in range(-6, 6):
                for ii in range(-3, 3):
                    win.blit(textures["Backrooms " + str(Backrooms.Level)], (Width - x % 256 + i * 256, y % 256 + ii * 256))
        
        for mechanism in mechanisms:
            mechanism.main()

        if not Backrooms.InBackrooms and in_cave is None:
            backrooms_portal.main()
            if backrooms_portal.x - 128 <= x <= backrooms_portal.x + 128 and backrooms_portal.y - 128 <= y <= backrooms_portal.y + 128:
                Backrooms.InBackrooms = True
                color = colors["Backrooms"]
                text_color = colors["Backrooms2"]
                i = -1
                for object in Backrooms.objects:
                    i += 1
                    backrooms_objects.append(Object(object, Backrooms.objects_x[i], Backrooms.objects_y[i], "Gannitto world/files/Images/Items/" + inventory.resourses[object].name + ".png", special_flags="Item"))
                x = 0
                y = 0
                pygame.mixer.Sound.play(Backrooms_lamps, -1)
                pygame.mixer.music.set_volume(0.5)
                aaa = 100
                AA = 0

        elif Backrooms.InBackrooms:
            
            if int(x / 2000) != Backrooms.room_x:
                Backrooms.get_rooms(int(x / 2000), int(y / 2000))
            if int(y / 2000) != Backrooms.room_y:
                Backrooms.get_rooms(int(x / 2000), int(y / 2000))

            Backrooms.room_x = int(x / 2000)
            Backrooms.room_y = int(y / 2000)
            match Backrooms.Level:
                case 0:
                    ...#win.fill((120, 100, 40))
                case 0.2:
                    ...#win.fill((170, 60, 50))
                case 1:
                    win.fill((100, 100, 100))
                case 2:
                    win.fill((50, 50, 50))
            for room in Backrooms.rooms:
                room.main(x, y)

            i = random.randint(1, 1000)
            if i == 1:
                pygame.mixer.Sound.play(Backrooms_rand_sound_1)
        
            
            match Backrooms.Level:
                case 0:
                    wall_color = Color(180, 160, 50)
                    next_levels = [0.2, 1]
                case 0.2:
                    wall_color = Color(200, 180, 70)
                    next_levels = [0, 1]
                case 1:
                    wall_color = Color(50, 50, 50)
                    next_levels = [2]
                case 2:
                    wall_color = Color(50, 50, 50)

            a, b, c, d = True, True, True, True

            for i in range(Width // 2 - 80, Width // 2 + 80):
                if win.get_at((i, Height // 2 + 127)) == wall_color:
                    a = False
                if win.get_at((Width // 2 - 100, i)) == wall_color:
                    b = False

            for i in range(Height // 2 - 100, Height // 2 + 100):
                if win.get_at((Width // 2 - 100, i)) == wall_color:
                    c = False
                if win.get_at((Width // 2 + 107, i)) == wall_color:
                    d = False

            aa = 0
            for i in [a, b, c, d]:
                if not i:
                    aa += 1

            if aa == 4:
                Backrooms.get_rooms(int(x / 2000), int(y / 2000))

            if aa == 3 and keys[pygame.K_n] and random.randint(1, 30) == 30:
                if Backrooms.Level == 0:
                    pygame.mixer.Sound.stop(Backrooms_lamps)
                AA = 100
                Backrooms.Level = random.choice(next_levels)
                x = 0
                y = 0
                Backrooms.get_rooms(0, 0)
                win.fill((0, 0, 0))

            if aaa > 0:
                win.blit(pygame.transform.scale(win, (Width - aaa * 2, Height - aaa * 2)), (aaa, aaa))
            aaa = 0
            if random.randint(1, 300) == 50:
                aaa = 50

            if AA > 0:
                win.blit(pygame.transform.scale(win, (Width - AA * 2, Height - AA * 2)), (AA, AA))
                AA -= 3
        if not Backrooms.InBackrooms:
            a = None
            for object in objects:
                if object.__class__ == Cave:
                    object.main()
                    if object.get_in() != None:
                        a = object.get_in()
            if in_cave != None and -64 <= x <= 64 and -64 <= y <= 64 and click[0] == 1:
                x = objects[in_cave + 1].x
                y = objects[in_cave + 1].y - 128
                in_cave = None
            if in_cave == None:
                if a != None:
                    in_cave = a
                    x = 0
                    y = -128
            if in_cave != None:
                win.fill((50, 50, 50))
                a = -1
                for i in objects:
                    a -= 1
                    if i.__class__ == Cave:
                        break
                pygame.draw.rect(win, (100, 100, 100), (objects[in_cave + 1].own_width // 2 * -1 - x + Width // 2, y - objects[in_cave + 1].own_height // 2 + Height // 2, objects[in_cave + 1].own_width, objects[in_cave + 1].own_height))
                win.blit(cave, (0 - x + Width // 2 - objects[in_cave + 1].w // 2, y - 0 + Height // 2 - objects[in_cave].h // 2))
                i = -1
                for object in objects[in_cave + 1].objects:
                    i += 1
                    object.main(x, y)
                    if object.__class__ == Object:
                        print(1)
                        if object.x - x + Width // 2 - object.w // 2 <= mouse_x <= object.x - x + Width // 2 + object.w // 2 and y - object.y + Height // 2 - object.h // 2 <= mouse_y <= y - object.y + Height // 2 + object.h // 2:
                            if object.special_flags == "Item":
                                mouse_object = "Click to pick the " + object.name
                                if click[0] == 1:
                                    inventory.increate(object.name, 1)
                                    pygame.mixer.Sound.play(Pick_an_item)
                                    del objects[in_cave + 1].objects[i]
                                    break
                            else:
                                if object.name == "Iron ore" and click[0] == 1 and inventory.whole_inventory[changed_slot] != None and inventory.whole_inventory[changed_slot].name in ["Stone pickaxe"]:
                                    object.special_flags -= 1
                                    object.image = pygame.transform.scale(object.image, (32, 32))
                                    for _ in range(random.randint(20, 25)):
                                        a = random.randint(0, 31)
                                        b = random.randint(0, 31)
                                        if object.image.get_at((a, b)).a != 0:
                                            object.image.set_at((a, b), (0, 0, 0, 99))
                                    object.image.set_alpha(object.image.get_alpha() - 1)
                                    object.image = pygame.transform.scale(object.image, (256, 256))
                                    if random.randint(1, 15) == 1:
                                        pygame.mixer.Sound.play(random.choice([Stone_breaking1, Stone_breaking2]))
                                    if object.special_flags == -1:
                                        del objects[in_cave + 1].objects[i]
                                        for i in range(random.randint(1, 3)):
                                            objects[in_cave + 1].objects.append(Object("Iron ore", random.randint(object.x - 128, object.x + 128), random.randint(object.y - 128, object.y + 128), "Gannitto world/files/Images/Items/Iron ore.png", special_flags="Item"))
                                        break
                                mouse_object = object.name
                        if object.name == "Pot":
                            if object.get_right_pressed() and inventory.whole_inventory[changed_slot] != None and inventory.whole_inventory[changed_slot].type == "Flower":
                                objects.append(Object(inventory.whole_inventory[changed_slot].name, object.x, object.y + 36, 64, 64, inventory.whole_inventory[changed_slot].image, "Item"))
                                inventory.whole_inventory[changed_slot].amount -= 1
                                inventory.resourses[inventory.whole_inventory[changed_slot].name].amount -= 1
                                if inventory.whole_inventory[changed_slot].amount == 0:
                                    inventory.whole_inventory[changed_slot] = None
                
            else:
                i = -1
                for object in objects:
                    i += 1
                    object.main(x, y)
                    if object.x - x + Width // 2 - object.image.get_width() // 2 <= mouse_x <= object.x - x + Width // 2 + object.image.get_width() // 2 and y - object.y + Height // 2 - object.image.get_height() // 2 <= mouse_y <= y - object.y + Height // 2 + object.image.get_height() // 2:
                        if object.special_flags == "Item":
                            mouse_object = "Click to pick the " + object.name
                            if click[0] == 1:
                                inventory.increate(object.name, 1)
                                pygame.mixer.Sound.play(Pick_an_item)
                                if in_cave != None and object.num <= in_cave: in_cave -= 1
                                for ii in objects:
                                    if ii.__class__ == Cave and object.num <= ii.num:
                                        ii.num -= 1
                                del objects[i]
                                break
                        else:
                            if object.name == "Tree" and click[0] == 1:
                                object.special_flags -= 1
                                object.image = pygame.transform.scale(object.image, (32, 32))
                                for _ in range(random.randint(20, 25)):
                                    a = random.randint(0, 31)
                                    b = random.randint(0, 31)
                                    if object.image.get_at((a, b)).a != 0:
                                        object.image.set_at((a, b), (0, 0, 0, 99))
                                object.image.set_alpha(object.image.get_alpha() - 1)
                                object.image = pygame.transform.scale(object.image, (256, 256))
                                if object.special_flags == -1:
                                    del objects[i]
                                    if in_cave != None: in_cave += 1
                                    for i in objects:
                                        if i.__class__ == Cave:
                                            i.num -= 1
                                    for i in range(random.randint(2, 5)):
                                        objects.append(Object("Wooden", random.randint(object.x - 128, object.x + 128), random.randint(object.y - 128, object.y + 128), "Gannitto world/files/Images/Items/Wooden.png", special_flags="Item"))
                                    
                                    for i in range(random.randint(1, 3)):
                                        objects.append(Object("Stick", random.randint(object.x - 128, object.x + 128), random.randint(object.y - 128, object.y + 128), "Gannitto world/files/Images/Items/Stick.png", special_flags="Item"))
                                    break
                            mouse_object = object.name
                    if object.name == "Pot":
                        if object.get_right_pressed() and inventory.whole_inventory[changed_slot] != None and inventory.whole_inventory[changed_slot].type == "Flower":
                            objects.append(Object(inventory.whole_inventory[changed_slot].name, object.x, object.y + 36, 64, 64, inventory.whole_inventory[changed_slot].image, "Item"))
                            inventory.whole_inventory[changed_slot].amount -= 1
                            inventory.resourses[inventory.whole_inventory[changed_slot].name].amount -= 1
                            if inventory.whole_inventory[changed_slot].amount == 0:
                                inventory.whole_inventory[changed_slot] = None
                    if object.name == "Pond":
                        if object.special_flags[0] == 0:
                            ...
                        else:
                            ...
                        
                        if object.special_flags[1] != 0 and inventory.whole_inventory[changed_slot] != None and inventory.whole_inventory[changed_slot].name == "Stone shovel" and object.get_left_pressed() and random.randint(1, 30) == 1:
                            objects.append(Object("Clay", random.randint(object.x - 128, object.x + 128), random.randint(object.y - 128, object.y + 128), "Gannitto world/files/Images/Items/Clay.png", special_flags="Item"))
                            object.special_flags[1] -= 1

        elif len(Backrooms.objects) != 1:
            i = -1
            for object in backrooms_objects:
                i += 1
                object.main(x, y)
                if click[0] == 1 and object.x - x + Width // 2 - object.w // 2 <= mouse_x <= object.x - x + Width // 2 + object.w // 2 and y - object.y + Height // 2 - object.h // 2 <= mouse_y <= y - object.y + Height // 2 + object.h // 2:
                    if object.special_flags == "Item":
                        inventory.increate(object.name, 1)
                        del backrooms_objects[i]
                        break
        
        if object_to_remove != None:
            del objects[object_to_remove]
            if in_cave != None: in_cave += 1
            for i in objects:
                if i.__class__ == Cave:
                    i.num += 1
            object_to_remove = None

        if not Backrooms.InBackrooms and in_cave is None:
            if random.randint(1, 500) == 1: mobs.append(SlimeEnemy(random.randint(x - Width, x + Width), random.randint(y - Height, y + Height)))

        for bullet in player_bullets:
            bullet.main()
        
        i = -1
        mobs_to_remove = []
        if len(mobs) != 0 and not Backrooms.InBackrooms and in_cave is None:
            for mob in mobs:
                i += 1
                if a == 1 and backrooms_portal.x - 128 <= mob.x <= backrooms_portal.x + 128 and backrooms_portal.y - 128 <= mob.y <= backrooms_portal.y + 128:
                    mobs_to_remove.append(i)
                if player_bullets != []:
                    b = -1
                    for ii in player_bullets:
                        b += 1
                        if mob.x - 64 <= ii.x <= mob.x + 64 and mob.y - 64 <= ii.y <= mob.y + 64:
                            mob.HP -= 15
                            try:
                                temp = mob.animation_images[(mob.animation_count - mob.animation_count % 5) // 5]
                            except IndexError:
                                temp = mob.animation_images[(mob.animation_count - mob.animation_count % 5) // 5 - 1]
                            for i in range(128):
                                for ii in range(128):
                                    if mob.animation_images[0].get_at((i, ii)).a != 0:
                                        temp.set_at((i, ii), (200, 0, 0, 80))
                            win.blit(temp, (mob.x - x + Width // 2 - 64, y - mob.y + Height // 2 - 32))
                            win.blit(textInfo.render(str(mob.HP), True, (180, 10, 10)), (mob.x + 58 - x + Width // 2 - 64, y - mob.y + Height // 2 - 32))
                            try:
                                if mob.rand_mob == 1:
                                    temp = pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Objects/Blue Slime " + str((mob.animation_count - mob.animation_count % 5) // 5 + 1) + ".png"), (128, 128))
                                else:
                                    temp = pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Objects/Pink Slime " + str((mob.animation_count - mob.animation_count % 5) // 5 + 1) + ".png"), (128, 128))
                            except FileNotFoundError:
                                if mob.rand_mob == 1:
                                    temp = pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Objects/Blue Slime " + str((mob.animation_count - mob.animation_count % 5) // 5) + ".png"), (128, 128))
                                else:
                                    temp = pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Objects/Pink Slime " + str((mob.animation_count - mob.animation_count % 5) // 5) + ".png"), (128, 128))
                            del player_bullets[b]
                            break
                mob.main()
                if mob.HP < 1:
                    for i in range(random.randint(1, 3)):
                        if mob.rand_mob == 1:
                            objects.append(Object("Blue slime", mob.x + random.randint(-30, 30), mob.y + random.randint(-30, 30), "Gannitto world/files/Images/Items/Blue slime.png", special_flags="Item"))
                        else:
                            objects.append(Object("Pink slime", mob.x + random.randint(-30, 30), mob.y + random.randint(-30, 30), "Gannitto world/files/Images/Items/Pink slime.png", special_flags="Item"))
                        del mobs[i]
                        break
        
        del i
        
        win.blit(Hiro, Hiro_rect)
        if inventory.whole_inventory[changed_slot] != None:
            if Hiro == Hiro_down_run_1:
                win.blit(inventory.whole_inventory[changed_slot].image, (Width // 2 - 80, Height // 2))

            if Hiro == Hiro_left_run_1:
                win.blit(inventory.whole_inventory[changed_slot].image, (Width // 2 - 70, Height // 2))
                win.blit(Hiro, Hiro_rect)

            if Hiro == Hiro_right_run_1:
                win.blit(pygame.transform.flip(inventory.whole_inventory[changed_slot].image, True, False), (Width // 2 - 30, Height // 2))

            elif Hiro == Hiro_up_run_1:
                win.blit(inventory.whole_inventory[changed_slot].image, (Width // 2 + 20, Height // 2))
                win.blit(Hiro, Hiro_rect)

        for i in range(Settings[3]):
            win.blit(pygame.transform.scale(win, (Width - i * 2, Height - i * 2)), (i, i))

        if keys[pygame.K_F3] and keys[pygame.K_LALT]:
            pygame.image.save(win, "C://Users/" + getpass.getuser() + "/Pictures/Your_Screenshot" + str(screenshot_num) + ".png")
            screenshot_num += 1
            for i in range(3):
                win.fill((200, 255, 200))
                clock.tick(FPS)
                pygame.display.update()
            time.sleep(0.1)
            chat.append(laungveges("Игра: ваш сриншот находится в ", "Your screenshot is in ") + "C://Users/" + getpass.getuser() + "/Pictures/Your_screenshot" + str(screenshot_num) + ".png")
            chat_tick += len(laungveges("Игра: ваш скриншот находится в ", "Your screenshot is in ") + "C://Users/" + getpass.getuser() + "/Pictures/Your_screenshot" + str(screenshot_num) + ".png") // 5 * FPS
        
        if inventory_open == 0:
            a = -70
            for i in range (10):
                a += 80
                if i == changed_slot: win.blit(Changed_inventory_slot, (a, 10))
                else: win.blit(Inventory_slot, (a, 10))
            inventory.draw_panel()
        else:
            a = 10
            b = 10
            for i in range (30):
                if i == changed_slot: win.blit(Changed_inventory_slot, (a, b))
                else: win.blit(Inventory_slot, (a, b))
                if a == 730:
                    a = -70
                    b += 80
                a += 80
            
            win.blit(Object_inventory_slot, (10, 250))
            win.blit(Tool_inventory_slot, (90, 250))
            if inventory.check_recipies() is not None:
                win.blit(Changed_inventory_slot, (730, 250))
                win.blit(inventory.resourses[inventory.check_recipies()[0]].image, (730, 250))
                if inventory.check_recipies()[2] != None:
                    win.blit(inventory.resourses[inventory.check_recipies()[2]].image, (10, 250))
                if inventory.check_recipies()[3] != None:
                    win.blit(inventory.resourses[inventory.check_recipies()[3]].image, (90, 250))
                if 730 <= mouse_x <= 810 and 250 <= mouse_y <= 330 and click[0]:
                    inventory.increate(inventory.check_recipies()[0], inventory.check_recipies()[1])
                    craft_items_list = [None] * 7
                    craft_amounts_list = [None] * 7
                    craft_images_list = [None] * 7
            
            if (810 <= mouse_x <= 874 and 10 <= mouse_y <= 74) or inventory.Split_items:
                win.blit(Split_items2, (810, 10))
                if click[0] and (810 <= mouse_x <= 874 and 10 <= mouse_y <= 74):
                    if inventory.Split_items:
                        inventory.Split_items = False
                    else:
                        inventory.Split_items = True
            else:
                win.blit(Split_items1, (810, 10))
            inventory.draw_whole()
            
            if 810 <= mouse_x <= 874 and 90 <= mouse_y <= 154:
                win.blit(Changed_inventory_slot, (810, 90))
                if click[0] == 1 and not craft_list_open:
                    craft_list_open = True

            if craft_list_open:
                back_button = Button(130, Height - 160, bigTextInfo.render("<", True, (0, 150, 0)), bigTextInfo.render("<", True, (0, 100, 0)), win)
                next_button = Button(Width - 130, Height - 160, bigTextInfo.render(">", True, (0, 150, 0)), bigTextInfo.render(">", True, (0, 100, 0)), win)
                win.blit(Changed_inventory_slot, (810, 90))
                a = pygame.Surface((Width, Height))
                a.fill((0, 0, 0))
                a.set_alpha(90)
                win.blit(a, (0, 0))
                pygame.draw.rect(win, text_color, (100, 100, Width - 200, Height - 200))
                pygame.draw.rect(win, (0, 150, 0), (100, 100, Width - 200, Height - 200), 10)
                win.blit(bigTextInfo.render("x", True, (0, 150, 0)), (Width - 160, 130))
                if Width - 160 <= mouse_x <= Width - 130 and 130 <= mouse_y <= 160:
                    win.blit(bigTextInfo.render("x", True, (0, 100, 0)), (Width - 160, 130))
                    if click[0] == 1:
                        craft_list_open = False
                win.blit(bigTextInfo.render(str(craft_list_page), True, (0, 150, 0)), (Width // 2 - 15, Height - 230))
                back_button.main(None)
                if back_button.get_pressed() and craft_list_page != 1:
                    craft_list_page -= 1
                next_button.main(None)
                if next_button.get_pressed() and craft_list_page < len(inventory.recipes) / 5:
                    craft_list_page += 1
                a = -1
                if craft_list_page < len(inventory.recipes) / 5 or len(inventory.recipes) % 5 == 0:
                    for i in range((craft_list_page - 1) * 5 - 1, (craft_list_page - 1) * 5 + 5 - 1):
                        a += 1
                        aa = -1
                        for ii in inventory.recipes[i].ingredients:
                            if ii == None:
                                break
                            else:
                                aa += 1
                                win.blit(Inventory_slot, (130 + aa * 80, 130 + a * 80))
                                try:
                                    win.blit(inventory.resourses[ii].image, (130 + aa * 80, 130 + a * 80))
                                except KeyError:
                                    win.blit(no_file_texture, (130 + aa * 80, 130 + a * 80))
                                win.blit(textInfo.render(str(inventory.recipes[i].ingredients_amounts[aa]), True, (0, 150, 0)), (140 + aa * 80, 172 + a * 80))
                        aa += 1
                        if inventory.recipes[i].need_object != None:
                            win.blit(Changed_inventory_slot, (150 + aa * 80, 130 + a * 80))
                            try:
                                win.blit(inventory.resourses[inventory.recipes[i].need_object].image, (200 + aa * 80, 130 + a * 80))
                            except KeyError:
                                win.blit(no_file_texture, (200 + aa * 80, 130 + a * 80))
                        aa += 1
                        if inventory.recipes[i].need_tool != None:
                            win.blit(Changed_inventory_slot, (150 + aa * 80, 130 + a * 80))
                            try:
                                win.blit(inventory.resourses[inventory.recipes[i].need_tool].image, (200 + aa * 80, 130 + a * 80))
                            except KeyError:
                                win.blit(no_file_texture, (200 + aa * 80, 130 + a * 80))
                        aa += 1
                        win.blit(Changed_inventory_slot, (150 + aa * 80, 130 + a * 80))
                        try:
                            win.blit(inventory.resourses[inventory.recipes[i].result].image, (200 + aa * 80, 130 + a * 80))
                            win.blit(textInfo.render(str(inventory.recipes[i].result_amount), True, (0, 150, 0)), (210 + aa * 80, 172 + a * 80))
                        except KeyError:
                            win.blit(no_file_texture, (200 + aa * 80, 130 + a * 80))
                        
                else:
                    a = -1
                    b = ""
                    for i in ((craft_list_page - 1) * 5 - 1, (craft_list_page - 1) * 5 - 1 + len(inventory.recipes) % 5):
                        b += str(i) + " "
                    print(b)
                    for i in ((craft_list_page - 1) * 5 - 1, (craft_list_page - 1) * 5 - 1 + len(inventory.recipes) % 5):
                        a += 1
                        aa = -1
                        for ii in inventory.recipes[i].ingredients:
                            if ii == None:
                                break
                            else:
                                aa += 1
                                win.blit(Inventory_slot, (130 + aa * 80, 130 + a * 80))
                                win.blit(inventory.resourses[ii].image, (130 + aa * 80, 130 + a * 80))
                                win.blit(textInfo.render(str(inventory.recipes[i].ingredients_amounts[aa]), True, (0, 150, 0)), (140 + aa * 80, 172 + a * 80))
                        aa += 1
                        if inventory.recipes[i].need_object != None:
                            win.blit(Changed_inventory_slot, (150 + aa * 80, 130 + a * 80))
                            win.blit(inventory.resourses[inventory.recipes[i].need_object].image, (200 + aa * 80, 130 + a * 80))
                        aa += 1
                        if inventory.recipes[i].need_tool != None:
                            win.blit(Changed_inventory_slot, (150 + aa * 80, 130 + a * 80))
                            win.blit(inventory.resourses[inventory.recipes[i].need_tool].image, (200 + aa * 80, 130 + a * 80))
                        aa += 1
                        win.blit(Changed_inventory_slot, (150 + aa * 80, 130 + a * 80))
                        win.blit(inventory.resourses[inventory.recipes[i].result].image, (200 + aa * 80, 130 + a * 80))
                        win.blit(textInfo.render(str(inventory.recipes[i].result_amount), True, (0, 150, 0)), (210 + aa * 80, 172 + a * 80))
            
            else:
                win.blit(Inventory_slot, (810, 90))

            if inventory.whole_inventory[changed_slot] != None and inventory.whole_inventory[changed_slot].name == "Wrench":
                if 810 <= mouse_x <= 874 and 170 <= mouse_y <= 234:
                    win.blit(Changed_inventory_slot, (810, 170))
                    if click[0]:
                        if item_settings_open:
                            item_settings_open = False
                        else:
                            item_settings_open = True
                        time.sleep(0.1)
                else:
                    win.blit(Inventory_slot, (810, 170))
        
        if item_settings_open:
            if inventory.whole_inventory[changed_slot].name == "Wrench":
                a = pygame.Surface((Width, Height))
                a.fill((0, 0, 0))
                a.set_alpha(90)
                win.blit(a, (0, 0))
                pygame.draw.rect(win, text_color, (100, 100, Width - 200, Height - 200))
                pygame.draw.rect(win, (0, 150, 0), (100, 100, Width - 200, Height - 200), 10)
                win.blit(pygame.transform.scale2x(inventory.whole_inventory[changed_slot].image), (Width // 2 - 64, 130))
                pygame.draw.line(win, (0, 150, 0), (150, 308), (Width - 150, 308), 10)
                win.blit(textInfo.render(laungveges("Только провод", "Only wire"), True, (0, 150, 0)), (130, 348))
                win.blit(textInfo.render(laungveges("Любые механизмы", "All mechanisms"), True, (0, 150, 0)), (Width // 2 - textInfo.render(laungveges("Любые механизмы", "All mechanisms"), True, (0, 150, 0)).get_width() // 2, 348))
                win.blit(textInfo.render(laungveges("Любые механизмы, кроме провода", "All mechanisms, but wire"), True, (0, 150, 0)), (Width - 150 - textInfo.render(laungveges("Любые механизмы, кроме провода", "All mechanisms, but wire"), True, (0, 150, 0)).get_width(), 378))

                if inventory.whole_inventory[changed_slot].settings == ["Only wire"]:
                    pygame.draw.rect(win, (0, 150, 0), (120, 278, 60, 60), 30)
                    pygame.draw.circle(win, (0, 150, 0), (Width // 2, 308), 30)
                    pygame.draw.circle(win, (0, 150, 0), (Width - 150, 308), 30)
                if inventory.whole_inventory[changed_slot].settings == []:
                    pygame.draw.circle(win, (0, 150, 0), (150, 308), 30)
                    pygame.draw.rect(win, (0, 150, 0), (Width // 2 - 30, 278, 60, 60), 30)
                    pygame.draw.circle(win, (0, 150, 0), (Width - 150, 308), 30)
                if inventory.whole_inventory[changed_slot].settings == ["All mechanisms, but wire"]:
                    pygame.draw.circle(win, (0, 150, 0), (150, 308), 30)
                    pygame.draw.circle(win, (0, 150, 0), (Width // 2, 308), 30)
                    pygame.draw.rect(win, (0, 150, 0), (Width - 180, 278, 60, 60), 30)

                if 120 <= mouse_x <= 180 and 278 <= mouse_y <= 338 and click[0]:
                    inventory.whole_inventory[changed_slot].settings = ["Only wire"]
                if Width // 2 - 30 <= mouse_x <= Width // 2 + 30 and 278 <= mouse_y <= 338 and click[0]:
                    inventory.whole_inventory[changed_slot].settings = []
                if Width - 180 <= mouse_x <= Width - 120 and 278 <= mouse_y <= 338 and click[0]:
                    inventory.whole_inventory[changed_slot].settings = ["All mechanisms, but wire"]
        
        if inventory.whole_inventory[changed_slot] is not None:
            if inventory_open == 0:
                win.blit(textInfo.render(inventory.whole_inventory[changed_slot].name, True, text_color), (10, 80))
            else:
                win.blit(textInfo.render(inventory.whole_inventory[changed_slot].name, True, text_color), (10, 340))
        
        if in_motherboard is not None:
            a = pygame.Surface((Width, Height))
            a.fill((0, 0, 0))
            a.set_alpha(90)
            win.blit(a, (0, 0))
            pygame.draw.rect(win, text_color, (Width // 2 - 300, Height // 2 - 300, 600, 600))
            pygame.draw.rect(win, (0, 150, 0), (Width // 2 - 300, Height // 2 - 300, 600, 600), 10)
            win.blit(bigTextInfo.render("x", True, (0, 150, 0)), (Width // 2 + 236, Height // 2 - 268))
            a = -1
            b = 0

            for i in in_motherboard.objects:
                a += 1
                if a == 32:
                    a = 0
                    b += 1
                if i is None:
                    pygame.draw.rect(win, (0, 150, 0), (Width // 2 - 300 + a * 18.75, Height // 2 - 300 + b * 18.75, 18.75, 18.75), 2)
                else:
                    i.main()
                    if i.condition == "On":
                        pygame.draw.rect(win, (180, 0, 0), (Width // 2 - 300 + a * 18.75, Height // 2 - 300 + b * 18.75, 18.75, 18.75))
                    if i.condition == "Off":
                        pygame.draw.rect(win, (180, 100, 100), (Width // 2 - 300 + a * 18.75, Height // 2 - 300 + b * 18.75, 18.75, 18.75))
            
            if Width // 2 + 236 <= mouse_x <= Width // 2 + 364 and Height // 2 - 332 <= mouse_y <= Height // 2 - 236:
                win.blit(bigTextInfo.render("x", True, (0, 100, 0)), (Width // 2 + 236, Height // 2 - 268))
                if click[0] == 1:
                    in_motherboard = None

        if menu_open == 1:
            if inventory_open == 0:
                win.blit(textInfo.render("X " + str(x // 50), True, text_color), (10, 300))
                win.blit(textInfo.render("Y " + str(y // 50), True, text_color), (10, 350))
                win.blit(textInfo.render("FPS " + str(FPS), True, text_color), (10, 400))
                if Backrooms.InBackrooms:
                    win.blit(textInfo.render("You are in backrooms lol", True, text_color), (10, 500))
                    win.blit(textInfo.render("Level " + str(Backrooms.Level), True, text_color), (10, 550))
            else:
                win.blit(textInfo.render("X " + str(x // 50), True, text_color), (10, 400))
                win.blit(textInfo.render("Y " + str(y // 50), True, text_color), (10, 450))
                win.blit(textInfo.render("FPS " + str(FPS), True, text_color), (10, 500))
                if Backrooms.InBackrooms:
                    win.blit(textInfo.render("You are in backrooms lol", True, text_color), (10, 600))
                    win.blit(textInfo.render("Level " + str(Backrooms.Level), True, text_color), (10, 650))
        
        if inventory.whole_inventory[changed_slot] != None and inventory.whole_inventory[changed_slot].name == "Wire":
            if in_motherboard is None:
                pygame.draw.rect(win, text_color, ((x // 64) * 64 - x + mouse_x - mouse_x % 64, y - (y // 64) * 64 + mouse_y - mouse_y % 64, 64, 64), 4)
                a = True
                if click[0]:
                    for mechanism in mechanisms:
                        if mechanism.x == (x + mouse_x - Width // 2) // 64 and mechanism.y == (y - mouse_y + Height // 2) // 64:
                            a = False
                            break
                
                    if a:
                        inventory.whole_inventory[changed_slot].amount -= 1
                        if inventory.whole_inventory[changed_slot].amount == 0:
                            inventory.whole_inventory[changed_slot] = None
                        mechanisms.append(Wire(None))
            else:
                a = True
                if click[0]:
                    for mechanism in in_motherboard.objects:
                        if mechanism != None and mechanism.x == (mouse_x - Width // 2 - 300) // 18.75 and mechanism.y == (mouse_y + Width // 2 - 300) // 18.75:
                            a = False
                            break
                
                    if a and Width // 2 - 300 <= mouse_x <= Width // 2 + 300 and  Height // 2 - 310 <= mouse_y < Height // 2 + 290:
                        inventory.whole_inventory[changed_slot].amount -= 1
                        if inventory.whole_inventory[changed_slot].amount == 0:
                            inventory.whole_inventory[changed_slot] = None
                        in_motherboard.objects[(mouse_x - Width // 2 - 300) // 19 + ((mouse_y + Width // 2 - 300) // 19 - 19) * 32] = (Wire(in_motherboard))

        if inventory.whole_inventory[changed_slot] != None and inventory.whole_inventory[changed_slot].name == "Lever":
            pygame.draw.rect(win, text_color, ((x // 64) * 64 - x + mouse_x - mouse_x % 64, y - (y // 64) * 64 + mouse_y - mouse_y % 64, 64, 64), 4)
            a = True
            if click[0]:
                for mechanism in mechanisms:
                    if mechanism.x == (x + mouse_x - Width // 2) // 64 and mechanism.y == (y - mouse_y + Height // 2) // 64:
                        a = False
                
                if a:
                    inventory.whole_inventory[changed_slot].amount -= 1
                    if inventory.whole_inventory[changed_slot].amount == 0:
                        inventory.whole_inventory[changed_slot] = None
                    mechanisms.append(Lever(None))

        if inventory.whole_inventory[changed_slot] != None and inventory.whole_inventory[changed_slot].name == "Wrench":
            pygame.draw.rect(win, text_color, ((x // 64) * 64 - x + mouse_x - mouse_x % 64, y - (y // 64) * 64 + mouse_y - mouse_y % 64, 64, 64), 4)
            if click[0]:
                for mechanism in mechanisms:
                    if mechanism.x == (x + mouse_x - Width // 2) // 64 and mechanism.y == (y - mouse_y + Height // 2) // 64:
                        if (inventory.whole_inventory[changed_slot].settings == ["Only wire"] and mechanism.__class__ == Wire) or inventory.whole_inventory[changed_slot].settings == [] or (inventory.whole_inventory[changed_slot].settings == ["All mechanisms, but wire"] and mechanism.__class__ != Wire):
                            del mechanisms[mechanism.num]
                        break

        if inventory.whole_inventory[changed_slot] != None and inventory.whole_inventory[changed_slot].name == "Random box":
            pygame.draw.rect(win, text_color, ((x // 64) * 64 - x + mouse_x - mouse_x % 64, y - (y // 64) * 64 + mouse_y - mouse_y % 64, 64, 64), 4)
            a = True
            if click[0]:
                for mechanism in mechanisms:
                    if mechanism.x == (x + mouse_x - Width // 2) // 64 and mechanism.y == (y - mouse_y + Height // 2) // 64:
                        a = False
                
                if a:
                    inventory.whole_inventory[changed_slot].amount -= 1
                    if inventory.whole_inventory[changed_slot].amount == 0:
                        inventory.whole_inventory[changed_slot] = None
                    mechanisms.append(Random_box(None))

        if inventory.whole_inventory[changed_slot] != None and inventory.whole_inventory[changed_slot].name == "Motherboard":
            pygame.draw.rect(win, text_color, ((x // 64) * 64 - x + mouse_x - mouse_x % 64, y - (y // 64) * 64 + mouse_y - mouse_y % 64, 64, 64), 4)
            a = True
            if click[0]:
                for mechanism in mechanisms:
                    if mechanism.x == (x + mouse_x - Width // 2) // 64 and mechanism.y == (y - mouse_y + Height // 2) // 64:
                        a = False
                
                if a:
                    inventory.whole_inventory[changed_slot].amount -= 1
                    if inventory.whole_inventory[changed_slot].amount == 0:
                        inventory.whole_inventory[changed_slot] = None
                    mechanisms.append(Motherboard(None))

        if inventory.whole_inventory[changed_slot] != None and inventory.whole_inventory[changed_slot].name == "Portal gun":
            pygame.draw.rect(win, text_color, ((x // 128) * 128 - x + mouse_x - mouse_x % 128, y - (y // 256) * 256 + mouse_y - mouse_y % 256, 128, 256), 4)
            if click[0]:
                a = 0
                for object in objects:
                    if object.x == (x + mouse_x - Width // 2) // 128 and object.y == (y - mouse_y + Height // 2) // 256:
                        a += 1
                
                if a != 2:
                    objects.append(Portal())

        if inventory.whole_inventory[changed_slot] != None and inventory.whole_inventory[changed_slot].name == "Table":
            pygame.draw.rect(win, text_color, ((x // 256) * 256 - x + mouse_x - mouse_x % 256, y - (y // 256) * 256 + mouse_y - mouse_y % 256, 256, 256), 4)
            if click[0]:
                a = 0
                for object in objects:
                    if object.x == (x + mouse_x - Width // 2) // 256 and object.y == (y - mouse_y + Height // 2) // 256:
                        a += 1
                
                if a != 2:
                    inventory.whole_inventory[changed_slot].amount -= 1
                    if inventory.whole_inventory[changed_slot].amount == 0:
                        inventory.whole_inventory[changed_slot] = None
                    objects.append(Object("Table", (x + mouse_x - Width // 2) // 256 * 256, (y - mouse_x + Height // 2) // 256 * 256, "Gannitto world/files/Images/Objects/Table.png", special_flags="Item"))
            
        if inventory.whole_inventory[changed_slot] != None and inventory.whole_inventory[changed_slot].name == "Wall table":
            pygame.draw.rect(win, text_color, ((x // 256) * 256 - x + mouse_x - mouse_x % 256, y - (y // 256) * 256 + mouse_y - mouse_y % 256, 256, 256), 4)
            if click[0]:
                a = 0
                for object in objects:
                    if object.x == (x + mouse_x - Width // 2) // 256 and object.y == (y - mouse_y + Height // 2) // 256:
                        a += 1
                
                if a != 2:
                    inventory.whole_inventory[changed_slot].amount -= 1
                    if inventory.whole_inventory[changed_slot].amount == 0:
                        inventory.whole_inventory[changed_slot] = None
                    objects.append(Object("Wall table", (x + mouse_x - Width // 2) // 256 * 256, (y - mouse_x + Height // 2) // 256 * 256, "Gannitto world/files/Images/Objects/Wall table.png", [256, 256], special_flags="Item"))

        if inventory.whole_inventory[changed_slot] != None and inventory.whole_inventory[changed_slot].name == "Furnace":
            pygame.draw.rect(win, text_color, ((x // 256) * 256 - x + mouse_x - mouse_x % 256, y - (y // 256) * 256 + mouse_y - mouse_y % 256, 256, 256), 4)
            if click[0]:
                a = 0
                for object in objects:
                    if object.x == (x + mouse_x - Width // 2) // 256 and object.y == (y - mouse_y + Height // 2) // 256:
                        a += 1
                
                if a != 2:
                    inventory.whole_inventory[changed_slot].amount -= 1
                    if inventory.whole_inventory[changed_slot].amount == 0:
                        inventory.whole_inventory[changed_slot] = None
                    objects.append(Object("Furnace", (x + mouse_x - Width // 2) // 256 * 256, (y - mouse_x + Height // 2) // 256 * 256, "Gannitto world/files/Images/Items/Furnace.png", [256, 256], special_flags="Item"))
        
        if inventory.whole_inventory[changed_slot] != None and inventory.whole_inventory[changed_slot].name in ["Wooden wall", "Brick wall", "Stone brick wall"]:
            pygame.draw.rect(win, text_color, ((x // 256) * 256 - x + mouse_x - mouse_x % 256, y - (y // 256) * 256 + mouse_y - mouse_y % 256, 256, 256), 4)
            a = True
            if click[0]:
                for object in objects:
                    if object.x == (x + mouse_x - Width // 2) - (x + mouse_x - Width // 2) % 256 and object.y == (y - mouse_y + Height // 2) - (y - mouse_y + Height // 2) % 256:
                        a = False
                
                if a:
                    inventory.whole_inventory[changed_slot].amount -= 1
                    if inventory.whole_inventory[changed_slot].amount == 0:
                        inventory.whole_inventory[changed_slot] = None
                    objects.append(Wall(inventory.whole_inventory[changed_slot].name))

        if mouse_object != None:
            if screenmode == "FULLSCREEN":
                win.blit(textInfo.render(mouse_object, True, text_color), (Width - textInfo.render(mouse_object, True, text_color).get_width() - 10, 10))
            else:
                win.blit(textInfo.render(mouse_object, True, text_color), (990 - textInfo.render(mouse_object, True, text_color).get_width(), 10))
                
        win.blit(textInfo.render(input_text, True, text_color), (10, Height - 30))

        if chat_tick != 0:
            a = 2
            for i in chat[len(chat) - 1 - chat_tick // 90:len(chat)]:
                a += 1
                win.blit(textInfo.render(i, True, text_color), (10, Height- a * 30))
            chat_tick -= 1

        if multyplayer_panel_open == 1:
            multyplayer_panel.fill(text_color)
            enable_multiplayer.main(None)
            enter_another_game.main(None)
            if enable_multiplayer.get_pressed():
                server = True
                new_socket = socket.socket()
                host_name = socket.gethostname()
                s_ip = socket.gethostbyname(host_name)

                port = 8080

                new_socket.bind((host_name, port))
                print("Binding successful!")
                print("This is your IP: ", s_ip)

                name = "abobus" #input('Enter name: ')

                new_socket.listen(3) 


                conn, add = new_socket.accept()

                print("Received connection from ", add[0])
                print('Connection Established. Connected From: ',add[0])

                client = (conn.recv(1024)).decode()
                print(client + ' has connected.')

            if enter_another_game.get_pressed():
                server = False
                socket_server = socket.socket()
                server_host = socket.gethostname()
                ip = socket.gethostbyname(server_host)
                sport = 8080

                print('This is your IP address: ',ip)
                server_host = "192.168.1.6" #input('Enter friend\'s IP address:')
                name = Settings[2] #input('Enter Friend\'s name: ')

                socket_server.connect((server_host, sport))

                socket_server.send(name.encode())
                server_name = socket_server.recv(1024)
                server_name = server_name.decode()

            win.blit(multyplayer_panel, (Width - 500, Height - 250))

        if multyplayer:
            if server:
                message = x + " " + y
                conn.send(message.encode())
                message = conn.recv(1024)
                message = message.decode()
                print(client, ':', message)
            else:
                message = (socket_server.recv(1024)).decode()
                print(server_name, ":", message)
                message = x + " " + y
                socket_server.send(message.encode())
        
        if inventory.whole_inventory[inventory.start_cell] != None and inventory.start_cell != 0 and hold_left:
            pygame.draw.rect(win, text_color, (mouse_x, mouse_y, max(textInfo.render(laungveges(inventory.whole_inventory[inventory.start_cell].info[0], inventory.whole_inventory[inventory.start_cell].info[1]), True, text_color).get_width(), textInfo.render(laungveges(inventory.whole_inventory[inventory.start_cell].purpose[0], inventory.whole_inventory[inventory.start_cell].purpose[1]), True, text_color).get_width()) + 40, 130), 3)
            win.blit(textInfo.render(laungveges(inventory.whole_inventory[inventory.start_cell].info[0], inventory.whole_inventory[inventory.start_cell].info[1]), True, text_color), (mouse_x + 20, mouse_y + 20))
            win.blit(textInfo.render(laungveges(inventory.whole_inventory[inventory.start_cell].purpose[0], inventory.whole_inventory[inventory.start_cell].purpose[1]), True, text_color), (mouse_x + 20, mouse_y + 50))
            
            win.blit(inventory.whole_inventory[inventory.start_cell].image, (mouse_x - 32, mouse_y - 32))
        
        if keys[pygame.K_F3] and not keys[pygame.K_LALT]:
            pygame.image.save(win, "C://Users/serez/Pictures/Your_Screenshot" + str(screenshot_num) + ".png")
            screenshot_num += 1
            for i in range(3):
                win.fill((200, 255, 200))
                clock.tick(FPS)
                pygame.display.update()
            time.sleep(0.1)
            chat.append(laungveges("Игра: ваш скриншот находится в ", "Your screenshot is in ") + "C://Users/" + getpass.getuser() + "/Pictures/Your_screenshot" + str(screenshot_num) + ".png")
            chat_tick += len(laungveges("Игра: ваш скриншот находится в ", "Your screenshot is in ") + "C://Users/" + getpass.getuser() + "/Pictures/Your_screenshot" + str(screenshot_num) + ".png") // 5 * FPS
            
        if keys[pygame.K_p]:
            import os
            win.fill((0, 0, 0))
            win = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
            win.blit(textInfo.render(laungveges("Не пугайтесь, игра не сломалась. Геймплей продолжится, когда вы закроете создатель плагинов.", "Don't worry, the game is not broken. The gameplay will continue, when you close the plugin creator"), True, (255, 255, 255)), ((Width - textInfo.size(laungveges("Не пугайтесь, игра не сломалась. Геймплей продолжится, когда вы закроете создатель плагинов.", "Don't worry, the game is not broken. The gameplay will continue, when you close the plugin creator"))[0]) // 2, Height // 2 - 32))
            pygame.display.update()
            Save_load_mananger = SaveLoadSystem(".save", path + "Gannitto world/files")
            Save_load_mananger.save_data(changed_laungvege, "Laungvege")
            os.system("python " + path + "/\"Gannitto world\"/files/Plugin_creater.py")

        if pygame.mouse.get_pressed()[0] == 1:
            mouse_click_image = 1
        try:
            win.blit(mouse_click_images[mouse_click_image - 1], (mouse_x - 64, mouse_y - 64))
            if mouse_click_image == 5:
                mouse_click_image = None
            else:
                mouse_click_image += 1
        except TypeError:
            pass
        
        pygame.display.update()
        clock.tick(FPS)



def worlds():

    global world_name, mouse, mouse_click_image

    page_back_button = Button(74, Height - 74, pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Buttons/Back.png"), (128, 128)), pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Buttons/Back 2.png"), (128, 128)), win)
    page_next_button = Button(Width - 74, Height - 74, pygame.transform.flip(pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Buttons/Back.png"), (128, 128)), True, False), pygame.transform.flip(pygame.transform.scale(pygame.image.load(path + "Gannitto world/files/Images/Buttons/Back 2.png"), (128, 128)), True, False), win)
    create_new_world_button = Button(Width // 2, 50, textInfo.render(laungveges("Создать новый мир", "Create new world"), True, (139, 155, 180)), textInfo.render(laungveges("Создать новый мир", "Create new world"), True, (58, 68, 102)), win)
    page = 1
    input_text = None

    while 1:

        mouse_x, mouse_y = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN and input_text is not None:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    world_name = input_text
                    from Inventory import get_items
                    get_items()
                    del get_items
                    start_game()
                else:
                    input_text += event.unicode

        for dirs, folder, files in os.walk(path + "Gannitto world/files/Worlds/"):
            inside_folders = folder
            break
        inside_folders.sort()
        win.fill((192, 203, 220))
        if input_text is None:
            create_new_world_button.main(None)
            if create_new_world_button.get_pressed():
                input_text = ""

            page_back_button.main(None)
            if page_back_button.get_pressed() and page != 1:
                page -= 1
            page_next_button.main(None)
            if page_next_button.get_pressed() and page < len(inside_folders) / 5:
                page += 1

            win.blit(textInfo.render(str(page), True, (139, 155, 180)), (Width // 2 - 10, Height - 60))

            if inside_folders != []:
                if page < len(inside_folders) / 5 or len(inside_folders) % 5 == 0:
                    a = 0
                    for i in range((page - 1) * 5, (page - 1) * 5 + 5):
                        a += 1
                        win.blit(textInfo.render(inside_folders[i], True, (139, 155, 180)), (50, 50 + a * 50))
                        if 50 <= mouse_x <= 50 + textInfo.size(inside_folders[i])[0] and 50 + a * 50 <= mouse_y <= 50 + a * 50 + textInfo.size(inside_folders[i])[1]:
                            win.blit(textInfo.render(inside_folders[i], True, (58, 68, 102)), (50, 50 + a * 50))
                            if click[0] == 1:
                                world_name = inside_folders[i]
                                start_game()
                else:
                    a = 0
                    for i in range((page - 1) * 5, (page - 1) * 5 + len(inside_folders) % 5):
                        a += 1
                        win.blit(textInfo.render(inside_folders[i], True, (139, 155, 180)), (50, 50 + a * 50))
                        if 50 <= mouse_x <= 50 + textInfo.size(inside_folders[i])[0] and 50 + a * 50 <= mouse_y <= 50 + a * 50 + textInfo.size(inside_folders[i])[1]:
                            win.blit(textInfo.render(inside_folders[i], True, (58, 68, 102)), (50, 50 + a * 50))
                            if click[0] == 1:
                                world_name = inside_folders[i]
                                start_game()

        else:
            win.blit(textInfo.render(laungveges("Введите имя мира:", "Enter world name:"), True, (139, 155, 180)), ((Width - textInfo.size(laungveges("Введите имя мира:", "Enter world name:"))[0]) // 2, Height // 2 - 50))
            win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))

        if keys[pygame.K_ESCAPE]:
            menu()

        if pygame.mouse.get_pressed()[0] == 1:
            mouse_click_image = 1
        try:
            win.blit(mouse_click_images[mouse_click_image - 1], (mouse_x - 64, mouse_y - 64))
            if mouse_click_image == 5:
                mouse_click_image = None
            else:
                mouse_click_image += 1
        except TypeError:
            pass
            
        pygame.display.update()
        clock.tick(30)



def menu():
    
    global win, screenmode, mobs, num, mouse_click_image
    play_button = Button(Width / 2, Height / 2 - 150, PlayButton, PlayButton2, win)
    settings_button = Button(Width / 2, Height / 2, SettingsButton, SettingsButton2, win)
    change_a_character_button = Button(Width / 2, Height / 2 + 150, ChangeACharacterButton, ChangeACharacterButton2, win)
    while 1:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_F11]:
            if screenmode == "FULLSCREEN":
                win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)
                screenmode = "RESIZABLE"
                play_button.x = 500
                play_button.y = 200
                settings_button.x = 500
                settings_button.y = 350
                change_a_character_button.x = 500
                change_a_character_button.y = 500
            else:
                win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                screenmode = "FULLSCREEN"
                play_button.x = Width / 2
                play_button.y = Height / 2 - 150
                settings_button.x = Width / 2
                settings_button.y = Height / 2
                change_a_character_button.x = Width / 2
                change_a_character_button.y = Height / 2 + 150
            time.sleep(0.1)
        
        win.fill(color)
        win.blit(Screensaver2, (0, 0))
        if num == 30: num = 1
        num += 1
        play_button.main(worlds)
        settings_button.main(settings)
        change_a_character_button.main(change_a_character)

        if pygame.mouse.get_pressed()[0] == 1:
            mouse_click_image = 1
        try:
            win.blit(mouse_click_images[mouse_click_image - 1], (mouse_x - 64, mouse_y - 64))
            if mouse_click_image == 5:
                mouse_click_image = None
            else:
                mouse_click_image += 1
        except TypeError:
            pass
        
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    menu()