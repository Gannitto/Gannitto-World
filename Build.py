import pygame
from Globals import path
from Functions import win_fill

select_images = {
		(256, 256): pygame.transform.scale(pygame.image.load(path + "Images/Select 256x256.png"), (256, 256))
		}

for image in select_images.values():
	image.set_alpha(50)

def draw_select_image(win, w, h, Width, Height, player, mouse_x, mouse_y):
	if (w, h) in select_images:
		win.blit(select_images[(w, h)], ((player.x + mouse_x - Width // 2) // w * w - player.x + Width // 2, player.y - (player.y - mouse_y + Height // 2) // h * h + Height // 2 - h))
	else:
		win_fill(rect=((player.x + mouse_x - Width // 2) // w * w - player.x + Width // 2, player.y - (player.y - mouse_y + Height // 2) // h * h + Height // 2 - h, w, h))


def build(
		build_tuple: tuple,
		object_to_build=False,
		item_name: str="",
		item_type: str="",
		get_item_from_inventory: int=1,
		pick_up_items: bool=True,
		particle_to_build=False,
		build_wall=False,
		needed_object: str="",
		remove_part: str="",
		command: str="..."
		):
	
	"""
	Используется для того, чтобы построить что-либо
	Аргументы:
	object_to_build - Объект, который ставится. Вместо значений x и y надо ставить 0
	item_name - Имя предмета, который нужно поставить. Можно перечислить несколько в одной строке через пробел, запятую без пробела
	item_type - Тип предмета, который нужно поставить. Можно использовать вместо item_name. Можно перечислить несколько в одной строке через пробел, запятую без пробела
	get_item_from_inventory - Брать ли предмет из инвентаря. Число отвечает за количество взятых предметов из инвентаря
	pick_up_items - Поднимать ли автоматически предметы, которые находятся на месте, где нужно поставить объект
	particle_to_build - Ставится ли частица вместо объекта или нет
	needed_object - Объект, который должен быть на месте, там где нужно поставить что-либо
	remove_part - Часть в названии предмета в выбранном слоте, которую надо вырезать
	command - Команда, которую надо выполнить, если поставился объект
	"""
	
	changed_slot, player, particles, Width, Height, world, whole_inventory, win = build_tuple

	if whole_inventory[changed_slot] is not None:

		changed_slot_name = whole_inventory[changed_slot].name.replace(remove_part, "") if remove_part in whole_inventory[changed_slot].name else whole_inventory[changed_slot].name

		if changed_slot_name in item_name.split(",") or whole_inventory[changed_slot].type in item_type.split(","):
			
			mouse_x, mouse_y = pygame.mouse.get_pos()
			draw_select_image(win, object_to_build.w, object_to_build.h, Width, Height, player, mouse_x, mouse_y)

			if pygame.mouse.get_pressed()[0]:
			
				for i, object in enumerate(world.visible_objects + particles):
				
					if i < len(world.visible_objects) or object.can_interfere_with_placing:

						if pygame.Rect((player.x + mouse_x - Width // 2) // object_to_build.w * object_to_build.w + object_to_build.w // 2, (player.y - mouse_y + Height // 2) // object_to_build.h * object_to_build.h + object_to_build.h // 2, object_to_build.w, object_to_build.h).colliderect(pygame.Rect(object.x, object.y, object.w, object.h)):
							if needed_object == object.name:
								needed_object = "Object found"
							else:
								break
				
				else:
				
					if needed_object in ("Object found", ""):
					
						whole_inventory[changed_slot].amount -= get_item_from_inventory
						if whole_inventory[changed_slot].amount == 0:
							whole_inventory[changed_slot] = None
						new_object = object_to_build.copy()
						new_object.x, new_object.y = ((player.x + mouse_x - Width // 2) // object_to_build.w * object_to_build.w + object_to_build.w // 2, (player.y - mouse_y + Height // 2) // object_to_build.h * object_to_build.h + object_to_build.h // 2)
						new_object.rect = pygame.Rect(new_object.x - new_object.w / 2, new_object.y - new_object.h / 2, new_object.w, new_object.h)
						if particle_to_build: particles.append(object_to_build)
						else: world.chunk_manager.get_chunk_at(new_object.x, new_object.y).objects.append(new_object)
						eval(command)

def check_build_objects(objects_templates, build_tuple):
	"""Проверяет все объекты, которые можно построить"""
	for name, object in objects_templates.items():
		build(build_tuple, object, name)
