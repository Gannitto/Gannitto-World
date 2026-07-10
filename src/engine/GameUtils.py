import pygame
import time
import random
from config.Globals import * 
from engine.Functions import win_darken, win_fill
import Saver
import Backrooms
import Ron
import sys

def save(darken:bool=True, save_world_settings:bool=False):
	global player
	Saver.save_objects(path + "Settings/Statistics.save", statistics)
	
	if world_name is not None:
		
		if multyplayer:
			another_players = []
			for player in ...:
				another_players.append(...)   # TODO
				another_players.append(...)
				
		else:

			Saver.save_objects(path + "Worlds/" + world_name + "/Mobs.save", mobs)
			Saver.save_objects(path + "Worlds/" + world_name + "/Info.save", [player.x, player.y, Backrooms.InBackrooms, Backrooms.Level, world.current_cave, player.speed, player.HP, start_time, Ron.X, Ron.Y, Ron.Home, world.chunk_manager.generator.seed])
			Saver.save_objects(path + "Worlds/" + world_name + "/Inventory.save", inventory.whole_inventory)
			Saver.save_objects(path + "Worlds/" + world_name + "/Resources.save", inventory.resources)
			Saver.save_objects(path + "Worlds/" + world_name + "/Effects.save", player.effects)

			new_particles = particles.copy()
			particle_count = 1
			for particle in new_particles:
				if particle.save_particle:
					pygame.image.save(particle.image, path + "Worlds/" + world_name +"/Images/Particle " + str(particle_count) + ".png")
					particle.image_path = path + "Worlds/Images/Particle " + str(particle_count) + ".png"
					particle_count += 1
				else: new_particles.remove(particle)
			Saver.save_objects(path + "Worlds/" + world_name + "/Particles.save", new_particles)
			world.chunk_manager.save_all_loaded_chunks()
				
	if darken and Settings["Display"][9]:
		win_darken(win.copy())
		
	if save_world_settings and world_name is not None:
		Saver.save_objects(path + "Worlds/" + world_name + "/Settings.save", [difficulty, player.god_mode])

def chat_message(message: str):
	global chat_tick
	chat.append(message)
	chat_tick = len(message) // 1.5 * FPS

display_image = lambda X, Y, W, H: (X - player.x + Width // 2 - W // 2, player.y - Y + Height // 2 - H // 2)

def tp(X: int, Y: int):
	global player
	player.x, player.y = X, Y
