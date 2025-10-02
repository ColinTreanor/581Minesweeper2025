"""
Minesweeper Constants Module

Module Name: constants.py
Description: Stores all global values used in implementation of MineSweeper

Inputs:
    - N/A

Outputs:
    - N/A

External Sources:
    - Pygame library for rendering and animation
    - Assets (sprites, fonts) located in the sprites/ and fonts/ directories

Author: Team 17
Creation Date: 9/8/2025
"""

import pygame
# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
START_BG_COLOR = (192,192,192)
START_DARK_LINE_COLOR = (128, 128, 128)
START_LIGHT_LINE_COLOR = (232, 232, 232)
BLACK = (0,0,0)
BUTTON_RED = (225, 105, 105)
 
# Screen information
SCREEN_WIDTH = 430
SCREEN_HEIGHT = 650

MAX_MINES = 20
MIN_MINES = 10

CELL_SIZE = 40
GRID_OFFSET_X = 30
GRID_OFFSET_Y = 30

x_AXIS = 10
TEXT_OFFSET_TITLE = 10
TEXT_OFFSET_TIME = 65
TEXT_OFFSET_FLAGS = 110
EMOJI_X_OFFSET_PLAYING = 200
EMOJI_Y_OFFSET_PLAYING = 160

empty_square = pygame.image.load('sprites/empty_square.png')
filled_square = pygame.image.load('sprites/filled_square.png')
flag_img = pygame.image.load('sprites/flag.png')
mine_img = pygame.image.load('sprites/mine.png')
mine_clicked_img = pygame.image.load('sprites/mineClicked.png')
mine_false_img = pygame.image.load('sprites/mineFalse.png')

grid1_img = pygame.image.load('sprites/grid1.png')
grid2_img = pygame.image.load('sprites/grid2.png')
grid3_img = pygame.image.load('sprites/grid3.png')
grid4_img = pygame.image.load('sprites/grid4.png')
grid5_img = pygame.image.load('sprites/grid5.png')
grid6_img = pygame.image.load('sprites/grid6.png')
grid7_img = pygame.image.load('sprites/grid7.png')
grid8_img = pygame.image.load('sprites/grid8.png')

emoji_play = pygame.image.load('sprites/playing.png')
emoji_lose = pygame.image.load('sprites/lose.png')

emoji_play = pygame.transform.scale(emoji_play, (60, 60))
emoji_lose = pygame.transform.scale(emoji_lose, (60, 60))
empty_square = pygame.transform.scale(empty_square, (CELL_SIZE, CELL_SIZE))
filled_square = pygame.transform.scale(filled_square, (CELL_SIZE, CELL_SIZE))
flag_img = pygame.transform.scale(flag_img, (CELL_SIZE, CELL_SIZE))
mine_img = pygame.transform.scale(mine_img, (CELL_SIZE, CELL_SIZE))
mine_clicked_img = pygame.transform.scale(mine_clicked_img, (CELL_SIZE, CELL_SIZE))
mine_false_img = pygame.transform.scale(mine_false_img, (CELL_SIZE, CELL_SIZE))

grid1_img = pygame.transform.scale(grid1_img, (CELL_SIZE, CELL_SIZE))
grid2_img = pygame.transform.scale(grid2_img, (CELL_SIZE, CELL_SIZE))
grid3_img = pygame.transform.scale(grid3_img, (CELL_SIZE, CELL_SIZE))
grid4_img = pygame.transform.scale(grid4_img, (CELL_SIZE, CELL_SIZE))
grid5_img = pygame.transform.scale(grid5_img, (CELL_SIZE, CELL_SIZE))
grid6_img = pygame.transform.scale(grid6_img, (CELL_SIZE, CELL_SIZE))
grid7_img = pygame.transform.scale(grid7_img, (CELL_SIZE, CELL_SIZE))
grid8_img = pygame.transform.scale(grid8_img, (CELL_SIZE, CELL_SIZE))

grid_imgs = {
    1: grid1_img,
    2: grid2_img,
    3: grid3_img,
    4: grid4_img,
    5: grid5_img,
    6: grid6_img,
    7: grid7_img,
    8: grid8_img,
}

agent_img = pygame.image.load('sprites/agent.png')
agent_img = pygame.transform.scale(agent_img, (CELL_SIZE, CELL_SIZE))

# Game Mode Constants
from enum import Enum

class GameMode(Enum):
    """Enumeration for different game modes"""
    SINGLE_PLAYER = "Single Player"
    MULTIPLAYER = "Multiplayer"
    AUTO_SOLVER = "Auto Solver"

class BotDifficulty(Enum):
    """Enumeration for bot difficulty levels"""
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"