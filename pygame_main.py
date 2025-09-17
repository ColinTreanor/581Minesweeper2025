import pygame
from game_engine import BoardEngine
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
    Game = BoardEngine()
    while True:     
        for event in pygame.event.get():              
            EventHandler.HandleEvent(event, Game)

        UIEngine.UpdateDisplay(DISPLAYSURF, Game)
        '''uncomment to test displaying the game screen
        time = 10
        UIEngine.DisplayPlayingScreen(DISPLAYSURF, Game.GetBoardState(), time)
        '''
        #upload window / surface changes
        pygame.display.update()
        #limit game speed to 60 FPS
        FramePerSec.tick(FPS)
    
if __name__ == "__main__":
    main()