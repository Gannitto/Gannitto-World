import pygame
import os
import random
from Globals import path, Settings

sounds = {}
for root, dirs, files in os.walk(path + "Sounds/"):
	for file in files:
		name, _ = os.path.splitext(file)
		sounds[name] = pygame.mixer.Sound(os.path.join(root, file))

music_channel = pygame.mixer.Channel(0)
music_channel.set_volume(Settings["Sound"][0], Settings["Sound"][0])
def play_sound(sound, rand_num=0, loops=0, maxtime=0, fade_ms=0):
	if rand_num != 0:
		sound += " " + str(random.randint(1, rand_num))
	if sound in sounds:
		channel = pygame.mixer.find_channel(force=True)
		channel.play(sounds[sound], loops, maxtime, fade_ms)

sound_channels = [
	pygame.mixer.Channel(i) for i in range(pygame.mixer.get_num_channels()) if i != 1
]
def set_sound_volume(volume):
	"""Устанавливает громкость для всех эффектов (от 0.0 до 1.0)"""
	for channel in sound_channels:
		channel.set_volume(volume)

set_sound_volume(Settings["Sound"][1] / 100)

def update_sounds(game, player, world):
	if game.time_system.day_phase == "Night" and not game.night_playing:
		music_channel.stop()
		music_channel.play(pygame.mixer.Sound(path + "Soundtracks/Night " + str(random.randint(1, 2)) + ".mp3"))
		game.night_playing = True

	elif not music_channel.get_busy() or (game.night_playing and game.time_system.day_phase != "Night"):

		game.night_playing = False
		music_channel.stop()

		match game.current_biome:

			case "Forest" | "Field":
				music_channel.queue(pygame.mixer.Sound(path + "Soundtracks/Forest " + str(random.randint(1, 3)) + ".mp3"))
				
			case "Desert":
				music_channel.queue(pygame.mixer.Sound(path + "Soundtracks/Desert " + str(random.randint(1, 2)) + ".mp3"))
				
			case "Swamp":
				music_channel.queue(pygame.mixer.Sound(path + "Soundtracks/Swamp " + str(random.randint(1, 2)) + ".mp3"))
				
			case "Taiga":
				music_channel.queue(pygame.mixer.Sound(path + "Soundtracks/Taiga " + str(random.randint(1, 1)) + ".mp3"))

	if player.animation_timer == 0 and (player.frame_index % 6 == 2 or player.frame_index % 6 == 5):

		if world.current_cave is not None:
			play_sound("Cave walking", 3)

		elif game.current_biome in ("Forest", "Field"):
			play_sound("Grass walking", 3)

		elif game.current_biome == "Desert":
			play_sound("Sand walking", 3)

		elif game.current_biome == "Taiga":
			play_sound("Snow walking", 3)

		elif game.current_biome == "Swamp":
			play_sound("Swamp walking", 3)

