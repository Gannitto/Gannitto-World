from Translator import t
from Functions import text
from Globals import Width, Height
from Classes import Projectile, ExplodingProjectile

class ItemActions:
	def __init__(self, game):
		self.game = game

	def handle_item_actions(self, mouse_x, mouse_y):
		match self.game.inventory.whole_inventory[self.game.inventory.changed_slot].name:

			case "Gun":

				for item_index, slot in enumerate(self.game.inventory.whole_inventory):
					if slot is not None and slot.name == "Bullet":
						self.game.inventory.reduce(item_index)
						self.game.world.projectiles.append(Projectile(self.game.player.x, self.game.player.y, mouse_x, mouse_y, "Bullet"))
						if self.game.multiplayer:
							self.game.events.append({"event_type": "projectile_added", "x": self.game.player.x, "y": self.game.player.y, "mouse_x": mouse_x, "mouse_y": mouse_y, "projectile_type": "Bullet"})
						break

			case "Bow":
				for item_index, slot in enumerate(self.game.inventory.whole_inventory):
					if slot is not None and slot.name == "Arrow":
						self.game.inventory.reduce(item_index)
						self.game.world.projectiles.append(Projectile(self.game.player.x, self.game.player.y, mouse_x, mouse_y, "Arrow"))
						if self.game.multiplayer:
							self.game.events.append({"event_type": "projectile_added", "x": self.game.player.x, "y": self.game.player.y, "mouse_x": mouse_x, "mouse_y": mouse_y, "projectile_type": "Arrow"})
						break

			case "Beer":

				self.game.effects.effects.append(["Drunk", 180])
				self.game.inventory.reduce(self.game.inventory.changed_slot)

			case "Grenade":

				self.game.world.projectiles.append(ExplodingProjectile(self.game.player.x, self.game.player.y, mouse_x, mouse_y, "Grenade", (self.game.player.x + mouse_x - Width // 2, self.game.player.y - mouse_y + Height // 2)))

				self.game.inventory.reduce(self.game.inventory.changed_slot)
					
		if self.game.inventory.whole_inventory[self.game.inventory.changed_slot] is not None and self.game.inventory.whole_inventory[self.game.inventory.changed_slot].type == "Food" and self.game.HP < 100:
			
			self.game.player.HP += self.game.inventory.whole_inventory[self.game.inventory.changed_slot].special_info
			self.game.inventory.reduce(self.game.inventory.changed_slot)
			
	
