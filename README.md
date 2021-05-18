# Battleship game

## Table of contents:
* [General info](#general_info)
* [Detailed description](#detalied_desc)
* [How to run the game](#how_to_run_script)
* [Technologies](#technologies)
* [Sources](#sources)

## General info
A Battleship game written in python using the pygame library. Can be played only with AI. Added options to choose board size, difficulty level, or user can arrange ships on the board by himself. 
## Detailed description
The game was created for a college course. We wrote a battleship game with AI that has three levels of difficulty. We wanted to implement more advanced AI, but unfortunately the idea was in the end deemed not worth implementing.  The AI on the easy level shoots randomly every time. On medium level it shoots randomly, but after hitting a ship it knows its next squares on the board. At hard level the AI is the same as at medium level, but in addition it knows not to shoot around a drowned ship. The gameplay is alternate (once the user shoots, once the AI shoots) and there are some rules in the game. 

* Ships cannot be stacked directly next to each other (only the corners of the ship can be in contact)
* Ships can be placed both vertically and horizontally, but they cannot go outside of the board area. 

The interface is designed to be user-friendly.
For the gameplay we used the algorithms invented and implemented by us thanks to which the game works correctly.  

Some of these algorithms are:
* Algorithm to automatically position the ships in such a way that it meets the conditions we set.
* Algorithm for correct running of the game (e.g. so the computer doesn't shoot again in the same field).

## How to run the game
First step is to install the necessary packages listed in the __requirements.txt__ file. It can be done using the virtual environment, or on your machine using the command

```
pip install -r requirements.txt
```

Then go to the __src__ folder and type the command:

```
python3 main.py
```

The game should launch and run properly. 

We have also added the ability to create a Linux application. This can be done inside __src__ folder using the command:
```
pyinstaller main.spec
```
It should create an application file that you can launch via the command line and play.


## Technologies:
* Python 3.8
* Interface - Pygame, Pygame-menu

## Sources:
* Pygame docs: [click](https://www.pygame.org/docs/)
