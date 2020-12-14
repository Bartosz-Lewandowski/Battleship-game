import random 
import numpy as np 
import pygame
from pygame.locals import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((240,180))
    running = True

    while running:
        for event in pygame.event.get():
            def set_ship(taken_spots, board_size, ship_size):
                new_taken_spots = []
                condition = True 
                while condition:
                    ship = []
                    axis = random.randint(0,1)
                    if axis == 0:
                        x = random.randint(1,board_size)
                        y = random.randint(1,board_size - ship_size)
                        ship.append((x,y))
                        for mast in range(1,ship_size):
                            ship.append((x,y+mast))
                    else :
                        x = random.randint(1,board_size - ship_size)
                        y = random.randint(1,board_size)
                        ship.append((x,y))
                        for mast in range(1,ship_size):
                            ship.append((x + mast,y))
                    condition = any(elem in ship for elem in taken_spots)
                for spot in ship:
                    if spot[0] == 1:
                        if spot[1] == board_size:
                            new_taken_spots.append((spot[0]+1,spot[1]))
                            new_taken_spots.append((spot[0],spot[1]-1))
                        elif spot[1] == 1:
                            new_taken_spots.append((spot[0]+1,spot[1]))
                            new_taken_spots.append((spot[0],spot[1]+1))
                        else:
                            new_taken_spots.append((spot[0]+1,spot[1]))
                            new_taken_spots.append((spot[0],spot[1]+1))
                            new_taken_spots.append((spot[0],spot[1]-1))

                    elif spot[0] == board_size:
                        if spot[1] == 1:
                            new_taken_spots.append((spot[0]-1,spot[1]))
                            new_taken_spots.append((spot[0],spot[1]+1))

                        elif spot[1] == board_size:
                            new_taken_spots.append((spot[0]-1,spot[1]))
                            new_taken_spots.append((spot[0],spot[1]-1))
                        else: 
                            new_taken_spots.append((spot[0]-1,spot[1]))
                            new_taken_spots.append((spot[0],spot[1]+1))
                            new_taken_spots.append((spot[0],spot[1]-1))

                    elif spot[1] == 1:
                        new_taken_spots.append((spot[0]+1,spot[1]))
                        new_taken_spots.append((spot[0]-1,spot[1]))
                        new_taken_spots.append((spot[0],spot[1]+1))
                    elif spot[1] == board_size:
                        new_taken_spots.append((spot[0],spot[1]-1))
                        new_taken_spots.append((spot[0]+1,spot[1]))
                        new_taken_spots.append((spot[0]-1,spot[1]))
                    else:
                        new_taken_spots.append((spot[0],spot[1]+1))
                        new_taken_spots.append((spot[0],spot[1]-1))
                        new_taken_spots.append((spot[0]+1,spot[1]))
                        new_taken_spots.append((spot[0]-1,spot[1]))
                new_taken_spots.extend(ship)
                new_taken_spots = list(dict.fromkeys(new_taken_spots))
                return(ship, new_taken_spots)

            def set_ships(board_size):
                ships = []
                taken_spots = []
                if board_size == 9:
                    ships_sizes = [3,3,3,2,2,1,1,1]
                    for i in ships_sizes:
                        tmp_ship = set_ship(taken_spots, board_size, i)
                        ships.extend(tmp_ship[0])
                        taken_spots.extend(tmp_ship[1])
                elif board_size == 12:
                    ships_sizes = [4,3,3,2,2,2,1,1,1,1]
                    for i in ships_sizes:
                        axis = random.randint(0,1)
                        tmp_ship = set_ship(taken_spots, board_size, i)
                        ships.extend(tmp_ship[0])
                        taken_spots.extend(tmp_ship[1])
                elif board_size == 15:
                    ships_sizes = [4,3,3,3,2,2,2,1,1,1,1,1]
                    for i in ships_sizes:
                        axis = random.randint(0,1)
                        tmp_ship = set_ship(taken_spots, board_size, i)
                        ships.extend(tmp_ship[0])
                        taken_spots.extend(tmp_ship[1])
                return(ships)


            def draw_matrix(board_size):
                ships = set_ships(board_size)
                matrix = np.zeros((board_size,board_size))
                for i in ships:
                    matrix[i[0]-1,i[1]-1] = 1
                return matrix


            test_ship = [(1, 1), (1, 2), (1, 3)] 
            test_taken = [(3, 7), (3, 5), (4, 6), (2, 6), (3, 8), (3, 6), (4, 7), (2, 7), (3, 9), (4, 8), (2, 8), (6, 8), (7, 9), (5, 9), (7, 8), (8, 9), (6, 9), (8, 8), (9, 9)]
            def check_validate(taken_spots, ship):
                if any(elem in ship for elem in taken_spots):
                    print('Ship is not validate')
                else:
                    print('Ship is validate')

            check_validate(test_taken,test_ship)

            if event.type == pygame.QUIT:
                running = False

if __name__=="__main__":
    main()


    image = pygame.image.load("01_image.png")