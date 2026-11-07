import pygame
from Assets import select_images, wall_types, door_types
from Functions import check_collision, win_fill
from Sound import play_sound
from Globals import path, Width, Height, win
from Classes import Object, Wall, Farmland

objects_templates = {
    "Table": Object("Table", 0, 0, "Images/Objects/Table.png", (256, 256), is_solid=True, breakable_by_hammer=True),
    "Wall table": Object("Wall table", 0, 0, "Images/Objects/Wall table.png", (256, 256), special_flags=1, is_solid=True, breakable_by_hammer=True),
    "Furnace": Object("Furnace", 0, 0, "Images/Items/Furnace.png", (256, 256), special_flags=1, is_solid=True, breakable_by_hammer=True),
    "Punch": Object("Punch", 0, 0, "Images/Objects/Punch 1.png", (256, 256), is_solid=True, breakable_by_hammer=True)
}

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
    if inventory.whole_inventory[slot] is None or inventory.whole_inventory[slot].amount < amount:
        return False
    inventory.whole_inventory[slot].amount -= amount
    if inventory.whole_inventory[slot].amount <= 0:
        inventory.whole_inventory[slot] = None
    return True

def build(
    game,
    size: tuple[int, int],
    item_name: str,
    spawn_callback,
    check_player: bool = True
):
    """
    Универсальная логика строительства.
    размеры size=(w, h)
    spawn_callback — функция вида f(grid_x, grid_y, build_rect), которая размещает объект в мире.
    """
    item = game.inventory.whole_inventory[game.inventory.changed_slot]
    if item is None or item.name != item_name:
        return None

    w, h = size
    mouse_x, mouse_y = pygame.mouse.get_pos()
    grid_x, grid_y = get_grid_position(game.player, mouse_x, mouse_y, w, h)
    
    # Специфический отступ для стен/дверей и грядок из вашего старого кода
    if item_name in wall_types or item_name in door_types:
        build_rect = pygame.Rect(grid_x - 128, grid_y - 128, w, h)
    elif item_name == "Stone hoe":
        build_rect = pygame.Rect(grid_x - 128, grid_y, w, h)
    else:
        build_rect = pygame.Rect(grid_x - w // 2, grid_y - h // 2, w, h)

    # Проверка коллизий
    if check_collision(build_rect, game, check_player=check_player):
        return None

    # Попытка списать ресурс (инструмент Stone hoe не тратится)
    if item_name != "Stone hoe":
        if not try_spend_resources(game.inventory, game.inventory.changed_slot, 1):
            return None

    # Вызов кастомной логики создания конкретного класса
    created_instance = spawn_callback(grid_x, grid_y, build_rect)
    return created_instance


def check_build_objects(game, mouse_x, mouse_y):
    """Проверяет все типы построек (объекты, стены, механизмы, грядки) при клике."""
    item = game.inventory.whole_inventory[game.inventory.changed_slot]
    if not item:
        return None
        
    click = pygame.mouse.get_pressed()[0]
    name = item.name

    # --- 1. ОБЪЕКТЫ ---
    if name in objects_templates:
        obj_template = objects_templates[name]
        draw_select_image(obj_template.w, obj_template.h, game, mouse_x, mouse_y)
        if click:
            def spawn_obj(gx, gy, rect):
                new_object = obj_template.copy()
                new_object.x, new_object.y = gx, gy
                new_object.rect = rect
                chunk = game.world.chunk_manager.get_chunk_at(gx, gy)
                chunk.objects.append(new_object)
                if game.multiplayer:
                    game.events.append({"event_type": "object_added", "object": new_object.__getstate__()})
                return new_object
            return build(game, (obj_template.w, obj_template.h), name, spawn_obj)

    # --- 2. СТЕНЫ И ДВЕРИ ---
    elif name in wall_types or name in door_types:
        wall_pos = (game.player.x + mouse_x - Width // 2) // 256 * 256 + 128, (game.player.y - mouse_y + Height // 2) // 256 * 256 + 128
        draw_select_image(256, 256, game, mouse_x, mouse_y)
        if click and wall_pos not in game.world.visible_walls:
            def spawn_wall(gx, gy, rect):
                is_door = name in door_types
                new_wall = Wall(game.world, name, wall_pos[0], wall_pos[1], is_door)
                game.world.chunk_manager.get_chunk_at(*wall_pos).walls[wall_pos] = new_wall
                
                # Обновление соседей
                for n_pos in ((wall_pos[0]-256, wall_pos[1]), (wall_pos[0]+256, wall_pos[1]), (wall_pos[0], wall_pos[1]-256), (wall_pos[0], wall_pos[1]+256)):
                    if n_pos in game.world.visible_walls:
                        game.world.visible_walls[n_pos].update_neigboors(game.world)
                        
                if game.multiplayer:
                    game.events.append({"event_type": "wall_added", "wall": new_wall.__getstate__()})
                return new_wall
            return build(game, (256, 256), name, spawn_wall, check_player=True)

    # --- 3. ГРЯДКИ ---
    elif name == "Stone hoe":
        farmland_pos = (game.player.x + mouse_x - Width // 2) // 128 * 128 + 128, (game.player.y - mouse_y + Height // 2) // 128 * 128
        draw_select_image(128, 128, game, mouse_x, mouse_y)
        if click and farmland_pos not in game.world.visible_farmlands:
            def spawn_farmland(gx, gy, rect):
                new_farm = Farmland(farmland_pos[0], farmland_pos[1])
                game.world.chunk_manager.get_chunk_at(*farmland_pos).farmlands[farmland_pos] = new_farm
                game.events.append({"event_type": "farmland_added", "farmland_pos": farmland_pos})
                play_sound("Dirt")
                return new_farm
            return build(game, (128, 128), name, spawn_farmland, check_player=False)

    # --- 4. МЕХАНИЗМЫ ---
    elif name in ["Wire", "Lever", "Motherboard", "Random box"]:
        # Для механизмов можно выставить сетку 64x64
        draw_select_image(64, 64, game, mouse_x, mouse_y)
        if click:
            def spawn_mechanism(gx, gy, rect):
                # Проверяем, нет ли уже механизма в этой точке
                mechs = game.world.mechanisms if game.in_motherboard is None else game.in_motherboard.objects
                target_x = (game.player.x + mouse_x - Width // 2) // 64
                target_y = (game.player.y - mouse_y + Height // 2) // 64
                
                for mech in mechs:
                    if mech and mech.x == target_x and mech.y == target_y:
                        return None # Место занято
                
                from Classes import Wire, Lever, Motherboard, RandomBox
                if name == "Wire":
                    new_mech = Wire(game.player, game.world, mouse_x, mouse_y, game.in_motherboard)
                elif name == "Lever":
                    new_mech = Lever(game.player, game.world, mouse_x, mouse_y, None)
                elif name == "Motherboard":
                    new_mech = Motherboard(game.player, game.world, mouse_x, mouse_y, None)
                elif name == "Random box":
                    new_mech = RandomBox(None)
                
                if game.in_motherboard is None:
                    game.world.mechanisms.append(new_mech)
                else:
                    idx = (mouse_x - Width // 2 - 300) // 19 + ((mouse_y + Width // 2 - 300) // 19 - 19) * 32
                    if 0 <= idx < len(game.in_motherboard.objects):
                        game.in_motherboard.objects[idx] = new_mech
                return new_mech
            return build(game, (64, 64), name, spawn_mechanism, check_player=False)

    return None

