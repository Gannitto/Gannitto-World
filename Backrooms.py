"""All information about backrooms is in this module"""

from random import *
import pygame
pygame.init()

win = pygame.display.set_mode((1000,700), pygame.RESIZABLE)

InBackrooms = False
objects = []
objects_x = []
objects_y = []
objects_w = []
objects_h = []
Level = 0
Light = 1
room_x = 0
room_y = 0

class Room():
    def __init__(self, x: int, y: int):
        class RoomObject():
            def __init__(self, x: int, y: int, w: int, h: int):
                self.x = x
                self.y = y
                self.w = w
                self.h = h
                self.biggest = False
                self.type = randint(0, 1)
                if self.type == 0:
                    match Level:
                        case 0:
                            self.color = (120, 100, 40, 1)
                        case 0.2:
                            self.color = (170, 60, 50, 1)
                        case 1:
                            self.color = (100, 100, 100, 1)
                else:
                    match Level:
                        case 0:
                            self.color = (180, 160, 50)
                        case 0.2:
                            self.color = (200, 180, 70)
                        case 1:
                            self.color = (50, 50, 50)
        self.x = x
        self.y = y
        self.rect1 = RoomObject(x * 1000, y * 1000, randint(100, 900), 1000)
        self.rect2 = RoomObject(x * 1000 + self.rect1.w, y * 1000, 1000 - self.rect1.w, 1000)
        self.rect1_1 = RoomObject(x * 1000, y * 1000, self.rect1.w, randint(100, 900))
        self.rect1_2 = RoomObject(x * 1000, self.rect1_1.h, self.rect1.w, 1000 - self.rect1_1.h)
        self.rect2_1 = RoomObject(x * 1000 + self.rect1.w, y * 1000, self.rect2.w, randint(100, 1000))
        self.rect2_2 = RoomObject(x * 1000 + self.rect1.w, y * 1000 + self.rect2_1.h, self.rect2.w, 1000 - self.rect2_1.h)
        
        if self.rect1_1.w * self.rect1_1.h > self.rect1_2.w * self.rect1_2.h and self.rect1_1.w * self.rect1_1.h > self.rect2_1.w * self.rect2_1.h and self.rect1_1.w * self.rect1_1.h > self.rect2_2.w * self.rect2_2.h:
            self.rect1_1.biggest = True
            self.rect1_1.type = 0
            if randint(1, 3) == 1:
                objects.append("Almond whater")
                objects_x.append(self.rect1.x)
                objects_y.append(self.rect1.y)
                objects_w.append(64)
                objects_h.append(64)
        elif self.rect1_2.w * self.rect1_2.h > self.rect1_1.w * self.rect1_1.h and self.rect1_2.w * self.rect1_2.h > self.rect2_1.w * self.rect2_1.h and self.rect1_2.w * self.rect1_2.h > self.rect2_2.w * self.rect2_2.h:
            self.rect1_2.biggest = True
            self.rect1_2.type = 0
            match Level:
                case 0:
                    self.rect1_2.color = (120, 100, 40)
                case 1:
                    self.rect1_2.color = (100, 100, 100)
        elif self.rect2_1.w * self.rect2_1.h > self.rect1_2.w * self.rect1_2.h and self.rect2_1.w * self.rect2_1.h > self.rect1_1.w * self.rect1_1.h and self.rect2_1.w * self.rect2_1.h > self.rect2_2.w * self.rect2_2.h:
            self.rect2_1.biggest = True
            self.rect2_1.type = 0
            match Level:
                case 0:
                    self.rect2_1.color = (120, 100, 40)
                case 1:
                    self.rect2_1.color = (100, 100, 100)
        else:
            self.rect2_2.biggest = True
            self.rect2_2.type = 0
            match Level:
                case 0:
                    self.rect2_2.color = (120, 100, 40)
                case 1:
                    self.rect2_2.color = (100, 100, 100)
        
        if not self.rect1_1.biggest:
            self.rect1_1_1 = RoomObject(self.rect1_1.x, self.rect1_1.y, self.rect1_1.w, self.rect1_1.h)
            if self.rect1_1.h < self.rect1_1.w:
                self.rect1_1_1.h //= 2
                a = 1
            else:
                self.rect1_1_1.w //= 2
                a = 2
            self.rect1_1_2 = RoomObject(self.rect1_1_1.x, self.rect1_1_1.y, self.rect1_1_1.w, self.rect1_1_1.h)
            if a == 1:
                self.rect1_1_2.y += self.rect1_1_2.h
            else:
                self.rect1_1_2.x += self.rect1_1_2.w
        
        if not self.rect1_2.biggest:
            self.rect1_2_1 = RoomObject(self.rect1_2.x, self.rect1_2.y, self.rect1_2.w, self.rect1_2.h)
            if self.rect1_2.h < self.rect1_2.w:
                self.rect1_2_1.h //= 2
                a = 1
            else:
                self.rect1_2_1.w //= 2
                a = 2
            self.rect1_2_2 = RoomObject(self.rect1_2_1.x, self.rect1_2_1.y, self.rect1_2_1.w, self.rect1_2_1.h)
            if a == 1:
                self.rect1_2_2.y += self.rect1_2_2.h
            else:
                self.rect1_2_2.x += self.rect1_2_2.w
        
        if not self.rect2_1.biggest:
            self.rect2_1_1 = RoomObject(self.rect2_1.x, self.rect2_1.y, self.rect2_1.w, self.rect2_1.h)
            if self.rect1_2.h < self.rect2_1.w:
                self.rect2_1_1.h //= 2
                a = 1
            else:
                self.rect2_1_1.w //= 2
                a = 2
            self.rect2_1_2 = RoomObject(self.rect2_1_1.x, self.rect2_1_1.y, self.rect2_1_1.w, self.rect2_1_1.h)
            if a == 1:
                self.rect2_1_2.y += self.rect2_1_2.h
            else:
                self.rect2_1_2.x += self.rect2_1_2.w
        
        if not self.rect2_2.biggest:
            self.rect2_2_1 = RoomObject(self.rect2_2.x, self.rect2_2.y, self.rect2_2.w, self.rect2_2.h)
            if self.rect2_2.h < self.rect2_2.w:
                self.rect2_2_1.h //= 2
                a = 1
            else:
                self.rect2_2_1.w //= 2
                a = 2
            self.rect2_2_2 = RoomObject(self.rect2_2_1.x, self.rect2_2_1.y, self.rect2_2_1.w, self.rect2_2_1.h)
            if a == 1:
                self.rect2_2_2.y += self.rect2_2_2.h
            else:
                self.rect2_2_2.x += self.rect2_2_2.w
    
    def main(self, player_x: int, player_y: int):
        """Shows the room"""
        from Gannitto_world import x, y
        if not self.rect1_1.biggest:
            if self.rect1_1_1.type == 1:
                pygame.draw.rect(win, self.rect1_1_1.color, (self.rect1_1_1.x - player_x, player_y - self.rect1_1_1.y, self.rect1_1_1.w, self.rect1_1_1.h))
            if self.rect1_1_1.type == 1:
                pygame.draw.rect(win, self.rect1_1_2.color, (self.rect1_1_2.x - player_x, player_y - self.rect1_1_2.y, self.rect1_1_2.w, self.rect1_1_2.h))
        if not self.rect1_2.biggest:
            if self.rect1_2_1.type == 1:
                pygame.draw.rect(win, self.rect1_2_1.color, (self.rect1_2_1.x - player_x, player_y - self.rect1_2_1.y, self.rect1_2_1.w, self.rect1_2_1.h))
            if self.rect1_2_2.type == 1:
                pygame.draw.rect(win, self.rect1_2_2.color, (self.rect1_2_2.x - player_x, player_y - self.rect1_2_2.y, self.rect1_2_2.w, self.rect1_2_2.h))
        if not self.rect2_1.biggest:
            if self.rect2_1_1.type == 1:
                pygame.draw.rect(win, self.rect2_1_1.color, (self.rect2_1_1.x - player_x, player_y - self.rect2_1_1.y, self.rect2_1_1.w, self.rect2_1_1.h))
            if self.rect2_1_2.type == 1:
                pygame.draw.rect(win, self.rect2_1_2.color, (self.rect2_1_2.x - player_x, player_y - self.rect2_1_2.y, self.rect2_1_2.w, self.rect2_1_2.h))
        if not self.rect2_2.biggest:
            if self.rect2_2_1.type == 1:
                pygame.draw.rect(win, self.rect2_2_1.color, (self.rect2_2_1.x - player_x, player_y - self.rect2_2_1.y, self.rect2_2_1.w, self.rect2_2_1.h))
            if self.rect2_2_2.type == 1:
                pygame.draw.rect(win, self.rect2_2_2.color, (self.rect2_2_2.x - player_x, player_y - self.rect2_2.y, self.rect2_2_2.w, self.rect2_2_2.h))

