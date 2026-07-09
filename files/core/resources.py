import pygame
from Globals import path, Settings

pygame.display.set_icon(pygame.image.load(path + "Gannitto-World/files/Images/Icon.png"))
pygame.display.set_caption("Gannitto-World")

Hiro_down_run_1 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Down/1.png"), (256, 256))
Hiro_down_run_2 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Down/2.png"), (256, 256))
Hiro_down_run_3 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Down/3.png"), (256, 256))
Hiro_down_run_4 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Down/4.png"), (256, 256))
Hiro_down_run_5 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Down/5.png"), (256, 256))
Hiro_down_run_6 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Down/6.png"), (256, 256))

Hiro_down_left = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Down-left/1.png"), (256, 256))
Hiro_down_right = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Down-right/1.png"), (256, 256))

Hiro_left_run_1 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Left/1.png"), (256, 256))
Hiro_left_run_2 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Left/2.png"), (256, 256))
Hiro_left_run_3 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Left/3.png"), (256, 256))
Hiro_left_run_4 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Left/4.png"), (256, 256))
Hiro_left_run_5 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Left/5.png"), (256, 256))
Hiro_left_run_6 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Left/6.png"), (256, 256))

Hiro_right_run_1 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Right/1.png"), (256, 256))
Hiro_right_run_2 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Right/2.png"), (256, 256))
Hiro_right_run_3 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Right/3.png"), (256, 256))
Hiro_right_run_4 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Right/4.png"), (256, 256))
Hiro_right_run_5 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Right/5.png"), (256, 256))
Hiro_right_run_6 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Right/6.png"), (256, 256))

Hiro_up_run_1 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Up/1.png"), (256, 256))
Hiro_up_run_2 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Up/2.png"), (256, 256))
Hiro_up_run_3 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Up/3.png"), (256, 256))
Hiro_up_run_4 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Up/4.png"), (256, 256))
Hiro_up_run_5 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Up/5.png"), (256, 256))
Hiro_up_run_6 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Up/6.png"), (256, 256))

Hiro_up_left = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Up-left/1.png"), (256, 256))

Hiro_up_right_run_1 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Players/Hiro/Normal/Up-right/1.png"), (256, 256))


arrow_down = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/DOWN.png"), (64, 64))
arrow_left = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/LEFT.png"), (64, 64))
arrow_right = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/RIGHT.png"), (64, 64))
arrow_up = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/UP.png"), (64, 64))


Inventory_slot = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Inventory slot.png"), (64, 64))
Changed_inventory_slot = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Inventory slot 2.png"), (64, 64))

Craft_list_inventory_slot = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Craft list slot.png"), (64, 64))
Changed_craft_list_inventory_slot = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Craft list slot 2.png"), (64, 64))

Object_inventory_slot = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Object inventory slot 2.png"), (64, 64))

Tool_inventory_slot = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Tool inventory slot 2.png"), (64, 64))

Split_items1 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Split items.png"), (64, 64))
Split_items2 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Split items 2.png"), (64, 64))

Compact_inventory1 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Compact inventory.png"), (64, 64))
Compact_inventory2 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Compact inventory 2.png"), (64, 64))

Craft_list_slot1 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Craft list slot.png"), (64, 64))
Craft_list_slot2 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Craft list slot 2.png"), (64, 64))

Game_menu_slot1 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Game menu slot.png"), (64, 64))
Game_menu_slot2 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Game menu slot 2.png"), (64, 64))

Menu_slot1 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Menu slot.png"), (64, 64))
Menu_slot2 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Menu slot 2.png"), (64, 64))

Multyplayer_slot1 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Multyplayer slot.png"), (64, 64))
Multyplayer_slot2 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Multyplayer slot 2.png"), (64, 64))

Close_slot1 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Close slot.png"), (64, 64))
Close_slot2 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Close slot 2.png"), (64, 64))

