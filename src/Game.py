import os
import pygame
import pygame_menu
from copy import deepcopy
from random import randint
import time 
import constants
from Tile import Tile
from set_ships import draw_matrix, set_ships
from Ship import Ship
from DraggableShip import DraggableShip
from GenericButton import GenericButton
from Shoot import Shoot

ships_layout_stage = pygame.event.Event(pygame.USEREVENT, attr1="layout_stage")
select_size_stage = pygame.event.Event(pygame.USEREVENT, attr1="select_size_stage")
start_game_stage = pygame.event.Event(pygame.USEREVENT, attr1="start_game_stage")
end_game = pygame.event.Event(pygame.USEREVENT, attr1="end_game")



class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Battleship')
        self.surface = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self.ships_layout_type = 0
        self.game_diff = 0
        self.my_theme = pygame_menu.themes.Theme(
            widget_font=pygame_menu.font.FONT_8BIT,
            background_color=(40, 41, 35),
            cursor_color=(255, 255, 255),
            cursor_selection_color=(80, 80, 80, 120),
            scrollbar_color=(39, 41, 42),
            scrollbar_slider_color=(65, 66, 67),
            selection_color=(255, 255, 255),
            title_background_color=(47, 48, 51),
            title_font_color=(215, 215, 215),
            widget_font_color=(200, 200, 200),
            title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
        )
        self.main_loop()

    def draw_menu(self):
        self.menu = pygame_menu.Menu(
            height=constants.HEIGHT,
            width=constants.WIDTH,
            theme=self.my_theme,
            title=" ",
        )
        
        self.main_menu()

    def main_loop(self):
        self.stage = "MENU"
        self.dragged_ship = None
        self.go_back_button = GenericButton(
            300,
            60,
            constants.WIDTH / 2 - 140,
            constants.HEIGHT - 80,
            "Back to menu",
            self.surface,
        )
        self.reset_layout = GenericButton(
            200,
            60,
            constants.WIDTH - 150,
            constants.HEIGHT - 950,
            "Reset",
            self.surface,
        )
        self.start_button = GenericButton(
            250,
            60,
            constants.WIDTH - 270,
            constants.HEIGHT - 1000,
            "Start Game",
            self.surface,
        )
        self.draw_menu()
        
        drag = False
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

                if event == ships_layout_stage:
                    self.surface.fill((40, 41, 35))
                    self.go_back_button.draw()
                    self.menu.disable()
                    if self.ships_layout_type == 0:
                        self.player_ships = set_ships(self.board_size - 1)
                        self.ships_matrix = draw_matrix(self.player_ships, self.board_size - 1)
                        self.stage = "PLAYING"
                        self.enemy_ships = set_ships(self.board_size - 1)
                        self.shooted = False
                        self.player_shooted = []
                        self.ai_shooted = []
                        pygame.event.post(start_game_stage)

                    else:
                        self.stage = "SET_SHIPS"
                        self.ships_matrix = [
                            [0 for i in range(0, self.board_size - 1)]
                            for i in range(0, self.board_size - 1)
                        ]
                        self.draw_board(chosing_stage=True)
                        self.go_back_button.draw()
                        self.reset_layout.draw()
                        self.start_button.draw()

                if event == start_game_stage:
                    self.surface.fill((40, 41, 35))
                    self.draw_board()
                    self.draw_ships()
                    self.go_back_button.draw()



                if event == end_game:
                    self.surface.fill((40, 41, 35))
                    if self.win == 1:
                        self.draw_text('You WON', 50, constants.WIDTH//2, constants.HEIGHT//2)
                    else:
                        self.draw_text("You LOST", 50, constants.WIDTH//2,constants.HEIGHT//2)
                    self.go_back_button.draw()


                # powstały 3 nowe eventy
                # mousebuttondown - naciśnięcie przycisku myszy
                # pos to współrzędne myszy
                # jesteśmy na etapie ustawiania statków
                # find_dragged znajduje kliknięty statek dla współrzędnych myszki i zapisuje go do self.dragged_ship
                # drag jest True bo jeszcze nie puściliśmy przycisku myszy
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.button_clicked = False
                    self.go_back_button.draw()
                    if self.go_back_button.clicked(pos) or self.reset_layout.clicked(pos):
                        self.button_clicked = True
                    if self.stage == "SET_SHIPS":
                        self.find_dragged(pos)
                        drag = True
                        self.reset_layout.draw()
                        self.start_button.draw()

                    if (self.stage == 'PLAYING' and 
                        pos[0] in range(int(self.tile_width) + int(self.offset_enemy_grid),int(self.tile_width * self.board_size) + int(self.offset_enemy_grid)) and 
                        pos[1] in range(int(self.tile_width) + self.offsetY,int(self.tile_width * self.board_size) + self.offsetY)):

                        

                        self.x = int((pos[0] - int(self.offset_enemy_grid))//self.tile_width)
                        self.y = int((pos[1] - self.offsetY)//self.tile_width)

                        if (self.x,self.y) in self.player_shooted:
                            print("You've already shot at this spot!")
                        else:
                            self.player_shooted.append((self.x,self.y))
                            self.enemy_ships = self.draw_shoot(self.x,self.y,self.enemy_board,self.enemy_ships,self.player_shooted)    
                            self.shooted = True

                        if self.shooted:                   
                            validate = False
                            while validate == False:
                                self.x_ai = randint(1,9)
                                self.y_ai = randint(1,9)
                                if (self.x_ai,self.y_ai) in self.ai_shooted:
                                    pass
                                else:
                                    validate = True
        
                            self.ai_shooted.append((self.x_ai,self.y_ai))
                            self.player_ships = self.draw_shoot(self.x_ai,self.y_ai,self.player_board, self.player_ships, self.ai_shooted)

                            print(self.enemy_ships)
                            self.shooted = False


                        if len(self.player_ships) == 0:
                            self.win = 0
                            pygame.event.post(end_game)
                        elif len(self.enemy_ships) == 0:
                            self.win = 1
                            pygame.event.post(end_game)


                # mousemotion - ruch myszy po planszy
                # etap przesuwania statku
                # bierzemy pozycję myszki i rysujemy od nowa planszę, statki i przesuwany statek
                if event.type == pygame.MOUSEMOTION:
                    if self.stage == "SET_SHIPS" and drag and self.dragged_ship is not None:
                        pos = pygame.mouse.get_pos()
                        self.surface.fill((40, 41, 35))
                        self.draw_playerboard()
                        self.draw_draggable_ships()
                        self.dragged_ship.move(pos)
                        self.go_back_button.draw()
                        self.reset_layout.draw()
                        self.start_button.draw()

                # mousebuttonup - zwolnienie przycisku myszy
                # pobieramy współrzędne myszki
                # do zmiennej tile zapisujemy kafelek na planszy, na który przesunęliśmy statek (jeśli to miejsce jest walidacyjne)
                # w if ustawiamy nową pozycję statku, jeśli miejsce jest poprawne
                # wszystko rysujemy ponownie
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.button_clicked and self.go_back_button.clicked(pos):
                            self.draw_menu()
                            self.stage = 'MENU'
                            self.button_clicked = False
    
                    if self.stage == "SET_SHIPS":
                        if self.dragged_ship is not None:
                            pos = pygame.mouse.get_pos()
                            tile = self.match_validate_tile_to_ship(pos)
                            if tile:
                                self.dragged_ship.set_new_pos(tile.xpos, tile.ypos)
                            self.dragged_ship = None
                            drag = False
                            self.surface.fill((40, 41, 35))
                            self.draw_playerboard()
                            self.draw_draggable_ships()
                            self.go_back_button.draw()
                            self.reset_layout.draw()
                            self.start_button.draw()

                        if self.button_clicked and self.reset_layout.clicked(pos):
                            self.surface.fill((40, 41, 35))
                            self.draw_playerboard()
                            self.ships_matrix = [
                                [0 for i in range(0, self.board_size - 1)]
                                for i in range(0, self.board_size - 1)
                            ]
                            self.draw_board(chosing_stage=True)
                            self.go_back_button.draw()
                            self.reset_layout.draw()
                            self.start_button.draw()
                            
                        if self.start_button.clicked(pos):
                            total_ship_tiles = 0
                            for row in self.ships_matrix:
                                for ship in row:
                                    if ship != 0:
                                        total_ship_tiles += 1
                            if total_ship_tiles == sum(self.avalaible_ships):
                                self.stage = "PLAYING"
                                pygame.event.post(start_game_stage)

            # main_loop end

            if self.menu.is_enabled():
                self.menu.update(events)
                self.menu.draw(self.surface)

            pygame.display.update()

    def main_menu(self):
        self.menu.clear()
        self.menu.add_image('statek.png', scale=(0.5,0.5))
        self.menu.add_vertical_margin(50)
        self.menu.add_label('MAIN MENU', font_size=100)
        self.menu.add_vertical_margin(200)
        
        self.menu.add_button("START GAME", lambda: self.start_the_game())
        self.menu.add_button("HELP", lambda: self.go_to_help())
        self.menu.add_button("Exit", pygame_menu.events.EXIT)

    def start_the_game(self):
        self.menu.clear()
        self.menu.add_label('Select board size', font_size=50)
        self.menu.add_vertical_margin(150)
        self.menu.add_button("9 x 9", lambda: self.select_size(10))
        self.menu.add_button("12 x 12", lambda: self.select_size(13))
        self.menu.add_button("15 x 15", lambda: self.select_size(16))
        self.menu.add_vertical_margin(100)
        self.menu.add_button('Back to menu', lambda: self.main_menu())

    def select_size(self,size):
        self.board_size = size
        if self.board_size == 10:
            self.avalaible_ships = constants.SHIPS_9
        if self.board_size == 13:
            self.avalaible_ships = constants.SHIPS_12
        if self.board_size == 16:
            self.avalaible_ships = constants.SHIPS_15
        self.menu.clear()
        self.menu.add_label('Select difficulty level', font_size=50)
        self.menu.add_vertical_margin(150)
        self.menu.add_button("Easy", lambda: self.select_difficulty(0))
        self.menu.add_button("Hard", lambda: self.select_difficulty(1))
        self.menu.add_vertical_margin(100)
        self.menu.add_button('Back to menu', lambda: self.main_menu())

    def select_difficulty(self,difficulty):
        if difficulty == 1:
            self.game_diff = 1
        elif difficulty == 0:
            self.game_diff = 0
        self.menu.clear()
        self.menu.add_label('Select ships layout', font_size=50)
        self.menu.add_vertical_margin(150)
        self.menu.add_button("Random", lambda: self.select_ships_layout(0))
        self.menu.add_button("Pick", lambda: self.select_ships_layout(1))
        self.menu.add_vertical_margin(100)
        self.menu.add_button('Back to menu', lambda: self.main_menu())
    
    def select_ships_layout(self,layout):
        if layout == 1:
            self.ships_layout_type = 1
        elif layout == 0:
            self.ships_layout_type = 0
        pygame.event.post(ships_layout_stage)
    
    def go_to_help(self):
        pass

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font('8-BIT WONDER.TTF',size)
        text_surface = font.render(text, True, (200, 200, 200))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.surface.blit(text_surface,text_rect)
    
    def draw_shoot(self, x,y, board,  x_ships, shooted):
        for ship in x_ships:
            if (x,y) in ship:
                col =  pygame.Color(255, 40, 0)
                Shoot(self.surface,
                        self.tile_width,
                        board[x][y].xpos,
                        board[x][y].ypos,
                        col
                        )
                break
            else :
                col = pygame.Color(128,128,128)
                Shoot(self.surface,
                        self.tile_width,
                        board[x][y].xpos,
                        board[x][y].ypos,
                        col
                        )

        for ship in x_ships:
            if all(x in shooted for x in ship):
                for j in ship:
                    x,y = j
                    col = pygame.Color(0,0,0)
                    Shoot(self.surface,
                        self.tile_width,
                        board[x][y].xpos,
                        board[x][y].ypos,
                        col
                        )
                x_ships.remove(ship)
        return x_ships      

    # tworzenie siatki planszy
    def generate_grid(self, offsetX, offsetY):
        tiles = [[] for i in range(0, self.board_size)]
        for x in range(0, self.board_size):
            for y in range(0, self.board_size):
                if x == 0 and y == 0:
                    continue
                if x == 0:
                    header = constants.LETTERS[y - 1]
                elif y == 0:
                    header = str(x)
                else:
                    header = None
                tiles[x].append(
                    Tile(
                        self.surface,
                        self.tile_width,
                        x * self.tile_width + offsetX,
                        y * self.tile_width + offsetY,
                        header=header,
                    )
                )
        return tiles

    # rysowanie planszy
    def draw_board(self, chosing_stage=False):
        self.tile_width = ((constants.WIDTH - 100) / self.board_size) // 2
        self.offset_enemy_grid = self.tile_width * self.board_size + 50
        self.offsetX = 20
        self.offsetY = 20
        self.player_board = self.generate_grid(self.offsetX, self.offsetY)
        self.draw_playerboard()
        if chosing_stage:
            line_number = 1
            self.draggable_ships = []
            for ship in self.avalaible_ships:
                self.draggable_ships.append(
                    DraggableShip(
                        self.surface,
                        self.tile_width,
                        self.offset_enemy_grid + 50,
                        line_number * 1.5 * self.tile_width,
                        ship,
                    )
                )
                line_number += 1
            self.draw_draggable_ships()
        else:
            self.enemy_board = self.generate_grid(self.offset_enemy_grid, self.offsetY)
            self.draw_enemyboard()

    def draw_ships(self):
        self.ship_tiles = []
        for x in range(0, len(self.ships_matrix)):
            for y in range(0, len(self.ships_matrix[x])):
                if self.ships_matrix[x][y] != 0:
                    self.ship_tiles.append(
                        Ship(
                            self.surface,
                            self.tile_width,
                            self.player_board[y + 1][x + 1].ypos,
                            self.player_board[y + 1][x + 1].xpos,
                        )
                    )



    # rysowanie statków wszystkich, oprócz aktualnie przesuwanego
    def draw_draggable_ships(self):
        for ship in self.draggable_ships:
            if not self.dragged_ship or ship.id != self.dragged_ship.id:
                ship.draw()

    # rysowanie planszy gracza
    def draw_playerboard(self):
        for row in self.player_board:
            for tile in row:
                tile.draw()

    # rysowanie planszy przeciwnika
    def draw_enemyboard(self):
        for row in self.enemy_board:
            for tile in row:
                tile.draw()

    # znajduje kliknięty statek i przypisuje do self.dragged_ship
    def find_dragged(self, pos):
        self.dragged_ship = None
        for ship in self.draggable_ships:
            if ship.is_dragged(pos):
                self.dragged_ship = ship
                break

    # zwraca kafelek, na który odłożyliśmy statek, jeśli miejsce jest walidacyjne
    def match_validate_tile_to_ship(self, pos):
        for row_idx, row in enumerate(self.player_board):
            for cell_idx, cell in enumerate(row):
                if row_idx == 0 or cell_idx == 0:
                    continue
                elif cell.clicked(pos):
                    if (
                        self.dragged_ship.draw_rotated
                        and self.board_size - cell_idx - self.dragged_ship.length >= 0
                        or not self.dragged_ship.draw_rotated
                        and self.board_size - row_idx - self.dragged_ship.length >= 0
                    ):
                        if self.validate_add_to_matrix(
                            cell_idx - 1,
                            row_idx - 1,
                            self.dragged_ship.length,
                            self.dragged_ship.id,
                            self.dragged_ship.draw_rotated,
                        ):
                            return cell
        return None

    # sprawdza czy miejsce nie jest zajęte i czy w otoczeniu statku w nowym ułożeniu nie ma innych statków
    def validate_add_to_matrix(self, x, y, length, ship_id, rotated):
        is_valid = True

        def check_surrounding(rowcheck, cellcheck):
            surrounding_valid = True
            if (
                rowcheck - 1 > 0
                and self.ships_matrix[rowcheck - 1][cellcheck] != 0
                and self.ships_matrix[rowcheck - 1][cellcheck] != ship_id
            ):
                surrounding_valid = False
            if (
                rowcheck + 1 < self.board_size - 1
                and self.ships_matrix[rowcheck + 1][cellcheck] != 0
                and self.ships_matrix[rowcheck + 1][cellcheck] != ship_id
            ):
                surrounding_valid = False
            if (
                cellcheck - 1 > 0
                and self.ships_matrix[rowcheck][cellcheck - 1] != 0
                and self.ships_matrix[rowcheck][cellcheck - 1] != ship_id
            ):
                surrounding_valid = False
            if (
                cellcheck + 1 < self.board_size - 1
                and self.ships_matrix[rowcheck][cellcheck + 1] != 0
                and self.ships_matrix[rowcheck][cellcheck + 1] != ship_id
            ):
                surrounding_valid = False
            return surrounding_valid

        # sprawdza czy miejsce nie jest zajęte przez inny statek
        for row_idx, row in enumerate(self.ships_matrix):
            for cell_idx, cell in enumerate(row):
                if (
                    rotated
                    and cell_idx == y
                    and row_idx >= x
                    and row_idx <= x + length - 1
                    and cell != 0
                    and cell != ship_id
                ):
                    is_valid = False
                if (
                    not rotated
                    and row_idx == x
                    and cell_idx >= y
                    and cell_idx <= y + length - 1
                    and cell != 0
                    and cell != ship_id
                ):
                    is_valid = False
        # jeśli ułożenie jest poprawne, aktualizuje macierz ships_matrix, przy okazji wykorzystując funkcję check_surrounding do dodatkowego sprawdzenia otoczenia
        # zwraca True (można ułożyć) albo False (nie można)
        if is_valid:
            temp_matrix = deepcopy(self.ships_matrix)
            for row_idx, row in enumerate(temp_matrix):
                for cell_idx, cell in enumerate(row):
                    if temp_matrix[row_idx][cell_idx] == ship_id:
                        temp_matrix[row_idx][cell_idx] = 0

                    if (
                        rotated
                        and cell_idx == y
                        and row_idx >= x
                        and row_idx <= x + length - 1
                    ):
                        if not check_surrounding(row_idx, cell_idx):
                            is_valid = False
                        else:
                            temp_matrix[row_idx][cell_idx] = ship_id

                    if (
                        not rotated
                        and row_idx == x
                        and cell_idx >= y
                        and cell_idx <= y + length - 1
                    ):
                        if not check_surrounding(row_idx, cell_idx):
                            is_valid = False
                        else:
                            temp_matrix[row_idx][cell_idx] = ship_id
        if is_valid:
            self.ships_matrix = deepcopy(temp_matrix)
        return is_valid