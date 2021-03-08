import pygame


class GenericButton:
    def __init__(self, w, h, x, y, header, window):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.header = header
        print(self.header)
        self.font = pygame.font.SysFont("Arial", int(h * 0.6))
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
