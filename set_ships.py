#importujemy potrzebne biblioteki
import random 
import numpy as np 

# Pierwsza funkcja, która będzie wywoływana w funkcji kolejnej 
# Przyjmuje na wejściu: taken_spots - zajęte miejsca na planszy, czyli miejsca na których nie można postawić statku
#                       board_size - rozmiar planszy, możliwe 3 opcje w zależności którą planszę wybrał użytkownik
#                       ship_size - rozmair ustawianego statku. 
# Funkcja ta ustawia JEDEN statek na planszy w takim miejscu, żeby było ono walidacyjne, czyli nie wychodziło 
# poza ramki planszy, oraz nie zajmowało już miejsc zajętych 
def set_ship(taken_spots, board_size, ship_size):
    # tworzymy pustą listę do której będą dodawane miejsca zajęte
    new_taken_spots = []
    #Tworzymy pewien warunek, który jest TRUE, i zostanie zmieniony na FALSE, jak statek zostanie ustawiony poprawnie na planszy
    condition = True 
    #Tworzymy pętlę while, która zachodzi dopóki warunek jest True
    while condition == True:
        #Pusta lista do której będą dodawane miejsca ustawionego statku
        ship = []
        #losujemy, czy statek ma być ustawiony pionowo, czy poziomo 
        axis = random.randint(0,1)
        #Jeżeli axis = 0 wtedy ustawiamy statek poziomo
        if axis == 0:
            #losujemy wartość x, czyli pierwszy wiersz od którego będzie układany statek
            x = random.randint(1,board_size)
            #losuje wartość y, czyli pierwszą kolumnę od której będzie układany statek
            y = random.randint(1,board_size - ship_size)
            #dodajemy koordynaty pierwszego masztu do listy ship
            ship.append((x,y))
            # dodajemy koordynaty każdego masztu do lsity ship poprzez pętle która zachodzi od 1 do długości statku, czyli np. dla 4 masztowca pętla będzie zachodzić od 1 do 4
            for mast in range(1,ship_size):
                ship.append((x,y+mast))
        # Tutaj powtarzamy te czynności, tylko w przypadku kiedy ustawiamy statek pionowo, czyli axis = 1
        else :
            # Proszę zwrócić uwagę na to, że zmienia się zakres losowania zmiennej x i y, ponieważ tutaj zachodzi zasada, że statek nie może wyjść poza ramki planszy. 
            x = random.randint(1,board_size - ship_size)
            y = random.randint(1,board_size)
            ship.append((x,y))
            for mast in range(1,ship_size):
                ship.append((x + mast,y))
        # Sprawdzamy, czy dany statek znajduje się na miejscach już zajętych.
        # Czyli sprawdzamy czy jakikolwiek element z listy ship jest w liście taken_spots. Jeżeli tak to wykonuje się pętla ponownie
        # bo warunek jest dalej True, a jeżeli nie to warunek zmienia się na False i wiemy, że statek jest walidacyjny, więc pętla się kończy
        condition = any(elem in ship for elem in taken_spots)
    # dodajemy koordynaty nowych miejsc zajętych na planszy przy okazji zwracając uwagę na warunki brzegowe,
    # czyli np. kiedy statek będzie ułożony w rogu, żeby nie dodawać miejsc, które do tej planszy nie należą.
    # robimy to poprzez pętle, która przechodzi przez wszystkie elementy statku
    for spot in ship:
        if spot[0] == 1 and spot[1] == board_size:
            new_taken_spots.append((spot[0]+1,spot[1]))
            new_taken_spots.append((spot[0],spot[1]-1))
        elif spot[0] == 1 and spot[1] == 1:
            new_taken_spots.append((spot[0]+1,spot[1]))
            new_taken_spots.append((spot[0],spot[1]+1))
        elif spot[0] == board_size and spot[1] == 1:
            new_taken_spots.append((spot[0]-1,spot[1]))
            new_taken_spots.append((spot[0],spot[1]+1))
        elif spot[0] == board_size and spot[1] == board_size:
            new_taken_spots.append((spot[0]-1,spot[1]))
            new_taken_spots.append((spot[0],spot[1]-1))
        elif spot[0] == 1:
            new_taken_spots.append((spot[0]+1,spot[1]))
            new_taken_spots.append((spot[0],spot[1]+1))
            new_taken_spots.append((spot[0],spot[1]-1))
        elif spot[0] == board_size:
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
    new_taken_spots.append(ship)
    # Zwracamy koordynaty statku, oraz zajęte miejsca, na których statku już nie można postawić 
    return(ship, new_taken_spots)

#druga funckja, która przyjmuje tylko informacje o rozmiarze planszy 
def set_ships(board_size):
    # Tworzymy pustą listę ships, w której będą zapisywane kolejno statki
    ships = []
    # Tworzymy pustą listę taken_spots, w której będą zapisywane kolejno zajęte miejsca
    taken_spots = []
    #Jeżeli rozmiar planszy będzie 9 to tworzymy listę z rozmiarami statków, które maja się na tej liście znaleźć 
    if board_size == 9:
        # czyli tutaj mamy 3 trójmasztowce, 2 dwumasztowce i 3 jednomasztowce
        ships_sizes = [3,3,3,2,2,1,1,1]
        #Przechodzimy pętlą przez każdy rozmiar statku 
        for i in ships_sizes:
            #wywołujemy poprzednią funckję dając jej parametry widoczne poniżej, gdzie i to rozmiar i-tego statku.
            tmp_ship = set_ship(taken_spots, board_size, i)
            #dodajemy statek do listy statków
            ships.extend(tmp_ship[0])
            #dodajemy zajęte miejsca do listy z zajętymi miejscami
            taken_spots.extend(tmp_ship[1])
    #Te same czynności, tylko dla planszy o rozmiarze 12        
    elif board_size == 12:
        ships_sizes = [4,3,3,2,2,2,1,1,1,1]
        for i in ships_sizes:
            axis = random.randint(0,1)
            tmp_ship = set_ship(taken_spots, board_size, i)
            ships.extend(tmp_ship[0])
            taken_spots.extend(tmp_ship[1])
    #Te same czynności, tylko dla planszy o rozmiarze 15
    elif board_size == 15:
        ships_sizes = [4,3,3,3,2,2,2,1,1,1,1,1]
        for i in ships_sizes:
            axis = random.randint(0,1)
            tmp_ship = set_ship(taken_spots, board_size, i)
            ships.extend(tmp_ship[0])
            taken_spots.extend(tmp_ship[1])
    #Zwracamy listę ze statkami 
    return(ships)

#Funckja do stworzenia macierzy, żeby było widoczne, jak zostały rozmieszczone statki 
#Tutaj nad jej działaniem nie będziemy się rozpisywać. Zamienia 0 na 1, dla koordynat z listy ships.
def draw_matrix(board_size):
    ships = set_ships(board_size)
    matrix = np.zeros((board_size,board_size))
    for i in ships:
        matrix[i[0]-1,i[1]-1] = 1
    return matrix

print('Ułożenie statków dla planszy o rozmiarze 9:\n')
print(draw_matrix(9))
print('\n\n')
print('Ułożenie statków dla planszy o rozmiarze 12:\n')
print(draw_matrix(12))
print('\n\n')
print('Ułożenie statków dla planszy o rozmiarze 15:\n')
print(draw_matrix(15))
print('\n\n')
