from Assets import Heart
from Translator import t
from Globals import Width, Height, win

class BarRenderer:

	def __init__(self, game):
		self.game = game

	def show_health_bar(self, mouse_x, mouse_y):
		if self.game.player.god_mode:
			return
		for heart_x in range(self.game.player.HP // 10):
			win.blit(Heart, (Width - 50 - heart_x * 40, 10))
		if Width - 10 - self.game.player.HP // 10 * 40 < mouse_x < Width - 10 and 40 < mouse_y < 104:
			mouse_object = t("Health bar")
