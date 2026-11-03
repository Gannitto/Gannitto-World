import pygame
from Assets import Backrooms_portal_images
from Globals import Width, Height, win, Settings

class BackroomsPortal:

	def __init__(self, X: int, Y: int):

		self.image = 0
		self.rect = Backrooms_portal_images[0].get_rect()
		self.x = X
		self.y = Y

	def main(self, player):

		win.blit(Backrooms_portal_images[self.image], (self.x - player.x + Width // 2 - 128, player.y - self.y + Height // 2 - 128))

		self.image += 1
		if self.image == 10:
			self.image = 0

		if Settings["Display"][3]:
			pygame.draw.rect(win, (0, 0, 0), (self.x - player.x + Width // 2 - 128, player.y - self.y + Height // 2 - 128, 256, 256), 3)

