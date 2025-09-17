from board import *
import pygame
from button import Button
import button as ButtonClass
from constants import *

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(3, 6)
        self.color = (255, 200, 50)
        self.life = 40
        self.vel = [random.uniform(-3, 3), random.uniform(-3, 3)]

    def update(self):
        self.x += self.vel[0]
        self.y += self.vel[1]
        self.life -= 1
        fade = max(self.life * 6, 0)
        r = min(255, fade)
        g = max(0, fade - 150)
        b = 0
        self.color = (r, g, b)

    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

def explosion_animation(screen, x, y):
    particles = [Particle(x, y) for _ in range(50)]
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for p in particles:
            p.update()
            p.draw(screen)
        pygame.display.update()
        clock.tick(30)
        particles = [p for p in particles if p.life > 0]
        if not particles:
            running = False

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

        #lose screen restart
        restart_img = pygame.Surface((200, 60))
        restart_img.fill((200, 0, 0))
        small_font = pygame.font.Font(None, 36)
        label = small_font.render("RESTART", True, (255, 255, 255))
        restart_img.blit(label, (40, 15))
        ButtonClass.ButtonList.append(ButtonClass.ButtonInfo(
            ButtonClass.ButtonTypes.LOSE_RESTART_GAME,
            restart_img, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100), GameState.LOSE_SCREEN
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
        match boardState.board.state:
            case GameState.START_SCREEN:
                UIEngine.DisplayStartScreen(surface, boardState)
            case GameState.PLAYING:
                UIEngine.DisplayPlayingScreen(surface, boardState)
            case GameState.WIN_SCREEN:
                UIEngine.DisplayWinScreen(surface)
            case GameState.LOSE_SCREEN:
                UIEngine.DisplayLoseScreen(surface)

        UIEngine.DisplayButtons(surface, boardState.board.state)
        return
    
    def DisplayStartScreen(surface : pygame.display, boardState : Board):
        # fill with background color
        surface.fill(START_BG_COLOR)

        # draw border lines to make background look nicer
        line_width = 20
        # weird math with coordinates, i think lines are drawn with x being the pos of the left edge and y being the pos of the middle of the edge ???
        pygame.draw.line(surface, START_DARK_LINE_COLOR, (SCREEN_WIDTH-line_width//2,0), (SCREEN_WIDTH-line_width//2,SCREEN_HEIGHT), line_width)
        pygame.draw.line(surface, START_DARK_LINE_COLOR, (0, SCREEN_HEIGHT-line_width//2), (SCREEN_WIDTH,SCREEN_HEIGHT-line_width//2), line_width)
        pygame.draw.line(surface, START_LIGHT_LINE_COLOR, (0,0+line_width//2), (SCREEN_WIDTH+line_width,0+line_width//2), line_width)
        pygame.draw.line(surface, START_LIGHT_LINE_COLOR, (0+line_width//2,0), (0+line_width//2,SCREEN_HEIGHT+line_width), line_width)
        # # get bolded font
        header_font_path = "fonts/Handjet-Bold.ttf"
        header_size = 48
        header_font = pygame.font.Font(header_font_path, header_size)
        # get regular font
        reg_font_path = "fonts/HandJet-Regular.ttf"
        reg_font_size = 32
        reg_font = pygame.font.Font(reg_font_path, reg_font_size)
        UIEngine._DrawText(surface, "Choose how many mines: ", reg_font, BLACK, 65, 150)

        # draw minesweeper title on screen
        minesweeper_title = pygame.image.load("./sprites/start_screen/minesweeper_title.png").convert_alpha()
        minesweeper_title = pygame.transform.scale_by(minesweeper_title, .75)
        surface.blit(minesweeper_title, (50,35))
        
        # # make up and down arrows
        # up_arrow = pygame.image.load("./sprites/start_screen/up_arrow.png").convert_alpha()
        # down_arrow = pygame.image.load("./sprites/start_screen/down_arrow.png").convert_alpha()
        # up_button = ButtonClass.ButtonInfo(ButtonClass.ButtonTypes.MINE_SELECT_UP_ARROW, up_arrow, (300,250), GameState.START_SCREEN)
        # down_button = ButtonClass.ButtonInfo(ButtonClass.ButtonTypes.MINE_SELECT_DOWN_ARROW, down_arrow, (300,305), GameState.START_SCREEN)
        # # append to test button list for now, uncertain of real implementation
        # # ButtonClass.ButtonList.append(up_button)
        # # ButtonClass.ButtonList.append(down_button)
        # # make start button
        # start_img = pygame.image.load("./sprites/start_screen/start_button.png").convert_alpha()
        # start_img = pygame.transform.scale_by(start_img, 2) # scale by a factor of 2
        # start_button = ButtonClass.ButtonInfo(ButtonClass.ButtonTypes.MINE_SELECT_START, start_img, (200,450), GameState.START_SCREEN)
        # # ButtonClass.ButtonList.append(start_button)
        # draw blank space for number of mines text to go
        pygame.draw.rect(surface, START_LIGHT_LINE_COLOR, pygame.Rect(150, 240, 100, 75))
        
        num_of_mines = boardState.board.mines
        # placeholder to draw number of mines 
        UIEngine._DrawText(surface, str(num_of_mines), header_font, BLACK, 175, 250)
        return
    
    def DisplayPlayingScreen(surface : pygame.display, boardState : Board):
        #TODO: implement this function to display playing screen
        surface.fill(BUTTON_RED)
        return
    
    def DisplayWinScreen(surface : pygame.display):
        WinFont = pygame.font.SysFont('Comic Sans MS', 80)
        WinText = 'You WIN!'
        WinTextSurface = WinFont.render(WinText, False, BLACK)
        WinTextSize = WinFont.size(WinText)
        surface.blit(WinTextSurface, (SCREEN_WIDTH / 2 - WinTextSize[0] / 2, 
                                      SCREEN_HEIGHT / 2 - WinTextSize[1] / 2))
        return
    
    #def DisplayLoseScreen(surface : pygame.display):
    #    surface.fill((0, 0, 0))
    #    font = pygame.font.Font(None, 74)
    #    text = font.render("You Lose!", True, (255, 0, 0))
    #    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
    #    surface.blit(text, text_rect)
    #    return
    
    def DisplayLoseScreen(surface : pygame.display):
        #TODO: implement this function to display lose screen
        return
        surface.fill((50, 50, 50))
        boardState.draw_board()
        pygame.display.update()
        pygame.time.delay(500) 

        screen_width, screen_height = surface.get_size()
        explosion_animation(surface, screen_width // 2, screen_height // 2)
        font = pygame.font.SysFont(None, 74)
        text = font.render('You Lose!', True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

        restart_img =pygme.suface((200, 60))
        restart_img.fill((200, 0, 0))
        small_font = pygame.font.SysFont(None, 36)
        restart_text = small_font.render('Restart', True, (255, 255, 255))
        restart_img.bilt(label,(40,15))
        restart_button = ButtonClass.Button(screen_width // 2, screen_height // 2 + 100, restart_img)

        running = True
        while running: 
            surface.fill((0, 0, 0))
            surface.blit(text, text_rect)
            if restart_button.draw(surface):
                return "restart"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()
        pygame.quit()

    
    
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
    