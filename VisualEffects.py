import pygame
from Functions import win, win_fill, Width, Height

# Пока что тут только эффект урона, но в будущем визуальные эффекты будут добавляться именно в этот модуль

class VisualEffects:
	def __init__(self, game):
		self.game = game

	def show_effects(self):

		if self.game.player.HP_animation_tick > 0 and not self.game.player.god_mode:
			self._damage()

	def _damage(self):
			self.game.player.HP_animation_tick += 1
			
			if self.game.player.HP_animation_tick < 6:
				win_fill((200, 0, 0), self.game.player.HP_animation_tick * 20)
				win.blit(pygame.transform.scale(win, (Width + self.game.player.HP_animation_tick * 2, Height + self.game.player.HP_animation_tick * 2)), (-self.game.player.HP_animation_tick, -self.game.player.HP_animation_tick))
			else:
				win_fill((200, 0, 0), (self.game.player.HP_animation_tick - 10 - self.game.player.HP_animation_tick - 10) * 20)

			if self.game.player.HP_animation_tick == 21:
				self.game.player.HP_animation_tick = 0

