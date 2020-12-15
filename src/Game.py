# importujemy wszystkie biblioteki i funkcje oraz klasy z innych plików projektu
import os
import pygame
import pygame_menu
import constants
from Tile import Tile
from set_ships import draw_matrix
from Ship import Ship
from DraggableShip import DraggableShip

# eventy, które zachodzą do tej pory (etap tworzenia oraz etap startu gry)
ships_laoyout_stage=pygame.event.Event(pygame.USEREVENT, attr1='layout_stage')
start_game_stage=pygame.event.Event(pygame.USEREVENT, attr1='start_game_stage')

# klasa Game
class Game(): 
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self.ships_layout_type = 0
        self.main_loop()
# Rysowanie menu, funkcja draw_menu przyjmuje jako argument size, a w funkcji start_the_game od razu przypisujemy 
# board_size (rozmiar planszy) pod ten size. W zależności od wybranego rozmiaru, do listy z dostępnymi statkami (available_ships)
# pobieramy odpowiednią tablicę z pliku constants. Board_size podajemy tutaj o 1 wyższy niż w rzeczywistości rysujemy, ponieważ 
# uwzględniamy 1 wiersz i 1 kolumnę na oznaczenia cyfrowe i literowe.
    def draw_menu(self):
        def start_the_game(size):
            self.board_size=size
            if(self.board_size == 10):
                self.avalaible_ships = constants.SHIPS_9
            if(self.board_size == 13):
                self.avalaible_ships = constants.SHIPS_12
            if(self.board_size == 16):
                self.avalaible_ships = constants.SHIPS_15
            pygame.event.post(ships_laoyout_stage) # uruchamiamy wydarzenie, które obejmuje etap tworzenia

# tutaj zajmujemy się menu głównym
        def set_ships_layout(selected, value):
            self.ships_layout_type = selected[1] # domyślnie sposób ułożenia jest losowy
# tworzenie menu za pomocą biblioteki pygame_menu, ustawiamy jego wielkość na taką, jak wielkość okna (z pliku constants.py)
        self.menu = pygame_menu.Menu(height=constants.HEIGHT,
                        width=constants.WIDTH,
                        theme=pygame_menu.themes.THEME_BLUE,
                        title='Board size')
# tutaj znajdują się przyciski widoczne w menu oraz rodzaj ułożenia do wyboru. Ułożenie zmiania set_ships_layout za pomocą zmiany
# wartości 0 (losowe ułożenie) na wartość 1 (ręczne ułożenie).
        self.menu.add_selector('Ships layout: ', [('Random', 0), ('Pick', 1)], onchange=set_ships_layout)
# Przyciski do wyboru rozmiaru planszy. Funkcja lambda przekazuje wywołanie funkcji start_the_game z odpowiednim argumentem ponownie
# zwiększonym o 1 (ponownie uwzglądniemy 1 kolumnę i 1 wiersz na oznaczenia cyfrowe i literowe).        
        self.menu.add_button('9 x 9', lambda: start_the_game(10))
        self.menu.add_button('12 x 12', lambda: start_the_game(13))
        self.menu.add_button('15 x 15', lambda: start_the_game(16))
# Przycisk exit, wywołujący zamknięcie programu       
        self.menu.add_button('Exit', pygame_menu.events.EXIT)

# Główna pętla, która wywołuje rysowanie menu. Pygame opiera się na wydarzeniach (events)
    def main_loop(self):
        # rysowanie menu
        self.draw_menu()
        # dopóki okno gry jest otwarte
        while True:
            # pobieramy i sprawdzamy wydarzenia
            events = pygame.event.get()
            for event in events:
                # jeśli wydarzenie jest typu pygame.QUIT, program się zamyka
                if event.type == pygame.QUIT:
                    exit()
# jeśli wydarzenie to zdefiniowany przez nas etap ustawiania statków to
                if event == ships_laoyout_stage:
                    # ustawiamy czarny kolor planszy
                    self.surface.fill((0,0,0))
                    # ukrywamy menu
                    self.menu.disable()
                    # jeśli wybraliśmy losowe ułożenie statków
                    if self.ships_layout_type == 0:
                        # rysujemy odpowiednią planszę
                        self.ships_matrix = draw_matrix(self.board_size-1)
                        # uruchamiamy wydarzenie startu gry
                        pygame.event.post(start_game_stage)
                    # jeśli wybraliśmy ręczne ustawienie statków 
                    else:
                        # tworzymy pustą macierz
                        self.ships_matrix=[[]]
                        # ustawiamy statki na planszy przeciwnika
                        self.draw_board(chosing_stage=True)
                # jeśli wydarzenie to start gry
                if event == start_game_stage:
                    # ustawiamy czarną planszę
                    self.surface.fill((0,0,0))
                    # rysujemy siatkę planszy oraz statki
                    self.draw_board()
                    self.draw_ships()

            # jeśli menu jest aktywne
            if self.menu.is_enabled():
                # menu się aktualizuje na podstawie eventów
                self.menu.update(events)
                # menu jest rysowane w oknie
                self.menu.draw(self.surface)

            pygame.display.update()
            
