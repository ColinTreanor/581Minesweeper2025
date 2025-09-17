from enum import Enum
import random
from constants import MAX_MINES, MIN_MINES
from pygame import time

class BoardPiece(Enum):
    #enum class to represent spaces
    MINE = 'M'
    FLAG = 'F'
    UNKNOWN = 'U'
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8

    def increment(self):
        if isinstance(self.value, int) and self.value < 8:
            next_value = self.value + 1
            return BoardPiece(next_value)
        
        return self


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
        self.mines: int = 10
        self.state: GameState = GameState.START_SCREEN
        self.StartTime = 0
        self.board_generated: bool = False
        self.visible_board: list = [[BoardPiece.UNKNOWN for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.actual_board: list = [[BoardPiece.ZERO for _ in range(self.board_size)] for _ in range(self.board_size)]

    def CalculateDuration(self):
        if not self.board_generated:
            return 0
        return (time.get_ticks() - self.StartTime) // 1000

    def GenerateBoard(self, startIdx: tuple):
        self.state = GameState.PLAYING
        self.board_generated = True
        
        # generate board based on players first click
        mines_placed: int = 0
        while(mines_placed < self.mines):
            rand_x = random.randint(0, self.board_size - 1)
            rand_y = random.randint(0, self.board_size - 1)
            if (startIdx != (rand_x, rand_y) and self.actual_board[rand_x][rand_y] != BoardPiece.MINE):
                self.actual_board[rand_x][rand_y] = BoardPiece.MINE
                mines_placed += 1 
            

                for x in range(max(0, rand_x - 1), min(rand_x + 2, self.board_size)):
                    for y in range(max(0, rand_y - 1), min(rand_y + 2, self.board_size)):

                        if(self.actual_board[x][y] != BoardPiece.MINE):
                            self.actual_board[x][y] = self.actual_board[x][y].increment()
                        

    def GetValue(self, spaceIdx: tuple):
        #return if it is mine, flag, or value
        return self.actual_board[spaceIdx[0]][spaceIdx[1]]

    def PrintActualBoard(self):
        # print board for debug
        for x in range(self.board_size):
            for y in range(self.board_size):
                if(self.actual_board[x][y] == BoardPiece.MINE):
                    print('M', end =' ')
                    continue
                print(self.actual_board[x][y].value, end=' ')
            print()

    def PrintVisibleBoard(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                if(self.visible_board[x][y] == BoardPiece.UNKNOWN):
                    print('U', end = ' ')
                    continue
                if(self.visible_board[x][y] == BoardPiece.FLAG):
                    print('F', end = ' ')
                    continue
                else: 
                    print(self.visible_board[x][y].value, end = ' ')

            print()

    def PlaceFlag(self, spaceIdx: tuple):
        r, c = spaceIdx
        if self.visible_board[r][c] == BoardPiece.FLAG:
            self.visible_board[r][c] = BoardPiece.UNKNOWN
        elif self.visible_board[r][c] == BoardPiece.UNKNOWN:
            self.visible_board[r][c] = BoardPiece.FLAG

    def RevealSpace(self, spaceIdx: tuple):
        r, c = spaceIdx
        print(f"RevealSpace called with indices: row={r}, col={c}")
        print(f"Board size: {self.board_size}, actual_board dimensions: {len(self.actual_board)} x {len(self.actual_board[0])}")

        if not (0 <= r < self.board_size and 0 <= c < self.board_size):
            print(f"Invalid indices: ({r}, {c}) - skipping")
            return

        revealedSpace = self.actual_board[r][c]
        if(not self.board_generated): #Generate underlying board on first move to ensure bomb isnt on selected tile. 
            self.GenerateBoard(spaceIdx)
            self.StartTime = time.get_ticks()

        revealedSpace = self.actual_board[spaceIdx[0]][spaceIdx[1]] # underlying space that the user picked. ie mine empty or how many surrounding mines

        if(self.visible_board[spaceIdx[0]][spaceIdx[1]] != BoardPiece.UNKNOWN):
            return

        match revealedSpace:
            
            case BoardPiece.MINE:
                self.visible_board[spaceIdx[0]][spaceIdx[1]] == BoardPiece.MINE
                self.state = GameState.LOSE_SCREEN
                return self.visible_board
            case BoardPiece.ZERO:
                self.visible_board[spaceIdx[0]][spaceIdx[1]] = 0

                for x in range(max(0, spaceIdx[0] - 1), min(spaceIdx[0] + 2, self.board_size)):
                    for y in range(max(0, spaceIdx[1] - 1), min(spaceIdx[1] + 2, self.board_size)):
                        self.RevealSpace((x, y))

                if(self.CheckWin()):
                    self.state = GameState.WIN_SCREEN
                    return self.visible_board

                return self.visible_board

            case _: # defualt case
                self.visible_board[spaceIdx[0]][spaceIdx[1]] = revealedSpace

                if(self.CheckWin()):
                    self.state = GameState.WIN_SCREEN
                    return self.visible_board

                return self.visible_board


    def ReturnVisableBoard(self):
        return self.visible_board

    def SetMines(self, mines: int):
        self.mines = mines

    def IncrimentMines(self):
        self.mines += 1

    def DecramentMines(self):    
        self.mines -= 1

    def CheckWin(self):
        for x in range(0, self.board_size):
            for y in range(0, self.board_size):
                if(self.actual_board[x][y] != BoardPiece.MINE and self.visible_board[x][y] == BoardPiece.UNKNOWN):
                    return False
                
        return True