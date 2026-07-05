import random

class BigRect:

	def __init__(self, rect_x: int, rect_y: int):

		self.x = rect_x
		self.y = rect_y
		self.biom = random.choice(("Forest", "Desert", "Field", "Taiga", "Swamp"))
		
	def generate(self, objects, items):

		from Globals import win, textInfo, Width, Height
		from Gannitto_world import Object
		import pygame
		import os
		try:
			path = os.path.abspath(__file__)[:-27]
			Bush = pygame.image.load(path + "Gannitto world/files/Images/Objects/Bush.png")
		except:
			path = os.path.abspath(__file__)[:-32]
		clock = pygame.time.Clock()
		a = True
		b = False
		#while a:
		#    for object in objects:
		#        if self.x - 50000 <= object.x <= self.x + 5000 and self.y - 5000 <= object.y <= self.y + 5000 and object.__class__ == Object:
		#            del object
		#            b = True
		#            break
		#    if not b:
		#        a = False
		#    else:
		#        b = False

		win.fill((192, 203, 220))
		pygame.draw.rect(win, (58, 68, 102), (0, 0, Width, Height), 10)
		pygame.draw.rect(win, (139, 155, 180), (10, 10, Width - 20, Height - 20), 10)

		match self.biom:

			case "Forest":
			
				Pond = pygame.image.load(path + "Gannitto world/files/Images/Objects/Pond.png")
				Reed = pygame.image.load(path + "Gannitto world/files/Images/Objects/Reed.png")
				for _ in range(random.randint(100, 500)):
					x, y = random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000)
					objects.append(Object(
						"Pond",
						x, y,
						"Gannitto world/files/Images/Objects/Pond.png", (512, 512), Pond, special_flags=[100, random.randint(10, 30)]))
					for _ in range(random.randint(2, 5)):
						objects.append(Object(
							"Reed",
							x + random.randint(-100, 612), y + random.randint(-100, 612),
							"Gannitto world/files/Images/Objects/Reed.png", (256, 256), Reed))

				from Gannitto_world import Cave
				for _ in range(random.randint(10, 30)):
					a, b = random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000)
					objects.append(Cave(a, b, 10000, 10000))

		return objects, items

