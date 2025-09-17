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
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

MAX_MINES = 20
MIN_MINES = 10

emoji_play = pygame.image.load('sprites/playing.png')
emoji_lose = pygame.image.load('sprites/lose.png')

emoji_play = pygame.transform.scale(emoji_play, (60, 60))
emoji_lose = pygame.transform.scale(emoji_lose, (60, 60))