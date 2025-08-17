import pygame
from room import Room

class House:
    def __init__(self):
        self.rooms = [
            Room(50, 50, 200, 150, "Living Room"),
            Room(300, 50, 200, 150, "Bedroom"),
            Room(50, 250, 200, 150, "Kitchen"),
            Room(300, 250, 200, 150, "Bathroom"),
        ]

    def draw(self, screen):
        for room in self.rooms:
            room.draw(screen)
