import numpy as np
from set_ships import set_ship,set_ships
import time
from random import randint

board_size = 9
player_ships = set_ships(board_size)
ai_ships = set_ships(board_size)
#################################################################################
def draw_player_board(ships: list, board_size: int):
    matrix = np.zeros((board_size,board_size))
    for j in ships:
        for i in j:
            matrix[i[0]-1,i[1]-1] = 1
    return matrix

def draw_ai_board(board_size):
    matrix = np.zeros((board_size,board_size))
    return matrix
##################################################################################

player_board = draw_player_board(player_ships,board_size)
ai_board = draw_ai_board(board_size)

def draw_shoot(x,y, board, x_ships, shooted):
    for ship in x_ships:
        if (x,y) in ship:
            board[x-1,y-1] = 2 
            break
        else :
            board[x-1,y-1] = 3

    for ship in x_ships:
        if all(x in shooted for x in ship):
            for j in ship:
                x,y = j
                board[x-1,y-1] = 9
            x_ships.remove(ship)

    return board

def play(x,y,player_board,ai_board):
    player_shooted = []
    ai_shooted = []
    end_game = False
    while end_game == False:
        print(player_board)
        print('\n')
        print(ai_board)
        validate = False
        while validate == False:
            x = int(input('Which row to shoot: '))
            y = int(input('Which column to shoot: '))
            if ai_board[x-1,y-1] == 3 or ai_board[x-1,y-1] == 2:
                print("You've already shot at this spot!")
            else:
                validate = True
        player_shooted.append((x,y))    
        ai_board = draw_shoot(x,y,ai_board, ai_ships, player_shooted)
        validate = False
        while validate == False:
            x = randint(1,9)
            y = randint(1,9)
            if player_board[x-1,y-1] == 3 or player_board[x-1,y-1] == 2:
               continue
            else:
                validate = True
        ai_shooted.append((x,y))
        player_board = draw_shoot(x,y,player_board, player_ships, ai_shooted)
        print(ai_ships)
        if len(player_ships) == 0:
            print('You LOSE!')
            end_game =  True
        elif len(ai_ships) == 0:
            print('Congrats! You win!')
            end_game = True

play(player_board,ai_board)