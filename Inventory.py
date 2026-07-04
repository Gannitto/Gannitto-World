import pygame
import os
pygame.init()

textInfo = pygame.font.Font(None, 20)
types = ["Just an item", "Weapon", "Food", "Drink", "Mechanism", "Flower", "Seed"]
path = os.path.abspath(__file__)[:-33]
if not os.path.exists(path):
	path = __file__[:-28]
	print(1)

class Resourse:

	"""Items with certain characteristics"""

	def __init__(self, name: str, image_path: str, info: list, purpose: list, type: str, special_info=None):

		self.name = name
		self.info = info
		self.purpose = purpose
		self.type = type
		self.amount = 0
		self.settings = []
		self.image_path = image_path
		self.image = pygame.transform.scale(pygame.image.load(image_path), (64, 64))
		self.special_info = special_info
		
	def __getstate__(self):
		
		# Возвращаем словарь состояния, исключая объект Surface
		state = self.__dict__.copy()
		del state['image']
		return state

	def __setstate__(self, state):
		pass
		# Восстанавливаем состояние и загружаем изображение
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

	def get_result(self):

		"""Проверяет, может ли быть какой-то результат от данных ингридеентов"""
		
		from Globals import craft_items_list, craft_amounts_list
		from Gannitto_world import player, world
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

		self.resourses = {

			"Mushroom": Resourse("Mushroom", path + "Gannitto world/files/Images/Items/Mushroom.png", [
				"Просто гриб, ничего больше",
				"Just a mushroom, nothong more"
			], [
				"Нету",
				"None"
			], types[0]),


			
			"Red mushroom": Resourse("Red mushroom", path + "Gannitto world/files/Images/Items/Red mushroom.png", [
				"Просто гриб, ничего больше",
				"Just a mushroom, nothong more"
			], [
				"Нету",
				"None"
			], types[0]),


			
			"Jar": Resourse("Jar", path + "Gannitto world/files/Images/Items/Jar.png", [
				"Нету",
				"None"
			], [
				"Нету",
				"None"
			], types[0]),



			"Gun": Resourse("Gun", path + "Gannitto world/files/Images/Items/Gun.png", [
				"Пушка, для которой нужны патроны",
				"A gun, that needs bullets"
			], [
				"С её помощью ты можешь стрелять, нажав на пробел",
				"You can shoot with it by pressing the spase"
			], types[1]),



			"Bullet": Resourse("Bullet", path + "Gannitto world/files/Images/Items/Bullet.png", [
				"Это пуля для пушки",
				"This is a bullet for gun"
			], [
				"С её помощью ты можешь стрелять, нажав на пробел(если у вас есть пистолет)",
				"You can shoot with it by pressing the spase(if you have a gun)"
			], types[0]),



			"Arrow": Resourse("Arrow", path + "Gannitto world/files/Images/Items/Arrow.png", [
				"Нету",
				"None"
			], [
				"Нету"
				"None"
			], types[0]),



			"Powder": Resourse("Powder", path + "Gannitto world/files/Images/Items/Powder.png", [
				"Покоритель битв и властелин взрывов",
				"Conqueror of battles and lord of explosions"
			], [
				"Используется для создания оружия",
				"Used to create weapons"
			], types[0]),



			"Grenade": Resourse("Grenade", path + "Gannitto world/files/Images/Items/Grenade.png", [
				"Опасная вещь",
				"Dangerous thing"
			], [
				"Можно кинуть во врага",
				"You can throw it at the enemy"
			], types[0]),



			"Almond whater": Resourse("Almond whater", path + "Gannitto world/files/Images/Items/Almond whater.png", [
				"Вода, вкус которой напомянает миндаль или ваниль",
				"Water, that tastes like almonds or vanilla"
			], [
				"Нету",
				"None"
			], types[3]),



			"Blue slime": Resourse("Blue slime", path + "Gannitto world/files/Images/Items/Blue Slime.png", [
				"Липкий гель синего цвета",
				"Blue sticky gel"
			], [
				"Нету",
				"None"
			], types[0]),



			"Pink slime": Resourse("Pink slime", path + "Gannitto world/files/Images/Items/Pink Slime.png", [
				"Липкий гель розового цвета",
				"Pink slicky gel"
			], [
				"None",
				"Нету"
			], types[0]),



			"Stick": Resourse("Stick", path + "Gannitto world/files/Images/Items/Stick.png", [
				"Простой и универсальный предмет",
				"Simple and versatile item"
			], [
				"Может использоваться для создания инструментов",
				"Can be used to create tools"
			], types[0]),



			"Iron ingot": Resourse("Iron ingot", path + "Gannitto world/files/Images/Items/Iron ingot.png", [
				"Ты можешь получить его, переплавив железную руду в печке",
				"You can get it, by smetling iron ore in a furnace"
			], [
				"Можно сделать ведро из трёх слитков на столе",
				"You can make a bucket of three ingots on the table"
			], types[0]),



			"Gold ingot": Resourse("Gold ingod", path + "Gannitto world/files/Images/Items/Gold ingot.png", [
				"Ты можешь получить его, переплавив золотую руду в печке",
				"You can get it, by smetling gold ore in a furnace"
			], [
				"Можно сделать золотое ведро из трёх слитков на столе",
				"You can make a gold bucket of three ingots on the table"
			], types[0]),



			"Bucket": Resourse("Bucket", path + "Gannitto world/files/Images/Items/Bucket.png", [
				"Ведро...",
				"Bucket..."
			], [
				"В него можно набрать воду",
				"You can put water in it"
			], types[0]),



			"Whater bucket": Resourse("Whater bucket", path + "Gannitto world/files/Images/Items/Whater bucket.png", [
				"Ведро...",
				"Bucket..."
			], [
				"Нету",
				"None"
			], types[0]),



			"Gold bucket": Resourse("Gold bucket", path + "Gannitto world/files/Images/Items/Gold bucket.png", [
				"Зачем тебе ЗОЛОТОЕ ведро?!",
				"Why do you need a GOLD bucket?!"
			], [
				"Нету",
				"None"
			], types[0]),



			"Thread": Resourse("Thread", path + "Gannitto world/files/Images/Items/Thread.png", [
				"Нету",
				"None"
			], [
				"Нету",
				"None"
			], types[0]),



			"Portal gun": Resourse("Portal gun", path + "Gannitto world/files/Images/Items/Portal gun.png", [
				"С помощью неё, ты можешь создовать порталы для телепортации",
				"With it, you can create teleportation portals"
			], [
				"Можно использовать для быстрого передвижения",
				"Can be used for fast movement"
			], types[0]),



			"Vending machine": Resourse("Vending machine", path + "Gannitto world/files/Images/Items/Vending machine.png", [
				"С помощью него можно обменивать вещи",
				"With it, you can vend items"
			], [
				"Удобно использовать в игре по сети",
				"Easy to use in online play"
			], types[0]),



			"Stone": Resourse("Stone", path + "Gannitto world/files/Images/Items/Stone.png", [
				"Спокойно лежит на земле",
				"Lies quietly on the ground"
			], [
				"Может использоваться для создания оружия",
				"Can be used to create weapons"
			], types[0]),



			"Poppy": Resourse("Poppy", path + "Gannitto world/files/Images/Items/Poppy.png", [
				"Красивый цветок",
				"A beautiful flower"
			], [
				"Можно посадить в горшок",
				"Can be planted in a pot"
			], types[5]),



			"Purple tulip": Resourse("Purple tulip", path + "Gannitto world/files/Images/Items/Purple tulip.png", [
				"Красивый цветок",
				"A beautiful flower"
			], [
				"Можно посадить в горшок",
				"Can be planted in a pot"
			], types[5]),



			"Orange tulip": Resourse("Orange tulip", path + "Gannitto world/files/Images/Items/Orange tulip.png", [
				"Красивый цветок",
				"A beautiful flower"
			], [
				"Можно посадить в горшок",
				"Can be planted in a pot"
			], types[5]),



			"Black tulip": Resourse("Black tulip", path + "Gannitto world/files/Images/Items/Black tulip.png", [
				"Красивый цветок",
				"A beautiful flower"
			], [
				"Можно посадить в горшок",
				"Can be planted in a pot"
			], types[5]),



			"Red tulip": Resourse("Red tulip", path + "Gannitto world/files/Images/Items/Red tulip.png", [
				"Красивый цветок",
				"A beautiful flower"
			], [
				"Можно посадить в горшок",
				"Can be planted in a pot"
			], types[5]),



			"Yellow tulip": Resourse("Yellow tulip", path + "Gannitto world/files/Images/Items/Yellow tulip.png", [
				"Красивый цветок",
				"A beautiful flower"
			], [
				"Можно посадить в горшок",
				"Can be planted in a pot"
			], types[5]),



			"Dandelion": Resourse("Dandelion", path + "Gannitto world/files/Images/Items/Dandelion.png", [
				"Красивый цветок",
				"A beautiful flower"
			], [
				"Можно посадить в горшок",
				"Can be planted in a pot"
			], types[5]),



			"Cotton grass": Resourse("Cotton grass", path + "Gannitto world/files/Images/Items/Cotton grass.png", [
				"Красивый цветок",
				"A beautiful flower"
			], [
				"Можно посадить в горшок",
				"Can be planted in a pot"
			], types[5]),



			"Rope": Resourse("Rope", path + "Gannitto world/files/Images/Items/Rope.png", [
				"",
				""
			], [
				"Нету",
				"None"
			], types[1]),



			"Stone spear": Resourse("Stone spear", path + "Gannitto world/files/Images/Items/Stone spear.png", [
				"Таким же оружием пользовались древние люди",
				"Ancient people used the same weapons"
			], [
				"Можно кидать во врагов",
				"Can be thrown at enemies"
			], types[1]),



			"Wooden": Resourse("Wooden", path + "Gannitto world/files/Images/Items/Wooden.png", [
				"Материал, получаемый из деревьев. Является необходимым компонентом для любого строителя",
				"Material obtained from trees. Is a necessary component for any builder"
			], [
				"Она может быть использована для создания мебели, топлива, построек и многих других предметов",
				"It can be used to create furniture, fuel, buildings and many other items."
			], types[0]),



			"Dark wooden": Resourse("Dark wooden", path + "Gannitto world/files/Images/Items/Dark wooden.png", [
				"Материал, получаемый из деревьев. Является необходимым компонентом для любого строителя",
				"Material obtained from trees. Is a necessary component for any builder"
			], [
				"Она может быть использована для создания мебели, топлива, построек и многих других предметов",
				"It can be used to create furniture, fuel, buildings and many other items."
			], types[0]),



			"Birch wooden": Resourse("Birch wooden", path + "Gannitto world/files/Images/Items/Birch wooden.png", [
				"Материал, получаемый из деревьев. Является необходимым компонентом для любого строителя",
				"Material obtained from trees. Is a necessary component for any builder"
			], [
				"Она может быть использована для создания мебели, топлива, построек и многих других предметов",
				"It can be used to create furniture, fuel, buildings and many other items."
			], types[0]),



			"Table": Resourse("Table", path + "Gannitto world/files/Images/Items/Table.png", [
				"Деревянный стол, на котором можно изготавливать предметы",
				"Wooden table, on which you can craft items"
			], [
				"Ты можешь поставить его",
				"You can put it"
			], types[0]),



			"Wall table": Resourse("Wall table", path + "Gannitto world/files/Images/Items/Wall table.png", [
				"Деревянный стол, на котором можно изготавливать стены",
				"Wooden table, on which you can craft walls"
			], [
				"Ты можешь поставить его",
				"You can put it"
			], types[0]),



			"Clay": Resourse("Clay", path + "Gannitto world/files/Images/Items/Clay.png", [
				"Как песок, но очень липкий",
				"Like sand, but very sticky"
			], [
				"Можно переплавить в кирпич",
				"Can be smelted into brick"
			], types[0]),



			"Brick": Resourse("Brick", path + "Gannitto world/files/Images/Items/Brick.png", [
				"Нету",
				"None"
			], [
				"Из него можно сделать кираичную стену",
				"You can make a brick wall out of it"
			], types[0]),



			"Pot": Resourse("Pot", path + "Gannitto world/files/Images/Items/Pot.png", [
				"Глиняный горшок",
				"Clay pot"
			], [
				"Ты можешь посадить в него растение",
				"You can put a plant in it"
			], types[0]),



			"Wire": Resourse("Wire", path + "Gannitto world/files/Images/Items/Wire.png", [
				"Нету",
				"None"
			], [
				"С помощью него можно делать различные механизмы",
				"With it, you can make various mechanisms"
			], types[0]),



			"Random box": Resourse("Random box", path + "Gannitto world/files/Images/Items/Random box.png", [
				"Нету",
				"None"
			], [
				"При получении сигнала с одной стороны, выдаёт его с другой с шансом 50%",
				"When recieving a signal from one side, gives it to the other with a 50% chance"
			], types[0]),



			"Lever": Resourse("Lever", path + "Gannitto world/files/Images/Items/Lever.png", [
				"Нету",
				"None"
			], [
				"Нету",
				"None"
			], types[0]),



			"Motherboard": Resourse("Motherboard", path + "Gannitto world/files/Images/Items/Motherboard.png", [
				"Нету",
				"None"
			], [
				"Нету",
				"None"
			], types[0]),



			"Wrench": Resourse("Wrench", path + "Gannitto world/files/Images/Items/Wrench.png", [
				"Какая-то штука",
				"Some thing"
			], [
				"С помощью него можно убрать провод", 
				"With it, you can remove the wire"
			], types[3]),



			"Stone pickaxe": Resourse("Stone pickaxe", path + "Gannitto world/files/Images/Items/Stone pickaxe.png", [
				"Понадобится любому шахтёру",
				"Nny miner needs"
			], [
				"С помощью неё ты можешь копать руду", 
				"with it you can dig ore"
			], types[0]),



			"Stone hammer": Resourse("Stone hammer", path + "Gannitto world/files/Images/Items/Stone hammer.png", [
				"Нету",
				"None"
			], [
				"Нету",
				"None"
			], types[0]),



			"Stone shovel": Resourse("Stone shovel", path + "Gannitto world/files/Images/Items/Stone shovel.png", [
				"Нету",
				"None"
			], [
				"Нету",
				"None"
			], types[0]),



			"Furnace": Resourse("Furnace", path + "Gannitto world/files/Images/Items/Furnace.png", [
				"Можно поставить",
				"You can put it"
			], [
				"С помощью печи, ты можешь переплавлять руды", 
				"With a furnace, you can melt down ores"
			], types[0]),



			"Stone brick": Resourse("Stone brick", path + "Gannitto world/files/Images/Items/Stone brick.png", [
				"Нету"
				"None"
			], [
				"Нету", 
				"None"
			], types[0]),



			"Wooden wall": Resourse("Wooden wall", path + "Gannitto world/files/Images/Items/Wooden wall.png", [
				"Стена, которая может сгореть",
				"A wall that can burn"
			], [
				"Можно поставить",
				"You can put it"
			], types[0]),



			"Brick wall": Resourse("Brick wall", path + "Gannitto world/files/Images/Items/Brick wall.png", [
				"Стена, которая не может сгореть",
				"A wall that can't burn"
			], [
				"Можно поставить",
				"You can put it"
			], types[0]),



			"Stone brick wall": Resourse("Stone brick wall", path + "Gannitto world/files/Images/Items/Stone brick wall.png", [
				"Стена, которая не может сгореть",
				"A wall that can't burn"
			], [
				"Можно поставить",
				"You can put it"
			], types[0]),



			"Wooden door": Resourse("Wooden door", path + "Gannitto world/files/Images/Items/Wooden door.png", [
				"Дверь, которая может сгореть",
				"A door that can burn"
			], [
				"Можно поставить",
				"You can put it"
			], types[0]),



			"Iron ore": Resourse("Iron ore", path + "Gannitto world/files/Images/Items/Iron ore.png", [
				"Блестящий и дорогой",
				"Shiny and expensive"
			], [
				"Ты можешь переплавить в железный слиток",
				"You can smelt it into an iron ingot"
			], types[0]),



			"Gold ore": Resourse("Gold ore", path + "Gannitto world/files/Images/Items/Gold ore.png", [
				"Блестящий и дорогой",
				"Shiny and expensive"
			], [
				"Ты можешь переплавить в золотой слиток",
				"You can smelt it into a gold ingot"
			], types[0]),



			"Candy cane": Resourse("Candy cane", path + "Gannitto world/files/Images/Items/Candy cane.png", [
				"Сладкая и липкая",
				"Sweet and sticky"
			], [
				"Можно съесть",
				"You can eat it"
			], types[0], 5),



			"Beer": Resourse("Beer", path + "Gannitto world/files/Images/Items/Beer.png", [
				"Нету",
				"None"
			], [
				"Нету",
				"None"
			], types[0]),



			"Bow": Resourse("Bow", path + "Gannitto world/files/Images/Items/Bow.png", [
				"Нету",
				"None"
			], [
				"Нету",
				"None"
			], types[0]),



			"Onion": Resourse("Onion", path + "Gannitto world/files/Images/Items/Onion.png", [
				"Горький, больше нечего сказать",
				"Bitter, nothibg more to say"
			], [
				"Можно съесть",
				"You can eat it"
			], types[2], 10),



			"Punch": Resourse("Punch", path + "Gannitto world/files/Images/Items/Punch.png", [
				"Нету",
				"None"
			], [
				"Нету",
				"None"
			], types[0]),



			"Stone hoe": Resourse("Stone hoe", path + "Gannitto world/files/Images/Items/Stone hoe.png", [
				"Древний инструмент земледелия",
				"Ancient farming tool"
			], [
				"Вы можете вскопать грядки с помощью неё",
				"You can dig up a farmland with it"
			], types[0]),



			"Carrot": Resourse("Carrot", path + "Gannitto world/files/Images/Items/Carrot.png", [
				"Вкусная и оранжевая",
				"Tasty and orange"
			], [
				"Можно съесть",
				"You can eat it"
			], types[2], 10),



			"Tomato": Resourse("Tomato", path + "Gannitto world/files/Images/Items/Tomato.png", [
				"Вкусный и красный",
				"Tasty and red"
			], [
				"Можно съесть",
				"You can eat it"
			], types[2], 10),


			
			"Cucumber": Resourse("Cucumber", path + "Gannitto world/files/Images/Items/Cucumber.png", [
				"Вкусный и зелёный",
				"Tasty and green"
			], [
				"Можно съесть",
				"You can eat it"
			], types[2], 10),


			
			"Corn": Resourse("Corn", path + "Gannitto world/files/Images/Items/Corn.png", [
				"Вкусная и жёлтая",
				"Tasty and yellow"
			], [
				"Можно съесть",
				"You can eat it"
			], types[2], 10),


			
			"Wheat": Resourse("Wheat", path + "Gannitto world/files/Images/Items/Wheat.png", [
				"",
				""
			], [
				"",
				""
			], types[0], 10),



			"Cucumber seeds": Resourse("Cucumber seeds", path + "Gannitto world/files/Images/Items/Cucumber seeds.png", [
				"Семена для сельского хозяйства",
				"Seeds for agriculture"
			], [
				"Используется для выращивания огурцов",
				"Used to grow cucumbers"
			], types[6], 10),



			"Corn seeds": Resourse("Corn seeds", path + "Gannitto world/files/Images/Items/Corn seeds.png", [
				"Семена для сельского хозяйства",
				"Seeds for agriculture"
			], [
				"Используется для выращивания кукурузы",
				"Used to grow corn"
			], types[6], 10),



			"Wheat seeds": Resourse("Wheat seeds", path + "Gannitto world/files/Images/Items/Wheat seeds.png", [
				"Семена для сельского хозяйства",
				"Seeds for agriculture"
			], [
				"Используется для выращивания пшеницы",
				"Used to grow wheat"
			], types[6], 10)
		}

		
		
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
		
		"""Adds item to inventory"""
		
		try:
			self.resourses[name].amount += amount
			self.update_whole()
		except KeyError:
			from Gannitto_world import t, chat_message
			chat_message(t("<<< Error increasing: item not found >>>"))
	
	def update_whole(self):
		
		for name, resource in self.resourses.items():
			if resource.amount != 0 and resource not in self.whole_inventory:
				self.whole_inventory.insert(self.whole_inventory.index(None), resource)
				self.whole_inventory.remove(None)

		def chek():
			for cell in self.whole_inventory:
				if cell is not None and cell.amount > 99:
					for _ in range(int(cell.amount / 99)):
						a = self.whole_inventory.index(None)
						self.whole_inventory[a] = Resourse(cell.name, cell.image_path, cell.info, cell.purpose, cell.type)
						self.whole_inventory[a].amount = 99
					cell.amount -= int(cell.amount / 99) * 99
					chek()

		chek()
	
	def get_amout(self, name: str):
		
		"""Возвращает количество предмета"""

		try:
			return self.resourses[name].amount
		except KeyError:
			return -1
	
	def draw_whole(self):
		
		"""Рисует весь инвентарь"""

		from Globals import win, craft_images_list, craft_amounts_list
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
			if cell is not None:
				win.blit(cell, (cell_x, 250))
				if craft_amounts_list != [None] * 7 and craft_amounts_list[i] > 1:
					win.blit(textInfo.render(str(craft_amounts_list[i]), True, (0, 150, 0)), (cell_x + 10, 292))
				cell_x += 80
				win.blit(Inventory_slot, (cell_x, 250))
			else:
				break
	
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
		
		if self.whole_inventory[self.start_cell] is not None and inventory.whole_inventory[self.start_cell] != self.whole_inventory[self.end_cell]:

			if self.end_cell_inventory == 0 and self.whole_inventory[self.end_cell] is not None and self.whole_inventory[self.start_cell].name == self.whole_inventory[self.end_cell].name :

				self.whole_inventory[self.end_cell].amount += self.whole_inventory[self.start_cell].amount
				self.whole_inventory[self.start_cell] = None

			else:

				if self.Split_items and self.whole_inventory[self.start_cell].amount % 2 == 0:
					self.whole_inventory[self.start_cell].amount //= 2
					self.whole_inventory[self.end_cell] = self.whole_inventory[self.start_cell]
				elif self.end_cell_inventory == 1:
					temp = craft_items_list[self.end_cell]
					craft_items_list[self.end_cell] = self.whole_inventory[self.start_cell].name
					craft_amounts_list[self.end_cell] = self.whole_inventory[self.start_cell].amount
					craft_images_list[self.end_cell] = self.whole_inventory[self.start_cell].image
					self.resourses[self.whole_inventory[self.start_cell].name].amount = 0
					self.whole_inventory[self.start_cell] = temp
					self.start_cell = 0
					self.end_cell = 0
				else:
					temp = self.whole_inventory[self.end_cell]
					self.whole_inventory[self.end_cell] = self.whole_inventory[self.start_cell]
					self.whole_inventory[self.start_cell] = temp
					self.start_cell = 0
					self.end_cell = 0

		self.update_whole()
		return craft_items_list, craft_amounts_list, craft_images_list

	def check_recipies(self):
		for recipie in self.recipes:
			if recipie.get_result() is not None:
				return recipie.get_result()
		return None

inventory = Inventory()

def get_start_items():

	"""Выдаёт в инвентарь начальные предметы"""

	inventory.whole_inventory = [None] * 30
	inventory.increate("Bow", 1)
	inventory.increate("Arrow", 99)
	
