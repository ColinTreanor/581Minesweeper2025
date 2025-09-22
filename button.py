"""
Minesweeper Button Module

Module Name: button.py
Description: Defines button types and button objects for the Minesweeper UI.
             Provides an enumeration for different button actions and a class
             for storing button attributes such as image, position, and state.
             Used by the UIEngine and EventHandler to handle interaction logic.

Inputs:
    - Button definitions with associated images, positions, and active states
    - User click positions checked against button hitboxes

Outputs:
    - List of available buttons (ButtonList)
    - ButtonInfo objects that provide attributes for rendering and interaction

External Sources:
    - Pygame library for images, rects, and collision detection

Author: Team 17
Creation Date: ___
"""
import pygame
from pygame.locals import *
from board import GameState
from enum import Enum
from UI_engine import UIEngine

class ButtonTypes(Enum):
    """Enumeration of all button types in the Minesweeper UI.
        Each enum value corresponds to a unique button function in the game.
        Members:
            MINE_SELECT_UP_ARROW (int): Increase mine count on start screen.
            MINE_SELECT_DOWN_ARROW (int): Decrease mine count on start screen.
            MINE_SELECT_START (int): Begin the game from the start screen.
            MIDGAME_RESTART_GAME (int): Restart during an active game.
            WIN_RESTART_GAME (int): Restart after a win.
            LOSE_RESTART_GAME (int): Restart after a loss.
    """
    #just enum class to represent pieces
    MINE_SELECT_UP_ARROW = 0
    MINE_SELECT_DOWN_ARROW = 1
    MINE_SELECT_START = 2
    # I made three separate in this template, but it may be possible to condense them 
    # if we place them in the same spot / use the same sprites
    MIDGAME_RESTART_GAME = 3
    WIN_RESTART_GAME = 4
    LOSE_RESTART_GAME = 5

class ButtonInfo():
    """Stores information about a UI button.
        Encapsulates the properties of a button, including its type,
        image, rectangular bounds, and the game state it belongs to.
        Attributes:
            mButtonType (ButtonTypes): The functional type of the button.
            mImg (pygame.Surface): The rendered image for the button.
            mRect (pygame.Rect): Rectangular hitbox for positioning and collision.
            mOnState (GameState): The game state in which the button is active.
        Methods:
            None (this class only stores button attributes)
    """
    def __init__(self, aButtonType : ButtonTypes, aImg : pygame.image, aCenter : tuple, aOnState : GameState):
        """Initialize a ButtonInfo object.
            Args:
                aButtonType (ButtonTypes): The functional type of this button.
                aImg (pygame.Surface): Pygame image used to render the button.
                aCenter (tuple): (x, y) coordinates for button center position.
                aOnState (GameState): The game state in which this button is active.
            Returns:
                None
        """
        self.mButtonType = aButtonType
        self.mImg = aImg
        self.mRect = self.mImg.get_rect()
        self.mRect.center = aCenter
        #used for checking if button should be displayed / considered as valid
        self.mOnState = aOnState

ButtonList = [
]