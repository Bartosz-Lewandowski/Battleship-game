import pygame
import uuid

class DraggableShip():
    def __init__(self, window, size, xpos, ypos, length):
        self.id = uuid.uuid4().hex 
        self.xpos = xpos
        self.ypos = ypos
        self.length = length
        self.size = size
        self.window = window
        self.color =  pygame.Color(0, 120, 120, 120)
        self.offset = int(size * 0.2)
        self.draw_rotated = False

    def draw(self):
        for i in range (0, self.length):
            if self.draw_rotated:
                rectangle = pygame.Rect((self.xpos +self.offset/2) , self.ypos+self.offset/1.6 + i*self.size, int(self.size * 0.8), int(self.size * 0.8))
                pygame.draw.rect(self.window, self.color, rectangle)
            else:
                rectangle = pygame.Rect((self.xpos +self.offset/2) + i*self.size, self.ypos+self.offset/1.6, int(self.size * 0.8), int(self.size * 0.8))
                pygame.draw.rect(self.window, self.color, rectangle)

    def is_dragged(self, pos):
        
        if pos[0] >= self.xpos and pos[0] <= self.xpos + self.size and pos[1] >= self.ypos and pos[1] <= self.ypos + self.size:
            self.draw_rotated = False
            return True

        elif not self.draw_rotated:
            if pos[0] >= self.xpos and pos[0] <= self.xpos + self.size * self.length and pos[1] >= self.ypos and pos[1] <= self.ypos + self.size:
                self.draw_rotated = True
                return True
        elif self.draw_rotated:
            if pos[0] >= self.xpos and pos[0] <= self.xpos + self.size and pos[1] >= self.ypos + self.size and pos[1] <= self.ypos +  self.length * self.size :
                self.draw_rotated = True
                return True
        return False

    def move(self, pos):
        for i in range (0, self.length):
            if self.draw_rotated:
                rectangle = pygame.Rect((pos[0] - self.offset*1.5), (pos[1] - self.offset*1.5  + i*self.size), int(self.size * 0.8), int(self.size * 0.8))
                pygame.draw.rect(self.window, self.color, rectangle)
            else:
                rectangle = pygame.Rect((pos[0] - self.offset*1.5) + i*self.size, pos[1]-self.offset*1.5, int(self.size * 0.8), int(self.size * 0.8))
                pygame.draw.rect(self.window, self.color, rectangle)

    def set_new_pos(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos