from enum import Enum
import pygame
import sys, os

# code to allow using python code from parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import button

pygame.init()

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS

GRAY = (189, 189, 189)
DARK_GRAY = (99, 99, 99)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
font = pygame.font.SysFont(None, 24)

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
        self.actual_board = self.create_board()

    # datastructure of each board coordinate
    # board[r][c] = {'mine': bool, 'neighbor_mines': int, 'revealed': bool, 'flagged': bool }
    # each board[r][c] contains if its a mine, how many neighboring mines, if its been flagged by a player
    # and if its been revealed on the board... lets use this as the data structure pls pls pls 

    def create_board(self):
        board = []
        for r in range(self.board_size):
            row = []
            for c in range(self.board_size):
                row.append({'mine': False, 'neighbor_mines': 0, 'revealed': False, 'flagged': False})
                #adds the data structure to each coord in the 10x10 grid 
            board.append(row)
        return board

    def PlaceMines(self):
        #place mines in board
        return
    
    def countNeighbors(self):
        #counts how many neightboring mines are around it
        return

    def draw_board(self):
        #mine_sprite = None
        #mine_explode_sprite = None

        for r in range(self.board_size):
            for c in range(self.board_size):
                cell = self.actual_board[r][c]
                rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)

                if cell['revealed']:
                    pygame.draw.rect(screen, GRAY, rect)
                    if cell['mine']:
                        pygame.draw.rect(screen, RED, rect)
                        #todo create stuff linking the mine sprite to mine cell
                        #screen.blit(mine_sprite, rect.center) along these lines? right now using draw
                        pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 4)
                    elif cell['neighbor_mines'] > 0:
                        text = font.render(str(cell['neighbor_mines']), True, BLACK)
                        text_rect = text.get_rect(center=rect.center)
                        screen.blit(text, text_rect)
                else: #if its an empty space
                    pygame.draw.rect(screen, DARK_GRAY, rect)

                if cell['flagged']:
                    #later update with the actual flag sprite, right now text will suffice
                    pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)

                pygame.draw.rect(screen, BLACK, rect, 1) #boarder

    def reveal_cell(self, r, c):
        cell = self.actual_board[r][c]
        if self.actual_board[r][c]['revealed'] or self.actual_board[r][c]['flagged']:
            return
        self.actual_board[r][c]['revealed'] = True
    
        if cell['mine']:
            # If a mine is clicked → set game to lose state
            self.state = GameState.LOSE_SCREEN

    def handle_click(self, x, y, button):
        # until theres actual functionaility in the event handler
        r = y // CELL_SIZE
        c = x // CELL_SIZE

        if button == 1:  #left click
            self.reveal_cell(r, c)
        elif button == 3:  #right click
            cell = self.actual_board[r][c]
            if not cell['revealed']:
                cell['flagged'] = not cell['flagged']
if __name__ == "__main__":
    board = Board()

    # main loop to run it rn
    running = True
    while running:
        screen.fill((255, 255, 255))
        board.draw_board()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.handle_click(*event.pos, event.button)

    pygame.quit()