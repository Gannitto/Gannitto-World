import pygame

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
	
	from Inventory import inventory
	changed_slot, player, particles, Width, Height, world = build_tuple
	from Gannitto_world import Particle, Pick_an_item
	from Functions import win_fill
	
	if inventory.whole_inventory[changed_slot] is not None:

		changed_slot_name = inventory.whole_inventory[changed_slot].name.replace(remove_part, "") if remove_part in inventory.whole_inventory[changed_slot].name else inventory.whole_inventory[changed_slot].name

		if changed_slot_name in item_name.split(",") or inventory.whole_inventory[changed_slot].type in item_type.split(","):
			
			mouse_x, mouse_y = pygame.mouse.get_pos()
			win_fill(rect=((player.x + mouse_x - Width // 2) // object_to_build.w * object_to_build.w - player.x + Width // 2, player.y - (player.y - mouse_y + Height // 2) // object_to_build.h * object_to_build.h + Height // 2 - object_to_build.h, object_to_build.w, object_to_build.h))
		
			if pygame.mouse.get_pressed()[0]:
			
				for i, object in enumerate(world.visible_objects + particles):
				
					if i < len(world.visible_objects) or object.can_interfere_with_placing:

						if pygame.Rect((player.x + mouse_x - Width // 2) // object_to_build.w * object_to_build.w + object_to_build.w // 2, (player.y - mouse_y + Height // 2) // object_to_build.h * object_to_build.h + object_to_build.h // 2, object_to_build.w, object_to_build.h).colliderect(pygame.Rect(object.x, object.y, object.w, object.h)):
							if pick_up_items and object.special_flags == "Item":
								particles.append(Particle(object.x, object.y, object.image, "round(self.calculated_variable[0])", "round(self.calculated_variable[1])", variable_to_calculate="((self.special_flags[0] // 2) / 10 / 10 * self.ticks, (self.special_flags[1] // 2) / 10 / 10 * self.ticks, (-self.special_flags[0] // 2) / 10 / 10 * (self.ticks - 10), (-self.special_flags[1] // 2) / 10 / 10 * (self.ticks - 10))", track_ticks=True, end_x=player.x, end_y=player.y, end_zone=30, end_command="(inventory.increate('" + object.name + "'),pygame.mixer.Sound.play(Pick_an_item))", special_flags=(player.x - object.x, player.y - object.y, (0 - 17) // (0 - 10))))
								world.chunk_manager.get_chunk_at(object.x, object.y).objects.remove(object)
								pygame.mixer.Sound.play(Pick_an_item)
							elif needed_object == object.name:
								needed_object = "Object found"
							else:
								break
				
				else:
				
					if needed_object in ("Object found", ""):
					
						inventory.whole_inventory[changed_slot].amount -= get_item_from_inventory
						if inventory.whole_inventory[changed_slot].amount == 0:
							inventory.whole_inventory[changed_slot] = None
					
						object_to_build.x, object_to_build.y = ((player.x + mouse_x - Width // 2) // object_to_build.w * object_to_build.w + object_to_build.w // 2, (player.y - mouse_y + Height // 2) // object_to_build.h * object_to_build.h + object_to_build.h // 2)
						if particle_to_build: particles.append(object_to_build)
						else: world.chunk_manager.get_chunk_at(object_to_build.x, object_to_build.y).objects.append(object_to_build)
						eval(command)
