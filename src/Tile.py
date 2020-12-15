import pygame
# tutaj jest pojedynczy kafelek z siatki planszy
class Tile(): 
    def __init__(self, window, size, xpos, ypos, header=None):
        # ustawiamy czcionkę i odpowiedni rozmiar, aby wartości z wiersza i kolumny z oznaczeniami były w odpowiednich pozycjach
        self.font = pygame.font.SysFont('Arial', int(size * 0.6))
        self.window = window
        # ustalamy kolor kafelków w modelu RGBA
        self.color =  pygame.Color(0, 64, 64, 64)
        # tworzymy kwadrat w danym położeniu, o danym rozmiarze
        self.rectangle = pygame.Rect(xpos, ypos, size, size)
        # dodatkowo ustalamy rozmiar czcionki liter proporcjonalny do rozmiaru planszy
        self.offset_letter = int(size * 0.3)
        # wartości x i y
        self.xpos = xpos
        self.ypos = ypos
        if(header):
            # jeśli znajduje się wiersz/kolumna z oznaczeniami to je zaznaczamy z odpowiednimi parametrami
            self.window.blit(self.font.render(header, True, (255,0,0)), (xpos+self.offset_letter, ypos+self.offset_letter))
        else:
            # jeśli nie ma żadnego nagłówka to rysujemy po prostu siatkę
            pygame.draw.rect(window, self.color, self.rectangle, 2)