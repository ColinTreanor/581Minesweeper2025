import pygame, sys, os
from pygame.locals import *

# code to allow using python code from parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import button as ButtonClass

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
    pygame.display.set_caption("Button Test")

    while True:     
        for event in pygame.event.get(): 
            if event.type == MOUSEBUTTONDOWN: 
                #put in event handler
                leftMousePressed = pygame.mouse.get_pressed()[0]
                rightMousePressed = pygame.mouse.get_pressed()[2]
                position = pygame.mouse.get_pos()
                if (leftMousePressed):
                    for button in ButtonClass.ButtonList:
                        #should add handling to check game state and only register click if the button's game state matches the current one
                        if (button.mRect.collidepoint(position)):
                            print(f"clicked: {button.mRect}")
                            #should maybe add handling to exit loop if button is clicked?
                            break
                elif (rightMousePressed):
                    print("right")

            if event.type == QUIT:
                #end pygame
                pygame.quit()
                #end python script
                sys.exit()

        #put in UI engine
        for button in ButtonClass.ButtonList:
            DISPLAYSURF.blit(button.mImg, button.mRect)

        #upload window / surface changes
        pygame.display.update()
        #limit game speed to 60 FPS
        FramePerSec.tick(FPS)
    
if __name__ == "__main__":
    main()
