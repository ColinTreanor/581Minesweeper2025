# Authored by: Benjamin Stonestreet
import random

ROWS = 10
COLUMNS = 10

class minesweeper:
    def __init__(self, mines=10):

        self.gameBoard = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.flagBoard = [[False for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.revealedBoard = [[False for _ in range(COLUMNS)] for _ in range(ROWS)]

        self.gameOver = False
        self.mines = mines

    def PlaceMines(self):
        placed_mines = 0
        while placed_mines < self.mines:
            row = random.randint(0, ROWS - 1)
            col = random.randint(0, COLUMNS - 1)
            if self.gameBoard[row][col] != 'M':
                self.gameBoard[row][col] = 'M'
                placed_mines += 1
                self.UpdateAdjacentCounts(row, col)

    def UpdateAdjacentCounts(self, row, col):
        for r in range(max(0, row - 1), min(ROWS, row + 2)):
            for c in range(max(0, col - 1), min(COLUMNS, col + 2)):
                if r == row and c == col:
                    continue
                if self.gameBoard[r][c] != 'M':
                    self.gameBoard[r][c] += 1

    def __str__(self):
        lines = []
        for r in range(ROWS):
            row_cells = []
            for c in range(COLUMNS):
                if self.revealedBoard[r][c]:
                    val = self.gameBoard[r][c]
                    if val == 'M':
                        ch = 'M'
                    elif val == 0:
                        ch = '.'
                    else:
                        ch = str(val)
                else:
                    ch = 'F' if self.flagBoard[r][c] else '#'
                row_cells.append(ch)
            lines.append(" ".join(row_cells))
        return "\n".join(lines)


    def DebugBoard(self):
        lines = []
        for r in range(ROWS):
            row_cells = []
            for c in range(COLUMNS):
                val = self.gameBoard[r][c]
                if val == 'M':
                    ch = 'M'
                elif val == 0:
                    ch = '.'
                else:
                    ch = str(val)
                row_cells.append(ch)
            lines.append(" ".join(row_cells))
        return "\n".join(lines)

    
