import pygame

class Ship():
    def __init__(self, window, size, xpos, ypos):
        self.window = window
        self.color =  pygame.Color(0, 120, 120, 120)
        self.offset = int(size * 0.2)
        self.rectangle = pygame.Rect(xpos +self.offset/2, ypos+self.offset/1.6, int(size * 0.8), int(size * 0.8))
        pygame.draw.rect(self.window, self.color, self.rectangle)