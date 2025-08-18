import pygame

class Room:
    def __init__(self, x, y, width, height, name):
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.font = pygame.font.Font(None, 24)

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        text = self.font.render(self.name, True, (0, 0, 0))
        screen.blit(text, (self.rect.x + 10, self.rect.y + 10))
