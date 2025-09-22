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
    - event_handler: For processing user interactions
    - board: Core game logic and state management
    - UI_engine: For drawing UI and game board
    - constants: For screen dimensions, colors, and configuration
Author: ___
Creation Date: ___
"""

import pygame
from event_handler import EventHandler
from board import *
from UI_engine import UIEngine
from constants import *

#includes scraps from https://coderslegacy.com/python/python-pygame-tutorial/
FPS = 60
FramePerSec = pygame.time.Clock()

def main():
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