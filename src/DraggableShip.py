import pygame
import uuid
# klasa dotycząca przesuwalnego statku
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
    # poprawiamy to co było tu wcześniej i zapisujemy w funkcji, matodą prób i błędów ustaliliśmy pozycje i rozmiary przeciągalnego statku           
    def draw(self):
        for i in range (0, self.length):
            if self.draw_rotated:
                rectangle = pygame.Rect((self.xpos +self.offset/2) , self.ypos+self.offset/1.6 + i*self.size, int(self.size * 0.8), int(self.size * 0.8))
                pygame.draw.rect(self.window, self.color, rectangle)
            else:
                rectangle = pygame.Rect((self.xpos +self.offset/2) + i*self.size, self.ypos+self.offset/1.6, int(self.size * 0.8), int(self.size * 0.8))
                pygame.draw.rect(self.window, self.color, rectangle)
    # funkcja odpowiadająca za przeciągalność statku - pos to aktualna pozycja kursora myszy na planszy
    def is_dragged(self, pos):
        # jeśli wartość współrzędnej x kursora myszy jest większa lub równa współrzędnej x początku kafelka i wartość współrzędnej x kursora myszy jest mniejsza lub równa od współrzędnej x początku 
        # kafelka zwiększonej o długość kafelka i wartość współrzędnej y kursora myszy jest większa lub równa współrzędnej y początku kafelka i wartość współrzędnej y kursora myszy jest mniejsza 
        # lub równa od współrzędnej y początku kafelka zwiększonej o długość kafelka - to znaczy że kursor znajduje się w pierwszym kafelku statku, czyli po kliknięciu nie obracamy statku (jest poziomy)
        if pos[0] >= self.xpos and pos[0] <= self.xpos + self.size and pos[1] >= self.ypos and pos[1] <= self.ypos + self.size:
            self.draw_rotated = False
            return True
        # sprawdzamy jak wyżej, ale czy kursor znajduje się w dalszych kafelku statku, który jest ułożony w poziomie, jeśli tak to obracamy statek i ostatecznie będzie on ustawiony pioniowo
        elif not self.draw_rotated:
            if pos[0] >= self.xpos and pos[0] <= self.xpos + self.size * self.length and pos[1] >= self.ypos and pos[1] <= self.ypos + self.size:
                self.draw_rotated = True
                return True
        # sprawdzamy to samo, ale dla statku ustawionego w pionie, jeśli kursor jest nad innym kafelkiem niż pierwszy to zostawiamy statek w pionie
        elif self.draw_rotated:
            if pos[0] >= self.xpos and pos[0] <= self.xpos + self.size and pos[1] >= self.ypos + self.size and pos[1] <= self.ypos +  self.length * self.size :
                self.draw_rotated = True
                return True
        return False
    # funkcja odpowiedzialna za przenoszenie statków na planszę, są ustalone dla nich parametry takie jak pozycja, czy wymiary
    # ustawione statki przyjmują aktualną pozycję kursora myszy w miejscu, w którym zostały upuszczone
    def move(self, pos):
        for i in range (0, self.length):
            if self.draw_rotated:
                rectangle = pygame.Rect((pos[0] - self.offset*1.5), (pos[1] - self.offset*1.5  + i*self.size), int(self.size * 0.8), int(self.size * 0.8))
                pygame.draw.rect(self.window, self.color, rectangle)
            else:
                rectangle = pygame.Rect((pos[0] - self.offset*1.5) + i*self.size, pos[1]-self.offset*1.5, int(self.size * 0.8), int(self.size * 0.8))
                pygame.draw.rect(self.window, self.color, rectangle)
    # ustawianie nowych współrzędnych
    def set_new_pos(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos