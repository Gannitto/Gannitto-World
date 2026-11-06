import pygame
import random
from Globals import Width, Height, textInfo, text_color, win

class EffectsSystem:
	def __init__(self):
		self.effects = []
	def handle_effects(self, dt):
		
		for effect_y, effect in enumerate(self.effects):

			win.blit(textInfo.render(effect[0], True, text_color, (0, 0, 0, 0.5)), (Width - 30 - textInfo.size(effect[0])[0], effect_y * 60 + 100))
			win.blit(textInfo.render(str(int(effect[1])), True, text_color, (0, 0, 0, 0.5)), (Width - 30 - textInfo.size(str(int(effect[1])))[0], effect_y * 60 + 130))

			match effect[0]:
				case "Drunk":
					d = pygame.Surface((Width, Height))
					d.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
					d.set_alpha(90)
					win.blit(d, (0, 0))

					for _ in range(10000):
						win.set_at((random.randint(0, Width), random.randint(0, Height)), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
						
					win.blit(win, (random.randint(-10, 10), random.randint(-10, 10)))

			effect[1] -= dt
			if effect[1] <= 0:
				self.effects.remove(effect)
		