Reference_slot1 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Reference slot.png"), (64, 64))
Reference_slot2 = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Slots/Reference slot 2.png"), (64, 64))
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
Multyplayer_slot1.set_alpha(Settings["Display"][1])
Multyplayer_slot2.set_alpha(Settings["Display"][1])
Close_slot1.set_alpha(Settings["Display"][1])
Close_slot2.set_alpha(Settings["Display"][1])
Reference_slot1.set_alpha(Settings["Display"][1])
Reference_slot2.set_alpha(Settings["Display"][1])

Portal_1 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Portal 1.png")
Portal_1 = pygame.transform.scale(Portal_1, (128, 256))
Portal_2 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Portal 2.png")
Portal_2 = pygame.transform.scale(Portal_2, (128, 256))

Vending_machine_image = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Objects/Vending machine.png"), (304, 560))

Wire_1 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Wire 1.png")
Wire_1 = pygame.transform.scale(Wire_1, (64, 64))
Wire_2 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Wire 2.png")
Wire_2 = pygame.transform.scale(Wire_2, (64, 64))
Wire_3 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Wire 3.png")
Wire_3 = pygame.transform.scale(Wire_3, (64, 64))
Wire_4 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Wire 4.png")
Wire_4 = pygame.transform.scale(Wire_4, (64, 64))
Wire_5 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Wire 5.png")
Wire_5 = pygame.transform.scale(Wire_5, (64, 64))
Wire_6 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Wire 6.png")
Wire_6 = pygame.transform.scale(Wire_6, (64, 64))
Wire_7 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Wire 7.png")
Wire_7 = pygame.transform.scale(Wire_7, (64, 64))
Wire_8 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Wire 8.png")
Wire_8 = pygame.transform.scale(Wire_8, (64, 64))
Wire_9 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Wire 9.png")
Wire_9 = pygame.transform.scale(Wire_9, (64, 64))
Wire_10 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Wire 10.png")
Wire_10 = pygame.transform.scale(Wire_10, (64, 64))
Wire_11 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Wire 11.png")
Wire_11 = pygame.transform.scale(Wire_11, (64, 64))

Random_box_1 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Random Box 1.png")
Random_box_1 = pygame.transform.scale(Random_box_1, (64, 64))
Random_box_2 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Random Box 2.png")
Random_box_2 = pygame.transform.scale(Random_box_2, (64, 64))
Random_box_3 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Random Box 3.png")
Random_box_3 = pygame.transform.scale(Random_box_3, (64, 64))
Random_box_4 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Random Box 4.png")
Random_box_4 = pygame.transform.scale(Random_box_4, (64, 64))

Slime1 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Blue Slime 1.png")
Slime1 = pygame.transform.scale(Slime1, (128, 128))
Slime1_2 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Blue Slime 2.png")
Slime1_2 = pygame.transform.scale(Slime1_2, (128, 128))
Slime1_3 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Blue Slime 3.png")
Slime1_3 = pygame.transform.scale(Slime1_3, (128, 128))
Slime1_4 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Blue Slime 4.png")
Slime1_4 = pygame.transform.scale(Slime1_4, (128, 128))
Slime2 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Pink Slime 1.png")
Slime2 = pygame.transform.scale(Slime2, (128, 128))
Slime2_2 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Pink Slime 2.png")
Slime2_2 = pygame.transform.scale(Slime2_2, (128, 128))
Slime2_3 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Pink Slime 3.png")
Slime2_3 = pygame.transform.scale(Slime2_3, (128, 128))
Slime2_4 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Pink Slime 4.png")
Slime2_4 = pygame.transform.scale(Slime2_4, (128, 128))

Hiro = Hiro_down_run_1




SLIME_TYPES = {
	1: [Slime1, Slime1_2, Slime1_3, Slime1_4],
	2: [Slime2, Slime2_2, Slime2_3, Slime2_4]
}

Butterfly1 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Butterfly 1 1.png")
Butterfly1 = pygame.transform.scale(Butterfly1, (32, 32))
Butterfly1_2 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Butterfly 1 2.png")
Butterfly1_2 = pygame.transform.scale(Butterfly1_2, (32, 32))
Butterfly1_3 = pygame.image.load(path + "Gannitto-World/files/Images/Objects/Butterfly 1 3.png")
Butterfly1_3 = pygame.transform.scale(Butterfly1_3, (32, 32))

