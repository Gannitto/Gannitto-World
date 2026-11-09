import pygame
from Functions import win, win_fill, Width, Height

# Пока что тут только эффект урона, но в будущем визуальные эффекты будут добавляться именно в этот модуль

class VisualEffects:
	def __init__(self, game):
		self.game = game

	def show_effects(self, dt):

		if self.game.player.damage_timer > 0 and not self.game.player.god_mode:
			self._damage(dt)

	def _damage(self, dt):
		self.game.player.damage_timer = max(self.game.player.damage_timer - dt, 0)
		
		if self.game.player.damage_timer < self.game.player.damage_cooldown / 2:
			damage_value = self.game.player.damage_timer / self.game.player.damage_cooldown
		else:
			damage_value = (self.game.player.damage_cooldown - self.game.player.damage_timer) / self.game.player.damage_cooldown
		win_fill((200, 0, 0), damage_value * 150)

