from board import *
import pygame
import button as ButtonClass
from constants import *
from constants import emoji_play, emoji_lose

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
    explosion_played = False
    
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
        label = small_font.render("RESTART", True, WHITE)
        restart_img.blit(label, (40, 15))
        ButtonClass.ButtonList.append(ButtonClass.ButtonInfo(
            ButtonClass.ButtonTypes.LOSE_RESTART_GAME,
            restart_img, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100), GameState.LOSE_SCREEN
        ))

        #win screen restart 
        win_restart_img = pygame.Surface((200, 60))
        win_restart_img.fill((0, 200, 0))
        small_font = pygame.font.Font(None, 36)
        win_label = small_font.render("RESTART", True, WHITE)
        win_restart_img.blit(win_label, (40, 15))
        ButtonClass.ButtonList.append(ButtonClass.ButtonInfo(
            ButtonClass.ButtonTypes.WIN_RESTART_GAME,
            win_restart_img, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100), GameState.WIN_SCREEN
        ))

        #playing screen restart
        playing_restart_img = pygame.Surface((140, 50))
        playing_restart_img.fill((255, 255, 255))
        pygame.draw.rect(playing_restart_img, (0, 0, 0), playing_restart_img.get_rect(), 2)
        restart_font = pygame.font.SysFont(None, 24)
        restart_label = restart_font.render("Restart", True, (0, 0, 0))
        restart_text_rect = restart_label.get_rect(center=(70, 25))
        playing_restart_img.blit(restart_label, restart_text_rect)
        ButtonClass.ButtonList.append(ButtonClass.ButtonInfo(
            ButtonClass.ButtonTypes.MIDGAME_RESTART_GAME,
            playing_restart_img,
            (80, 550), GameState.PLAYING
        ))
        return

    def UpdateDisplay(surface : pygame.display, board : Board, time):
        '''
        will do one of the following:
            - display start screen
            - display win screen
            - display lose screen
            - display current board
        probably using switch statement to differentiate between
        '''
        match board.state:
            case GameState.START_SCREEN:
                UIEngine.DisplayStartScreen(surface, board, time)
            case GameState.PLAYING:
                UIEngine.DisplayPlayingScreen(surface, board, time)
            case GameState.WIN_SCREEN:
                UIEngine.DisplayWinScreen(surface, time)
            case GameState.LOSE_SCREEN:
                UIEngine.DisplayLoseScreen(surface, time)

        UIEngine.DisplayButtons(surface, board.state, time)
        return
    
    def DisplayStartScreen(surface : pygame.display, board : Board, time):
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
        reg_font_path = "fonts/Handjet-Regular.ttf"
        reg_font_size = 32
        reg_font = pygame.font.Font(reg_font_path, reg_font_size)
        UIEngine._DrawText(surface, "Choose how many mines: ", reg_font, BLACK, 65, 150)

        # draw minesweeper title on screen
        minesweeper_title = pygame.image.load("./sprites/start_screen/minesweeper_title.png").convert_alpha()
        minesweeper_title = pygame.transform.scale_by(minesweeper_title, .75)
        surface.blit(minesweeper_title, (50,35))
        
        pygame.draw.rect(surface, START_LIGHT_LINE_COLOR, pygame.Rect(150, 240, 100, 75))
        
        num_of_mines = board.mines
        # placeholder to draw number of mines 
        UIEngine._DrawText(surface, str(num_of_mines), header_font, BLACK, 175, 250)
        return
    
    def DisplayPlayingScreen(surface : pygame.display, board : Board, time): #have to update all things calling this to include time as a param
        UIEngine.explosion_played = False
        surface.fill(START_BG_COLOR)

        GRAY = (150, 150, 150) #we can probably make these global vars for the rest of the screens
        RED   = (255, 0, 0)
        BLACK = (0, 0, 0)
        DARK_GRAY = (50, 50, 50)
        WHITE = (255, 255, 255)

        #creating the coords is a little bit of a mess sorry, when you blit its basically surface.blit(x value, y value)
        cell_size = 40
        font = pygame.font.SysFont(None, 24)
        big_font = pygame.font.SysFont(None, 56)
        title = big_font.render("Minesweeper", True, BLACK)
        surface.blit(title, (10, board.board_size * cell_size + 10))
        time_display = big_font.render(f"Time: {time}", True, BLACK)
        surface.blit(time_display, (10, board.board_size * cell_size + 80))

        for r in range(board.board_size):
            for c in range(board.board_size):
                visible_piece = board.visible_board[r][c]
                actual_piece = board.actual_board[r][c]
                rect = pygame.Rect(c * cell_size, r * cell_size, cell_size, cell_size)

                if visible_piece == BoardPiece.FLAG:
                    # Draw the unrevealed square (dark gray)
                    pygame.draw.rect(surface, DARK_GRAY, rect)
                    # Draw red dot for flag
                    flag_center = (rect.centerx, rect.centery)
                    pygame.draw.circle(surface, RED, flag_center, 8)
                elif visible_piece != BoardPiece.UNKNOWN:
                    pygame.draw.rect(surface, GRAY, rect)

                    if actual_piece == BoardPiece.MINE:
                        pygame.draw.rect(surface, RED, rect)
                        #minesprite blit add mayhaps
                    else:
                        if actual_piece.value > 0:
                            text = font.render(str(actual_piece.value), True, BLACK)
                            text_rect = text.get_rect(center=rect.center)
                            surface.blit(text, text_rect)
                            #if it has at least one mine it renders the string into text and then you can get rect to center the
                            #text in the cell box and then blit it to display 
                else:
                    pygame.draw.rect(surface, DARK_GRAY, rect)
                pygame.draw.rect(surface, BLACK, rect, 1)
        return
    
    def DisplayWinScreen(surface : pygame.display, time):
        surface.fill((0, 0, 0))
        WinFont = pygame.font.SysFont(None, 74)
        WinText = 'You WIN!'
        WinTextSurface = WinFont.render(WinText, False, GREEN)
        WinTextSize = WinFont.size(WinText)
        surface.blit(WinTextSurface, (SCREEN_WIDTH / 2 - WinTextSize[0] / 2, 
                                      SCREEN_HEIGHT / 2 - WinTextSize[1] / 2))
        return
    
    def DisplayLoseScreen(surface : pygame.display, time):
        if not UIEngine.explosion_played:
            explosion_animation(surface, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            UIEngine.explosion_played = True

        surface.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("You Lose!", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        surface.blit(text, text_rect)
        return

    def DisplayButtons(surface : pygame.display, gameState : GameState, time):
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
    