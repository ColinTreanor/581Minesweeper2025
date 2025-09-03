import pygame, sys
from enum import Enum
from pygame.locals import *

#includes scraps from https://coderslegacy.com/python/python-pygame-tutorial/

class BoardPiece(Enum):
    NO_MINE = 1
    MINE = 2
    FLAG = 3

class GameState(Enum):
    START_SCREEN = 1
    PLAYING = 2
    WIN_SCREEN = 3
    LOSE_SCREEN = 4

class Board:
    board_size: int = 10

    def __init__(self, mines : int):
        self.mines: int = mines
        self.state: GameState = GameState.START_SCREEN
        self.board: list = [[BoardPiece.NO_MINE for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.GenerateBoard()

    def GenerateBoard(self):
        #place mines in board
        return
    
    def GetValue(self, pieceIdx: tuple):
        #return if it is mine, flag, or value
        return

class BoardEngine:
    board: Board = None

    def __init__(self):
        return
    
    def CreateBoard(self, mines: int):
        self.board: Board = Board(mines)
        return
    
    def GetBoardState(self):
        return self.board

class UIEngine:
    def UpdateDisplay(self, surface, BoardState):
        '''
        will do one of the following:
            - display start screen
            - display win screen
            - display lose screen
            - display current board
        probably using switch statement to differentiate between
        '''
        return
 
class EventHandler:
    def HandleEvent(event: pygame.event, game : BoardEngine):
        '''
        will do one of the following:
            - close the game
            - tell BoardEngine to return to StartScreen
            - tell BoardEngine to make new game with certain mines
            - tell BoardEngine to register click if it is users turn (use bool to keep track of that)
        probably using a switch statement
        ''' 
        if event.type == QUIT:
            #end pygame
            pygame.quit()
            #end python script
            sys.exit()
        return

FPS = 60
FramePerSec = pygame.time.Clock()
 
# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

def main():
    #make pygame stuff
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption("Game")

    #make our classes
    Game = BoardEngine()
    UI = UIEngine()
    while True:     
        for event in pygame.event.get():              
            EventHandler.HandleEvent(event, Game)

        UI.UpdateDisplay(DISPLAYSURF, Game.GetBoardState())

        #upload window / surface changes
        pygame.display.update()
        #limit game speed to 60 FPS
        FramePerSec.tick(FPS)
    
if __name__ == "__main__":
    main()