import pygame
import random
from Globals import win, Width, Height
from Classes import Particle

class PlayerAnimations:
	def __init__(self, game):
		self.game = game

	def handle_animations(self):
		
		player = self.game.player

		if player.animation[0] is None:
			
			if random.randint(1, 300) == 1:
				player.animation = ["Close eyes", 0, 16]

		elif player.animation[1] <= player.animation[2]:
			player.animation[1] += 1
		else:
			player.animation = [None, 0]

		player.changed_item_x = 0
		player.changed_item_y = 0
		frame = player.frame_index % len(player.animations[player.direction])

		match player.direction:

			case "Down":

				match frame:
					# 97, 209
					case 0 | 1 | 3 | 4 | 6 | 7:

						player.changed_item_x = Width // 2 - 80
						player.changed_item_y = Height // 2

						match player.animation[0]:

							case "Close eyes":

								if player.animation[1] < 9:
									win.fill(player.eye_color, (Width // 2 - 24, Height / 2 - 32, 8, player.animation[1] * 2))
									win.fill(player.eye_color, (Width // 2 + 16, Height / 2 - 32, 8, player.animation[1] * 2))
								else:
									win.fill(player.eye_color, (Width // 2 - 24, Height / 2 - 32, 8, (8 - player.animation[1] + 8) * 2))
									win.fill(player.eye_color, (Width // 2 + 16, Height / 2 - 32, 8, (8 - player.animation[1] + 8) * 2))

						match frame:

							case 1 | 3:
								
								a = pygame.Surface((16, 24))
								a.fill((0, 0, 0))
								a.set_alpha(90)
								self.game.world.particles.append(Particle(player.x + 16, player.y + 96, a, end_time=3))

							case 4 | 6:

								a = pygame.Surface((16, 24))
								a.fill((0, 0, 0))
								a.set_alpha(90)
								self.game.world.particles.append(Particle(player.x - 32, player.y + 96, a, end_time=3))

					case 2:

						player.changed_item_x = Width // 2 - 74
						player.changed_item_y = Height // 2 - 16

						match player.animation[0]:

							case "Close eyes":

								if player.animation[1] < 9:
									win.fill(player.eye_color, (Width // 2 - 24, Height / 2 - 24, 8, player.animation[1] * 2))
									win.fill(player.eye_color, (Width // 2 + 16, Height / 2 - 24, 8, player.animation[1] * 2))
								else:
									win.fill(player.eye_color, (Width // 2 - 24, Height / 2 - 24, 8, (8 - player.animation[1] + 8) * 2))
									win.fill(player.eye_color, (Width // 2 + 16, Height / 2 - 24, 8, (8 - player.animation[1] + 8) * 2))

					case 5:

						player.changed_item_x = Width // 2 - 94
						player.changed_item_y = Height // 2 - 16

						match player.animation[0]:

							case "Close eyes":

								if player.animation[1] < 9:
									win.fill(player.eye_color, (Width // 2 - 24, Height / 2 - 24, 8, player.animation[1] * 2))
									win.fill(player.eye_color, (Width // 2 + 16, Height / 2 - 24, 8, player.animation[1] * 2))
								else:
									win.fill(player.eye_color, (Width // 2 - 24, Height / 2 - 24, 8, (8 - player.animation[1] + 8) * 2))
									win.fill(player.eye_color, (Width // 2 + 16, Height / 2 - 24, 8, (8 - player.animation[1] + 8) * 2))

			case "Left":

				match frame:

					case 0 | 1 | 3 | 4 | 6 | 7:

						player.changed_item_x = Width // 2 - 84
						player.changed_item_y = Height // 2 - 16

						match player.animation[0]:

							case "Close eyes":

								if player.animation[1] < 9:
									win.fill(player.eye_color, (Width // 2 - 24, Height / 2 - 32, 8, player.animation[1] * 2))
								else:
									win.fill(player.eye_color, (Width // 2 - 24, Height / 2 - 32, 8, (8 - player.animation[1] + 8) * 2))

					case 2:

						player.changed_item_x = Width // 2 - 104
						player.changed_item_y = Height // 2

						match player.animation[0]:

							case "Close eyes":

								if player.animation[1] < 9:
									win.fill(player.eye_color, (Width // 2 - 24, Height / 2 - 24, 8, player.animation[1] * 2))
								else:
									win.fill(player.eye_color, (Width // 2 - 24, Height / 2 - 24, 8, (8 - player.animation[1] + 8) * 2))

					case 5:

						player.changed_item_x = Width // 2 - 70
						player.changed_item_y = Height // 2

						match player.animation[0]:

							case "Close eyes":

								if player.animation[1] < 9:
									win.fill(player.eye_color, (Width // 2 - 24, Height / 2 - 24, 8, player.animation[1] * 2))
								else:
									win.fill(player.eye_color, (Width // 2 - 24, Height / 2 - 24, 8, (8 - player.animation[1] + 8) * 2))

			case "Right":

				match frame:

					case 0 | 1 | 3 | 4:

						player.changed_item_x = Width // 2 - 20
						player.changed_item_y = Height // 2

						match player.animation[0]:

							case "Close eyes":

								if player.animation[1] < 9:
									win.fill(player.eye_color, (Width // 2 + 16, Height / 2 - 32, 8, player.animation[1] * 2))
								else:
									win.fill(player.eye_color, (Width // 2 + 16, Height / 2 - 32, 8, (8 - player.animation[1] + 8) * 2))

					case 2:

						player.changed_item_x = Width // 2 - 32
						player.changed_item_y = Height // 2

						match player.animation[0]:

							case "Close eyes":

								if player.animation[1] < 9:
									win.fill(player.eye_color, (Width // 2 + 16, Height / 2 - 24, 8, player.animation[1] * 2))
								else:
									win.fill(player.eye_color, (Width // 2 + 16, Height / 2 - 24, 8, (8 - player.animation[1] + 8) * 2))

					case 5 | 6 | 7:

						player.changed_item_x = Width // 2 - 16
						player.changed_item_y = Height // 2 + 16

						match player.animation[0]:

							case "Close eyes":

								if player.animation[1] < 9:
									win.fill(player.eye_color, (Width // 2 + 16, Height / 2 - 24, 8, player.animation[1] * 2))
								else:
									win.fill(player.eye_color, (Width // 2 + 16, Height / 2 - 24, 8, (8 - player.animation[1] + 8) * 2))

