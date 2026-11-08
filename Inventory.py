import pygame
import os
import json
import math
from itertools import product
from Assets import Inventory_slot, Changed_inventory_slot, Object_inventory_slot, Tool_inventory_slot, Split_items1, Split_items2, Compact_inventory1, Compact_inventory2, Craft_list_inventory_slot, Changed_craft_list_inventory_slot, Heart
from Functions import win_fill, draw_key, text, get_text_height
from Globals import path, win, Settings, Width, Height, textInfo, bigTextInfo, text_color
from Translator import t

pygame.init()
types = ("Just an item", "Tool", "Food", "Drink", "Mechanism", "Flower", "Seed", "Build")

class Resource:

	"""Предмет с определёнными характеристиками"""

	def __init__(self, name: str="", item_type: str="Just an item", info=["", ""], purpose=["", ""], special_info=None, max_stack=99, image_path=""):

		self.name = name
		self.info = info
		self.purpose = purpose
		self.type = item_type
		self.amount = 0
		self.settings = []
		if image_path == "":
			self.image_path = path + "Images/Items/" + name + ".png"
		else:
			self.image_path = image_path
		self.image = pygame.transform.scale(pygame.image.load(self.image_path), (64, 64))
		self.special_info = special_info
		self.max_stack = max_stack
		
	def __getstate__(self):
		
		state = self.__dict__.copy()
		del state["image"]
		return state

	def __setstate__(self, state):

		self.__dict__.update(state)
		self.image = pygame.transform.scale(pygame.image.load(self.image_path), (64, 64))

class Recipe:

	def __init__(self, ingredients: list, ingredients_amounts: list, result: str, result_amount: str, need_object: str = None, need_tool: str = None):

		for i in range(7 - len(ingredients)):
			ingredients.append(None)
			ingredients_amounts.append(None)

		self.ingredients = ingredients
		self.ingredients_amounts = ingredients_amounts
		self.result = result
		self.result_amount = result_amount
		self.need_object = need_object
		self.need_tool = need_tool

	def get_result(self, whole_inventory, need_object, craft_items_list, craft_amounts_list):

		"""Проверяет, может ли быть какой-то результат от данных ингридиентов"""

		if craft_items_list == self.ingredients and craft_amounts_list == self.ingredients_amounts:
			b = None
			c = True
			d = None

			if self.need_object is not None:
				if self.need_object == need_object:
					b = self.need_object
				else:
					return None
			
			if self.need_tool is not None:
				c = False
				for cell in whole_inventory:
					if cell is not None and cell.name == self.need_tool:
						c = True
						d = cell.name
			if c:
				return [self.result, self.result_amount, b, d]
			else:
				return None
		else:
			return None

