import pygame
from pygame.locals import *
from board import GameState
from enum import Enum
from UI_engine import UIEngine

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

ButtonList = [
]