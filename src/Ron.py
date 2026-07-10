import pygame
import os
from config.Globals import path

X = 0
Y = 0
Home = [0, 0]
Ron_run = "Down"
costum = 0
changed_slot = 0
animation = [None, 0]
window = [False, 0]

down_images = [

	pygame.transform.scale(pygame.image.load(path + "assets/Images/Players/Ron/Normal/Down/1.png"), (256, 256))

	]

inventory = {"Bow": 0, "Arrow": 0, "Stick": 0, "Iron ingot": 0}

def show(x, y):

	from main  import win, Width, Height
	from engine.Functions import shadow

	match Ron_run:

		case "Down":

			win.blit(shadow(down_images[costum], "Ron Down" + str(costum), len_shadow=50), (X - x + Width // 2 - 128, y - Y + Height // 2 - 128))

def check_animations():
	...

def show_animations():
	...

def walk(x: int, y: int):
	
	global X, Y

	if Home is None:

		if not (-256 < X - x < 256):
			if X < x:
				X += 50
			elif x < X:
				X -= 50
		
		if not (-256 < Y - y < 256):
			if Y < y:
				Y += 50
			elif y < Y:
				Y -= 50

	else:

		if not (-256 < X - Home[0] < 256):
			if X < Home[0]:
				X += 30
			elif Home[0] < X:
				X -= 30
		
		if not (-256 < Y - Home[1] < 256):
			if Y < Home[1]:
				Y += 30
			elif Home[1] < Y:
				Y -= 30

def check_items(x, y, items: list, world):

	"""Проверяет лежащие предметы вокруг Рона"""

	global inventory, X, Y

	if Home is None:

		for object in items:

			if x - 256 <= object.x <= x + 256 and y - 256 <= object.y <= y + 256 and object.object_class == "Object" and object.special_flags == "Item" and object.name in ["Arrow", "Stick", "Iron ingot"]:
				
				if not (-32 < X - object.x < 32) and not (-32 < Y - object.y < 32):
					
					if X < object.x:
						X += 30
					elif object.x < X:
						X -= 30

					if Y < object.y:
						Y += 30
					elif object.y < Y:
						Y -= 30

					break

				else:

					inventory[object.name] += 1
					world.chunk_manager.get_chunk_at(object.x, object.y).objects.remove(object)
					break

	return items

def check_mobs(mobs: list, Width, Height, FPS, player_bullets: list, Bullet, x, y):

	"""Проверяет мобов вокруг Рона"""

	from random import randint
	
	for mob in mobs:

		if inventory["Arrow"] > 0 and X - Width // 2 <= mob.x <= X + Width // 2 and Y - Height // 2 <= mob.y <= Y + Height // 2 and mob.mob_class == "SlimeEnemy" and randint(1, FPS / 2) == 1:

			player_bullets.append(Bullet(X, Y, mob.x - x + Width // 2 - 64, y - mob.y + Height // 2 - 32, "Arrow"))

			break

	return mobs, player_bullets


def get_start_items():

	"""Выдаёт Рону в инвентарь начальные предметы"""

	inventory["Bow"] = 1
	inventory["Arrow"] = 99