class Inventory:

	def __init__(self, game):

		self.resources = {}
		self.game = game

		if os.path.exists(path + "Items.json"):
			with open(path + "Items.json", "r", encoding="utf-8") as f:
				for item_type, items in json.load(f).items():
					for name, item in items.items():
						self.resources[name] = Resource(name=name, item_type=item_type, **item)
		
		self.recipes = [
			
		   Recipe(["Stick", "Stone"], [2, 3], "Stone pickaxe", 1),
		   Recipe(["Stick", "Stone"], [1, 2], "Stone hammer", 1),
		   Recipe(["Stick", "Stone"], [3, 1], "Stone spear", 1),
		   Recipe(["Stick", "Stone"], [2, 1], "Stone hoe", 1),
		   Recipe(["Wooden"], [10], "Table", 1),
		   Recipe(["Dark wooden"], [10], "Table", 1),
		   Recipe(["Birch wooden"], [10], "Table", 1),
		   Recipe(["Stone"], [20], "Furnace", 1),
		   Recipe(["Table", "Iron ingot"], [1, 1], "Wall table", 1),
		   Recipe(["Clay"], [1], "Brick", 1, "Furnace"),
		   Recipe(["Stone"], [1], "Stone brick", 1),
		   Recipe(["Wooden"], [3], "Wooden wall", 1, "Wall table"),
		   Recipe(["Brick"], [3], "Brick wall", 1, "Wall table"),
		   Recipe(["Stone brick"], [3], "Stone brick wall", 1, "Wall table"),
		   Recipe(["Iron ore"], [1], "Iron ingot", 1, "Furnace", "Wooden"),
		   Recipe(["Iron ore"], [1], "Iron ingot", 1, "Furnace", "Dark wooden"),
		   Recipe(["Iron ore"], [1], "Iron ingot", 1, "Furnace", "Birch wooden"),
		   Recipe(["Gold ore", "Wooden"], [1, 1], "Gold ingot", 1, "Furnace"),
		   Recipe(["Gold ore", "Dark wooden"], [1, 1], "Gold ingot", 1, "Furnace"),
		   Recipe(["Gold ore", "Birch wooden"], [1, 1], "Gold ingot", 1, "Furnace"),
		   Recipe(["Iron ingot"], [3], "Bucket", 1, "Table"),
		   Recipe(["Stone", "Stick"], [1, 1], "Lever", 1),
		   Recipe(["Brick"], [2], "Pot", 1, "Furnace"),
		   Recipe(["Stick", "Thread"], [3, 2], "Bow", 1),
		   Recipe(["Stick", "Iron ingot"], [1, 1], "Arrow", 10),
		   Recipe(["Powder", "Iron ingot"], [3, 1], "Grenade", 1, "Table"),
		   Recipe(["Cucumber"], [1], "Cucumber seeds", 3),
		   Recipe(["Tomato"], [1], "Tomato seeds", 3),
		   Recipe(["Wheat"], [1], "Wheat seeds", 3),
		   Recipe(["Corn"], [1], "Corn seeds", 3)
		   
		]
		
		self.inventory_panel = [None] * 10
		self.whole_inventory = [None] * 30
		self.start_cell = None
		self.end_cell = None
		self.end_cell_inventory = 0
		self.Split_items = False
		self.last_changed_item = None
		self.craft_items_list = [None] * 7
		self.craft_amounts_list = [None] * 7
		self.craft_images_list = [None] * 7
		self.changed_slot = 0
		self.slot_animations = [[False, 15] for _ in range(30)]   # Используется для анимации при наведении на слот
		self.special_slot_animations = {"Craft list slot": [False, 0.6], "Game menu slot": [False, 0.6], "Menu slot": [False, 0.6], "Multiplayer slot": [False, 0.6], "Reference slot": [False, 0.6], "Close slot": [False, 0.6], "Split items slot": [False, 0.6], "Compact inventory slot": [False, 0.6]}   # Используется для анимации при наведении на слот, который выполняет какое-либо действие
	
	def increate(self, name: str, amount: int=1):
		
		"""Выдаёт предмет в инвентарь"""
		
		try:
			amount = int(amount)

			resource_template = self.resources[name]
			remaining = amount
			
			# Сначала пытаемся добавить в существующие стеки
			for item in self.whole_inventory:
				if item is not None and item.name == name:
					space = item.max_stack - item.amount
					if space > 0:
						add = min(remaining, space)
						item.amount += add
						remaining -= add
						if remaining == 0:
							return
			
			# Если остались предметы, создаем новые слоты
			while remaining > 0:
				# Ищем пустой слот
				empty_slot = None
				for i, slot in enumerate(self.whole_inventory):
					if slot is None:
						empty_slot = i
						break
				
				if empty_slot is None:
					# Нет свободных слотов
					break
				
				# Создаем новый предмет
				new_item = Resource(
					resource_template.name,
					resource_template.type,
					resource_template.info,
					resource_template.purpose,
					resource_template.special_info,
					resource_template.max_stack,
					resource_template.image_path
				)
				
				add = min(remaining, new_item.max_stack)
				new_item.amount = add
				self.whole_inventory[empty_slot] = new_item
				remaining -= add
		except KeyError:
			self.game.chat_message(t("<<< Error increasing: item not found >>>"))
	
	def compact_inventory(self):
		"""Компактизирует инвентарь: объединяет одинаковые предметы и убирает пустые слоты"""
		
		# Словарь для группировки предметов по имени
		items_dict = {}
		
		for item in self.whole_inventory:
			if item is not None:
				if item.name not in items_dict:
					items_dict[item.name] = []
				items_dict[item.name].append(item)
		
		self.whole_inventory = [None] * len(self.whole_inventory)
		current_index = 0
		
		# Предметы объединяются, потом добавляются обратно
		for name, items in items_dict.items():
			total_amount = sum(item.amount for item in items)
			template = items[0]  # Первый предмет берётся как шаблон
			
			# Разбиваем на стеки по максимальному размеру
			while total_amount > 0:
				if current_index >= len(self.whole_inventory):
					# Инвентарь переполнен
					break
				
				stack_size = min(total_amount, template.max_stack)
				
				new_item = Resource(
					template.name,
					template.info,
					template.purpose,
					template.type,
					template.special_info,
					template.max_stack,
					template.image_path
				)
				new_item.amount = stack_size
				
				self.whole_inventory[current_index] = new_item
				current_index += 1
				total_amount -= stack_size

	def draw_whole(self):
		
		"""Рисует весь инвентарь"""

		cell_x = cell_y = 10
		for cell in self.whole_inventory:
			if cell is not None:
				win.blit(cell.image, (cell_x, cell_y))
				if cell.amount > 1:
					win.blit(textInfo.render(str(cell.amount), True, (0, 150, 0)), (cell_x + 10, cell_y + 42))
			cell_x += 80
			if cell_x == 810:
				cell_x = 10
				cell_y += 80
		cell_x = 170
		win.blit(Inventory_slot, (170, 250))
		i = -1
		
		for cell in self.craft_images_list:
			i += 1
			if cell is None:
				break
			else:
				win.blit(cell, (cell_x, 250))
				if self.craft_amounts_list != [None] * 7 and self.craft_amounts_list[i] > 1:
					win.blit(textInfo.render(str(self.craft_amounts_list[i]), True, (0, 150, 0)), (cell_x + 10, 292))
				cell_x += 80
				win.blit(Inventory_slot, (cell_x, 250))
	
	def draw_panel(self):
		
		"""Draws the top panel"""

		i = 0
		cell_x = cell_y = 10
		for cell in self.whole_inventory:
			i += 1
			if i == 11:
				break
			if cell is not None:
				win.blit(cell.image, (cell_x, cell_y))
				if cell.amount > 1:
					win.blit(textInfo.render(str(cell.amount), True, (0, 150, 0)), (cell_x + 10, cell_y + 42))
			cell_x += 80
	
	def set_start_cell(self, mouse_x: int, mouse_y: int):

		for yy in range(0, 3):
			for xx in range(0, 10):
				cell_x = 10 + xx * 80
				cell_y = 10 + yy * 80
				if cell_x <= mouse_x <= cell_x + 64 and cell_y <= mouse_y <= cell_y + 64:
					self.start_cell = yy * 10 + xx
					return

		self.start_cell = None
	
	def set_end_cell(self, mouse_x: int, mouse_y: int):
		
		if self.start_cell is None:
			return None

		for yy in range(0, 3):
			for xx in range(0, 10):
				cell_x = 10 + xx * 80
				cell_y = 10 + yy * 80
				if cell_x <= mouse_x <= cell_x + 64 and cell_y <= mouse_y <= cell_y + 64:
					self.end_cell = yy * 10 + xx
					self.end_cell_inventory = 0
		
		for X in range(2, 9):
			cell_x = 10 + X * 80
			if cell_x <= mouse_x <= cell_x + 64 and 250 <= mouse_y <= 314:
				self.end_cell = X - 2
				self.end_cell_inventory = 1
		return self.swap_cells()
	
	def swap_cells(self):
		
		"""Перемещает слоты в инвентаре"""
		
		if self.whole_inventory[self.start_cell] is not None:
			if self.end_cell_inventory == 0:
				# Обычная замена слотов в инвентаре
				if self.whole_inventory[self.end_cell] is not None and self.whole_inventory[self.start_cell].name == self.whole_inventory[self.end_cell].name:
					# Объединяем стеки
					space = self.whole_inventory[self.end_cell].max_stack - self.whole_inventory[self.end_cell].amount
					if space > 0:
						move_amount = min(self.whole_inventory[self.start_cell].amount, space)
						self.whole_inventory[self.end_cell].amount += move_amount
						self.whole_inventory[self.start_cell].amount -= move_amount
						if self.whole_inventory[self.start_cell].amount == 0:
							self.whole_inventory[self.start_cell] = None
				else:
					
					if self.Split_items:
						if self.whole_inventory[self.start_cell].amount % 2 == 0:
							self.whole_inventory[self.start_cell].amount //= 2
							new_item = Resource(
								self.whole_inventory[self.start_cell].name,
								self.whole_inventory[self.start_cell].info,
								self.whole_inventory[self.start_cell].purpose,
								self.whole_inventory[self.start_cell].type,
								self.whole_inventory[self.start_cell].special_info,
								self.whole_inventory[self.start_cell].max_stack,
								self.whole_inventory[self.start_cell].image_path
							)
							self.whole_inventory[self.end_cell] = new_item
							self.whole_inventory[self.end_cell].amount = self.whole_inventory[self.start_cell].amount
					else:
						# Обычный обмен
						temp = self.whole_inventory[self.end_cell]
						self.whole_inventory[self.end_cell] = self.whole_inventory[self.start_cell]
						self.whole_inventory[self.start_cell] = temp
			
			elif self.end_cell_inventory == 1:
				# Перемещение в крафт
				temp = self.craft_items_list[self.end_cell]
				self.craft_items_list[self.end_cell] = self.whole_inventory[self.start_cell].name
				self.craft_amounts_list[self.end_cell] = self.whole_inventory[self.start_cell].amount
				self.craft_images_list[self.end_cell] = self.whole_inventory[self.start_cell].image
				self.whole_inventory[self.start_cell] = None
				
				if temp is not None:
					# Возвращаем предмет из крафта
					self.increate(temp, 1)
		
		self.start_cell = 0
		self.end_cell = 0
		return self.craft_items_list, self.craft_amounts_list, self.craft_images_list

	def check_recipies(self, need_object):
		for recipie in self.recipes:
			result = recipie.get_result(self.whole_inventory, need_object, self.craft_items_list, self.craft_amounts_list)
			if result is not None:
				return result
		return None

	def get_start_items(self):

		"""Выдаёт в инвентарь начальные предметы"""

		self.whole_inventory = [None] * 30
		self.increate("Bow", 1)
		self.increate("Arrow", 99)

	def reduce(self, slot: int, amount: int = 1):
		if self.whole_inventory[slot].amount - amount > 0:
			self.whole_inventory[slot].amount -= amount
		elif self.whole_inventory[slot].amount - amount == 0:
			self.whole_inventory[slot] = None

	def check_new_items(self):
		new_item = False
		if self.whole_inventory[self.changed_slot] is None:
			new_changed_item = None
		else:
			new_changed_item = self.whole_inventory[self.changed_slot].name
		if self.last_changed_item != new_changed_item:
			new_item = True
			self.last_changed_item = new_changed_item
		return new_item

	def draw_inventory(self, mouse_x, mouse_y, dt, need_object):

		if self.game.inventory_open:

			if 10 < mouse_x < 794 and 10 < mouse_y < 314:
				mouse_object = t("Inventory (I)")

			# Механика анимации слотов
			if Settings["Display"][5]:
				for yy, xx in product(range(0, 3), range(0, 10)):
					
					cell_x = 10 + xx * 80
					cell_y = 10 + yy * 80
				
					if cell_x <= mouse_x <= cell_x + 64 and cell_y <= mouse_y <= cell_y + 64:
						if self.slot_animations[yy * 10 + xx][0]:
							if self.slot_animations[yy * 10 + xx][1] < dt * 150:
								self.slot_animations[yy * 10 + xx][1] += dt * 30
								self.slot_animations[yy * 10 + xx][2] -= dt * 90
								self.slot_animations[yy * 10 + xx][2] = abs(self.slot_animations[yy * 10 + xx][2])
						else:
							self.slot_animations[yy * 10 + xx] = [True, 0, 10]
						
					elif self.slot_animations[yy * 10 + xx][0]:
						self.slot_animations[yy * 10 + xx][0] = False
						self.slot_animations[yy * 10 + xx][1] = 0
					elif self.slot_animations[yy * 10 + xx][1] < dt * 250:
						self.slot_animations[yy * 10 + xx][1] += dt * 30
			slot_x = 10
			slot_y = 10

			for slot in range(30):
				
				if slot == self.changed_slot: win.blit(Changed_inventory_slot, (slot_x, slot_y))
				else:
					
					if self.slot_animations[slot][0]:
						try:win.blit(pygame.transform.scale(Inventory_slot, (64 - self.slot_animations[slot][2], 64 - self.slot_animations[slot][2])), (slot_x, slot_y))
						except: win.blit(pygame.transform.scale(Inventory_slot, (64, 64)), (slot_x, slot_y))

					else:
						win.blit(pygame.transform.scale(Inventory_slot, (64, 64)), (slot_x, slot_y))
						
				slot_x += 80
				if slot_x == 810:
					slot_x = 10
					slot_y += 80
			
			win.blit(Object_inventory_slot, (10, 250))
			
			if need_object is not None:
				win.blit(self.resources[need_object].image, (10, 250))

			win.blit(Tool_inventory_slot, (90, 250))

			item_to_get = self.check_recipies(need_object)
			
			if item_to_get is not None:

				win.blit(Changed_inventory_slot, (730, 250))
				win.blit(self.resources[item_to_get[0]].image, (730, 250))

				if item_to_get[2] is not None:
					win.blit(self.resources[item_to_get[2]].image, (10, 250))
				if item_to_get[3] is not None:
					win.blit(self.resources[item_to_get[3]].image, (90, 250))
				if 730 <= mouse_x <= 810 and 250 <= mouse_y <= 330 and self.game.release:
					self.increate(item_to_get[0], item_to_get[1])
					self.craft_items_list = [None] * 7
					self.craft_amounts_list = [None] * 7
					self.craft_images_list = [None] * 7
			
			# Разделение предметов
			if 810 <= mouse_x <= 874 and 10 <= mouse_y <= 74:
				if self.special_slot_animations["Split items slot"][0]:
					if self.special_slot_animations["Split items slot"][1] < dt * 150:
						self.special_slot_animations["Split items slot"][1] += dt * 30
						self.special_slot_animations["Split items slot"][2] -= dt * 90
						self.special_slot_animations["Split items slot"][2] = abs(self.special_slot_animations["Split items slot"][2])
				else:
					self.special_slot_animations["Split items slot"] = [True, 0, 10]
				
				if self.game.release:
					self.Split_items = not self.Split_items
				
			elif self.special_slot_animations["Split items slot"][0]:
				self.special_slot_animations["Split items slot"][0] = False
				self.special_slot_animations["Split items slot"][1] = 0
			elif self.special_slot_animations["Split items slot"][1] < dt * 250:
				self.special_slot_animations["Split items slot"][1] += dt * 30

			if self.special_slot_animations["Split items slot"][0] or self.Split_items:
				try:
					if Settings["Display"][5]: win.blit(pygame.transform.scale(Split_items2, (64 - self.special_slot_animations["Split items slot"][2], 64 - self.special_slot_animations["Split items slot"][2])), (810, 10))
					else: win.blit(pygame.transform.scale(Split_items2, (64, 64)), (810, 10))
				except: win.blit(pygame.transform.scale(Split_items2, (64, 64)), (810, 10))
				mouse_object = t("Split items")
			
			else:
				win.blit(pygame.transform.scale(Split_items1, (64, 64)), (810, 10))
			
			# Сжатие инвентаря
			
			if 810 <= mouse_x <= 874 and 170 <= mouse_y <= 234:
				if self.special_slot_animations["Compact inventory slot"][0]:
					if self.special_slot_animations["Compact inventory slot"][1] < dt * 150:
						self.special_slot_animations["Compact inventory slot"][1] += dt * 30
						self.special_slot_animations["Compact inventory slot"][2] -= dt * 90
						self.special_slot_animations["Compact inventory slot"][2] = abs(self.special_slot_animations["Compact inventory slot"][2])
				else:
					self.special_slot_animations["Compact inventory slot"] = [True, 0, 10]
				
				if self.game.release:
					self.compact_inventory()
				
			elif self.special_slot_animations["Compact inventory slot"][0]:
				self.special_slot_animations["Compact inventory slot"][0] = False
				self.special_slot_animations["Compact inventory slot"][1] = 0
			elif self.special_slot_animations["Compact inventory slot"][1] < dt * 250:
				self.special_slot_animations["Compact inventory slot"][1] += dt * 30

			if self.special_slot_animations["Compact inventory slot"][0]:
				try:
					if Settings["Display"][5]: win.blit(pygame.transform.scale(Compact_inventory2, (64 - self.special_slot_animations["Compact inventory slot"][2], 64 - self.special_slot_animations["Compact inventory slot"][2])), (810, 170))
					else: win.blit(pygame.transform.scale(Compact_inventory2, (64, 64)), (810, 170))
				except: win.blit(pygame.transform.scale(Compact_inventory2, (64, 64)), (810, 170))
				mouse_object = t("Compact inventory")
			
			else:
				win.blit(pygame.transform.scale(Compact_inventory1, (64, 64)), (810, 170))

			self.draw_whole()
			
			if self.game.craft_list_open:

				win.blit(Changed_craft_list_inventory_slot, (810, 90))
				win_fill(rect=(970, 0, Width - 970, Height))
					
				for cell_y, recipe in enumerate(self.recipes):
					cell_y += 1
					cell_x = -1
					for ii in recipe.ingredients:
						if ii is None:
							break
						else:
							cell_x += 1
							win.blit(Inventory_slot, (970 + cell_x * 80, 10 + self.game.craft_list_offset + cell_y * 80))
							win.blit(self.resources[ii].image, (970 + cell_x * 80, 10 + self.game.craft_list_offset + cell_y * 80))
							win.blit(textInfo.render(str(recipe.ingredients_amounts[cell_x]), True, (0, 150, 0)), (980 + cell_x * 80, 52 + self.game.craft_list_offset + cell_y * 80))
					if recipe.need_object is not None:
						cell_x = 8
						win.blit(Changed_inventory_slot, (990 + cell_x * 80, 10 + self.game.craft_list_offset + cell_y * 80))
						win.blit(self.resources[recipe.need_object].image, (990 + cell_x * 80, 10 + self.game.craft_list_offset + cell_y * 80))
					if recipe.need_tool is not None:
						cell_x = 9
						win.blit(Changed_inventory_slot, (990 + cell_x * 80, 10 + self.game.craft_list_offset + cell_y * 80))
						win.blit(self.resources[recipe.need_tool].image, (990 + cell_x * 80, 10 + self.game.craft_list_offset + cell_y * 80))
					cell_x = 10
					win.blit(Changed_inventory_slot, (990 + cell_x * 80, 10 + self.game.craft_list_offset + cell_y * 80))
					win.blit(self.resources[recipe.result].image, (990 + cell_x * 80, 10 + self.game.craft_list_offset + cell_y * 80))
					win.blit(textInfo.render(str(recipe.result_amount), True, (0, 150, 0)), (1000 + cell_x * 80, 52 + self.game.craft_list_offset + cell_y * 80))

				if 810 <= mouse_x <= 874 and 90 <= mouse_y <= 154 and self.game.release:
					self.game.craft_list_open = False
						
			else:
				
				if 810 <= mouse_x <= 874 and 90 <= mouse_y <= 154:
					if self.special_slot_animations["Craft list slot"][0]:
						if self.special_slot_animations["Craft list slot"][1] < dt * 150:
							self.special_slot_animations["Craft list slot"][1] += dt * 30
							self.special_slot_animations["Craft list slot"][2] -= dt * 90
							self.special_slot_animations["Craft list slot"][2] = abs(self.special_slot_animations["Craft list slot"][2])
					else:
						self.special_slot_animations["Craft list slot"] = [True, 0, 10]
					
					if self.game.release:
						self.game.craft_list_open = True
					
				elif self.special_slot_animations["Craft list slot"][0]:
					self.special_slot_animations["Craft list slot"][0] = False
					self.special_slot_animations["Craft list slot"][1] = 0
				elif self.special_slot_animations["Craft list slot"][1] < dt * 250:
					self.special_slot_animations["Craft list slot"][1] += dt * 30

				if self.special_slot_animations["Craft list slot"][0] and Settings["Display"][5]:
					try:win.blit(pygame.transform.scale(Changed_craft_list_inventory_slot, (64 - self.special_slot_animations["Craft list slot"][2], 64 - self.special_slot_animations["Craft list slot"][2])), (810, 90))
					except: win.blit(pygame.transform.scale(Changed_craft_list_inventory_slot, (64, 64)), (810, 90))
					mouse_object = t("Craft list")
			
				else:
					win.blit(pygame.transform.scale(Craft_list_inventory_slot, (64, 64)), (810, 90))

			if self.game.alt_pressed:
				draw_key(" I ", 42, 344)

			if self.whole_inventory[self.changed_slot] is not None and self.whole_inventory[self.changed_slot].name == "Wrench":

				if 900 <= mouse_x <= 964 and 10 <= mouse_y <= 74:
					win.blit(Changed_inventory_slot, (900, 10))
					if self.game.release: self.game.item_settings_open = True
				else:
					win.blit(Inventory_slot, (900, 10))
		else:
			
			if 10 < mouse_x < 794 and 10 < mouse_y < 74:
				mouse_object = t("Inventory (I)")

			for slot_x in range(10):
				if slot_x == self.changed_slot: win.blit(Changed_inventory_slot, (slot_x * 80 + 10, 10))
				else: win.blit(Inventory_slot, (slot_x * 80 + 10, 10))

			self.draw_panel()
			
			if self.game.alt_pressed:
				draw_key(" I ", 42, 104)

	def show_description(self, mouse_x, mouse_y, click):

		if self.game.inventory_open:
			if click[0] and not self.game.hold_left:
				self.set_start_cell(mouse_x, mouse_y)
				self.game.hold_left = True
			if self.game.hold_left and not click[0]:
				result = self.set_end_cell(mouse_x, mouse_y)
				if result:
					self.craft_items_list, self.craft_amounts_list, self.craft_images_list = result
				self.game.hold_left = False

		if self.start_cell:
			if self.whole_inventory[self.start_cell] is not None and self.start_cell > -1 and self.game.hold_left:

				item_text = t("Item info " + self.whole_inventory[self.start_cell].name) + "\n" + t("Item purpose " + self.whole_inventory[self.start_cell].name)
				
				text_height = get_text_height(item_text) + 40
				if self.whole_inventory[self.start_cell].type == "Food":
					text_height += 84
				
				for yy, xx in product(range(0, 3), range(0, 10)):
					cell_x = 10 + xx * 80
					cell_y = 10 + yy * 80
					if cell_x <= mouse_x <= cell_x + 64 and cell_y <= mouse_y <= cell_y + 64:
						win_fill(rect=(cell_x, cell_y, 64, 64))
						break

				pygame.draw.rect(win, text_color, (mouse_x, mouse_y, Width // 3 + 40, text_height))
				pygame.draw.rect(win, (0, 150, 0), (mouse_x, mouse_y, Width // 3 + 40, text_height), 3)
				text(item_text, mouse_x + 20, mouse_y + 20, color=(0, 150, 0), max_width=Width // 3)
				
				if self.whole_inventory[self.start_cell].type == "Food":
					win.blit(Heart, (mouse_x + 20, mouse_y + text_height - 84))
					win.blit(textInfo.render(str(self.whole_inventory[self.start_cell].special_info), True, text_color), (mouse_x + 52 - textInfo.size(str(self.whole_inventory[self.start_cell].special_info))[0] // 2, mouse_y + text_height - 59))
				
				win.blit(self.whole_inventory[self.start_cell].image, (mouse_x - 32, mouse_y - 32))
		
	def draw_item_settings(self, mouse_x, mouse_y):

		if self.game.item_settings_open:

			if self.whole_inventory[self.changed_slot].name == "Wrench":

				win_fill()

				pygame.draw.rect(win, text_color, (100, 100, Width - 200, Height - 200))
				pygame.draw.rect(win, (0, 150, 0), (100, 100, Width - 200, Height - 200), 10)
				win.blit(pygame.transform.scale2x(self.whole_inventory[self.changed_slot].image), (Width // 2 - 64, 130))
				pygame.draw.line(win, (0, 150, 0), (150, 308), (Width - 150, 308), 10)
				win.blit(textInfo.render(t("Only wire"), True, (0, 150, 0)), (130, 348))
				win.blit(textInfo.render(t("All mechanisms"), True, (0, 150, 0)), (Width // 2 - textInfo.size(t("All mechanisms"))[0] // 2, 348))
				win.blit(textInfo.render(t("All mechanisms except wire"), True, (0, 150, 0)), (Width - 150 - textInfo.size(t("All mechanisms except wire"))[0], 378))

				if self.whole_inventory[self.changed_slot].settings == ["Only wire"]:
					pygame.draw.rect(win, (0, 150, 0), (120, 278, 60, 60), 30)
					pygame.draw.circle(win, (0, 150, 0), (Width // 2, 308), 30)
					pygame.draw.circle(win, (0, 150, 0), (Width - 150, 308), 30)
				if self.whole_inventory[self.changed_slot].settings == []:
					pygame.draw.circle(win, (0, 150, 0), (150, 308), 30)
					pygame.draw.rect(win, (0, 150, 0), (Width // 2 - 30, 278, 60, 60), 30)
					pygame.draw.circle(win, (0, 150, 0), (Width - 150, 308), 30)
				if self.whole_inventory[self.changed_slot].settings == ["All mechanisms, but wire"]:
					pygame.draw.circle(win, (0, 150, 0), (150, 308), 30)
					pygame.draw.circle(win, (0, 150, 0), (Width // 2, 308), 30)
					pygame.draw.rect(win, (0, 150, 0), (Width - 180, 278, 60, 60), 30)

				if 120 <= mouse_x <= 180 and 278 <= mouse_y <= 338 and self.game.release:
					self.whole_inventory[self.changed_slot].settings = ["Only wire"]
				if Width // 2 - 30 <= mouse_x <= Width // 2 + 30 and 278 <= mouse_y <= 338 and self.game.release:
					self.whole_inventory[self.changed_slot].settings = []
				if Width - 180 <= mouse_x <= Width - 120 and 278 <= mouse_y <= 338 and self.game.release:
					self.whole_inventory[self.changed_slot].settings = ["All mechanisms, but wire"]
				
				win.blit(bigTextInfo.render("x", True, (0, 150, 0)), (Width - 160, 130))
				
				if self.game.alt_pressed:
					draw_key("ESC", Width - 160, 170)
					
				if Width - 160 <= mouse_x <= Width - 130 and 130 <= mouse_y <= 160:
					win.blit(bigTextInfo.render("x", True, (0, 100, 0)), (Width - 160, 130))
					if self.game.release:
						self.game.item_settings_open = False

