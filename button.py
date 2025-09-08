import pygame
from pygame.locals import *
from board import GameState
from enum import Enum

class ButtonTypes(Enum):
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
    def __init__(self, aButtonType : ButtonTypes, aImg : pygame.image, aCenter : tuple, aOnState : GameState):
        self.mButtonType = aButtonType
        self.mImg = aImg
        self.mRect = self.mImg.get_rect()
        self.mRect.center = aCenter
        #used for checking if button should be displayed / considered as valid
        self.mOnState = aOnState
    
# template for how buttons would be initialized for list
TestButtonList = [
    # ButtonInfo(ButtonTypes.MINE_SELECT_UP_ARROW, pygame.image.load("sprites/mine.png"), (100, 100), GameState.START_SCREEN ), 
    # ButtonInfo(ButtonTypes.MINE_SELECT_DOWN_ARROW, pygame.image.load("sprites/mineClicked.png"), (300, 300), GameState.START_SCREEN ), 
    # ButtonInfo(ButtonTypes.MINE_SELECT_START, pygame.image.load("sprites/mineFalse.png"), (200, 500), GameState.START_SCREEN ),
]

#TODO: add list for actual buttons