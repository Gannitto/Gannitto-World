import pygame
import os
pygame.init()

textInfo = pygame.font.Font(None, 20)
types = ["Just an item", "Weapon", "Food", "Drink", "Mechanism", "Flower"]
path = os.path.abspath(__file__)[: os.path.abspath(__file__).index("Gannitto world")]

class Resourse:
    """Items with certain characteristics"""

    def __init__(self, name: str, image_path: str, info: list, purpose: list, type: str):
        self.name = name
        self.info = info
        self.purpose = purpose
        self.type = type
        self.amount = 0
        self.settings = []
        self.image_path = image_path
        self.image = pygame.transform.scale(pygame.image.load(image_path), (64, 64))

class Recipe:
    def __init__(self, ingredients: list, ingredients_amounts: list, result: str, result_amount: str, need_object: str = None, need_tool: str = None):
        for i in range(7 - len(ingredients)):
            ingredients.append(None)
            ingredients_amounts.append(None)
        self.ingredients = ingredients
        self.ingredients_amounts = ingredients_amounts
        self.result = result
        self.result_amount = result_amount
        self.need_object = need_object
        self.need_tool = need_tool

    def get_result(self):
        """Checks if any result can be obtained from the current ingredients"""
        from Gannitto_world import craft_items_list, craft_amounts_list, objects, x, y
        if craft_items_list == self.ingredients and craft_amounts_list == self.ingredients_amounts:
            a = True
            b = None
            c = True
            d = None

            if self.need_object != None:
                a = False
                for object in objects:
                    if x - 1000 <= object.x <= x + 1000 and y - 1000 <= object.y <= y + 1000 and object.name == self.need_object:
                        a = True
                        b = object.name
                        break
            
            if self.need_tool != None:
                c = False
                for cell in inventory.whole_inventory:
                    if cell != None and cell.name == self.need_tool:
                        c = True
                        d = cell.name
            if a and c:
                return [self.result, self.result_amount, b, d]
            else:
                return None
        else:
            return None

