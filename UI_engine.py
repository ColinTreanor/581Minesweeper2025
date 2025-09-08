from board import *
import pygame
import button as ButtonClass
from constants import *


class UIEngine:
    #Thinking no member variables, just member functions to implement functionality
    def InitializeButtonList():
        #up arrow
        ButtonClass.ButtonList.append(ButtonClass.ButtonInfo(
            ButtonClass.ButtonTypes.MINE_SELECT_UP_ARROW, 
            pygame.image.load("./sprites/start_screen/up_arrow.png").convert_alpha(), 
            (3/4 * SCREEN_WIDTH, 5/12 * SCREEN_HEIGHT), GameState.START_SCREEN
        ))
        #down arrow
        ButtonClass.ButtonList.append(ButtonClass.ButtonInfo(
            ButtonClass.ButtonTypes.MINE_SELECT_DOWN_ARROW, 
            pygame.image.load("./sprites/start_screen/down_arrow.png").convert_alpha(), 
            (3/4 * SCREEN_WIDTH, SCREEN_HEIGHT / 2 + 5), GameState.START_SCREEN
        ))
        #start button
        start_img = pygame.image.load("./sprites/start_screen/start_button.png").convert_alpha()
        start_img = pygame.transform.scale_by(start_img, 2)
        ButtonClass.ButtonList.append(ButtonClass.ButtonInfo(
            ButtonClass.ButtonTypes.MINE_SELECT_START, start_img,
            (1/2 * SCREEN_WIDTH, 3/4 * SCREEN_HEIGHT), GameState.START_SCREEN
        ))
        #win screen restart
        ButtonClass.ButtonList.append(ButtonClass.ButtonInfo(
            ButtonClass.ButtonTypes.WIN_RESTART_GAME, pygame.image.load("sprites/placeholder_restart.png"), 
            (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.75), GameState.WIN_SCREEN 
        )) 
        return

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
        # fill with background color
        surface.fill(START_BG_COLOR)

        # draw border lines to make background look nicer
        line_width = 20
        # weird math with coordinates, i think lines are drawn with x representing the left edge and y representing the middle of the edge ???
        pygame.draw.line(surface, START_DARK_LINE_COLOR, (400-line_width//2,0), (400-line_width//2,600), line_width)
        pygame.draw.line(surface, START_DARK_LINE_COLOR, (0, 600-line_width//2), (400,600-line_width//2), line_width)
        pygame.draw.line(surface, START_LIGHT_LINE_COLOR, (0,0+line_width//2), (400+line_width,0+line_width//2), line_width)
        pygame.draw.line(surface, START_LIGHT_LINE_COLOR, (0+line_width//2,0), (0+line_width//2,600+line_width), line_width)

        # get header font
        reg_font_path = "fonts/Handjet-Regular.ttf"
        reg_font_size = 32
        reg_font = pygame.font.Font(reg_font_path, reg_font_size)
        UIEngine._DrawText(surface, "Choose how many mines: ", reg_font, BLACK, 65, 150)

        # draw minesweeper title on screen
        minesweeper_title = pygame.image.load("./sprites/start_screen/minesweeper_title.png").convert_alpha()
        minesweeper_title = pygame.transform.scale_by(minesweeper_title, .75)
        surface.blit(minesweeper_title, (50,35))

        # draw blank space for number of mines text to go
        pygame.draw.rect(surface, START_LIGHT_LINE_COLOR, pygame.Rect(150, 240, 100, 75))
        
        return
    
    def DisplayPlayingScreen(surface : pygame.display, boardState : Board):
        #TODO: implement this function to display playing screen
        return
    
    def DisplayWinScreen(surface : pygame.display):
        WinFont = pygame.font.SysFont('Comic Sans MS', 80)
        WinText = 'You WIN!'
        WinTextSurface = WinFont.render(WinText, False, BLACK)
        WinTextSize = WinFont.size(WinText)
        surface.blit(WinTextSurface, (SCREEN_WIDTH / 2 - WinTextSize[0] / 2, 
                                      SCREEN_HEIGHT / 2 - WinTextSize[1] / 2))
        return
    
    def DisplayLoseScreen(surface : pygame.display):
        #TODO: implement this function to display lose screen
        return
    
    def DisplayButtons(surface : pygame.display, gameState : GameState):
        for button in ButtonClass.ButtonList: 
            if (gameState == button.mOnState):
                surface.blit(button.mImg, button.mRect)
        return
    
    def _DrawText(surface: pygame.display, text: str, font: pygame.font, text_col, x: int, y: int):
        """
        Function that draws text to the screen
        Params:
            surface: surface to write text to
            text: text to be written
            font: font to use to write text
            text_col: color of text. Type is any color format pygame accepts, usually (r, g, b, a)
            x: x coordinate for text
            y: y coordinate of text
        """
        img = font.render(text, True, text_col)
        surface.blit(img,(x,y))
    