# tworzymy siatkę planszy
    def draw_grid(self, offsetX, offsetY):
        # tworzymy listę list na kafelki, o długości od 0 do rozmiaru planszy
        tiles = [[] for i in range(0, self.board_size)]
        # dla każdego x i y, czyli wypółrzędnych danego kafelka
        for x in range (0, self.board_size):
            for y in range(0, self.board_size):
                # jeśli zarówno x i y mają wartość 0, to nie rysujemy siatki (zostawiamy 1 "kratkę" nienarysowaną, żeby 
                # wszystko się zgadzało po nanaiesieniu liczb oraz liter), po prostu przechodzimy dalej
                if(x == 0 and y == 0):
                    continue
                # w kolumnie 0 umieszczamy oznaczenia literowe
                if(x==0):
                    header = constants.LETTERS[y-1]
                # w wierszu 0 umieszczamy oznaczenia liczbowe
                elif(y == 0):
                    header = str(x)
                # jeśli nie mamy oznaczeń liczbowych ani literowych, to nic się tutaj nie tworzy
                else:
                    header = None
                # poszczególne kafelki w siatce są dodawane do listy tiles, trzeba dać im jako parametry surface (okno) oraz wymiary:
                # rozmiar kafelka, odległości, w których mają być rysowane kafelki (odpowiednie przemnożenie x i y dla każdego elementu)
                # offsetX i offsetY to wybrane metodą prób i błędów wartości, aby przesunąć każdy element o stałą wartość
                tiles[x].append(Tile(self.surface, self.tile_width, x*self.tile_width+offsetX, y*self.tile_width+offsetY, header=header))
        return tiles
# rysowanie planszy, chosing_stage odpowiada za renderowanie planszy gracza z przesuwalnymi statkiami lub z planszą przeciwnika po prawej stronie (true/false) 
    def draw_board(self, chosing_stage=False):
        # ustawiamy szerokość kafelka
        self.tile_width = ((constants.WIDTH - 100)/ self.board_size) / 2  
        # ustawiamy odległość planszy przeciwnika od planszy gracza
        self.offset_enemy_grid = self.tile_width * self.board_size + 50
        # tutaj są te wartości odległości, które sobie dopasowaliśmy
        offsetX = 20
        offsetY = 20
        # planszę gracza zaczynamy rysować od miejsca o współrzędnych okna (offsetX, offsetY) 
        self.player_board = self.draw_grid(offsetX, offsetY)
        # jeśli chosing_stage == True
        if chosing_stage:
            # rysujemy po prawej stronie statki czekające na ułożenie na planszy
            self.draw_draggable_ships()
        else:
            # w przeciwnym przypadku jest rysowana plansza przeciwnika
            self.enemy_board = self.draw_grid(self.offset_enemy_grid, offsetY)
# rysowanie statków
    def draw_ships(self):
        # tworzymy listę na kafelki statków
        self.ship_tiles = []
        # dla współrzędnych x i y sprawdzamy
        for x in range(0, len(self.ships_matrix)):
            for y in range(0, len(self.ships_matrix[x])):
                # jeśli wartość w danej współrzędnej wynosi 1
                if(self.ships_matrix[x][y] == 1):
                    # wstawaimy kafelek statku, bierzemy pod uwagę okno, szerokość kafelka oraz wymiary planszy gracza
                    # przesuwamy dane miejsce o 1, ponieważ uwzględniamy 1 wiersz i 1 kolumnę, które wykorzystaliśmy na oznaczenia
                    self.ship_tiles.append(Ship(self.surface, self.tile_width, self.player_board[x+1][y+1].ypos, self.player_board[x+1][y+1].xpos))
 # rysowanie przesuwalnych statków (to jeszcze jest niedopracowane, ponieważ na razie nie działa i to jest wersja, którą aktualnie
 # będziemy rozbudowywać i testować)       
    def draw_draggable_ships(self):
        line_number = 1
        for ship in self.avalaible_ships:
            DraggableShip(self.surface, self.tile_width, self.offset_enemy_grid+50, line_number*1.5*self.tile_width, ship)
            line_number += 1