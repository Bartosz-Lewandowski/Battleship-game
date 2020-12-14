import os
import pygame
import pygame_menu
import constants
from Tile import Tile
from set_ships import draw_matrix
from Ship import Ship
from DraggableShip import DraggableShip

ships_laoyout_stage=pygame.event.Event(pygame.USEREVENT, attr1='layout_stage')
start_game_stage=pygame.event.Event(pygame.USEREVENT, attr1='start_game_stage')

class Game(): 
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self.ships_layout_type = 0
        self.main_loop()

    def draw_menu(self):
        def start_the_game(size):
            self.board_size=size
            if(self.board_size == 10):
                self.avalaible_ships = constants.SHIPS_9
            if(self.board_size == 13):
                self.avalaible_ships = constants.SHIPS_12
            if(self.board_size == 16):
                self.avalaible_ships = constants.SHIPS_15
            pygame.event.post(ships_laoyout_stage)

        def set_ships_layout(selected, value):
            self.ships_layout_type = selected[1]

        self.menu = pygame_menu.Menu(height=constants.HEIGHT,
                        width=constants.WIDTH,
                        theme=pygame_menu.themes.THEME_BLUE,
                        title='Board size')
        self.menu.add_selector('Ships layout: ', [('Random', 0), ('Pick', 1)], onchange=set_ships_layout)
        self.menu.add_button('9 x 9', lambda: start_the_game(10))
        self.menu.add_button('12 x 12', lambda: start_the_game(13))
        self.menu.add_button('15 x 15', lambda: start_the_game(16))
        self.menu.add_button('Exit', pygame_menu.events.EXIT)

    def main_loop(self):
        self.draw_menu()
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

                if event == ships_laoyout_stage:
                    self.surface.fill((0,0,0))
                    self.menu.disable()
                    if self.ships_layout_type == 0:
                        self.ships_matrix = draw_matrix(self.board_size-1)
                        pygame.event.post(start_game_stage)
                    else:
                        self.ships_matrix=[[]]
                        self.draw_board(chosing_stage=True)

                if event == start_game_stage:
                    self.surface.fill((0,0,0))
                    self.draw_board()
                    self.draw_ships()


            if self.menu.is_enabled():
                self.menu.update(events)
                self.menu.draw(self.surface)

            pygame.display.update()
            

    def draw_grid(self, offsetX, offsetY):
        tiles = [[] for i in range(0, self.board_size)]
        for x in range (0, self.board_size):
            for y in range(0, self.board_size):
                if(x == 0 and y == 0):
                    continue
                if(x==0):
                    header = constants.LETTERS[y-1]
                elif(y == 0):
                    header = str(x)
                else:
                    header = None
                tiles[x].append(Tile(self.surface, self.tile_width, x*self.tile_width+offsetX, y*self.tile_width+offsetY, header=header))
        return tiles

    def draw_board(self, chosing_stage=False):
        self.tile_width = ((constants.WIDTH - 100)/ self.board_size) / 2  
        self.offset_enemy_grid = self.tile_width * self.board_size + 50
        offsetX = 20
        offsetY = 20
        self.player_board = self.draw_grid(offsetX, offsetY)
        if chosing_stage:
            self.draw_draggable_ships()
        else:
            self.enemy_board = self.draw_grid(self.offset_enemy_grid, offsetY)

    def draw_ships(self):
        self.ship_tiles = []
        for x in range(0, len(self.ships_matrix)):
            for y in range(0, len(self.ships_matrix[x])):
                if(self.ships_matrix[x][y] == 1):
                    self.ship_tiles.append(Ship(self.surface, self.tile_width, self.player_board[x+1][y+1].ypos, self.player_board[x+1][y+1].xpos))
        
    def draw_draggable_ships(self):
        line_number = 1
        for ship in self.avalaible_ships:
            DraggableShip(self.surface, self.tile_width, self.offset_enemy_grid+50, line_number*1.5*self.tile_width, ship)
            line_number += 1