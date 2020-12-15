import pygame

# tworzymy klasę dotyczącą przesuwalnego statku
class DraggableShip():
    def __init__(self, window, size, xpos, ypos, length):
        self.window = window
        self.color =  pygame.Color(0, 120, 120, 120)
        self.offset = int(size * 0.2)
        for i in range (0, length):
            # definiujemy odpowiedni kwadrat z opcjami pozycji i rozmiaru danego statku
            rectangle = pygame.Rect((xpos +self.offset/2) + i*size, ypos+self.offset/1.6, int(size * 0.8), int(size * 0.8))
            # rysujemy statek 
            pygame.draw.rect(self.window, self.color, rectangle)