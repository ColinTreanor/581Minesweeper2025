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

CELL_SIZE = 40

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