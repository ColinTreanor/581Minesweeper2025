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
Creation Date: 9/8/2025
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
            GAME_MODE_TOGGLE (int): Toggle between game modes.
            agent_difficulty_DROPDOWN (int): Open bot difficulty dropdown.
            agent_difficulty_EASY (int): Set bot difficulty to easy.
            agent_difficulty_MEDIUM (int): Set bot difficulty to medium.
            agent_difficulty_HARD (int): Set bot difficulty to hard.
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
    # Game mode and bot difficulty buttons
    GAME_MODE_TOGGLE = 6
    agent_difficulty_DROPDOWN = 7
    agent_difficulty_EASY = 8
    agent_difficulty_MEDIUM = 9
    agent_difficulty_HARD = 10

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

ButtonList = []

class DropdownInfo():
    """Stores information about a dropdown menu.
    
    Manages dropdown state, options, and positioning for bot difficulty selection.
    
    Attributes:
        is_open (bool): Whether the dropdown is currently expanded.
        selected_option (str): Currently selected option text.
        options (list): List of available dropdown options.
        main_rect (pygame.Rect): Main dropdown button rectangle.
        option_rects (list): List of rectangles for each dropdown option.
        position (tuple): (x, y) position of the dropdown.
    """
    def __init__(self, options, position, selected_option=None):
        """Initialize a dropdown menu.
        
        Args:
            options (list): List of string options for the dropdown.
            position (tuple): (x, y) coordinates for dropdown position.
            selected_option (str): Initially selected option (defaults to first).
        """
        self.is_open = False
        self.options = options
        self.selected_option = selected_option or options[0]
        self.position = position
        
        # Create main dropdown button rect
        self.main_rect = pygame.Rect(position[0], position[1], 120, 30)
        
        # Create option rects (positioned below main button when open)
        self.option_rects = []
        for i, option in enumerate(options):
            rect = pygame.Rect(position[0], position[1] + 30 + (i * 25), 120, 25)
            self.option_rects.append(rect)
    
    def toggle(self):
        """Toggle dropdown open/closed state."""
        self.is_open = not self.is_open
    
    def select_option(self, option):
        """Select a specific option and close dropdown.
        
        Args:
            option (str): The option to select.
        """
        if option in self.options:
            self.selected_option = option
            self.is_open = False
    
    def get_clicked_option(self, pos):
        """Check if a click position hits any dropdown option.
        
        Args:
            pos (tuple): (x, y) click coordinates.
            
        Returns:
            str or None: The clicked option text, or None if no option clicked.
        """
        if not self.is_open:
            return None
            
        for i, rect in enumerate(self.option_rects):
            if rect.collidepoint(pos):
                return self.options[i]
        return None

ButtonList = [
]

# Global dropdown for bot difficulty selection
agent_difficulty_dropdown = None