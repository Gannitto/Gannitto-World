import pygame
from Globals import path, Width, Height, Settings
from Cache import load

def load_textures(path_to_image: str, num: int, size: int, use_cache=True):
	return [load(f"{path_to_image}{i}.png", size, use_cache=use_cache) for i in range(num)]

wall_types = ("Wooden wall", "Brick wall", "Stone brick wall")
door_types = ("Wooden door",)
wall_images = {}

for wall_type in wall_types:
	wall_images[wall_type] = load_textures(f"{path}Images/Walls/{wall_type}/", 14, 256)

for door_type in door_types:
	wall_images[door_type] = (
		load(path + "Images/Walls/" + door_type + "/1.png", 256),
		load(path + "Images/Walls/" + door_type + "/2.png", 256),
		load(path + "Images/Walls/" + door_type + "/1 Open.png", 256),
		load(path + "Images/Walls/" + door_type + "/2 Open.png", 256)
	)

slime_types = ("Blue Slime", "Pink Slime")
slime_images = {}
red_slime_images = {}
color_surface = pygame.Surface((128, 128), pygame.SRCALPHA)
color_surface.fill((200, 0, 0, 200))
for slime_type in slime_types:
	slime_images[slime_type] = load_textures(f"{path}Images/Mobs/{slime_type} ", 4, 128)
	red_slime_images[slime_type] = load_textures(f"{path}Images/Mobs/{slime_type} ", 4, 128, use_cache=False)
	for frame in red_slime_images[slime_type]:
		frame.blit(color_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

spider_animation_images = {
		"Left": load(path + "Images/Mobs/Spider.png", 256),
		"Left attack": load(path + "Images/Mobs/Spider attack.png", 256),
		"Right": load(path + "Images/Mobs/Spider 2.png", 256),
		"Right attack": load(path + "Images/Mobs/Spider 2 attack.png", 256)
		}

color_surface = pygame.Surface((256, 256), pygame.SRCALPHA)
color_surface.fill((200, 0, 0, 150))

spider_red_animation_images = {
		"Left": load(path + "Images/Mobs/Spider.png", 256, use_cache=False),
		"Left attack": load(path + "Images/Mobs/Spider attack.png", 256, use_cache=False),
		"Right": load(path + "Images/Mobs/Spider 2.png", 256, use_cache=False),
		"Right attack": load(path + "Images/Mobs/Spider 2 attack.png", 256, use_cache=False)
		}

for frame in spider_red_animation_images.values():
	frame.blit(color_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

butterfly_images = load_textures(path + "Images/Mobs/Butterfly ", 3, 32)
wire_images = load_textures(path + "Images/Objects/Wire ", 11, 64)
random_box_images = load_textures(path + "Images/Objects/Random Box ", 4, 64)

Portal_1 = load(path + "Images/Objects/Portal 1.png", 128, 256)
Portal_2 = load(path + "Images/Objects/Portal 2.png", 128, 256)

Vending_machine_image = load(path + "Images/Objects/Vending machine.png", 304, 560)

arrow_down = load(path + "Images/DOWN.png", 64, convert_alpha=False)
arrow_left = load(path + "Images/LEFT.png", 64, convert_alpha=False)
arrow_right = load(path + "Images/RIGHT.png", 64, convert_alpha=False)
arrow_up = load(path + "Images/UP.png", 64, convert_alpha=False)

Heart = load(path + "Images/Heart.png", 32)
web_texture = load(path + "Images/Objects/Piece of web.png", 128)
explosion_texture = load(path + "Images/Objects/Explosion.png", 128)
cave_texture = load(path + "Images/Objects/Cave.png", 128)
drop_texture = load(path + "Images/Objects/Drop.png", 64)
no_file_texture = load(path + "Images/No-file texture.png", 64, convert_alpha=False)

bg_scale_factor = max(Width // 128, Height // 64)
Screensaver2 = load(path + "Images/Screensavers/Screensaver 2.png", Height * 128 // 64, Height, False)

farmland_images = (load(path + "Images/Objects/Farmland.png", 128),)
plant_types = ("Wheat", "Cucumber", "Tomato", "Corn", "Onion")
seed_types = {
		"Wheat seeds": "Wheat",
		"Cucumber seeds": "Cucumber",
		"Tomato seeds": "Tomato",
		"Corn seeds": "Corn",
		"Onion": "Onion"
		}

plant_images = {}
for plant_type in plant_types:
	plant_images[plant_type] = load_textures(f"{path}Images/Plants/{plant_type} ", 4, 128)

biomes = ("Desert", "Field", "Forest", "Swamp", "Taiga")
biome_textures = {}
for biome in biomes:
	biome_textures[biome] = load(path + f"Images/Biomes/{biome}.png", 256)

Backrooms_portal_images = load_textures(path + "Images/Objects/Backrooms portal ", 10, 256)

Inventory_slot = load(path + "Images/Slots/Inventory slot.png", 64).convert_alpha()
Changed_inventory_slot = load(path + "Images/Slots/Inventory slot 2.png", 64).convert_alpha()

Craft_list_inventory_slot = load(path + "Images/Slots/Craft list slot.png", 64).convert_alpha()
Changed_craft_list_inventory_slot = load(path + "Images/Slots/Craft list slot 2.png", 64).convert_alpha()

Object_inventory_slot = load(path + "Images/Slots/Object inventory slot 2.png", 64).convert_alpha()

Tool_inventory_slot = load(path + "Images/Slots/Tool inventory slot 2.png", 64).convert_alpha()

Split_items1 = load(path + "Images/Slots/Split items.png", 64).convert_alpha()
Split_items2 = load(path + "Images/Slots/Split items 2.png", 64).convert_alpha()

Compact_inventory1 = load(path + "Images/Slots/Compact inventory.png", 64).convert_alpha()
Compact_inventory2 = load(path + "Images/Slots/Compact inventory 2.png", 64).convert_alpha()

Craft_list_slot1 = load(path + "Images/Slots/Craft list slot.png", 64).convert_alpha()
Craft_list_slot2 = load(path + "Images/Slots/Craft list slot 2.png", 64).convert_alpha()

Game_menu_slot1 = load(path + "Images/Slots/Game menu slot.png", 64).convert_alpha()
Game_menu_slot2 = load(path + "Images/Slots/Game menu slot 2.png", 64).convert_alpha()

Menu_slot1 = load(path + "Images/Slots/Menu slot.png", 64).convert_alpha()
Menu_slot2 = load(path + "Images/Slots/Menu slot 2.png", 64).convert_alpha()

Multiplayer_slot1 = load(path + "Images/Slots/Multiplayer slot.png", 64).convert_alpha()
Multiplayer_slot2 = load(path + "Images/Slots/Multiplayer slot 2.png", 64).convert_alpha()

Close_slot1 = load(path + "Images/Slots/Close slot.png", 64).convert_alpha()
Close_slot2 = load(path + "Images/Slots/Close slot 2.png", 64).convert_alpha()

Reference_slot1 = load(path + "Images/Slots/Reference slot.png", 64).convert_alpha()
Reference_slot2 = load(path + "Images/Slots/Reference slot 2.png", 64).convert_alpha()

Open_inventory_slot = load(path + "Images/Slots/Open inventory slot.png", 64).convert_alpha()
Open_inventory_slot2 = load(path + "Images/Slots/Open inventory slot 2.png", 64).convert_alpha()

Inventory_slot.set_alpha(Settings["Display"][1])
Changed_inventory_slot.set_alpha(Settings["Display"][1])
Craft_list_inventory_slot.set_alpha(Settings["Display"][1])
Changed_craft_list_inventory_slot.set_alpha(Settings["Display"][1])
Object_inventory_slot.set_alpha(Settings["Display"][1])
Tool_inventory_slot.set_alpha(Settings["Display"][1])
Split_items1.set_alpha(Settings["Display"][1])
Split_items2.set_alpha(Settings["Display"][1])
Compact_inventory1.set_alpha(Settings["Display"][1])
Compact_inventory2.set_alpha(Settings["Display"][1])
Craft_list_slot1.set_alpha(Settings["Display"][1])
Craft_list_slot2.set_alpha(Settings["Display"][1])
Game_menu_slot1.set_alpha(Settings["Display"][1])
Game_menu_slot2.set_alpha(Settings["Display"][1])
Menu_slot1.set_alpha(Settings["Display"][1])
Menu_slot2.set_alpha(Settings["Display"][1])
Multiplayer_slot1.set_alpha(Settings["Display"][1])
Multiplayer_slot2.set_alpha(Settings["Display"][1])
Close_slot1.set_alpha(Settings["Display"][1])
Close_slot2.set_alpha(Settings["Display"][1])
Reference_slot1.set_alpha(Settings["Display"][1])
Reference_slot2.set_alpha(Settings["Display"][1])

select_images = {
	(512, 512): load(path + "Images/Select/512x512.png", 512),
	(256, 256): load(path + "Images/Select/256x256.png", 256),
	(128, 128): load(path + "Images/Select/128x128.png", 128),
	(64, 64): load(path + "Images/Select/64x64.png", 64)
}

