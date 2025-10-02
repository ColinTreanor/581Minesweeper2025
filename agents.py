"""
Minesweeper Game Agents

Module Name: agents.py
    Description: Includes all logic for implementing 'AI' agents to play minesweeper against or autosolve.

Inputs: 
    - Visible / Actual board (depending on method)
    - Solve mode (VS, Multiplayer, Auto-Solve)

Outputs:
    - Returns (x, y) of desired coordinate

External Sources: 
    - None

Authors: Riley Anderson, Hannah Smith, Jacob Richards, Ryland Edwards
Creation Date: 9/23/2025
"""

#current purpose of this file is to create a skeleton for development. If your implementation requires changes, make them!
from board import BoardPiece, Board, GameState
import random
class Agent():
    #Agent class will be instantiated with a difficulty level, and will use that to determine which algorithm to run
    #run function will only need board state
    #this way, the agent class is agnostic to if it is running in VS or Auto-Solve mode
    def __init__(self, difficulty):
        self.difficulty = difficulty #0 = EASY, 1 = MEDIUM, 2 = HARD

        if difficulty == 1:
            self.medium_setup()

    def run_agent(self, board : Board):
        if self.difficulty == 0:
            click = self.easy_agent()
        elif self.difficulty == 1:
            click = self.medium_agent(board.visible_board)
        elif self.difficulty == 2:
            click = self.hard_agent(board.visible_board, board.actual_board)

        return click #(x, y) tuple to click
    
    def easy_agent(self):
        #function that returns easy mode (x, y) tuple
        pass

    def find_neighbors(self, x, y, board):
        #function that returns list of (x, y) tuples of neighbors
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(board) and 0 <= ny < len(board[0]):
                    neighbors.append((nx, ny))
        return neighbors
    def medium_setup(self):
        self.flagged = set() 
        #setting up class variables for medium agent
        pass

    def medium_agent(self, visible_board):
        #function that returns either a tuple to click, or None if there is no other option
        for x in range(len(visible_board)):
            for y in range(len(visible_board[0])):
                if visible_board[x][y] == BoardPiece.MINE:
                    return None
                if visible_board[x][y] != BoardPiece.UNKNOWN and visible_board[x][y] != BoardPiece.FLAG:
                    neighbors = self.find_neighbors(x, y, visible_board)
                    unknown_neighbors = [(nx, ny) for (nx, ny) in neighbors if visible_board[nx][ny] == BoardPiece.UNKNOWN and (nx, ny) not in self.flagged]
                    flagged_neighbors = [(nx, ny) for (nx, ny) in neighbors if (visible_board[nx][ny] == BoardPiece.FLAG or (nx, ny) in self.flagged)]

                    # If the number of flagged neighbors equals the number on the square, all other unknown neighbors are safe to click
                    if len(flagged_neighbors) == visible_board[x][y]:
                        for (nx, ny) in unknown_neighbors:
                            print("Clicking at", (nx, ny))
                            return (nx, ny)  # Return the coordinates of a safe square to click

                    # If the number of unknown neighbors equals the number on the square minus the number of flagged neighbors, all unknown neighbors are bombs
                    print(visible_board[x][y], len(flagged_neighbors), len(unknown_neighbors))
                    if len(unknown_neighbors) > 0 and len(unknown_neighbors) == visible_board[x][y] - len(flagged_neighbors):
                        for (nx, ny) in unknown_neighbors:
                            print("Flagging at", (nx, ny))
                            self.flagged.add((nx, ny)) # Mark these as flagged
                    
        covered_cells = [(x, y) for x in range(len(visible_board)) for y in range(len(visible_board[0])) if visible_board[x][y] == BoardPiece.UNKNOWN and (x, y) not in self.flagged]
        if len(covered_cells) > 0:
            random_choice = random.choice(covered_cells)
            print("No safe moves found, clicking at random covered cell", random_choice)
            return random_choice  # If no safe moves found, return a random covered cell to click
        return None  # If no moves found, return None
    

    def hard_agent(self, visible_board, actual_board):
        #function that returns hard mode (x, y) tuple
        
        # Iterate through the board to find an unrevealed square that is not a bomb
        for x in range(len(visible_board)):
            for y in range(len(visible_board[0])):
                # Check if the square is unrevealed and not a bomb
                if (visible_board[x][y] == BoardPiece.UNKNOWN and 
                    actual_board[x][y] != BoardPiece.MINE):
                    return (x, y)  # Return the coordinates of the safe square
        
        # If no safe unrevealed squares found, return None
        return None

def testing():
    board = Board()
    actual_board = board.actual_board
    board.GenerateBoard((5,5))
    move = 0
    agent = Agent(1)
    while move != None:
        move = agent.run_agent(board.visible_board)
        if move is None:
            break  # no moves left
        # Check bomb hit
        print("Agent is clicking at", move)
        if actual_board[move[0]][move[1]] == BoardPiece.MINE:
            print("Agent hit a mine at", move)
            board.state = GameState.LOSE_SCREEN
            break 
        if move != None or board.state != GameState.PLAYING:
            board.RevealSpace((move[0], move[1]))
            print()
            print("Visible Board:")
            board.PrintVisibleBoard()
            print()
            print("Actual Board:")
            board.PrintActualBoard()
            print("++++++++++++++++++++++++++++++++")
    if board.state == GameState.WIN_SCREEN:
        print("You Win!")
    elif board.state == GameState.LOSE_SCREEN:
        print("Game Over")
#testing()