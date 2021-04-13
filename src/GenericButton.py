import pygame
from parse_path import parse_path

class GenericButton:
    def __init__(self, w, h, x, y, header, window):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.header = header
        self.font_name = parse_path('8-BIT WONDER.TTF')
        self.font = pygame.font.Font(self.font_name, int(h * 0.4))
        self.window = window
        self.color = pygame.Color(0, 164, 164, 164)
        self.rectangle = pygame.Rect(x, y, w, h)
        self.offset_letter=int(self.h * 0.3)

    def draw(self):
        if self.header:
            self.window.blit(
                self.font.render(self.header, True, (200, 200, 200)),
                (self.x + self.offset_letter, self.y + self.offset_letter),
            )

    def clicked(self, pos):
        return (
            pos[0] >= self.x
            and pos[0] <= self.x + self.w
            and pos[1] >= self.y
            and pos[1] <= self.y + self.h
        )
