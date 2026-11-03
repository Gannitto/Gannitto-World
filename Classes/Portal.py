from Assets import Portal_1, Portal_2
from Globals import Width, Height, win

class Portal:

	def __init__(self, world, player, mouse_x, mouse_y):

		self.x = (player.x + mouse_x - Width // 2) // 128
		self.y = (player.y + mouse_y - Height // 2) // 256
		a = False
		for object in world.visible_objects:
			if object.__class__ == Portal and (self.x, self.y) != (object.x, object.y):
				a = True
		if a:
			self.image = Portal_2
		else:
			self.image = Portal_1

	def main(self, world, player):

		for object in world.visible_objects:
			if object.__class__ == Portal and (self.x, self.y) != (object.x, object.y):
				if self.x * 128 <= player.x <= self.x * 128 + 128 and self.y * 256 - 256 <= player.y <= self.y * 256:
					player.x = object.x * 128
					player.y = object.y * 256 - 257
		
		win.blit(self.image, (self.x * 128 + Width // 2 - player.x, player.y - self.y * 256 + Height // 2))
