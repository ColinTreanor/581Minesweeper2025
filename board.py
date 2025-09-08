from enum import Enum

class BoardPiece(Enum):
    #just enum class to represent pieces
    NO_MINE = 1
    MINE = 2
    FLAG = 3
    UNKNOWN = 4

class GameState(Enum):
    #just enum class to represent states
    START_SCREEN = 1
    PLAYING = 2
    WIN_SCREEN = 3
    LOSE_SCREEN = 4

class Board:
    #will store mines, state, board list(s) and size
    board_size: int = 10

    def __init__(self):
        self.ResetBoard()

    def ResetBoard(self):
        self.mines: int = 0
        self.state: GameState = GameState.START_SCREEN
        self.visible_board: list = [[BoardPiece.UNKNOWN for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.actual_board: list = [[BoardPiece.NO_MINE for _ in range(self.board_size)] for _ in range(self.board_size)]

    def CreateBoard(self, mines: int):
        self.mines = mines
        self.state = GameState.PLAYING
        GenerateBoard()

    def GenerateBoard(self):
        #place mines in board
        return
    
    def GetValue(self, pieceIdx: tuple):
        #return if it is mine, flag, or value
        return