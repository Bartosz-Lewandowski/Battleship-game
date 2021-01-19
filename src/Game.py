import os
import pygame
import pygame_menu
from copy import deepcopy
import constants
from Tile import Tile
from set_ships import draw_matrix
from Ship import Ship
from DraggableShip import DraggableShip

ships_laoyout_stage = pygame.event.Event(pygame.USEREVENT, attr1="layout_stage")
start_game_stage = pygame.event.Event(pygame.USEREVENT, attr1="start_game_stage")


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self.ships_layout_type = 0
        self.main_loop()

    def draw_menu(self):
        def start_the_game(size):
            self.board_size = size
            if self.board_size == 10:
                self.avalaible_ships = constants.SHIPS_9
            if self.board_size == 13:
                self.avalaible_ships = constants.SHIPS_12
            if self.board_size == 16:
                self.avalaible_ships = constants.SHIPS_15
            pygame.event.post(ships_laoyout_stage)

        def set_ships_layout(selected, value):
            self.ships_layout_type = selected[1]

        self.menu = pygame_menu.Menu(
            height=constants.HEIGHT,
            width=constants.WIDTH,
            theme=pygame_menu.themes.THEME_BLUE,
            title="Board size",
        )
        self.menu.add_selector(
            "Ships layout: ", [("Random", 0), ("Pick", 1)], onchange=set_ships_layout
        )
        self.menu.add_button("9 x 9", lambda: start_the_game(10))
        self.menu.add_button("12 x 12", lambda: start_the_game(13))
        self.menu.add_button("15 x 15", lambda: start_the_game(16))
        self.menu.add_button("Exit", pygame_menu.events.EXIT)

    def main_loop(self):
        self.stage = "MENU"
        self.dragged_ship = None
        self.draw_menu()
        drag = False
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                if event == ships_laoyout_stage:
                    self.surface.fill((0, 0, 0))
                    self.menu.disable()
                    if self.ships_layout_type == 0:
                        self.ships_matrix = draw_matrix(self.board_size - 1)
                        pygame.event.post(start_game_stage)
                    else:
                        self.stage = "SET_SHIPS"
                        self.ships_matrix = [
                            [0 for i in range(0, self.board_size - 1)]
                            for i in range(0, self.board_size - 1)
                        ]
                        self.draw_board(chosing_stage=True)
                if event == start_game_stage:
                    self.surface.fill((0, 0, 0))
                    self.draw_board()
                    self.draw_ships()
               
               # powstały 3 nowe eventy
               # mousebuttondown - naciśnięcie przycisku myszy
               # pos to współrzędne myszy
               # jesteśmy na etapie ustawiania statków
               # find_dragged znajduje kliknięty statek dla współrzędnych myszki i zapisuje go do self.dragged_ship
               # drag jest True bo jeszcze nie puściliśmy przycisku myszy 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.stage == "SET_SHIPS":
                        self.find_dragged(pos)
                        drag = True
                # mousemotion - ruch muszy po planszy
                # etap przesuwania statku
                # bierzemy pozycję myszki i rysujemy od nowa planszę, statki i przesuwany statek
                if event.type == pygame.MOUSEMOTION:
                    if drag and self.dragged_ship is not None:
                        pos = pygame.mouse.get_pos()
                        self.surface.fill((0, 0, 0))
                        self.draw_playerboard()
                        self.draw_draggable_ships()
                        self.dragged_ship.move(pos)
                # mousebuttonup - zwolnienie przycisku myszy
                # pobieramy współrzędne myszki 
                # do zmiennej tile zapisujemy kafelek na planszy, na który przesunęliśmy statek (jeśli to miejsce jest walidacyjne)
                # w if ustawiamy nową pozycję statku, jeśli miejsce jest poprawne
                # wszystko rysujemy ponownie
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.stage == "SET_SHIPS" and self.dragged_ship is not None:
                        pos = pygame.mouse.get_pos()
                        tile = self.match_validate_tile_to_ship(pos)
                        if tile:
                            self.dragged_ship.set_new_pos(tile.xpos, tile.ypos)
                        self.dragged_ship = None
                        drag = False
                        self.surface.fill((0, 0, 0))
                        self.draw_playerboard()
                        self.draw_draggable_ships()
            # main_loop end

            if self.menu.is_enabled():
                self.menu.update(events)
                self.menu.draw(self.surface)

            pygame.display.update()
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
        self.tile_width = ((constants.WIDTH - 100) / self.board_size) / 2
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
                if self.ships_matrix[x][y] == 1:
                    self.ship_tiles.append(
                        Ship(
                            self.surface,
                            self.tile_width,
                            self.player_board[x + 1][y + 1].ypos,
                            self.player_board[x + 1][y + 1].xpos,
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