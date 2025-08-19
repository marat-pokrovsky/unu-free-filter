import pygame
import random
from player import Player
from house import House
from mob import Mob

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Smart Home Adventure")

        self.player = Player(400, 300)
        self.house = House()
        self.mobs = [Mob(random.randint(0, 800), random.randint(0, 600)) for _ in range(5)]


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.player.handle_keys()

            for mob in self.mobs:
                mob.update()

            self.screen.fill((255, 255, 255))  # White background

            self.house.draw(self.screen)
            self.player.draw(self.screen)

            for mob in self.mobs:
                mob.draw(self.screen)

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
