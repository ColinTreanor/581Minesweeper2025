from board import *
import pygame
import button as ButtonClass


class UIEngine:
    #Thinking no member variables, just member functions to implement functionality

    def UpdateDisplay(surface : pygame.display, boardState : Board):
        '''
        will do one of the following:
            - display start screen
            - display win screen
            - display lose screen
            - display current board
        probably using switch statement to differentiate between
        '''
        match boardState.state:
            case GameState.START_SCREEN:
                UIEngine.DisplayStartScreen(surface)
            case GameState.PLAYING:
                UIEngine.DisplayPlayingScreen(surface, boardState)
            case GameState.WIN_SCREEN:
                UIEngine.DisplayWinScreen(surface)
            case GameState.LOSE_SCREEN:
                UIEngine.DisplayLoseScreen(surface)

        UIEngine.DisplayButtons(surface, boardState.state)
        return
    
    def DisplayStartScreen(surface : pygame.display):
        #TODO: implement this function to display start screen
        return
    
    def DisplayPlayingScreen(surface : pygame.display, boardState : Board):
        #TODO: implement this function to display playing screen
        return
    
    def DisplayWinScreen(surface : pygame.display):
        #TODO: implement this function to display win screen
        return
    
    def DisplayLoseScreen(surface : pygame.display):
        #TODO: implement this function to display lose screen
        return
        
    
    def DisplayButtons(surface : pygame.display, gameState : GameState):
        #TODO: update this with actual list of buttons when those are added
        for button in ButtonClass.TestButtonList:
            if (gameState == button.mOnState):
                surface.blit(button.mImg, button.mRect)
        return
    