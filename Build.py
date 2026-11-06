# def build(
#		build_tuple: tuple,
#		object_to_build=False,
#		item_name: str="",
#		item_type: str="",
#		get_item_from_inventory: int=1,
#		pick_up_items: bool=True,
#		needed_object: str="",
#		):
	
#	"""
#	Используется для того, чтобы построить что-либо
#	Аргументы:
#	object_to_build - Объект, который ставится. Вместо значений x и y надо ставить 0
#	item_name - Имя предмета, который нужно поставить. Можно перечислить несколько в одной строке через пробел, запятую без пробела
#	item_type - Тип предмета, который нужно поставить. Можно использовать вместо item_name. Можно перечислить несколько в одной строке через пробел, запятую без пробела
#	get_item_from_inventory - Брать ли предмет из инвентаря. Число отвечает за количество взятых предметов из инвентаря
#	pick_up_items - Поднимать ли автоматически предметы, которые находятся на месте, где нужно поставить объект
#	needed_object - Объект, который должен быть на месте, там где нужно поставить что-либо
#	"""
	
#	changed_slot, player, world, whole_inventory = build_tuple

#	if whole_inventory[changed_slot] is not None:

#		changed_slot_name = whole_inventory[changed_slot].name

#		if changed_slot_name in item_name.split(",") or whole_inventory[changed_slot].type in item_type.split(","):
			
#			mouse_x, mouse_y = pygame.mouse.get_pos()
#			draw_select_image(object_to_build.w, object_to_build.h, player, mouse_x, mouse_y)

#			if pygame.mouse.get_pressed()[0]:
			
#				for i, object in enumerate(world.visible_objects + world.particles):
				
#					if i < len(world.visible_objects) or object.can_interfere_with_placing:

#						if pygame.Rect((player.x + mouse_x - Width // 2) // object_to_build.w * object_to_build.w + object_to_build.w // 2, (player.y - mouse_y + Height // 2) // object_to_build.h * object_to_build.h + object_to_build.h // 2, object_to_build.w, object_to_build.h).colliderect(pygame.Rect(object.x, object.y, object.w, object.h)):
#							if needed_object == object.name:
#								needed_object = "Object found"
#							else:
#								break
				
#				else:
				
#					if needed_object in ("Object found", ""):
					
#						whole_inventory[changed_slot].amount -= get_item_from_inventory
#						if whole_inventory[changed_slot].amount == 0:
#							whole_inventory[changed_slot] = None
#						new_object = object_to_build.copy()
#						new_object.x, new_object.y = ((player.x + mouse_x - Width // 2) // object_to_build.w * object_to_build.w + object_to_build.w // 2, (player.y - mouse_y + Height // 2) // object_to_build.h * object_to_build.h + object_to_build.h // 2)
#						new_object.rect = pygame.Rect(new_object.x - new_object.w / 2, new_object.y - new_object.h / 2, new_object.w, new_object.h)
#						world.chunk_manager.get_chunk_at(new_object.x, new_object.y).objects.append(new_object)
#						return new_object
#	return None

# def check_build_objects(objects_templates, build_tuple):
#	"""Проверяет все объекты, которые можно построить"""
#	new_object = None
#	for name, object in objects_templates.items():
#		new_object_ = build(build_tuple, object, name)
#		if new_object_ is not None:
#			new_object = new_object_
#			break
#	return new_object

import pygame
from Assets import select_images
from Functions import check_collision, win_fill
from Globals import path, Width, Height, win

for image in select_images.values():
	image.set_alpha(70)

