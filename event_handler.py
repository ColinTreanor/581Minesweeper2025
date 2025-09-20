import pygame, sys
from pygame.locals import *
from game_engine import BoardEngine
from board import *
import button as ButtonClass

class EventHandler:
    #Thinking no member variables, just member functions to implement functionality

    def HandleEvent(event: pygame.event, game : Board):
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
                        if (button.mRect.collidepoint(position) and button.mOnState == game.state):
                            #TODO: implement other button functionality
                            # print(f"Button Type: {button.mButtonType}")
                            match button.mButtonType:
                                case ButtonClass.ButtonTypes.WIN_RESTART_GAME | ButtonClass.ButtonTypes.LOSE_RESTART_GAME | ButtonClass.ButtonTypes.MIDGAME_RESTART_GAME:
                                    game.ResetBoard()
                                case ButtonClass.ButtonTypes.MINE_SELECT_UP_ARROW:
                                    # only update mines if it is less than max mines value
                                    if game.mines < MAX_MINES:
                                        game.IncrimentMines()
                                case ButtonClass.ButtonTypes.MINE_SELECT_DOWN_ARROW:
                                    # only update mines if there are more than min mines value
                                    if game.mines > MIN_MINES:
                                        game.DecramentMines()
                                case ButtonClass.ButtonTypes.MINE_SELECT_START:
                                    game.state = GameState.PLAYING
                            break

                    if (game.state == GameState.PLAYING): 
                        #added rudimentery for clicking cell 
                         x, y = pygame.mouse.get_pos()
                         r = y // 40 #cell size - 40
                         c = x // 40 
                         game.RevealSpace((r, c))
                         #TODO: implement functionality for clicking cell
                        # print("Placeholder for left click functionality")

                elif (rightMousePressed):
                    if (game.state == GameState.PLAYING):
                         x, y = pygame.mouse.get_pos()
                         r = y // 40 #cell size - 40
                         c = x // 40 
                         game.PlaceFlag((r, c))
                         #TODO: implement functionality for clicking cell
                       #  print("Placeholder for right click functionality")

        if event.type == QUIT:
            #end pygame 
            pygame.quit() 
            #end python script
            sys.exit()
        return