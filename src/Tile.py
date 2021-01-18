import pygame
class Tile(): 
    def __init__(self, window, size, xpos, ypos, header=None):
        self.size = size
        self.font = pygame.font.SysFont('Arial', int(size * 0.6))
        self.window = window
        self.color =  pygame.Color(0, 64, 64, 64)
        self.rectangle = pygame.Rect(xpos, ypos, size, size)
        self.offset_letter = int(size * 0.3)
        self.xpos = xpos
        self.ypos = ypos
        self.header = header

    def draw(self):
        if(self.header):
            self.window.blit(self.font.render(self.header, True, (255,0,0)), (self.xpos+self.offset_letter, self.ypos+self.offset_letter))
        else:
            pygame.draw.rect(self.window, self.color, self.rectangle, 2)
    
    def clicked(self, pos):
        return pos[0] >= self.xpos and pos[0] <= self.xpos + self.size and pos[1] >= self.ypos and pos[1] <= self.ypos + self.size
