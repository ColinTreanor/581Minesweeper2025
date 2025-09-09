import pygame, sys
from pygame.locals import *
from game_engine import BoardEngine
from board import *
import button as ButtonClass

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
        if event.type == MOUSEBUTTONDOWN: 
                #put in event handler
                leftMousePressed = pygame.mouse.get_pressed()[0]
                rightMousePressed = pygame.mouse.get_pressed()[2]
                position = pygame.mouse.get_pos()

                if (leftMousePressed):
                    for button in ButtonClass.ButtonList: 
                        if (button.mRect.collidepoint(position) and button.mOnState == game.GetBoardState().state):
                            #TODO: implement other button functionality
                            print(f"Button Type: {button.mButtonType}")
                            match button.mButtonType:
                                case ButtonClass.ButtonTypes.WIN_RESTART_GAME | ButtonClass.ButtonTypes.LOSE_RESTART_GAME:
                                    game.Restart()
                            break

                    if (game.GetBoardState().state == GameState.PLAYING):
                         #TODO: implement functionality for clicking cell
                         print("Placeholder for left click functionality")

                elif (rightMousePressed):
                    if (game.GetBoardState().state == GameState.PLAYING):
                         #TODO: implement functionality for clicking cell
                         print("Placeholder for right click functionality")

        if event.type == QUIT:
            #end pygame 
            pygame.quit() 
            #end python script
            sys.exit()
        return