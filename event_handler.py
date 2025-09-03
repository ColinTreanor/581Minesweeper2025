import pygame, sys
from pygame.locals import *
from game_engine import BoardEngine

'''
define the button rects here
use the rects in event handler to determine event
maybe make them a separate class to allow accessing with UI?
button instances:
- reset
- start game
- maybe up and down arrow (might be using arrow keys instead)
'''

 
class EventHandler:
    #Thinking no member variables, just member functions to implement functionality

    def HandleEvent(event: pygame.event, game : BoardEngine):
        '''
        will do one of the following:
            - close the game
            - tell BoardEngine to return to StartScreen
            - tell BoardEngine to make new game with certain mines
            - tell BoardEngine to register click if it is users turn (use bool to keep track of that)
        probably using a switch statement
        ''' 
        if event.type == QUIT:
            #end pygame
            pygame.quit()
            #end python script
            sys.exit()
        return