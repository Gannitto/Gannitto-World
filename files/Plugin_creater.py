import pygame
import os
import Saver
import getpass
import time
from Globals import path

pygame.init()
win = pygame.display.set_mode((800,500), pygame.RESIZABLE)
clock = pygame.time.Clock()
textInfo = pygame.font.Font("Font.ttf", 18)
Width, Height = pygame.display.get_surface().get_size()
pygame.display.set_icon(pygame.image.load("Icon.ico"))
pygame.display.set_caption("Plugin creater")

class Button:

	def __init__(self, x: int, y: int, image1: pygame.Surface, image2: pygame.Surface, surface):
		self.w = image1.get_width()
		self.h = image1.get_height()
		self.x = x
		self.y = y
		self.image = image1
		self.image1 = image1
		self.image2 = image2
		self.surface = surface
	
	def main(self, action=None):
		"""Shows the button"""
		import time

		mouse_x, mouse_y = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		if self.x - self.w / 2 < mouse_x < self.x + self.w / 2 and self.y - self.h / 2 < mouse_y < self.y + self.h / 2:
			self.image = self.image2
			if click[0] == 1:
				time.sleep(0.1)
				pygame.mixer.Sound.play(pygame.mixer.Sound(path + "Gannitto-World/files/Sounds/Button Pressed.mp3"))
				if action is not None:
					action()
		else:
			self.image = self.image1
		
		self.surface.blit(self.image, (self.x - self.w / 2, self.y - self.h / 2))

	def get_pressed(self) -> bool:
		
		mouse_x, mouse_y = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		if self.x - self.w / 2 < mouse_x < self.x + self.w / 2 and self.y - self.h / 2 < mouse_y < self.y + self.h / 2:
			self.image = self.image2
			if click[0] == 1:
				return True
		else:
			self.image = self.image1
			return False

