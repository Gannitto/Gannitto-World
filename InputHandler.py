import pygame
import sys
import time
from Functions import create_throw_particle, win_darken
from Globals import hot_keys, win, Width, Height, Settings
from Classes import Object, Particle

class InputHandler:
	def __init__(self, game, save, music_channel):
		self.game = game
		self.save = save
		self.music_channel = music_channel

	def handle_events(self, events):

		for event in events:
			
			if event.type == pygame.QUIT:
				self.game.statistics[1] += (time.time() - self.game.start_time) / 3600
				if self.game.multiplayer:
					self.game.net.disconnect()
				self.save()
				sys.exit()

			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					self.game.release = True
			
			elif event.type == pygame.MOUSEWHEEL and not any((self.game.item_settings_open, self.game.ron.window[0], self.game.in_motherboard)):
				if self.game.craft_list_open:
					self.game.craft_list_offset = max((min(self.game.craft_list_offset + event.y * Settings["Game"][2], 0)), self.game.craft_list_max_offset)
				else:
					self.game.inventory.changed_slot -= event.y
					if self.game.inventory.changed_slot > 9: self.game.inventory.changed_slot = 0
					if self.game.inventory.changed_slot < 0: self.game.inventory.changed_slot = 9

			if event.type == pygame.KEYUP:
				if self.game.chat_open:
					if event.key == hot_keys["Close"]:
						self.game.chat_open = False
						self.game.input_system.stop_input()
				else:
					if event.key == hot_keys["Show keys"]:
						self.game.alt_pressed = not self.game.alt_pressed
					if event.key == hot_keys["Use item"]:
						use_item_pressed = True
					if event.key == hot_keys["Multiplayer menu"]:
						self.game.multiplayer_menu_open = True
					if event.key == hot_keys["Set Ron home"]:
						self.game.ron.home = [self.game.player.x, self.game.player.y]
					if event.key == hot_keys["Menu"]:
						self.game.menu_open = not self.game.menu_open
					if event.key == hot_keys["Open chat"]:
						self.game.chat_open = True
						self.game.input_system.start_input("Chat", 20, Height - 40, (255, 255, 255))
					if event.key == hot_keys["Execute command"]:
						self.game.chat_open = True
						self.game.input_system.start_input("Chat", 20, Height - 40, (255, 255, 255), input_text="/")

					if event.key == hot_keys["Close"]:
	
						if self.game.item_settings_open:
							self.game.item_settings_open = False
						elif self.game.ron.window[0]:
							self.game.ron.window[0] = False
						elif self.game.in_motherboard is not None:
							self.game.in_motherboard = None
						elif self.game.craft_list_open:
							self.game.craft_list_open = False
						elif self.game.inventory_open:
							self.game.inventory_open = False
						else:
							self.music_channel.stop()
							self.game.statistics[1] += (time.time() - self.game.start_time) / 3600
							self.save()
							self.game.world.chunk_manager.chunks = {}
							self.game.world.mobs = []
							self.game.effects.effects = []
							particles = []
							self.game.chat = []
							self.game.main_chat = []
							self.game.chat_tick = 0
							self.game.inventory.whole_inventory = [None] * 30
							self.game.world_name = None
							if self.game.multiplayer:
								self.game.net.disconnect()
							win_darken(win)
							self.game.does_lighten = False
							return self.game.main_menu.main_menu

					if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0, ):
						last_changed_slot = self.game.inventory.changed_slot
						self.game.inventory.changed_slot = int(event.unicode) - 1 + 10 * (event.key == pygame.K_0)
						self.game.player.changed_item = self.game.inventory.whole_inventory[self.game.inventory.changed_slot]
						if self.game.player.changed_item is not None:
							self.game.player.changed_item = self.game.player.changed_item.name

					if event.key == hot_keys["Help"]:
						self.music_channel.stop()
						self.game.statistics[1] += (time.time() - self.game.start_time) / 3600
						self.save(False)
						return self.game.settings_menu.help

					if event.key == hot_keys["Inventory"]:
						self.game.inventory_open = not self.game.inventory_open
						if not self.game.inventory_open:
							if self.game.inventory.craft_items_list != [None] * 7:
								for item_index, item in enumerate(self.game.inventory.craft_items_list):
									if item is not None:
										self.game.inventory.increate(item, self.game.inventory.craft_amounts_list[item_index])
							self.game.inventory.craft_items_list = [None] * 7
							self.game.inventory.craft_amounts_list = [None] * 7
							self.game.inventory.craft_images_list = [None] * 7

					if event.key == hot_keys["Throw away the item"] and self.game.inventory.whole_inventory[self.game.inventory.changed_slot] is not None:
						
						if self.game.Backrooms.InBackrooms:
							self.game.world.backrooms_objects.append(Object(self.game.inventory.whole_inventory[self.game.inventory.changed_slot].name, self.game.player.x, self.game.player.y, "Images/Items/" + self.game.inventory.whole_inventory[self.game.inventory.changed_slot].name + ".png", special_flags="Item"))
						else:
							self.game.world.particles.append(create_throw_particle(Object, Particle, self.game.player, self.game.world, self.game, self.game.inventory.whole_inventory[self.game.inventory.changed_slot].image, self.game.inventory.whole_inventory[self.game.inventory.changed_slot].name))
						
						self.game.inventory.reduce(self.game.inventory.changed_slot)

