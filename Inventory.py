import pygame
import os
import json
from Globals import path
from Translator import translator

pygame.init()
t = translator.get
textInfo = pygame.font.Font(None, 20)
types = ["Just an item", "Tool", "Food", "Drink", "Mechanism", "Flower", "Seed", "Build"]

class Resource:

	"""Предмет с определёнными харрактеристиками"""

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

	def get_result(self, player, world, craft_items_list, craft_amounts_list):

		"""Проверяет, может ли быть какой-то результат от данных ингридеентов"""

		if craft_items_list == self.ingredients and craft_amounts_list == self.ingredients_amounts:
			a = True
			b = None
			c = True
			d = None

			if self.need_object != None:
				a = False
				for object in world.objects:
					if player.x - 1000 <= object.x <= player.x + 1000 and player.y - 1000 <= object.y <= player.y + 1000 and object.name == self.need_object:
						a = True
						b = object.name
						break
			
			if self.need_tool != None:
				c = False
				for cell in inventory.whole_inventory:
					if cell != None and cell.name == self.need_tool:
						c = True
						d = cell.name
			if a and c:
				return [self.result, self.result_amount, b, d]
			else:
				return None
		else:
			return None

class Inventory:

	def __init__(self):

		self.resources = {}

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
		self.start_cell = 0
		self.end_cell = 0
		self.end_cell_inventory = 0
		self.Split_items = False
	
	def increate(self, name: str, amount: int=1):
		
		"""Выдаёт предмет в инвентарь"""
		
		try:
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
					from Gannitto_world import t, chat_message
					chat_message(t("<<< Inventory is full! >>>"))
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
			from Gannitto_world import t, chat_message
			chat_message(t("<<< Error increasing: item not found >>>"))
	
	def update_whole(self):
		
		for name, resource in self.resources.items():
			if resource.amount != 0 and resource not in self.whole_inventory:
				self.whole_inventory.insert(self.whole_inventory.index(None), resource)
				self.whole_inventory.remove(None)

		def check():
			for cell in self.whole_inventory:
				if cell is not None and cell.amount > 99:
					for _ in range(int(cell.amount / 99)):
						a = self.whole_inventory.index(None)
						self.whole_inventory[a] = Resource(cell.name, cell.image_path, cell.info, cell.purpose, cell.type)
						self.whole_inventory[a].amount = 99
					cell.amount -= int(cell.amount / 99) * 99
					check()

		check()

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
					template.image_path,
					template.info,
					template.purpose,
					template.type,
					template.special_info,
					template.max_stack
				)
				new_item.amount = stack_size
				
				self.whole_inventory[current_index] = new_item
				current_index += 1
				total_amount -= stack_size

	def draw_whole(self, craft_images_list, craft_amounts_list):
		
		"""Рисует весь инвентарь"""

		from Globals import win
		from Gannitto_world import Inventory_slot
		cell_x = cell_y = 10
		for cell in self.whole_inventory:
			if cell is not None:
				try:win.blit(cell.image, (cell_x, cell_y))
				except:print(cell)
				if cell.amount > 1:
					win.blit(textInfo.render(str(cell.amount), True, (0, 150, 0)), (cell_x + 10, cell_y + 42))
			cell_x += 80
			if cell_x == 810:
				cell_x = 10
				cell_y += 80
		cell_x = 170
		win.blit(Inventory_slot, (170, 250))
		i = -1
		
		for cell in craft_images_list:
			i += 1
			if cell is None:
				break
			else:
				win.blit(cell, (cell_x, 250))
				if craft_amounts_list != [None] * 7 and craft_amounts_list[i] > 1:
					win.blit(textInfo.render(str(craft_amounts_list[i]), True, (0, 150, 0)), (cell_x + 10, 292))
				cell_x += 80
				win.blit(Inventory_slot, (cell_x, 250))
	
	def draw_panel(self):
		
		"""Draws the top panel"""

		from Globals import win
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
	
	def set_start_cell(self, mouse__x: int, mouse__y: int):

		for yy in range(0, 3):
			for xx in range(0, 10):
				cell_x = 10 + xx * 80
				cell_y = 10 + yy * 80
				if cell_x <= mouse__x <= cell_x + 64 and cell_y <= mouse__y <= cell_y + 64:
					self.start_cell = yy * 10 + xx
					return
	
	def set_end_cell(self, mouse__x: int, mouse__y: int, craft_items_list, craft_amounts_list, craft_images_list):

		for yy in range(0, 3):
			for xx in range(0, 10):
				cell_x = 10 + xx * 80
				cell_y = 10 + yy * 80
				if cell_x <= mouse__x <= cell_x + 64 and cell_y <= mouse__y <= cell_y + 64:
					self.end_cell = yy * 10 + xx
					self.end_cell_inventory = 0
		
		for X in range(2, 9):
			cell_x = 10 + X * 80
			if cell_x <= mouse__x <= cell_x + 64 and 250 <= mouse__y <= 314:
				self.end_cell = X - 2
				self.end_cell_inventory = 1
		return self.swap_cells(craft_items_list, craft_amounts_list, craft_images_list)
	
	def swap_cells(self, craft_items_list, craft_amounts_list, craft_images_list):
		
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
								self.whole_inventory[self.start_cell].image_path,
								self.whole_inventory[self.start_cell].info,
								self.whole_inventory[self.start_cell].purpose,
								self.whole_inventory[self.start_cell].type,
								self.whole_inventory[self.start_cell].special_info,
								self.whole_inventory[self.start_cell].max_stack
							)
							self.whole_inventory[self.end_cell] = new_item
					else:
						# Обычный обмен
						temp = self.whole_inventory[self.end_cell]
						self.whole_inventory[self.end_cell] = self.whole_inventory[self.start_cell]
						self.whole_inventory[self.start_cell] = temp
			
			elif self.end_cell_inventory == 1:
				# Перемещение в крафт
				temp = craft_items_list[self.end_cell]
				craft_items_list[self.end_cell] = self.whole_inventory[self.start_cell].name
				craft_amounts_list[self.end_cell] = self.whole_inventory[self.start_cell].amount
				craft_images_list[self.end_cell] = self.whole_inventory[self.start_cell].image
				self.whole_inventory[self.start_cell] = None
				
				if temp is not None:
					# Возвращаем предмет из крафта
					self.increate(temp, 1)
		
		self.start_cell = 0
		self.end_cell = 0
		# self.compact_inventory()	# Компактизируем после каждого изменения
		return craft_items_list, craft_amounts_list, craft_images_list

	def check_recipies(self, player, world, craft_items_list, craft_amounts_list):
		for recipie in self.recipes:
			result = recipie.get_result(player, world, craft_items_list, craft_amounts_list)
			if result is not None:
				return result
		return None

inventory = Inventory()
def get_start_items():

	"""Выдаёт в инвентарь начальные предметы"""

	inventory.whole_inventory = [None] * 30
	inventory.increate("Bow", 1)
	inventory.increate("Arrow", 99)
	
