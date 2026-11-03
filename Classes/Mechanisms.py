import pygame
from Assets import wire_images, random_box_images
from Cache import load
from Globals import Width, Height, win, textInfo, path

class Wire:

	def __init__(self, player, world, mouse_x, mouse_y, in_motherboard):

		self.in_motherboard = in_motherboard
		if self.in_motherboard is None:
			self.x = (player.x + mouse_x - Width // 2) // 64
			self.y = (player.y - mouse_y + Height // 2) // 64
		else:
			self.x = (mouse_x - Width // 2 - 300) // 18.75
			self.y = (mouse_y + Width // 2 - 300) // 18.75
		self.condition = "Off"
		self.image = wire_images[0]
		self.neigbords = []
		self.neigbords_on = 0
		self.neigbords_none = 0
		self.num = len(world.mechanisms)
	
	def main(self, world, player):

		self.neigbords = []
		self.neigbords_on = 0
		self.neigbords_none = 0

		if self.in_motherboard is None:
			for mechanism in world.mechanisms:
				if mechanism.__class__ in (Wire, Lever, Motherboard):
					if ((mechanism.x == self.x and mechanism.y in (self.y + 1, self.y - 1)) or (mechanism.x in (self.x - 1, self.x + 1) and mechanism.y == self.y)) and mechanism.num != self.num:

						self.neigbords.append(mechanism)
						if mechanism.__class__ == Motherboard:

							if mechanism.left_condition == "On" and mechanism.x >= self.x:
								self.neigbords_on += 1
							if mechanism.left_condition is None and mechanism.x >= self.x:
								self.neigbords_none += 1
						else:

							if mechanism.condition == "On":
								self.neigbords_on += 1
							elif mechanism.condition is None:
								self.neigbords_none += 1

				elif mechanism.__class__ == RandomBox:

					if mechanism.x - self.x in (1, -1) and mechanism.y == self.y and mechanism.num != self.num:

						self.neigbords.append(mechanism)

						if mechanism.condition == "On":
							self.neigbords_on += 1
						elif mechanism.condition is None:
							self.condition = None

		else:

			for mechanism in self.in_motherboard.objects:

				if mechanism.__class__ in (Wire, Lever, Motherboard):
					if ((mechanism.x == self.x and mechanism.y in (self.y + 1, self.y - 1)) or (mechanism.x in (self.x - 1, self.x + 1) and mechanism.y == self.y)) and mechanism.num != self.num:
						self.neigbords.append(mechanism)
						if mechanism.condition == "On":
							self.neigbords_on += 1
						elif mechanism.condition is None:
							self.neigbords_none += 1

				elif mechanism.__class__ == RandomBox:

					if mechanism.x - self.x in (1, -1) and mechanism.y == self.y and mechanism.num != self.num:
						self.neigbords.append(mechanism)
						if mechanism.condition == "On":
							self.neigbords_on += 1
						elif mechanism.condition is None:
							self.condition = None

		if len(self.neigbords) == 1:

			if self.neigbords[0].x == self.x:
				self.image = wire_images[1]
			else:
				self.image = wire_images[0]

		elif len(self.neigbords) == 2:

			if self.neigbords[0].x == self.x == self.neigbords[1].x:
				self.image = wire_images[1]
			elif self.neigbords[0].y == self.y == self.neigbords[1].y:
				self.image = wire_images[0]
			elif (self.neigbords[0].x == self.x - 1 and self.neigbords[1].y == self.y + 1) or (self.neigbords[1].x == self.x - 1 and self.neigbords[0].y == self.y + 1):
				self.image = wire_images[2]
			elif (self.neigbords[0].x == self.x + 1 and self.neigbords[1].y == self.y + 1) or (self.neigbords[1].x == self.x + 1 and self.neigbords[0].y == self.y + 1):
				self.image = wire_images[3]
			elif (self.neigbords[0].x == self.x + 1 and self.neigbords[1].y == self.y - 1) or (self.neigbords[1].x == self.x + 1 and self.neigbords[0].y == self.y - 1):
				self.image = wire_images[4]
			elif (self.neigbords[0].x == self.x - 1 and self.neigbords[1].y == self.y - 1) or (self.neigbords[1].x == self.x - 1 and self.neigbords[0].y == self.y - 1):
				self.image = wire_images[5]

		elif len(self.neigbords) == 3:

			if self.neigbords[0].y != self.y + 1 and self.neigbords[1].y != self.y + 1 and self.neigbords[2].y != self.y + 1:
				self.image = wire_images[6]
			if self.neigbords[0].y != self.y - 1 and self.neigbords[1].y != self.y - 1 and self.neigbords[2].y != self.y - 1:
				self.image = wire_images[7]
			if self.neigbords[0].x != self.x + 1 and self.neigbords[1].x != self.x + 1 and self.neigbords[2].x != self.x + 1:
				self.image = wire_images[8]
			if self.neigbords[0].x != self.x - 1 and self.neigbords[1].x != self.x - 1 and self.neigbords[2].x != self.x - 1:
				self.image = wire_images[9]

		if len(self.neigbords) == 4:
			self.image = wire_images[10]

		if self.neigbords_on != 0 and self.condition == "Off":
			self.condition = "On"
		if self.condition is None:
			self.condition = "Off"
		elif self.neigbords_none != 0:
			self.condition = None
		
		if self.in_motherboard is None:

			win.blit(textInfo.render(self.condition, True, (0, 0, 0)), (self.x * 64 + Width // 2 - player.x, player.y - self.y * 64 + Height // 2 - 16))
			win.blit(self.image, (self.x * 64 + Width // 2 - player.x, player.y - self.y * 64 + Height // 2 - 16))

class Lever:

	def __init__(self, player, world, mouse_x, mouse_y, in_motherboard):

		self.in_motherboard = in_motherboard
		self.x = (player.x + mouse_x - Width // 2) // 64
		self.y = (player.y - mouse_y + Height // 2) // 64
		self.condition = False
		self.image1 = load(path + "Images/Objects/Lever 1.png", 64)
		self.image2 = load(path + "Images/Objects/Lever 2.png", 64)
		self.image = self.image1
		self.neigbords = []
		self.num = len(world.mechanisms)

	def main(self, world, player):

		click = pygame.mouse.get_pressed()
		mouse_x, mouse_y = pygame.mouse.get_pos()
		self.neigbords = []

		for mechanism in world.mechanisms:

			if mechanism.__class__ == Wire:
				if ((mechanism.x == self.x and mechanism.y in (self.y + 1, self.y - 1)) or (mechanism.x in (self.x - 1, self.x + 1) and mechanism.y == self.y)) and mechanism.num != self.num:
					self.neigbords.append(mechanism)

			elif mechanism.__class__ == RandomBox:
				if mechanism.x - self.x in (1, -1) and mechanism.y == self.y and mechanism.num != self.num:
					self.neigbords.append(mechanism)

		if click[0] and self.x * 64 + Width // 2 - player.x <= mouse_x <= self.x * 64 + Width // 2 - player.x + 64 and player.y - self.y * 64 + Height // 2 - 16 <= mouse_y <= player.y - self.y * 64 + Height // 2 - 16 + 64:

			if self.image == self.image1:
				self.image = self.image2
				self.condition = "On"
			else:
				self.image = self.image1
				self.condition = None

		win.blit(self.image, (self.x * 64 + Width // 2 - player.x, player.y - self.y * 64 + Height // 2 - 16))

class RandomBox:

	def __init__(self, player, world, mouse_x, mouse_y, in_motherboard):
		
		self.x = (player.x + mouse_x - Width // 2) // 64
		self.y = (player.y - mouse_y + Height // 2) // 64

		self.on = False
		self.image = random_box_images[0]
		self.neigbords = []
		self.neigbords_on = 0
		self.num = len(world.mechanisms)
		self.in_motherboard = in_motherboard
	
	def main(self, world, player):

		self.neigbords = []
		self.neigbords_on = 0

		for mechanism in world.mechanisms:

			if mechanism.y == self.y and mechanism.x - self.x in (1, -1) and mechanism.num != self.num:

				self.neigbords.append(mechanism)
				if mechanism.on:
					self.neigbords_on += 1
		
		if len(self.neigbords) == 1:

			if self.neigbords[0].x == self.x - 1:
				self.image = random_box_images[1]
			else:
				self.image = random_box_images[2]

		elif len(self.neigbords) == 2:
			self.image = random_box_images[3]

		else:
			self.image = random_box_images[0]
		
		win.blit(self.image, (self.x * 64 + Width // 2 - player.x, player.y - self.y * 64 + Height // 2 - 16))

class LogicGate:

	def __init__(self, player, world, mouse_x, mouse_y, in_motherboard):

		self.x = (player.x + mouse_x - Width // 2) // 64
		self.y = (player.y - mouse_y + Height // 2) // 64

		self.image = wire_images[10]
		self.neigbords = []
		self.neigbords_on = 0
		self.num = len(world.mechanisms)
		self.in_motherboard = in_motherboard
	
	def main(self, world, player):

		self.neigbords = []
		self.neigbords_on = 0

		for mechanism in world.mechanisms:

			if mechanism.__class__ in (Wire, Lever):

				if ((mechanism.x == self.x and mechanism.y in (self.y + 1, self.y - 1)) or (mechanism.x in (self.x - 1, self.x + 1) and mechanism.y == self.y)) and mechanism.num != self.num:
					self.neigbords.append(mechanism)
					if mechanism.condition == "On":
						self.neigbords_on += 1

			elif mechanism.__class__ == RandomBox:

				if mechanism.x - self.x in (1, -1) and mechanism.y == self.y and mechanism.num != self.num:
					self.neigbords.append(mechanism)
					if mechanism.condition == "On":
						self.neigbords_on += 1

		if len(self.neigbords) == 1:

			if self.neigbords[0].x == self.x:
				self.image = wire_images[1]
			else:
				self.image = wire_images[0]

		elif len(self.neigbords) == 2:
			if self.neigbords[0].x == self.x == self.neigbords[1].x:
				self.image = wire_images[1]
			elif self.neigbords[0].y == self.y == self.neigbords[1].y:
				self.image = wire_images[0]
			elif (self.neigbords[0].x == self.x - 1 and self.neigbords[1].y == self.y + 1) or (self.neigbords[1].x == self.x - 1 and self.neigbords[0].y == self.y + 1):
				self.image = wire_images[2]
			elif (self.neigbords[0].x == self.x + 1 and self.neigbords[1].y == self.y + 1) or (self.neigbords[1].x == self.x + 1 and self.neigbords[0].y == self.y + 1):
				self.image = wire_images[3]
			elif (self.neigbords[0].x == self.x + 1 and self.neigbords[1].y == self.y - 1) or (self.neigbords[1].x == self.x + 1 and self.neigbords[0].y == self.y - 1):
				self.image = wire_images[4]
			elif (self.neigbords[0].x == self.x - 1 and self.neigbords[1].y == self.y - 1) or (self.neigbords[1].x == self.x - 1 and self.neigbords[0].y == self.y - 1):
				self.image = wire_images[5]

		elif len(self.neigbords) == 3:
			if self.neigbords[0].y != self.y + 1 and self.neigbords[1].y != self.y + 1 and self.neigbords[2].y != self.y + 1:
				self.image = wire_images[6]
			if self.neigbords[0].y != self.y - 1 and self.neigbords[1].y != self.y - 1 and self.neigbords[2].y != self.y - 1:
				self.image = wire_images[7]
			if self.neigbords[0].x != self.x + 1 and self.neigbords[1].x != self.x + 1 and self.neigbords[2].x != self.x + 1:
				self.image = wire_images[8]
			if self.neigbords[0].x != self.x - 1 and self.neigbords[1].x != self.x - 1 and self.neigbords[2].x != self.x - 1:
				self.image = wire_images[9]

		if len(self.neigbords) == 4:
			self.image = wire_images[10]

		if self.neigbords_on != 0 and self.condition == "Off":
			self.condition = "On"
		if self.condition is None:
			self.condition = "Off"
		elif self.neigbords_none != 0:
			self.condition = None
		
		if not self.in_motherboard:
			win.blit(self.image, (self.x * 64 + Width // 2 - player.x, player.y - self.y * 64 + Height // 2 - 16))

class Motherboard:

	def __init__(self, player, world, mouse_x, mouse_y, in_motherboard):

		self.x = (player.x + mouse_x - Width // 2) // 64
		self.y = (player.y - mouse_y + Height // 2) // 64

		self.condition = "Off"
		self.image = load(path + "Images/Objects/Motherboard.png", 64)
		self.neigbords = []
		self.neigbords_on = 0
		self.neigbords_none = 0
		self.num = len(world.mechanisms)
		self.in_motherboard = in_motherboard
		self.objects = [None] * 1024
		self.objects_left = []
		self.objects_left_xy = []
		self.left_condition = "Off"
		self.objects_right = []
		self.objects_right_xy = []
		self.right_condition = "Off"
		self.objects_up = []
		self.objects_up_xy = []
		self.up_condition = "Off"
		self.objects_down = []
		self.objects_down_xy = []
		self.down_condition = "Off"
	
	def main(self, world, player):

		self.neigbords = []
		self.neigbords_on = 0
		self.neigbords_none = 0

		self.objects_left = []
		self.objects_left_xy = []
		self.objects_right = []
		self.objects_right_xy = []
		self.objects_up = []
		self.objects_up_xy = []
		self.objects_down = []
		self.objects_down_xy = []

		for mechanism in world.mechanisms:

			if mechanism.__class__ in (Wire, Lever, Motherboard):

				if ((mechanism.x == self.x and mechanism.y in (self.y + 1, self.y - 1)) or (mechanism.x in (self.x - 1, self.x + 1) and mechanism.y == self.y)) and mechanism.num != self.num:
					self.neigbords.append(mechanism)
					if mechanism.condition == "On" and mechanism.x <= self.x and self.left_condition == "Off":
						self.left_condition = "On"
					elif mechanism.condition is None and mechanism.x <= self.x:
						self.left_condition = None

			elif mechanism.__class__ == RandomBox:

				if mechanism.x - self.x in (1, -1) and mechanism.y == self.y and mechanism.num != self.num:
					self.neigbords.append(mechanism)
					if mechanism.condition == "On":
						self.neigbords_on += 1
					elif mechanism.condition is None:
						self.condition = None

		for i in self.objects:

			if i is not None:

				if i.x + 32 == 0:

					self.objects_left.append(i.condition)
					self.objects_left_xy.append(i)
				
				elif i.x == -1:
					self.objects_right.append(i.condition)
					self.objects_right_xy.append(i)

				if i.y == 21:

					self.objects_up.append(i.condition)
					self.objects_up_xy.append(i)

				elif i.y == 52:

					self.objects_down.append(i.condition)
					self.objects_down_xy.append(i)
					
		if (any(self.objects_left) and self.left_condition == "Off") or self.left_condition == "On":

			self.left_condition = "On"

			for i in self.objects_left_xy:
				if self.objects[self.objects.index(i)].condition == "Off":
					self.objects[self.objects.index(i)].condition = "On"

		if self.left_condition is None:
			self.left_condition = "Off"

		elif None in self.objects_left:
			self.left_condition = None
			for i in self.objects_left_xy:
				self.objects[self.objects.index(i)].condition = None
		
		self.get_pressed(player)

		if not self.in_motherboard:
			win.blit(self.image, (self.x * 64 + Width // 2 - player.x, player.y - self.y * 64 + Height // 2 - 16))

	def get_pressed(self, player):

		mouse_x, mouse_y = pygame.mouse.get_pos()
		if self.in_motherboard is None:
			if self.x * 64 + Width // 2 - player.x <= mouse_x <= self.x * 64 + Width // 2 - player.x + 64 and player.y - self.y * 64 + Height // 2 - 16 <= mouse_y <= player.y - self.y * 64 + Height // 2 - 16 + 64 and in_motherboard is None and pygame.mouse.get_pressed()[0]:
				in_motherboard = self
