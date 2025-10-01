"""
Minesweeper Game Board Module

Module Name: board.py
Description: Core game logic for Minesweeper including board generation, game state management,
            and player interactions. Handles mine placement, space revelation, flag placement,
            and win/lose conditions.

Inputs: 
    - Player coordinates for space revelation and flag placement
    - Mine count configuration
    - Board size parameters

Outputs:
    - Game board states (visible and actual)
    - Game state transitions (playing, win, lose)
    - Timer functionality for game duration

External Sources: 
    - implementation based on classic Minesweeper game rules
    - Pygame library used for timing functionality
    - Python enum module for type safety

Author: Benjamin Stonestreet
Creation Date: 9/10/2025
"""

from enum import Enum  # Python standard library for enumeration types
import random  # Python standard library for random number generation
from constants import MAX_MINES, MIN_MINES  # Local constants module for mine limits
from pygame import time  # Pygame library for game timing functionality
import pygame

# Initialize pygame sound effects 
pygame.mixer.init()
ding = pygame.mixer.Sound("./soundfiles/ding.mp3") 
swoosh = pygame.mixer.Sound("./soundfiles/swoosh.mp3")
swooshReverse = pygame.mixer.Sound("./soundfiles/swooshreverse.mp3")
explosion= pygame.mixer.Sound("./soundfiles/explosion.mp3")
winner=pygame.mixer.Sound("./soundfiles/winner.mp3")
welcome=pygame.mixer.Sound("./soundfiles/gamestart.mp3")
menuSound=pygame.mixer.Sound("./soundfiles/menuselect.mp3")

class BoardPiece(Enum):
    """Enumeration class to represent different types of board spaces
    
    Used to maintain type safety and clear representation of board states.
    Includes both display states (MINE, FLAG, UNKNOWN) and numerical mine counts (0-8).
    """
    MINE = 'M' # Mine indicator for dangerous spaces
    FLAG = 'F' # Flag marker placed by player to indicate suspected mine
    UNKNOWN = 'U' # Unknown/unrevealed space that player hasn't clicked yet

    # Numerical values representing count of adjacent mines
    ZERO = 0      # No adjacent mines - safe space
    ONE = 1       # One adjacent mine
    TWO = 2       # Two adjacent mines
    THREE = 3     # Three adjacent mines
    FOUR = 4      # Four adjacent mines
    FIVE = 5      # Five adjacent mines
    SIX = 6       # Six adjacent mines
    SEVEN = 7     # Seven adjacent mines
    EIGHT = 8     # Eight adjacent mines (maximum possible)

    def __sub__(self, other):
        if isinstance(other, (BoardPiece, int)):
            return self.value - (other.value if isinstance(other, BoardPiece) else other)
        return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, BoardPiece):
            return self.value == other.value
        elif isinstance(other, (int, str)):
            return self.value == other
        return NotImplemented
    
    def increment(self):
        """Increments the numerical value of non-mine spaces
        
        Used during board generation to count adjacent mines for each space.
        Only increments integer values up to maximum of 8.
        
        Returns:
            BoardPiece: Incremented value or self if at maximum or is a mine
        """
        if isinstance(self.value, int) and self.value < 8:
            next_value = self.value + 1
            return BoardPiece(next_value)
        return self


class GameState(Enum):
    """Enumeration class to represent different game states"""
    START_SCREEN = 1
    PLAYING = 2
    WIN_SCREEN = 3
    LOSE_SCREEN = 4


class Board:
    board_size: int = 10

    def __init__(self):
        self.ResetBoard()
        self.prev_click = [0, 0]

    def ResetBoard(self):
        self.mines: int = 10
        self.flags: int = 10
        self.state: GameState = GameState.START_SCREEN
        self.StartTime = 0
        self.board_generated: bool = False
        self.visible_board: list = [[BoardPiece.UNKNOWN for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.actual_board: list = [[BoardPiece.ZERO for _ in range(self.board_size)] for _ in range(self.board_size)]

    def CalculateDuration(self):
        if not self.board_generated:
            return 0
        elif self.state == GameState.PLAYING:
            return (time.get_ticks() - self.StartTime) // 1000
        else:
            return self.StartTime // 1000
            

    def GenerateBoard(self, startIdx: tuple):
        self.state = GameState.PLAYING
        self.board_generated = True
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
        return self.actual_board[spaceIdx[0]][spaceIdx[1]]

    def PrintActualBoard(self):
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
                    if hasattr(self.visible_board[x][y], 'value'):
                        print(self.visible_board[x][y].value, end = ' ')
                    else:
                        print(self.visible_board[x][y], end = ' ')
            print()

    def PlaceFlag(self, spaceIdx: tuple):
        r, c = spaceIdx
        if self.visible_board[r][c] == BoardPiece.FLAG:
            self.visible_board[r][c] = BoardPiece.UNKNOWN
            self.flags += 1
            swooshReverse.play()
        elif self.visible_board[r][c] == BoardPiece.UNKNOWN:
            self.visible_board[r][c] = BoardPiece.FLAG
            self.flags -= 1
            swoosh.play()

    def RevealSpace(self, spaceIdx: tuple):
        r, c = spaceIdx
        if not (0 <= r < self.board_size and 0 <= c < self.board_size):
            return False
        revealedSpace = self.actual_board[r][c]
        if(not self.board_generated):
            self.GenerateBoard(spaceIdx)
            self.StartTime = time.get_ticks()
        revealedSpace = self.actual_board[spaceIdx[0]][spaceIdx[1]]
        if(self.visible_board[spaceIdx[0]][spaceIdx[1]] != BoardPiece.UNKNOWN):
            return False

        match revealedSpace:
            case BoardPiece.MINE:
                self.visible_board[spaceIdx[0]][spaceIdx[1]] = BoardPiece.MINE
                self.StartTime = time.get_ticks() - self.StartTime
                self.state = GameState.LOSE_SCREEN
                explosion.play()
                return self.visible_board
                
            case BoardPiece.ZERO:
                self.visible_board[spaceIdx[0]][spaceIdx[1]] = 0
                ding.play()
                for x in range(max(0, spaceIdx[0] - 1), min(spaceIdx[0] + 2, self.board_size)):
                    for y in range(max(0, spaceIdx[1] - 1), min(spaceIdx[1] + 2, self.board_size)):
                        self.RevealSpace((x, y))
                if(self.CheckWin()):
                    self.state = GameState.WIN_SCREEN
                    self.StartTime = time.get_ticks() - self.StartTime
                    winner.play()
                    return self.visible_board
                return self.visible_board

            case _:
                self.visible_board[spaceIdx[0]][spaceIdx[1]] = revealedSpace
                if(self.CheckWin()):
                    self.state = GameState.WIN_SCREEN
                    self.StartTime = time.get_ticks() - self.StartTime
                    winner.play()
                    return self.visible_board
                ding.play()
                return self.visible_board

    def ReturnVisableBoard(self):
        return self.visible_board

    def SetMines(self, mines: int):
        self.mines = mines
        self.flags = mines

    def IncrementMines(self):
        self.mines += 1
        self.flags += 1

    def DecrementMines(self):
        self.mines -= 1
        self.flags -= 1

    def CheckWin(self):
        for x in range(0, self.board_size):
            for y in range(0, self.board_size):
                if(self.actual_board[x][y] != BoardPiece.MINE and 
                   (self.visible_board[x][y] == BoardPiece.UNKNOWN or 
                    self.visible_board[x][y] == BoardPiece.FLAG)):
                    return False
        return True
    
    def move_agent(self, rc):
        r, c = rc
        self.prev_click = [r, c]