class Wall:

    def __init__(self, x, y, type: int, Width: int = 1000, Height: int = 1000):
        self.x = x
        self.y = y
        self.type = type
        if self.type == 0:
            match Level:
                case 0:
                    self.color = (120, 100, 40)
                case 1 | 2:
                    self.color = (100, 100, 100)
        else:
            match Level:
                case 0:
                    self.color = (180, 160, 50)
                case 1 | 2:
                    self.color = (50, 50, 50)
        self.Width = Width
        self.Height = Height

    def main(self, player_x: int, player_y: int):
        match self.type:
            case 0:
                pygame.draw.rect(win, self.color, (self.x * 1000 - player_x, player_y - self.y, self.Width, self.Height))
            case 1:
                pygame.draw.rect(win, self.color, (self.x * 1000 - player_x, player_y - self.y, self.Width, self.Height))

def get_rooms(Room_x: int, Room_y: int):
    """Generates a random room"""

    global rooms
    match Level:
        case 0 | 0.2 | 1:
            rooms = [Room(Room_x * 2 + col, Room_y * 2 + row) for row in range(-5, 5) for col in range(-5, 5)]
        case 2:
            rooms = []
            for col in range(-5, 5):
                for row in range(-3, 3):
                    if Room_y == 0:
                        rooms.append(Wall(Room_x * 2 + col, Room_y * 2 + row, 0, Height=300))
                    else:
                        rooms.append(Wall(Room_x * 2 + col, Room_y * 2 + row, 1))

get_rooms(0, 0)
