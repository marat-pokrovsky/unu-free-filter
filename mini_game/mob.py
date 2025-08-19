import pygame
import random

class Mob:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.direction_change_interval = 60  # Change direction every 60 frames
        self.direction_timer = 0
        self.direction_x = 0
        self.direction_y = 0
        self.change_direction()

    def change_direction(self):
        self.direction_x = random.choice([-1, 0, 1])
        self.direction_y = random.choice([-1, 0, 1])

    def update(self):
        self.direction_timer += 1
        if self.direction_timer >= self.direction_change_interval:
            self.direction_timer = 0
            self.change_direction()

        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed

        # Keep the mob within the screen boundaries
        if self.x < 0:
            self.x = 0
        if self.x > 800:
            self.x = 800
        if self.y < 0:
            self.y = 0
        if self.y > 600:
            self.y = 600


    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 8)
