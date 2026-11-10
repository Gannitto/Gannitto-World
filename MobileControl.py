from Assets import arrow_down, arrow_left, arrow_right, arrow_up, Open_inventory_slot, Open_inventory_slot2
from Classes import Button
from Globals import Width, Height, win
from Config import Settings

class MobileControl:
	def __init__(self, game):
		self.game = game
		self.init_buttons()

	def init_buttons(self):

		self.up_b = Button(Width - 148, Height - 148, arrow_up, arrow_up, sound=False, cooldown=0)
		self.left_b = Button(Width - 222, Height - 74, arrow_left, arrow_left, sound=False, cooldown=0)
		self.down_b = Button(Width - 148, Height - 74, arrow_down, arrow_down, sound=False, cooldown=0)
		self.right_b = Button(Width - 74, Height - 74, arrow_right, arrow_right, sound=False, cooldown=0)

	def show_buttons(self, mouse_x, mouse_y, click):
		if Settings["Game"]["Telephone control"]:

			self.up_b.main()
			self.left_b.main()
			self.down_b.main()
			self.right_b.main()
			if self.game.inventory_open:
				win.blit(Open_inventory_slot2, (890, 10))
				if 890 <= mouse_x <= 954 and 10 <= mouse_y <= 74 and click[0]:
					self.game.inventory_open = False
			else:
				win.blit(Open_inventory_slot, (810, 10))
				if 810 <= mouse_x <= 874 and 10 <= mouse_y <= 74 and click[0]:
					self.game.inventory_open = True
		
