import random 
import numpy as np 
import constants

def set_ship(taken_spots, board_size, ship_size):
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
    return(ship)

def add_new_taken_spots(ship, board_size):
    new_taken_spots = []
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

    return new_taken_spots


def set_ships(board_size):
    ships = []
    taken_spots = []
    if board_size == 9:
        ships_sizes = constants.SHIPS_9
        for i in ships_sizes:
            tmp_ship = set_ship(taken_spots, board_size, i)
            ships.append(tmp_ship)
            taken_spots.extend(add_new_taken_spots(tmp_ship, board_size))
    elif board_size == 12:
        ships_sizes = constants.SHIPS_12
        for i in ships_sizes:
            tmp_ship = set_ship(taken_spots, board_size, i)
            ships.append(tmp_ship)
            taken_spots.extend(add_new_taken_spots(tmp_ship, board_size))
    elif board_size == 15:
        ships_sizes = constants.SHIPS_15
        for i in ships_sizes:
            tmp_ship = set_ship(taken_spots, board_size, i)
            ships.append(tmp_ship)
            taken_spots.extend(add_new_taken_spots(tmp_ship, board_size))
    return(ships)



def draw_matrix(ships, board_size):
    matrix = np.zeros((board_size,board_size))
    for j in ships:
        for i in j:
            matrix[i[1]-1,i[0]-1] = 1
    return matrix


