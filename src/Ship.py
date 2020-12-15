import pygame

# tworzymy klasę dla statku
class Ship():
    # funkcji przekazujemy okno, rozmiar statku oraz pozycję w postaci x i y
    def __init__(self, window, size, xpos, ypos):
        self.window = window
        # ustalamy kolor statków w modelu RGBA
        self.color =  pygame.Color(0, 120, 120, 120)
        # dopasowujemy rozmiar kafelka metodą prób i błędów
        self.offset = int(size * 0.2)
        # definiujemy kwadratowy kafelek i dajemy mu odpowiednie wymiary, aby znajdował się w danym miejscu planszy
        self.rectangle = pygame.Rect(xpos +self.offset/2, ypos+self.offset/1.6, int(size * 0.8), int(size * 0.8))
        # rysujemy powyższy kafelek w oknie, w danym kolorze
        pygame.draw.rect(self.window, self.color, self.rectangle)