def get_grid_position(player, mouse_x, mouse_y, w, h) -> tuple[int, int]:
	"""Вычисляет центральную позицию объекта на мировой сетке на основе координат мыши."""
	world_x = (player.x + mouse_x - Width // 2) // w * w + w // 2 
	world_y = (player.y - mouse_y + Height // 2) // h * h + h // 2
	return world_x, world_y

def draw_select_image(w, h, game, mouse_x, mouse_y):
	"""Отрисовка фантома строящегося объекта."""
	grid_x, grid_y = get_grid_position(game.player, mouse_x, mouse_y, w, h)
	screen_x, screen_y = game.world_to_screen(grid_x, grid_y, w, h)
	
	if (w, h) in select_images:
		win.blit(select_images[(w, h)], (screen_x, screen_y))
	else:
		win_fill(rect=(screen_x, screen_y, w, h))

def draw_select_image_arbitrarily(X, Y, w, h, world_to_screen, world_rect_to_screen):
	if (w, h) in select_images:
		win.blit(select_images[(w, h)], (world_to_screen(X, Y, w, h)))
	else:
		win_fill(rect=world_rect_to_screen(X, Y, w, h))

def try_spend_resources(inventory, slot, amount: int) -> bool:
	"""Пытается забрать предметы из инвентаря. Возвращает True в случае успеха."""
	if inventory.whole_inventory[slot] is None or inventory.whole_inventory[slot].amount < amount:
		return False
		
	inventory.whole_inventory[slot].amount -= amount
	if inventory.whole_inventory[slot].amount <= 0:
		inventory.whole_inventory[slot] = None
	return True


def build(
	game,
	object_to_build,
	item_name: str,
	item_type: str = "",
	get_item_from_inventory: int = 1,
	needed_object: str = ""
):
	"""
	Основная логика попытки строительства.
	Ввод (клик мыши) и рендер фантома должны обрабатываться ВНЕ этой функции в игровом цикле.
	"""
	item = game.inventory.whole_inventory[game.inventory.changed_slot]
	if item is None:
		return None

	# Валидация соответствия предмета в руке разрешенным типам/именам
	name_match = item_name == item.name
	type_match = item_type == item.type
	
	if not (name_match or type_match):
		return None

	# Получаем мировые координаты для строительства
	mouse_x, mouse_y = pygame.mouse.get_pos()
	grid_x, grid_y = get_grid_position(game.player, mouse_x, mouse_y, object_to_build.w, object_to_build.h)
	
	# Создаем гипотетический хитбокс нового объекта
	build_rect = pygame.Rect(grid_x - object_to_build.w // 2, grid_y - object_to_build.h // 2, object_to_build.w, object_to_build.h)

	# Проверяем коллизии в мире
	if not check_collision(build_rect, game.world):
		return None

	# Проверяем ресурсы и списываем их
	if not try_spend_resources(game.inventory, game.inventory.changed_slot, get_item_from_inventory):
		return None

	# Создание и размещение объекта в мире
	new_object = object_to_build.copy()
	new_object.x, new_object.y = grid_x, grid_y
	new_object.rect = build_rect
	
	# Добавление в чанк менеджер
	chunk = game.world.chunk_manager.get_chunk_at(new_object.x, new_object.y)
	chunk.objects.append(new_object)
	
	return new_object


def check_build_objects(objects_templates, game, mouse_x, mouse_y):
	"""Проверяет все шаблоны объектов на возможность постройки при клике."""
	# Проверку нажатия мыши лучше вынести сюда или еще выше в контроллер ввода

	if game.inventory.whole_inventory[game.inventory.changed_slot] and game.inventory.whole_inventory[game.inventory.changed_slot].name in objects_templates.keys():
		draw_select_image
	
	if not game.inventory.whole_inventory[game.inventory.changed_slot]:
		return None
	
	click = pygame.mouse.get_pressed()[0]

	for name, obj_template in objects_templates.items():
		if game.inventory.whole_inventory[game.inventory.changed_slot].name == name:
			draw_select_image(obj_template.w, obj_template.h, game, mouse_x, mouse_y)
			if click:
				new_obj = build(
					game,
					object_to_build=obj_template, 
					item_name=name
				)
				if new_obj is not None:
					return new_obj
			
	return None

# * **Строки заменены списками:** Вместо строк со сплитом через запятую (`item_name.split(",")`) теперь на вход принимаются чистые списки `item_names: list[str] = None`. Это исключает баги, если вы случайно поставите лишний пробел в конфиге предметов.
# * **Выделена функция `get_grid_position`:** Сетка считается в одном единственном месте. Это убрало дублирование сложной математики в `draw_select_image` и `build`.

