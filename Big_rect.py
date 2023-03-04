import random

class BigRect:
    def __init__(self, rect_x: int, rect_y: int):
        self.x = rect_x
        self.y = rect_y
        self.biom = random.choice(["Grass", "Sand", "Field", "Snow", "Swamp"])

    def generate(self, objects):
        from Gannitto_world import Object, win, textInfo, Width, Height
        import pygame
        import getpass
        path = "C://Users/" + getpass.getuser() + "/Desktop/"
        self.biom = "Grass"#random.choice(["Grass", "Sand", "Field", "Snow", "Swamp"])
        a = True
        b = False
        #while a:
        #    for object in objects:
        #        if self.x - 50000 <= object.x <= self.x + 5000 and self.y - 5000 <= object.y <= self.y + 5000 and object.__class__ == Object:
        #            del object
        #            b = True
        #            break
        #    if not b:
        #        a = False
        #    else:
        #        b = False
        match self.biom:

            case "Grass":

                win.blit(textInfo.render("World generation - 0%", True, (139, 155, 180)), ((Width - textInfo.size("World generation - 0%")[0]) // 2, Height // 2 + 20))
                win.blit(textInfo.render("Adding bushes...", True, (139, 155, 180)), ((Width - textInfo.size("Adding bushes...")[0]) // 2, Height // 2 + 50))
                Bush = pygame.image.load(path + "Gannitto world/files/Images/Objects/Bush.png")
                for _ in range(random.randint(500, 1000)):
                    objects.append(Object(
                        "Bush",
                        random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000),
                        "Gannitto world/files/Images/Objects/Bush.png", [128, 128], Bush))
                pygame.display.update()
            


                win.fill((192, 203, 220), (0, Height // 2 + 18, Width, Height))
                win.blit(textInfo.render("World generation - 8%", True, (139, 155, 180)), ((Width - textInfo.size("World generation - 8%")[0]) // 2, Height // 2 + 20))
                win.blit(textInfo.render("Adding ponds with reeds...", True, (139, 155, 180)), ((Width - textInfo.size("Adding ponds...")[0]) // 2, Height // 2 + 50))
                Pond = pygame.image.load(path + "Gannitto world/files/Images/Objects/Pond.png")
                Reed = pygame.image.load(path + "Gannitto world/files/Images/Objects/Reed.png")
                for _ in range(random.randint(100, 500)):
                    x, y = random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000)
                    objects.append(Object(
                        "Pond",
                        x, y,
                        "Gannitto world/files/Images/Objects/Pond.png", [512, 512], Pond, special_flags=[100, random.randint(10, 30)]))
                    for _ in range(random.randint(2, 5)):
                        objects.append(Object(
                            "Reed",
                            x + random.randint(-100, 612), y + random.randint(-100, 612),
                            "Gannitto world/files/Images/Objects/Reed.png", [256, 256], Reed))
                pygame.display.update()




                win.fill((192, 203, 220), (0, Height // 2 + 18, Width, Height))
                win.blit(textInfo.render("World generation - 16%", True, (139, 155, 180)), ((Width - textInfo.size("World generation - 16%")[0]) // 2, Height // 2 + 20))
                win.blit(textInfo.render("Adding stones...", True, (139, 155, 180)), ((Width - textInfo.size("Adding stones...")[0]) // 2, Height // 2 + 50))
                Stone = pygame.image.load(path + "Gannitto world/files/Images/Items/Stone.png")
                for _ in range(random.randint(500, 1000)):
                    objects.append(Object(
                        "Stone",
                        random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000),
                        "Gannitto world/files/Images/Items/Stone.png", image=Stone, special_flags="Item"))
                pygame.display.update()



                win.fill((192, 203, 220), (0, Height // 2 + 18, Width, Height))
                win.blit(textInfo.render("World generation - 24%", True, (139, 155, 180)), ((Width - textInfo.size("World generation - 24%")[0]) // 2, Height // 2 + 20))
                win.blit(textInfo.render("Adding poppies...", True, (139, 155, 180)), ((Width - textInfo.size("Adding poppies...")[0]) // 2, Height // 2 + 50))
                Poppy = pygame.image.load(path + "Gannitto world/files/Images/Items/Poppy.png")
                for _ in range(random.randint(1000, 5000)):
                    objects.append(Object(
                        "Poppy",
                        random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000),
                        "Gannitto world/files/Images/Items/Poppy.png", image=Poppy, special_flags="Item"))
                pygame.display.update()



                win.fill((192, 203, 220), (0, Height // 2 + 18, Width, Height))
                win.blit(textInfo.render("World generation - 32%", True, (139, 155, 180)), ((Width - textInfo.size("World generation - 32%")[0]) // 2, Height // 2 + 20))
                win.blit(textInfo.render("Adding purple tulips...", True, (139, 155, 180)), ((Width - textInfo.size("Adding purple tulips...")[0]) // 2, Height // 2 + 50))
                Red_tulip = pygame.image.load(path + "Gannitto world/files/Images/Items/Purple tulip.png")
                for _ in range(random.randint(1000, 5000)):
                    objects.append(Object(
                        "Purple tulip",
                        random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000),
                        "Gannitto world/files/Images/Items/Purple tulip.png", image=Red_tulip, special_flags="Item"))
                pygame.display.update()



                win.fill((192, 203, 220), (0, Height // 2 + 18, Width, Height))
                win.blit(textInfo.render("World generation - 40%", True, (139, 155, 180)), ((Width - textInfo.size("World generation - 40%")[0]) // 2, Height // 2 + 20))
                win.blit(textInfo.render("Adding orange tulips...", True, (139, 155, 180)), ((Width - textInfo.size("Adding orange tulips...")[0]) // 2, Height // 2 + 50))
                Orange_tulip = pygame.image.load(path + "Gannitto world/files/Images/Items/Orange tulip.png")
                for _ in range(random.randint(1000, 5000)):
                    objects.append(Object(
                        "Orange tulip",
                        random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000),
                        "Gannitto world/files/Images/Items/Orange tulip.png", image=Orange_tulip, special_flags="Item"))
                pygame.display.update()



                win.fill((192, 203, 220), (0, Height // 2 + 18, Width, Height))
                win.blit(textInfo.render("World generation - 48%", True, (139, 155, 180)), ((Width - textInfo.size("World generation - 48%")[0]) // 2, Height // 2 + 20))
                win.blit(textInfo.render("Adding black tulips...", True, (139, 155, 180)), ((Width - textInfo.size("Adding black tulips...")[0]) // 2, Height // 2 + 50))
                Black_tulip = pygame.image.load(path + "Gannitto world/files/Images/Items/Black tulip.png")
                for _ in range(random.randint(1000, 5000)):
                    objects.append(Object(
                        "Black tulip",
                        random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000),
                        "Gannitto world/files/Images/Items/Black tulip.png", image=Black_tulip, special_flags="Item"))
                pygame.display.update()



                win.fill((192, 203, 220), (0, Height // 2 + 18, Width, Height))
                win.blit(textInfo.render("World generation - 56%", True, (139, 155, 180)), ((Width - textInfo.size("World generation - 56%")[0]) // 2, Height // 2 + 20))
                win.blit(textInfo.render("Adding red tulips...", True, (139, 155, 180)), ((Width - textInfo.size("Adding red tulips...")[0]) // 2, Height // 2 + 50))
                Red_tulip = pygame.image.load(path + "Gannitto world/files/Images/Items/Red tulip.png")
                for _ in range(random.randint(1000, 5000)):
                    objects.append(Object(
                        "Red tulip",
                        random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000),
                        "Gannitto world/files/Images/Items/Red tulip.png", image=Red_tulip, special_flags="Item"))
                pygame.display.update()



                win.fill((192, 203, 220), (0, Height // 2 + 18, Width, Height))
                win.blit(textInfo.render("World generation - 64%", True, (139, 155, 180)), ((Width - textInfo.size("World generation - 64%")[0]) // 2, Height // 2 + 20))
                win.blit(textInfo.render("Adding yellow tulips...", True, (139, 155, 180)), ((Width - textInfo.size("Adding yellow tulips...")[0]) // 2, Height // 2 + 50))
                Yellow_tulip = pygame.image.load(path + "Gannitto world/files/Images/Items/Yellow tulip.png")
                for _ in range(random.randint(1000, 5000)):
                    objects.append(Object(
                        "Yellow tulip",
                        random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000),
                        "Gannitto world/files/Images/Items/Yellow tulip.png", image=Yellow_tulip, special_flags="Item"))
                pygame.display.update()



                win.fill((192, 203, 220), (0, Height // 2 + 18, Width, Height))
                win.blit(textInfo.render("World generation - 72%", True, (139, 155, 180)), ((Width - textInfo.size("World generation - 72%")[0]) // 2, Height // 2 + 20))
                win.blit(textInfo.render("Adding mushrooms...", True, (139, 155, 180)), ((Width - textInfo.size("Adding mushrooms...")[0]) // 2, Height // 2 + 50))
                Mushroom = pygame.image.load(path + "Gannitto world/files/Images/Items/Mushroom.png")
                for _ in range(random.randint(1000, 5000)):
                    objects.append(Object(
                        "Mushroom",
                        random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000),
                        "Gannitto world/files/Images/Items/Mushroom.png", image=Mushroom, special_flags="Item"))
                pygame.display.update()



                win.fill((192, 203, 220), (0, Height // 2 + 18, Width, Height))
                win.blit(textInfo.render("World generation - 80%", True, (139, 155, 180)), ((Width - textInfo.size("World generation - 80%")[0]) // 2, Height // 2 + 20))
                win.blit(textInfo.render("Adding red mushrooms...", True, (139, 155, 180)), ((Width - textInfo.size("Adding red mushrooms...")[0]) // 2, Height // 2 + 50))
                Red_mushroom = pygame.image.load(path + "Gannitto world/files/Images/Items/Red mushroom.png")
                for _ in range(random.randint(1000, 5000)):
                    objects.append(Object(
                        "Red mushroom",
                        random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000),
                        "Gannitto world/files/Images/Items/Red mushroom.png", image=Red_mushroom, special_flags="Item"))
                pygame.display.update()



                win.fill((192, 203, 220), (0, Height // 2 + 18, Width, Height))
                win.blit(textInfo.render("World generation - 88%", True, (139, 155, 180)), ((Width - textInfo.size("World generation - 88%")[0]) // 2, Height // 2 + 20))
                win.blit(textInfo.render("Adding trees...", True, (139, 155, 180)), ((Width - textInfo.size("Adding trees...")[0]) // 2, Height // 2 + 50))
                Tree = pygame.image.load(path + "Gannitto world/files/Images/Objects/Tree.png")
                for _ in range(random.randint(10000, 50000)):
                    objects.append(Object(
                        "Tree",
                        random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000), 
                        "Gannitto world/files/Images/Objects/Tree.png", [256, 256], Tree, special_flags=100))




            case "Sand":

                
                win.blit(textInfo.render("World generation - 0%", True, (139, 155, 180)), ((Width - textInfo.size("World generation - 0%")[0]) // 2, Height // 2 + 20))
                win.blit(textInfo.render("Adding cactuses...", True, (139, 155, 180)), ((Width - textInfo.size("Adding cactuses...")[0]) // 2, Height // 2 + 50))
                Cactus = pygame.image.load(path + "Gannitto world/files/Images/Objects/Cactus.png")
                for _ in range(random.randint(5000, 10000)):
                    objects.append(Object(
                        "Cactus",
                        random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000),
                        "Gannitto world/files/Images/Objects/Cactus.png", [256, 256], Cactus))
                pygame.display.update()



                win.fill((192, 203, 220), (0, Height // 2 + 18, Width, Height))
                win.blit(textInfo.render("World generation - 50%", True, (139, 155, 180)), ((Width - textInfo.size("World generation - 50%")[0]) // 2, Height // 2 + 20))
                win.blit(textInfo.render("Adding piles of sand...", True, (139, 155, 180)), ((Width - textInfo.size("Adding piles of sand...")[0]) // 2, Height // 2 + 50))
                Pile_of_sand = pygame.image.load(path + "Gannitto world/files/Images/Objects/Pile of sand.png")
                for _ in range(random.randint(500, 1000)):
                    objects.append(Object(
                        "Pile of sand",
                        random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000),
                        "Gannitto world/files/Images/Objects/Pile of sand.png", [256, 256] ,Pile_of_sand))
                pygame.display.update()




            case "Swamp":
                

                win.blit(textInfo.render("World generation - 0%", True, (139, 155, 180)), ((Width - textInfo.size("World generation - 0%")[0]) // 2, Height // 2 + 20))
                win.blit(textInfo.render("Adding dark trees...", True, (139, 155, 180)), ((Width - textInfo.size("Adding dark trees...")[0]) // 2, Height // 2 + 50))
                Dark_tree = pygame.image.load(path + "Gannitto world/files/Images/Objects/Dark tree.png")
                for _ in range(random.randint(3000, 8000)):
                    objects.append(Object(
                        "Dark tree",
                        random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000),
                        "Gannitto world/files/Images/Objects/Dark tree.png", [256, 256], Dark_tree))
                pygame.display.update()


                
                win.fill((192, 203, 220), (0, Height // 2 + 18, Width, Height))
                win.blit(textInfo.render("World generation - 33%", True, (139, 155, 180)), ((Width - textInfo.size("World generation - 33%")[0]) // 2, Height // 2 + 20))
                win.blit(textInfo.render("Adding mushrooms...", True, (139, 155, 180)), ((Width - textInfo.size("Adding mushrooms...")[0]) // 2, Height // 2 + 50))
                Mushroom = pygame.image.load(path + "Gannitto world/files/Images/Items/Mushroom.png")
                for _ in range(random.randint(1000, 5000)):
                    objects.append(Object(
                        "Mushroom",
                        random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000),
                        "Gannitto world/files/Images/Items/Mushroom.png", image=Mushroom, special_flags="Item"))
                pygame.display.update()



                win.fill((192, 203, 220), (0, Height // 2 + 18, Width, Height))
                win.blit(textInfo.render("World generation - 66%", True, (139, 155, 180)), ((Width - textInfo.size("World generation - 66%")[0]) // 2, Height // 2 + 20))
                win.blit(textInfo.render("Adding red mushrooms...", True, (139, 155, 180)), ((Width - textInfo.size("Adding red mushrooms...")[0]) // 2, Height // 2 + 50))
                Red_mushroom = pygame.image.load(path + "Gannitto world/files/Images/Items/Mushroom.png")
                for _ in range(random.randint(1000, 5000)):
                    objects.append(Object(
                        "Red mushroom",
                        random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000),
                        "Gannitto world/files/Images/Items/Red mushroom.png", image=Red_mushroom, special_flags="Item"))
                
                



            case "Snow":


                win.fill((192, 203, 220), (0, Height // 2 + 18, Width, Height))
                win.blit(textInfo.render("World generation - 0%", True, (139, 155, 180)), ((Width - textInfo.size("World generation - 0%")[0]) // 2, Height // 2 + 20))
                win.blit(textInfo.render("Adding spruces...", True, (139, 155, 180)), ((Width - textInfo.size("Adding spreces...")[0]) // 2, Height // 2 + 50))
                Spruce = pygame.image.load(path + "Gannitto world/files/Images/Objects/Spruce.png")
                for _ in range(random.randint(3000, 8000)):
                    objects.append(Object(
                        "Spruce",
                        random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000),
                        "Gannitto world/files/Images/Objects/Spruce.png", [512, 512], Spruce))
                pygame.display.update()



                win.fill((192, 203, 220), (0, Height // 2 + 18, Width, Height))
                win.blit(textInfo.render("World generation - 50%", True, (139, 155, 180)), ((Width - textInfo.size("World generation - 50%")[0]) // 2, Height // 2 + 20))
                win.blit(textInfo.render("Adding dark bushes...", True, (139, 155, 180)), ((Width - textInfo.size("Adding dark bushes...")[0]) // 2, Height // 2 + 50))
                Dark_bush = pygame.image.load(path + "Gannitto world/files/Images/Objects/Dark bush.png")
                for _ in range(random.randint(3000, 8000)):
                    objects.append(Object(
                        "Dark tree",
                        random.randint(self.x - 50000, self.x + 50000), random.randint(self.y - 50000, self.y + 50000),
                        "Gannitto world/files/Images/Objects/Dark bush.png", [128, 128], Dark_bush))
        return objects



    def main(self):
        from Gannitto_world import x, y
        if self.x - 50000 <= x <= self.x + 50000 and self.y - 50000 <= y <= self.y + 50000:
            return self.biom
        else:
            return None


