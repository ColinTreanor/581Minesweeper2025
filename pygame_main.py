"""
Minesweeper Main Entry Point

Module Name: pygame_main.py
Description:
    Initializes the Pygame environment and is the main entry point for the Minesweeper application.
    Sets up the game window, initializes button and other UI components, creates the game Board object,
    and runs the main event loop that processes user input and updates the display

Inputs:
    - User events from Pygame (mouse clicks, quit event)
    - Board state (mines, flags, revealed spaces, win/lose condition)

Outputs:
    - Rendered Minesweeper window showing the appropriate screen:
        * Start screen
        * Active game screen
        * Win screen
        * Lose screen

External Sources:
    - pygame: Graphics and event system
    - Original template was initially created from / expanded on some parts in https://coderslegacy.com/python/python-pygame-tutorial/

Author: Team 17
Creation Date: 9/3/2025
"""

import pygame
from event_handler import EventHandler
from board import *
from UI_engine import UIEngine
from constants import *

FPS = 60
FramePerSec = pygame.time.Clock()

def main():
    """Main execution loop for the Minesweeper game

        Initializes and configures the game window, creates the Board
        object, sets up UI elements, and enters the infinite event loop.

        Flow of execution:
            1. Initialize Pygame and configure display window
            2. Call UIEngine to initialize interactive buttons
            3. Create Board object in START_SCREEN state
            4. Run event loop:
                - Capture and process user input with EventHandler
                - Update game visuals using UIEngine
                - Refresh window at fixed frame rate (FPS)
        Inputs:
            - User mouse/keyboard events handled by EventHandler
            - Board state transitions (START_SCREEN, PLAYING, WIN_SCREEN, LOSE_SCREEN)

        Outputs:
            - Updated graphical display showing current game state
            - Consistent frame rate controlled rendering
        """
    #make pygame stuff
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption("Game")

    #setup buttons
    UIEngine.InitializeButtonList()

    #make our classes
    Game = Board()

    while True:     
        for event in pygame.event.get():
            EventHandler.HandleEvent(event, Game)

        UIEngine.UpdateDisplay(DISPLAYSURF, Game, time=Game.CalculateDuration()) #need time calculation
        
        #upload window / surface changes
        pygame.display.update()
        #limit game speed to 60 FPS
        FramePerSec.tick(FPS)
    
if __name__ == "__main__":
    main()