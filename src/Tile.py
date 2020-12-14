import pygame
class Tile(): 
    def __init__(self, window, size, xpos, ypos, header=None):
        self.font = pygame.font.SysFont('Arial', int(size * 0.6))
        self.window = window
        self.color =  pygame.Color(0, 64, 64, 64)
        self.rectangle = pygame.Rect(xpos, ypos, size, size)
        self.offset_letter = int(size * 0.3)
        self.xpos = xpos
        self.ypos = ypos
        if(header):
            self.window.blit(self.font.render(header, True, (255,0,0)), (xpos+self.offset_letter, ypos+self.offset_letter))
        else:
            pygame.draw.rect(window, self.color, self.rectangle, 2)