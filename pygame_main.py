import pygame
from game_engine import BoardEngine
from event_handler import EventHandler
from board import *
from UI_engine import UIEngine

#includes scraps from https://coderslegacy.com/python/python-pygame-tutorial/
FPS = 60
FramePerSec = pygame.time.Clock()
 
# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

def main():
    #make pygame stuff
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption("Game")

    #make our classes
    Game = BoardEngine()
    UI = UIEngine()
    while True:     
        for event in pygame.event.get():              
            EventHandler.HandleEvent(event, Game)

        UI.UpdateDisplay(DISPLAYSURF, Game.GetBoardState())

        #upload window / surface changes
        pygame.display.update()
        #limit game speed to 60 FPS
        FramePerSec.tick(FPS)
    
if __name__ == "__main__":
    main()