class Inventory:
    def __init__(self):

        self.resourses = {
            "Mushroom": Resourse("Mushroom", path + "Gannitto world/files/Images/Items/Mushroom.png", [
                "???????????? ????????, ???????????? ????????????",
                "Just a mushroom, nothong more"
            ], [
                "????????",
                "None"
            ], types[0]),


            
            "Red mushroom": Resourse("Red mushroom", path + "Gannitto world/files/Images/Items/Red mushroom.png", [
                "???????????? ????????, ???????????? ????????????",
                "Just a mushroom, nothong more"
            ], [
                "????????",
                "None"
            ], types[0]),


            
            "Jar": Resourse("Jar", path + "Gannitto world/files/Images/Items/Jar.png", [
                "????????",
                "None"
            ], [
                "????????",
                "None"
            ], types[0]),



            "Gun": Resourse("Gun", path + "Gannitto world/files/Images/Items/Gun.png", [
                "??????????, ?????? ?????????????? ?????????? ??????????????",
                "A gun, that needs bullets"
            ], [
                "?? ???? ?????????????? ???? ???????????? ????????????????, ?????????? ???? ????????????",
                "You can shoot with it by pressing the spase"
            ], types[1]),



            "Bullet": Resourse("Bullet", path + "Gannitto world/files/Images/Items/Bullet.png", [
                "?????? ???????? ?????? ??????????",
                "This is a bullet for gun"
            ], [
                "?? ???? ?????????????? ???? ???????????? ????????????????, ?????????? ???? ????????????(???????? ?? ?????? ???????? ????????????????)",
                "You can shoot with it by pressing the spase(if you have a gun)"
            ], types[0]),



            "Almond whater": Resourse("Almond whater", path + "Gannitto world/files/Images/Items/Almond whater.png", [
                "????????, ???????? ?????????????? ???????????????????? ?????????????? ?????? ????????????",
                "Water, that tastes like almonds or vanilla"
            ], [
                "????????",
                "None"
            ], types[3]),



            "Blue slime": Resourse("Blue slime", path + "Gannitto world/files/Images/Items/Blue Slime.png", [
                "???????????? ???????? ???????????? ??????????",
                "Blue sticky gel"
            ], [
                "????????",
                "None"
            ], types[0]),



            "Pink slime": Resourse("Pink slime", path + "Gannitto world/files/Images/Items/Pink Slime.png", [
                "???????????? ???????? ???????????????? ??????????",
                "Pink slicky gel"
            ], [
                "None",
                "????????"
            ], types[0]),



            "Stick": Resourse("Stick", path + "Gannitto world/files/Images/Items/Stick.png", [
                "??????????",
                "A stick"
            ], [
                "????????",
                "None"
            ], types[0]),



            "Iron ingot": Resourse("Iron ingot", path + "Gannitto world/files/Images/Items/Iron ingot.png", [
                "???? ???????????? ???????????????? ??????, ???????????????????? ???????????????? ???????? ?? ??????????",
                "You can get it, by smetling iron ore in a furnace"
            ], [
                "?????????? ?????????????? ?????????? ???? ???????? ?????????????? ???? ??????????",
                "You can make a bucket of three ingots on the table"
            ], types[0]),



            "Gold ingot": Resourse("Gold ingod", path + "Gannitto world/files/Images/Items/Gold ingot.png", [
                "???? ???????????? ???????????????? ??????, ???????????????????? ?????????????? ???????? ?? ??????????",
                "You can get it, by smetling gold ore in a furnace"
            ], [
                "?????????? ?????????????? ?????????????? ?????????? ???? ???????? ?????????????? ???? ??????????",
                "You can make a gold bucket of three ingots on the table"
            ], types[0]),



            "Bucket": Resourse("Bucket", path + "Gannitto world/files/Images/Items/Bucket.png", [
                "??????????...",
                "Bucket..."
            ], [
                "????????",
                "None"
            ], types[0]),



            "Gold bucket": Resourse("Gold bucket", path + "Gannitto world/files/Images/Items/Gold bucket.png", [
                "?????????? ???????? ?????????????? ???????????!",
                "Why do you need a GOLD bucket?!"
            ], [
                "????????",
                "None"
            ], types[0]),



            "Thread": Resourse("Thread", path + "Gannitto world/files/Images/Items/Thread.png", [
                "????????",
                "None"
            ], [
                "????????",
                "None"
            ], types[0]),



            "Portal gun": Resourse("Portal gun", path + "Gannitto world/files/Images/Items/Portal gun.png", [
                "?? ?????????????? ??????, ???? ???????????? ?????????????????? ?????????????? ?????? ????????????????????????",
                "With it, you can create teleportation portals"
            ], [
                "?????????? ???????????????????????? ?????? ???????????????? ????????????????????????",
                "Can be used for fast movement"
            ], types[0]),



            "Vending machine": Resourse("Vending machine", path + "Gannitto world/files/Images/Items/Vending machine.png", [
                "?? ?????????????? ???????? ?????????? ???????????????????? ????????",
                "With it, you can vend items"
            ], [
                "???????????? ???????????????????????? ?? ???????? ???? ????????",
                "Easy to use in online play"
            ], types[0]),



            "Stone": Resourse("Stone", path + "Gannitto world/files/Images/Items/Stone.png", [
                "????????",
                "None"
            ], [
                "????????",
                "None"
            ], types[0]),



            "Poppy": Resourse("Poppy", path + "Gannitto world/files/Images/Items/Poppy.png", [
                "???????????????? ????????????",
                "A beautiful flower"
            ], [
                "????????",
                "None"
            ], types[5]),



            "Purple tulip": Resourse("Purple tulip", path + "Gannitto world/files/Images/Items/Purple tulip.png", [
                "???????????????? ????????????",
                "A beautiful flower"
            ], [
                "????????",
                "None"
            ], types[5]),



            "Orange tulip": Resourse("Orange tulip", path + "Gannitto world/files/Images/Items/Orange tulip.png", [
                "???????????????? ????????????",
                "A beautiful flower"
            ], [
                "????????",
                "None"
            ], types[5]),



            "Black tulip": Resourse("Black tulip", path + "Gannitto world/files/Images/Items/Black tulip.png", [
                "???????????????? ????????????",
                "A beautiful flower"
            ], [
                "????????",
                "None"
            ], types[5]),



            "Red tulip": Resourse("Red tulip", path + "Gannitto world/files/Images/Items/Red tulip.png", [
                "???????????????? ????????????",
                "A beautiful flower"
            ], [
                "????????",
                "None"
            ], types[5]),



            "Yellow tulip": Resourse("Yellow tulip", path + "Gannitto world/files/Images/Items/Yellow tulip.png", [
                "???????????????? ????????????",
                "A beautiful flower"
            ], [
                "????????",
                "None"
            ], types[5]),



            "Rope": Resourse("Rope", path + "Gannitto world/files/Images/Items/Rope.png", [
                "????????",
                "None"
            ], [
                "????????",
                "None"
            ], types[1]),



            "Stone spear": Resourse("Stone spear", path + "Gannitto world/files/Images/Items/Stone spear.png", [
                "????????",
                "None"
            ], [
                "????????",
                "None"
            ], types[1]),



            "Wooden": Resourse("Wooden", path + "Gannitto world/files/Images/Items/Wooden.png", [
                "????????",
                "None"
            ], [
                "????????",
                "None"
            ], types[0]),



            "Table": Resourse("Table", path + "Gannitto world/files/Images/Items/Table.png", [
                "???????????????????? ????????, ???? ?????????????? ?????????? ?????????????????????????? ????????????????",
                "Wooden table, on which you can craft items"
            ], [
                "???? ???????????? ?????????????????? ??????",
                "You can put it"
            ], types[0]),



            "Wall table": Resourse("Wall table", path + "Gannitto world/files/Images/Items/Wall table.png", [
                "???????????????????? ????????, ???? ?????????????? ?????????? ?????????????????????????? ??????????",
                "Wooden table, on which you can craft walls"
            ], [
                "???? ???????????? ?????????????????? ??????",
                "You can put it"
            ], types[0]),



            "Clay": Resourse("Clay", path + "Gannitto world/files/Images/Items/Clay.png", [
                "?????? ??????????, ???? ?????????? ????????????",
                "Like sand, but very sticky"
            ], [
                "?????????? ?????????????????????? ?? ????????????",
                "Can be smelted into brick"
            ], types[0]),



            "Brick": Resourse("Brick", path + "Gannitto world/files/Images/Items/Brick.png", [
                "????????",
                "None"
            ], [
                "???? ???????? ?????????? ?????????????? ?????????????????? ??????????",
                "You can make a brick wall out of it"
            ], types[0]),



            "Pot": Resourse("Pot", path + "Gannitto world/files/Images/Items/Pot.png", [
                "???????????????? ????????????",
                "Clay pot"
            ], [
                "???? ???????????? ???????????????? ?? ???????? ????????????????",
                "You can put a plant in it"
            ], types[0]),



            "Wire": Resourse("Wire", path + "Gannitto world/files/Images/Items/Wire.png", [
                "????????",
                "None"
            ], [
                "?? ?????????????? ???????? ?????????? ???????????? ?????????????????? ??????????????????",
                "With it, you can make various mechanisms"
            ], types[0]),



            "Random box": Resourse("Random box", path + "Gannitto world/files/Images/Items/Random box.png", [
                "????????",
                "None"
            ], [
                "?????? ?????????????????? ?????????????? ?? ?????????? ??????????????, ???????????? ?????? ?? ???????????? ?? ???????????? 50%",
                "When recieving a signal from one side, gives it to the other with a 50% chance"
            ], types[0]),



            "Lever": Resourse("Lever", path + "Gannitto world/files/Images/Items/Lever.png", [
                "????????",
                "None"
            ], [
                "????????",
                "None"
            ], types[0]),



            "Motherboard": Resourse("Motherboard", path + "Gannitto world/files/Images/Items/Motherboard.png", [
                "????????",
                "None"
            ], [
                "????????",
                "None"
            ], types[0]),



            "Wrench": Resourse("Wrench", path + "Gannitto world/files/Images/Items/Wrench.png", [
                "??????????-???? ??????????",
                "Some thing"
            ], [
                "?? ?????????????? ???????? ?????????? ???????????? ????????????", 
                "With it, you can remove the wire"
            ], types[3]),



            "Stone pickaxe": Resourse("Stone pickaxe", path + "Gannitto world/files/Images/Items/Stone pickaxe.png", [
                "?????????????????????? ???????????? ??????????????",
                "Nny miner needs"
            ], [
                "?? ?????????????? ?????? ???? ???????????? ???????????? ????????", 
                "with it you can dig ore"
            ], types[0]),



            "Stone hammer": Resourse("Stone hammer", path + "Gannitto world/files/Images/Items/Stone hammer.png", [
                "????????",
                "None"
            ], [
                "????????",
                "None"
            ], types[0]),



            "Stone shovel": Resourse("Stone shovel", path + "Gannitto world/files/Images/Items/Stone shovel.png", [
                "????????",
                "None"
            ], [
                "????????",
                "None"
            ], types[0]),



            "Furnace": Resourse("Furnace", path + "Gannitto world/files/Images/Items/Furnace.png", [
                "?????????? ??????????????????",
                "You can put it"
            ], [
                "?? ?????????????? ????????, ???? ???????????? ???????????????????????? ????????", 
                "With a furnace, you can melt down ores"
            ], types[0]),



            "Stone brick": Resourse("Stone brick", path + "Gannitto world/files/Images/Items/Stone brick.png", [
                "????????"
                "None"
            ], [
                "????????", 
                "None"
            ], types[0]),



            "Wooden wall": Resourse("Wooden wall", path + "Gannitto world/files/Images/Items/Wooden wall.png", [
                "?????????? ??????????????????",
                "You can put it"
            ], [
                "????????",
                "None"
            ], types[0]),



            "Brick wall": Resourse("Brick wall", path + "Gannitto world/files/Images/Items/Brick wall.png", [
                "?????????? ??????????????????",
                "You can put it"
            ], [
                "????????",
                "None"
            ], types[0]),



            "Stone brick wall": Resourse("Stone brick wall", path + "Gannitto world/files/Images/Items/Stone brick wall.png", [
                "?????????? ??????????????????",
                "You can put it"
            ], [
                "????????",
                "None"
            ], types[0]),



            "Iron ore": Resourse("Iron ore", path + "Gannitto world/files/Images/Items/Iron ore.png", [
                "???? ???????????? ?????????????????????? ?? ???????????????? ????????????",
                "You can smelt it into an iron ingot"
            ], [
                "????????",
                "None"
            ], types[0]),



            "Candy cane": Resourse("Candy cane", path + "Gannitto world/files/Images/Items/Candy cane.png", [
                "?????????????? ?? ????????????",
                "Sweet and sticky"
            ], [
                "????????",
                "None"
            ], types[0])
        }

        
        
        self.recipes = [
           Recipe(["Stick", "Stone"], [2, 3], "Stone pickaxe", 1),
           Recipe(["Stick", "Stone"], [1, 2], "Stone hammer", 1),
           Recipe(["Stick", "Stone"], [3, 1], "Stone spear", 1),
           Recipe(["Stick", "Stone"], [2, 1], "Stone spear", 1),
           Recipe(["Wooden"], [10], "Table", 1),
           Recipe(["Stone"], [20], "Furnace", 1),
           Recipe(["Table", "Iron ingot"], [1, 1], "Wall table", 1),
           Recipe(["Clay"], [1], "Brick", 1, "Furnace"),
           Recipe(["Stone"], [1], "Stone brick", 1),
           Recipe(["Wooden"], [3], "Wooden wall", 1, "Wall table"),
           Recipe(["Brick"], [3], "Brick wall", 1, "Wall table"),
           Recipe(["Stone brick"], [3], "Stone brick wall", 1, "Wall table"),
           Recipe(["Iron ore"], [1], "Iron ingot", 1, "Furnace"),
           Recipe(["Iron ingot"], [3], "Bucket", 1, "Table"),
           Recipe(["Stone", "Stick"], [1, 1], "Lever", 1),
           Recipe(["Brick"], [2], "Pot", 1, "Furnace")
        ]
        
        self.inventory_panel = [None] * 10
        self.whole_inventory = [None] * 30
        self.start_cell = 0
        self.end_cell = 0
        self.end_cell_inventory = 0
        self.Split_items = False
    
    def increate(self, name: str, amount: int):
        """Adds item to inventory"""
        try:
            self.resourses[name].amount += amount
            self.update_whole()
        except KeyError:
            if name.__class__ != str:
                print("Error increating: name must be str")
            else:
                print("Error increasing: item not found")
    
    def update_whole(self):
        
        for name, resource in self.resourses.items():
            if resource.amount != 0 and resource not in self.whole_inventory:
                self.whole_inventory.insert(self.whole_inventory.index(None), resource)
                self.whole_inventory.remove(None)

        def chek():
            for cell in self.whole_inventory:
                if cell is not None and cell.amount > 99:
                    for _ in range(int(cell.amount / 99)):
                        a = self.whole_inventory.index(None)
                        self.whole_inventory[a] = Resourse(cell.name, cell.image_path, cell.info, cell.purpose, cell.type)
                        self.whole_inventory[a].amount = 99
                    cell.amount -= int(cell.amount / 99) * 99
                    chek()

        chek()
        for i in self.whole_inventory:
            ...#if i is not None: print(i.amount)
    
    def get_amout(self, name: str):
        """Returns an amount of a particular item"""

        try:
            return self.resourses[name].amount
        except KeyError:
            return -1
    
    def draw_whole(self):
        """Draws the whole inventory"""

        from Gannitto_world import win, craft_images_list, craft_amounts_list, Inventory_slot
        cell_x = cell_y = 10
        for cell in self.whole_inventory:
            if cell != None:
                win.blit(cell.image, (cell_x, cell_y))
                if cell.amount > 1:
                    win.blit(textInfo.render(str(cell.amount), True, (0, 150, 0)), (cell_x + 10, cell_y + 42))
            cell_x += 80
            if cell_x == 810:
                cell_x = 10
                cell_y += 80
        cell_x = 170
        win.blit(Inventory_slot, (170, 250))
        i = -1
        for cell in craft_images_list:
            i += 1
            if cell != None:
                win.blit(cell, (cell_x, 250))
                if craft_amounts_list != [None] * 7 and craft_amounts_list[i] > 1:
                    win.blit(textInfo.render(str(craft_amounts_list[i]), True, (0, 150, 0)), (cell_x + 10, 292))
                cell_x += 80
                win.blit(Inventory_slot, (cell_x, 250))
            else:
                break
    
    def draw_panel(self):
        """Draws the top panel"""

        from Gannitto_world import win
        i = 0
        cell_x = cell_y = 10
        for cell in self.whole_inventory:
            i += 1
            if i == 11:
                break
            if cell is not None:
                win.blit(cell.image, (cell_x, cell_y))
                if cell.amount > 1:
                    win.blit(textInfo.render(str(cell.amount), True, (0, 150, 0)), (cell_x + 10, cell_y + 42))
            cell_x += 80
    
    def set_start_cell(self, mouse__x: int, mouse__y: int):

        for yy in range(0, 3):
            for xx in range(0, 10):
                cell_x = 10 + xx * 80
                cell_y = 10 + yy * 80
                if cell_x <= mouse__x <= cell_x + 64 and cell_y <= mouse__y <= cell_y + 64:
                    self.start_cell = yy * 10 + xx
                    return
    
    def set_end_cell(self, mouse__x: int, mouse__y: int):

        for yy in range(0, 3):
            for xx in range(0, 10):
                cell_x = 10 + xx * 80
                cell_y = 10 + yy * 80
                if cell_x <= mouse__x <= cell_x + 64 and cell_y <= mouse__y <= cell_y + 64:
                    self.end_cell = yy * 10 + xx
                    self.end_cell_inventory = 0
        
        for x in range(2, 9):
            cell_x = 10 + x * 80
            if cell_x <= mouse__x <= cell_x + 64 and 250 <= mouse__y <= 314:
                self.end_cell = x - 2
                self.end_cell_inventory = 1
        self.swap_cells()
        return
    
    def swap_cells(self):
        """Swap cells in inventory"""

        from Gannitto_world import craft_items_list, craft_amounts_list, craft_images_list
        if self.whole_inventory[self.start_cell] != None:
            if self.Split_items and self.whole_inventory[self.start_cell].amount % 2 == 0:
                self.whole_inventory[self.start_cell].amount //= 2
                self.whole_inventory[self.end_cell] = self.whole_inventory[self.start_cell]
            elif self.end_cell_inventory == 1:
                temp = craft_items_list[self.end_cell]
                craft_items_list[self.end_cell] = self.whole_inventory[self.start_cell].name
                craft_amounts_list[self.end_cell] = self.whole_inventory[self.start_cell].amount
                craft_images_list[self.end_cell] = self.whole_inventory[self.start_cell].image
                self.resourses[self.whole_inventory[self.start_cell].name].amount = 0
                self.whole_inventory[self.start_cell] = temp
                self.start_cell = 0
                self.end_cell = 0
            else:
                temp = self.whole_inventory[self.end_cell]
                self.whole_inventory[self.end_cell] = self.whole_inventory[self.start_cell]
                self.whole_inventory[self.start_cell] = temp
                self.start_cell = 0
                self.end_cell = 0

    def check_recipies(self):
        for recipie in self.recipes:
             if recipie.get_result() is not None:
                return recipie.get_result()
        return None

inventory = Inventory()

def get_items():
    inventory.whole_inventory = [None] * 30
    inventory.increate("Gun", 1)
    inventory.increate("Bullet", 99)