from board import *
import pygame


class UIEngine:
    #Thinking no member variables, just member functions to implement functionality

    def UpdateDisplay(self, surface : pygame.display, BoardState):
        '''
        will do one of the following:
            - display start screen
            - display win screen
            - display lose screen
            - display current board
        probably using switch statement to differentiate between
        '''
        return