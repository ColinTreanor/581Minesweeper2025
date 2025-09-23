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

class Agent():
    #Agent class will be instantiated with a difficulty level, and will use that to determine which algorithm to run
    #run function will only need board state
    #this way, the agent class is agnostic to if it is running in VS or Auto-Solve mode
    def __init__(self, difficulty):
        self.difficulty = difficulty #0 = EASY, 1 = MEDIUM, 2 = HARD

        if difficulty == 1:
            self.medium_setup()

    def run_agent(self, board_state):
        if self.difficulty == 0:
            click = self.easy_agent()
        elif self.difficulty == 1:
            click = self.medium_agent(board_state)
        elif self.difficulty == 2:
            click = self.hard_agent(board_state)

        return click #(x, y) tuple to click
    
    def easy_agent(self):
        #function that returns easy mode (x, y) tuple
        pass

    def medium_agent(self, visible_board):
        #function that returns medium mode (x, y) tuple
        pass

    def medium_setup(self):
        #setting up class variables for medium agent
        self.current_cell
        pass

    def hard_agent(self, actual_board):
        #function that returns hard mode (x, y) tuple
        pass

        