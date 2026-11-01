import pygame
import os
import random
from Globals import path, Settings

sounds = {}
for root, dirs, files in os.walk(path + "Sounds/"):
	for file in files:
		sounds[file[:-4]] = pygame.mixer.Sound(os.path.join(root, file))

music_channel = pygame.mixer.Channel(1)
music_channel.set_volume(Settings["Sound"][0], Settings["Sound"][0])
def play_sound(sound, rand_num=0, loops=0, maxtime=0, fade_ms=0):
	if rand_num != 0:
		sound += " " + str(random.randint(1, rand_num))
	channel = pygame.mixer.find_channel(force=True)
	if channel is not None:
		channel.play(sounds[sound], loops, maxtime, fade_ms)

sound_channels = [
	pygame.mixer.Channel(i) for i in range(pygame.mixer.get_num_channels()) if i != 1
]
def set_sound_volume(volume):
	"""Устанавливает громкость для всех эффектов (от 0.0 до 1.0)"""
	for channel in sound_channels:
		channel.set_volume(volume)

set_sound_volume(Settings["Sound"][1] / 100)