Bacteria_walk_left = (

	pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Objects/Bacteria 1.png"), (256, 512)),
	pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Objects/Bacteria 2.png"), (256, 512)),
	pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Objects/Bacteria 3.png"), (256, 512)),
	pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Objects/Bacteria 4.png"), (256, 512)),
	pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Objects/Bacteria 5.png"), (256, 512)),
	pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Objects/Bacteria 6.png"), (256, 512))

	)

Screensaver2 = pygame.image.load(path + "Gannitto-World/files/Images/Screensavers/Screensaver 2.png")


Heart = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Heart.png"), (32, 32))

textures = {

	"Forest": pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Bioms/Forest.png"), (256, 256)),
	"Desert": pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Bioms/Desert.png"), (256, 256)),
	"Field": pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Bioms/Field.png"), (256, 256)),
	"Taiga": pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Bioms/Taiga.png"), (256, 256)),
	"Swamp": pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Bioms/Swamp.png"), (256, 256)),
	"Backrooms 0": pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Bioms/Backrooms 0.png"), (256, 256)),
	"Backrooms 0.2": pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Bioms/Backrooms 0.2.png"), (256, 256)),
	"Backrooms 1": pygame.transform.scale(pygame.Surface((256, 256)), (256, 256)),

	}

Backrooms_portal_images = (
	pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Objects/Backrooms portal 1.png"), (256, 256)),
	pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Objects/Backrooms portal 2.png"), (256, 256)),
	pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Objects/Backrooms portal 3.png"), (256, 256)),
	pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Objects/Backrooms portal 4.png"), (256, 256)),
	pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Objects/Backrooms portal 5.png"), (256, 256)),
	pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Objects/Backrooms portal 6.png"), (256, 256)),
	pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Objects/Backrooms portal 7.png"), (256, 256)),
	pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Objects/Backrooms portal 8.png"), (256, 256)),
	pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Objects/Backrooms portal 9.png"), (256, 256)),
	pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Objects/Backrooms portal 10.png"), (256, 256))
)

mouse_click_images = (
	 pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Mouse click 1.png"), (128, 128)),
	 pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Mouse click 2.png"), (128, 128)),
	 pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Mouse click 3.png"), (128, 128)),
	 pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Mouse click 4.png"), (128, 128)),
	 pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Mouse click 5.png"), (128, 128))
	 )

no_file_texture = pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/No-file texture.png"), (64, 64))

Button_click = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Button Pressed.mp3")
Stone_breaking1 = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Stone breaking 1.mp3")
Stone_breaking2 = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Stone breaking 2.mp3")
Grass_walking1 = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Grass walking 1.mp3")
Grass_walking2 = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Grass walking 2.mp3")
Grass_walking3 = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Grass walking 3.mp3")
Snow_walking1 = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Snow walking 1.mp3")
Snow_walking2 = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Snow walking 2.mp3")
Snow_walking3 = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Snow walking 3.mp3")
Sand_walking1 = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Sand walking 1.mp3")
Sand_walking2 = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Sand walking 2.mp3")
Sand_walking3 = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Sand walking 3.mp3")
Swamp_walking1 = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Swamp walking 1.mp3")
Swamp_walking2 = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Swamp walking 2.mp3")
Swamp_walking3 = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Swamp walking 3.mp3")
Cave_walking1 = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Cave walking 1.mp3")
Cave_walking2 = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Cave walking 2.mp3")
Cave_walking3 = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Cave walking 3.mp3")
Backrooms_lamps = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Backrooms/1.mp3")
Backrooms_rand_sound_1 = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Backrooms/Random Sounds/1.mp3")
Pick_an_item = pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Pick an item.mp3")

music_channel = pygame.mixer.Channel(1)
music_channel.set_volume(Settings["Sound"][0], Settings["Sound"][0])