create_new_plugin_but = Button(Width // 2, Height // 2 - 30, textInfo.render("Create new plugin", True, (139, 155, 180)), textInfo.render("Create new plugin", True, (58, 68, 102)), win)
my_plugins_but = Button(Width // 2, Height // 2 + 30, textInfo.render("My plugins", True, (139, 155, 180)), textInfo.render("My plugins", True, (58, 68, 102)), win)
upload_plugin_but = Button(Width // 2, Height // 2, textInfo.render("Upload plugin", True, (139, 155, 180)), textInfo.render("Upload blugin", True, (58, 68, 102)), win)

add_but = Button(Width // 2, 50, textInfo.render("Add", True, (139, 155, 180)), textInfo.render("Add", True, (58, 68, 102)), win)
export_but = Button(Width // 2, Height - 50, textInfo.render("Export", True, (139, 155, 180)), textInfo.render("Export", True, (58, 68, 102)), win)

item_but = Button(Width // 2, 150, textInfo.render("Item", True, (139, 155, 180)), textInfo.render("Item", True, (58, 68, 102)), win)
recipe_but = Button(Width // 2, 190, textInfo.render("Recipe", True, (139, 155, 180)), textInfo.render("Recipe", True, (58, 68, 102)), win)
object_but = Button(Width // 2, 240, textInfo.render("Object", True, (139, 155, 180)), textInfo.render("Object", True, (58, 68, 102)), win)
command_but = Button(Width // 2, 290, textInfo.render("Command", True, (139, 155, 180)), textInfo.render("Command", True, (58, 68, 102)), win)

def create_new_plugin():

	global Width, Height, mouse_x, mouse_y
	input_text = ""
	stage = 1
	additions = []
	editable_element = 0
	editable_part = 0

	while 1:

		Width, Height = pygame.display.get_surface().get_size()
		keys = pygame.key.get_pressed()
		mouse_x, mouse_y = pygame.mouse.get_pos()

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				quit()

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE:
					input_text = input_text[:-1]
				elif event.key != pygame.K_RETURN:
					input_text += event.unicode

		win.fill((192, 203, 220))
		
		pygame.draw.rect(win, (58, 68, 102), (0, 0, Width, Height), 10)
		pygame.draw.rect(win, (139, 155, 180), (10, 10, Width - 20, Height - 20), 10)

		match stage:

			case 1:

				win.blit(textInfo.render("Enter plugin name:", True, (139, 155, 180)), ((Width - textInfo.size("Enter plugin name:")[0]) // 2, Height // 2 - 50))
				win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
				if keys[pygame.K_RETURN] and input_text != "":
					plugin_name = input_text
					input_text = ""
					stage += 1
			case 2:
				add_but.main()
				export_but.main()
				a = -1
				for i in additions:
					a += 1
					win.blit(textInfo.render(i[0], True, (139, 155, 180)), (50, 50 + a * 94))
					match i[0]:
						case "Item":
							try:
								win.blit(pygame.transform.scale(pygame.image.load(i[2]), (64, 64)), (textInfo.size(i[0])[0] + 100, 50 + a * 94))
							except FileNotFoundError:
								win.blit(pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/No-file texture.png"), (64, 64)), (textInfo.size(i[0])[0] + 100, 50 + a * 94))
							if 50 <= mouse_x <= 50 + textInfo.size(i[0])[0] and 50 + a * 94 <= mouse_y <= 50 + a * 94 + textInfo.size(i[0])[1] and click[0]:
								win.blit(textInfo.render(i[0], True, (58, 68, 102)), (50, 50 + a * 94))
								stage += 1
								editable_element = a - 1
								editable_part = 0

				if add_but.get_pressed():
					stage += 1
					additions.append([])
					editable_element = len(additions) - 1

				if export_but.get_pressed() and additions != []:
					stage = 4
			case 3:

				if additions[editable_element] != [] and editable_part == 0:
					editable_part += 1
					input_text = additions[editable_element][1]
					a = False
				if editable_part == 0:
					win.blit(textInfo.render("Choose the addition type", True, (139, 155, 180)), ((Width - textInfo.size("Choose the addition type")[0]) // 2, 80))

					item_but.main()
					if item_but.get_pressed():
						editable_part += 1
						additions[editable_element].append("Item")
						additions[editable_element].append("")
						input_text = additions[editable_element][editable_part]
						a = True

					recipe_but.main()
					if recipe_but.get_pressed():
						editable_part += 1
						additions[editable_element].append("Recipe")
						additions[editable_element].append("")
						input_text = additions[editable_element][editable_part]
						a = True
						
					object_but.main()
					if object_but.get_pressed():
						editable_part += 1
						additions[editable_element].append("Object")
						additions[editable_element].append("")
						input_text = additions[editable_element][editable_part]
						a = True

					command_but.main()
					if command_but.get_pressed():
						editable_part += 1
						additions[editable_element].append("Command")
						additions[editable_element].append("")
						input_text = additions[editable_element][editable_part]
						a = True

				else:

					match additions[editable_element][0]:

						case "Item":
							match editable_part:
								case 1:
									win.blit(textInfo.render("Enter item name:", True, (139, 155, 180)), ((Width - textInfo.size("Enter item name:")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text != "":
										additions[editable_element][editable_part] = input_text
										editable_part += 1
										time.sleep(0.2)
										if a:
											additions[editable_element].append("")
										input_text = additions[editable_element][editable_part]
								case 2:
									win.blit(textInfo.render("Enter item image path", True, (139, 155, 180)), ((Width - textInfo.size("Enter item image path:")[0]) // 2, Height // 2 - 130))
									win.blit(textInfo.render("The game can support the following formants:", True, (139, 155, 180)), ((Width - textInfo.size("The game can support the following formants:")[0]) // 2, Height // 2 - 90))
									win.blit(pygame.font.Font(None, 33).render("JPG, PNG, GIF(non-animated), BMP, PCX, TIF, LBM, PBM, PGM, PPM, XPM", True, (139, 155, 180)), ((Width - pygame.font.Font(None, 33).size("JPG, PNG, GIF(non-animated), BMP, PCX, TIF, LBM, PBM, PGM, PPM, XPM")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text != "":
										additions[editable_element][editable_part] = input_text
										editable_part += 1
										time.sleep(0.2)
										if a:
											additions[editable_element].append("")
										input_text = additions[editable_element][editable_part]
								case 3:
									win.blit(textInfo.render("Enter info in Russian(if you want):", True, (139, 155, 180)), ((Width - textInfo.size("Enter item info in Russian(if you want):")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text != "":
										additions[editable_element][editable_part] = input_text
										editable_part += 1
										time.sleep(0.2)
										if a:
											additions[editable_element].append("")
										input_text = additions[editable_element][editable_part]
								case 4:
									win.blit(textInfo.render("Enter item info in English:", True, (139, 155, 180)), ((Width - textInfo.size("Enter item info in English:")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text != "":
										additions[editable_element][editable_part] = input_text
										editable_part += 1
										time.sleep(0.2)
										if a:
											additions[editable_element].append("")
										input_text = additions[editable_element][editable_part]
								case 5:
									win.blit(textInfo.render("Enter item purpose in Russian:", True, (139, 155, 180)), ((Width - textInfo.size("Enter item purpose(if you want):")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text != "":
										additions[editable_element][editable_part] = input_text
										editable_part += 1
										time.sleep(0.2)
										if a:
											additions[editable_element].append("")
										input_text = additions[editable_element][editable_part]
								case 6:
									win.blit(textInfo.render("Enter item purpose in English:", True, (139, 155, 180)), ((Width - textInfo.size("Enter item purpose(if you want):")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text != "":
										additions[editable_element][editable_part] = input_text
										editable_part += 1
										time.sleep(0.2)
										if a:
											additions[editable_element].append("")
										input_text = additions[editable_element][editable_part]
								case 7:
									win.blit(textInfo.render("Enter one of these item types:", True, (139, 155, 180)), ((Width - textInfo.size("Enter one of these item types:")[0]) // 2, Height // 2 - 90))
									win.blit(textInfo.render("\"Just an item\", \"Weapon\", \"Food\", \"Drink\", \"Mechanism\", \"Flower\"", True, (139, 155, 180)), ((Width - textInfo.size("\"Just an item\", \"Weapon\", \"Food\", \"Drink\", \"Mechanism\", \"Flower\"")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text in ["Just an item", "Weapon", "Food", "Drink", "Mechanism", "Flower"]:
										stage -= 1
										additions[editable_element][editable_part] = input_text
										input_text = ""
										editable_part = 0
										time.sleep(0.2)

						case "Recipe":
							match editable_part:
								case 1:
									win.blit(textInfo.render("Enter the names of ingredients separated by commas without spaces", True, (139, 155, 180)), ((Width - textInfo.size("Enter the names of ingredients separated by commas without spaces")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text != "":
										additions[editable_element][editable_part] = input_text.split(",")
										editable_part += 1
										time.sleep(0.2)
										if a:
											additions[editable_element].append("")
										input_text = additions[editable_element][editable_part]

								case 2:
									win.blit(textInfo.render("Enter ingrediens amounts separated by commas without spaces", True, (139, 155, 180)), ((Width - textInfo.size("Enter ingrediens amounts separated by commas without spaces")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text != "":
										additions[editable_element][editable_part] = input_text.split(",")
										editable_part += 1
										time.sleep(0.2)
										if a:
											additions[editable_element].append("")
										input_text = additions[editable_element][editable_part]
								
								case 3:
									win.blit(textInfo.render("Enter result of craft", True, (139, 155, 180)), ((Width - textInfo.size("Enter result of this craft")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text != "":
										additions[editable_element][editable_part] = input_text
										editable_part += 1
										time.sleep(0.2)
										if a:
											additions[editable_element].append("")
										input_text = additions[editable_element][editable_part]
								
								case 4:
									win.blit(textInfo.render("Enter result amount of craft", True, (139, 155, 180)), ((Width - textInfo.size("Enter result amount of this craft")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text != "":
										additions[editable_element][editable_part] = input_text
										editable_part += 1
										time.sleep(0.2)
										if a:
											additions[editable_element].append("")
										input_text = additions[editable_element][editable_part]
								
								case 5:
									win.blit(textInfo.render("Enter need object for craft(if you don't want, write \"None\")", True, (139, 155, 180)), ((Width - textInfo.size("Enter need object for craft(if you don't want, write \"None\")")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text != "":
										if input_text == "None":
											additions[editable_element][editable_part] = None
										else:
											additions[editable_element][editable_part] = input_text
										editable_part += 1
										time.sleep(0.2)
										if a:
											additions[editable_element].append("")
										input_text = additions[editable_element][editable_part]

								case 6:
									win.blit(textInfo.render("Enter need item for craft(if you don't want, write \"None\")", True, (139, 155, 180)), ((Width - textInfo.size("Enter need item for craft(if you don't want, write \"None\")")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text:
										stage -= 1
										if input_text == "None":
											additions[editable_element][editable_part] = None
										else:
											additions[editable_element][editable_part] = input_text
										input_text = ""
										editable_part = 0
										time.sleep(0.2)

						case "Object":
							match editable_part:
								case 1:
									win.blit(textInfo.render("Enter object name:", True, (139, 155, 180)), ((Width - textInfo.size("Enter object name:")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text != "":
										additions[editable_element][editable_part] = input_text
										editable_part += 1
										time.sleep(0.2)
										if a:
											additions[editable_element].append("")
										input_text = additions[editable_element][editable_part]
								case 2:
									win.blit(textInfo.render("Enter object image path", True, (139, 155, 180)), ((Width - textInfo.size("Enter object image path:")[0]) // 2, Height // 2 - 130))
									win.blit(textInfo.render("The game can support the following formants:", True, (139, 155, 180)), ((Width - textInfo.size("The game can support the following formants:")[0]) // 2, Height // 2 - 90))
									win.blit(pygame.font.Font(None, 33).render("JPG, PNG, GIF(non-animated), BMP, PCX, TIF, LBM, PBM, PGM, PPM, XPM", True, (139, 155, 180)), ((Width - pygame.font.Font(None, 33).size("JPG, PNG, GIF(non-animated), BMP, PCX, TIF, LBM, PBM, PGM, PPM, XPM")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text != "":
										additions[editable_element][editable_part] = input_text
										editable_part += 1
										time.sleep(0.2)
										if a:
											additions[editable_element].append("")
										input_text = additions[editable_element][editable_part]
								case 3:
									win.blit(textInfo.render("Enter object x:", True, (139, 155, 180)), ((Width - textInfo.size("Enter object x:")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text != "":
										try:
											additions[editable_element][editable_part] = int(input_text)
											editable_part += 1
											time.sleep(0.2)
											if a:
												additions[editable_element].append("")
											input_text = additions[editable_element][editable_part]
										except ValueError:
											pass
								case 4:
									win.blit(textInfo.render("Enter object y:", True, (139, 155, 180)), ((Width - textInfo.size("Enter object y:")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text != "":
										try:
											additions[editable_element][editable_part] = int(input_text)
											editable_part += 1
											time.sleep(0.2)
											if a:
												additions[editable_element].append("")
											input_text = additions[editable_element][editable_part]
										except ValueError:
											pass
								case 5:
									win.blit(textInfo.render("Enter object special flags:", True, (139, 155, 180)), ((Width - textInfo.size("Enter object special flags:")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text != "":
										if input_text == "None":
											additions[editable_element][editable_part] = None
										else:
											additions[editable_element][editable_part] = input_text
										editable_part += 1
										time.sleep(0.2)
										if a:
											additions[editable_element].append("")
										input_text = additions[editable_element][editable_part]
								case 6:
									win.blit(textInfo.render("Enter the name of the world in which this object will be:", True, (139, 155, 180)), ((Width - textInfo.size("Enter the name of the world in which this object will be:")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text != "":
										stage -= 1
										additions[editable_element][editable_part] = input_text
										input_text = ""
										editable_part = 0
										time.sleep(0.2)

						case "Command":
							match editable_part:
								case 1:
									win.blit(textInfo.render("Enter the command:", True, (139, 155, 180)), ((Width - textInfo.size("Enter the command:")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text != "":
										additions[editable_element][editable_part] = input_text
										editable_part += 1
										time.sleep(0.2)
										if a:
											additions[editable_element].append("")
										input_text = additions[editable_element][editable_part]
								case 2:
									win.blit(textInfo.render("Choose when the command will be executed:", True, (139, 155, 180)), ((Width - textInfo.size("Choose when the command will be executed:")[0]) // 2, Height // 2 - 114))
									win.blit(textInfo.render("1 - At the beginning of the code", True, (139, 155, 180)), ((Width - textInfo.size("1 - At the beginning of the code")[0]) // 2, Height // 2 - 82))
									win.blit(textInfo.render("2 - Every game tick", True, (139, 155, 180)), ((Width - textInfo.size("2 - Every game tick")[0]) // 2, Height // 2 - 50))
									win.blit(textInfo.render(input_text, True, (139, 155, 180)), ((Width - textInfo.size(input_text)[0]) // 2, Height // 2 - 18))
									if keys[pygame.K_RETURN] and input_text in ["1", "2"]:
										stage -= 1
										additions[editable_element][editable_part] = input_text
										input_text = ""
										editable_part = 0
										time.sleep(0.2)

			case 4:

				try:
					Saver.save_objects(path + "Gannitto-World/files/" + plugin_name + ".save", additions)
				except OSError:
					Saver.save_objects(path + "Gannitto-World/files/My plugin.save", additions)
				my_plugins()

		pygame.display.update()
		clock.tick(30)

def upload_plugin():
	
	plugin_path = os.getcwd()
	page_back_button = Button(74, Height - 74, pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Buttons/Back.png"), (128, 128)), pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Buttons/Back 2.png"), (128, 128)), win)
	page_next_button = Button(Width - 74, Height - 74, pygame.transform.flip(pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Buttons/Back.png"), (128, 128)), True, False), pygame.transform.flip(pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Buttons/Back 2.png"), (128, 128)), True, False), win)
	page = 1

	while 1:

		mouse_x, mouse_y = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		keys = pygame.key.get_pressed()

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				quit()

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE:
					plugin_path = plugin_path[:-1]
				elif event.key != pygame.K_RETURN:
					plugin_path += event.unicode

		for dirs, folder, files in os.walk(plugin_path):
			inside_files = files
			inside_folders = folder
			break
		
		win.fill((192, 203, 220))
		pygame.draw.rect(win, (58, 68, 102), (0, 0, Width, Height), 10)
		pygame.draw.rect(win, (139, 155, 180), (10, 10, Width - 20, Height - 20), 10)

		page_back_button.main()
		if page_back_button.get_pressed() and page != 1:
			page -= 1
		page_next_button.main()
		if page_next_button.get_pressed():
			page += 1

		win.blit(textInfo.render(plugin_path, True, (139, 155, 180)), (50, 50))
		win.blit(textInfo.render(str(page), True, (139, 155, 180)), (Width // 2 - 10, Height - 60))

		c = []
		b = -1
		for i in inside_files:
			b += 1
			if os.path.splitext(plugin_path + "\\" + i)[1] != ".save":
				c.append(b)

		a = -1
		for i in c:
			a += 1
			del inside_files[i - a]

		file_list = inside_folders + inside_files
		changed_file = ""
		
		if file_list != []:

			if page < len(file_list) / 5 or len(file_list) % 5 == 0:
				a = 0
				for i in range((page - 1) * 5, (page - 1) * 5 + 5):
					a += 1
					try:
						if 50 <= mouse_x <= 50 + textInfo.size(file_list[i])[0] and 50 + a * 50 <= mouse_y <= 80 + a * 50:
							win.blit(textInfo.render(file_list[i], True, (58, 68, 102)), (50, 50 + a * 50))
							if click[0] == 1:
								changed_file = file_list[i]
						else:
							win.blit(textInfo.render(file_list[i], True, (139, 155, 180)), (50, 50 + a * 50))
					except:
						break

			else:
				a = 0
				for i in range((page - 1) * 5, (page - 1) * 5 + len(inside_folders + inside_files) % 5):
					a += 1
					try:
						if 50 <= mouse_x <= 50 + textInfo.size(file_list[i])[0] and 50 + a * 50 <= mouse_y <= 80 + a * 50:
							win.blit(textInfo.render(file_list[i], True, (58, 68, 102)), (50, 50 + a * 50))
							if click[0] == 1:
								changed_file = file_list[i]
						else:
							win.blit(textInfo.render(file_list[i], True, (139, 155, 180)), (50, 50 + a * 50))
					except:
						break

			if keys[pygame.K_ESCAPE]:
				break
		
		if changed_file != "":
			if os.path.splitext(plugin_path + "\\" + changed_file)[1] == ".save":
				os.rename(plugin_path + "\\" + changed_file, __file__[:-23] + "\Plugins\\" + changed_file)
			else:
				if plugin_path[len(plugin_path) - 1] == "\\":
					plugin_path += changed_file
				else:
					plugin_path += "\\" + changed_file

		pygame.display.update()
		clock.tick(30)

def my_plugins():

	page_back_button = Button(74, Height - 74, pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Buttons/Back.png"), (128, 128)), pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Buttons/Back 2.png"), (128, 128)), win)
	page_next_button = Button(Width - 74, Height - 74, pygame.transform.flip(pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Buttons/Back.png"), (128, 128)), True, False), pygame.transform.flip(pygame.transform.scale(pygame.image.load(path + "Gannitto-World/files/Images/Buttons/Back 2.png"), (128, 128)), True, False), win)
	page = 1

	while 1:

		mouse_x, mouse_y = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		keys = pygame.key.get_pressed()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
		inside_files = []
		for dirs, folder, files in os.walk(path + "Gannitto-World/Plugins/"):
			inside_files = files
			break
		
		win.fill((192, 203, 220))
		pygame.draw.rect(win, (58, 68, 102), (0, 0, Width, Height), 10)
		pygame.draw.rect(win, (139, 155, 180), (10, 10, Width - 20, Height - 20), 10)

		page_back_button.main()
		if page_back_button.get_pressed() and page != 1:
			page -= 1
		page_next_button.main()
		if page_next_button.get_pressed() and page < len(inside_files) / 5:
			page += 1

		win.blit(textInfo.render(str(page), True, (139, 155, 180)), (Width // 2 - 10, Height - 60))

		if len(inside_files) != 0:
			if page < len(inside_files) / 5 or len(inside_files) % 5 == 0:
				a = 0
				for i in range((page - 1) * 5, (page - 1) * 5 + 5):
					a += 1
					win.blit(textInfo.render(inside_files[i][0:-5], True, (139, 155, 180)), (50, 50 + a * 50))
			else:
				a = 0
				for i in range((page - 1) * 5, (page - 1) * 5 + len(inside_files) % 5):
					a += 1
					win.blit(textInfo.render(inside_files[i][0:-5], True, (139, 155, 180)), (50, 50 + a * 50))

		if keys[pygame.K_ESCAPE]:
			break

		pygame.display.update()
		clock.tick(30)


while True:

	mouse_x, mouse_y = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	Width, Height = pygame.display.get_surface().get_size()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()

	win.fill((192, 203, 220))

	pygame.draw.rect(win, (58, 68, 102), (0, 0, Width, Height), 10)
	pygame.draw.rect(win, (139, 155, 180), (10, 10, Width - 20, Height - 20), 10)

	create_new_plugin_but.main(create_new_plugin)
	my_plugins_but.main(my_plugins)
	upload_plugin_but.main(upload_plugin)

	pygame.display.update()
	clock.tick(30)
