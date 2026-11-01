import pygame
from Globals import path, Settings

Button_click = pygame.mixer.Sound(path + "Sounds/Button Pressed.mp3")
Stone_breaking1 = pygame.mixer.Sound(path + "Sounds/Stone breaking 1.mp3")
Stone_breaking2 = pygame.mixer.Sound(path + "Sounds/Stone breaking 2.mp3")
Grass_walking1 = pygame.mixer.Sound(path + "Sounds/Grass walking 1.mp3")
Grass_walking2 = pygame.mixer.Sound(path + "Sounds/Grass walking 2.mp3")
Grass_walking3 = pygame.mixer.Sound(path + "Sounds/Grass walking 3.mp3")
Snow_walking1 = pygame.mixer.Sound(path + "Sounds/Snow walking 1.mp3")
Snow_walking2 = pygame.mixer.Sound(path + "Sounds/Snow walking 2.mp3")
Snow_walking3 = pygame.mixer.Sound(path + "Sounds/Snow walking 3.mp3")
Sand_walking1 = pygame.mixer.Sound(path + "Sounds/Sand walking 1.mp3")
Sand_walking2 = pygame.mixer.Sound(path + "Sounds/Sand walking 2.mp3")
Sand_walking3 = pygame.mixer.Sound(path + "Sounds/Sand walking 3.mp3")
Swamp_walking1 = pygame.mixer.Sound(path + "Sounds/Swamp walking 1.mp3")
Swamp_walking2 = pygame.mixer.Sound(path + "Sounds/Swamp walking 2.mp3")
Swamp_walking3 = pygame.mixer.Sound(path + "Sounds/Swamp walking 3.mp3")
Cave_walking1 = pygame.mixer.Sound(path + "Sounds/Cave walking 1.mp3")
Cave_walking2 = pygame.mixer.Sound(path + "Sounds/Cave walking 2.mp3")
Cave_walking3 = pygame.mixer.Sound(path + "Sounds/Cave walking 3.mp3")
Backrooms_lamps = pygame.mixer.Sound(path + "Sounds/Backrooms/1.mp3")
Backrooms_rand_sound_1 = pygame.mixer.Sound(path + "Sounds/Backrooms/Random Sounds/1.mp3")
Pick_an_item = pygame.mixer.Sound(path + "Sounds/Pick an item.mp3")

music_channel = pygame.mixer.Channel(1)
music_channel.set_volume(Settings["Sound"][0], Settings["Sound"][0])
def play_sound(sound, loops=0, maxtime=0, fade_ms=0):
	pygame.mixer.find_channel().play(sound, loops, maxtime, fade_ms)
sound_channels = [
	pygame.mixer.Channel(i) for i in range(pygame.mixer.get_num_channels()) if i != 1
]
def set_sound_volume(volume):
	"""Устанавливает громкость для всех эффектов (от 0.0 до 1.0)"""
	for channel in sound_channels:
		channel.set_volume(volume)

set_sound_volume(Settings["Sound"][1] / 100)
