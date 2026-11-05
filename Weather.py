import random
from Assets import drop_texture
from Globals import Width, Height
from Classes import Particle

class WeatherSystem():
	def __init__(self, world):

		self.world = world
		self.weather = "Clear"

	def update(self):
		if random.randint(1, 18000) == 1: self.weather = random.choice(("Clear", "Rain"))

	def draw(self):

		match self.weather:
			
			case "Rain":
				offset = random.randint(-10, 10)
				for _ in range(15):
					self.world.particles.append(Particle(random.randint(1, Width), -50, drop_texture,  x_bias=random.randint(-5, 5) + offset, y_bias=random.randint(30, 40), display_mode=lambda X, Y, w, h: (X, Y), end_y=Height, end_zone=30))

