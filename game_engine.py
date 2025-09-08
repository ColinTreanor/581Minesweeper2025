from board import *

class BoardEngine:
    #will store board, update it accordingly, and expose it for UIEngine to use
    board: Board = Board()

    def __init__(self):
        return
    
    def CreateBoard(self, mines: int):
        self.board.CreateBoard(mines)
        return
    
    def GetBoardState(self):
        return self.board