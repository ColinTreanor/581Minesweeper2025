"""
Minesweeper UI Engine Module

Module Name: UI_engine.py
Description: Handles all rendering and UI logic for the Minesweeper game.
             Responsible for drawing game boards, start/win/lose screens,
             buttons, animations, and headers. Provides centralized
             display update functionality that responds to the Board's
             current game state.

Inputs:
    - Board state (actual and visible boards, game state, timers, flags)
    - User interface assets (sprites, fonts, colors)

Outputs:
    - Graphical rendering of the game board
    - Display of buttons, timers, and game messages
    - Particle explosion animations on loss

External Sources:
    - Pygame library for rendering and animation
    - Assets (sprites, fonts) located in the sprites/ and fonts/ directories

Author: Team 17
Creation Date: 9/3/2025
"""


from board import *
import pygame
import button as ButtonClass
from constants import *
import math
from time import sleep as sleep


class Particle:
    """Represents a single particle for the explosion animation.

    Each particle has a position, velocity, color, and lifespan.
    Particles move outward from the explosion origin and fade
    over time until they disappear.

    Attributes:
        x (float): X-coordinate of the particle.
        y (float): Y-coordinate of the particle.
        radius (int): Particle size in pixels.
        color (tuple): RGB color of the particle.
        life (int): Frames remaining before the particle disappears.
        vel (list[float]): [x, y] velocity vector for movement.
    """
    def __init__(self, x, y):
        """Initialize a particle at a given position.
            Args:
                x (float): Starting x-coordinate.
                y (float): Starting y-coordinate.
        """
        self.x = x
        self.y = y
        self.radius = random.randint(3, 6)
        self.color = (255, 200, 50)
        self.life = 40
        self.vel = [random.uniform(-3, 3), random.uniform(-3, 3)]

    def update(self):
        """Update particle position, velocity, and fade color.
            Moves the particle according to its velocity and reduces
            its remaining life, adjusting its color for a fading effect.
        """
        self.x += self.vel[0]
        self.y += self.vel[1]
        self.life -= 1
        fade = max(self.life * 6, 0)
        r = min(255, fade)
        g = max(0, fade - 150)
        b = 0
        self.color = (r, g, b)

    def draw(self, screen):
        """Render the particle onto the given screen surface.

            Args:
                screen (pygame.Surface): The surface to draw the particle on.
        """
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


def explosion_animation(screen, x, y):
    """Play a particle explosion animation at given coordinates.
        Args:
            screen (pygame.Surface): Surface to render the explosion on.
            x (int): X-coordinate of explosion center.
            y (int): Y-coordinate of explosion center.
        Returns:
            None
    """
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
    """Engine for rendering Minesweeper UI and updating displays."""
    explosion_played = False
    agent_pos = [30, 30]

    def InitializeButtonList():
        """Initialize all interactive buttons for the game UI.
            Creates and positions all button objects used in the game,
            including:
                - Mine count selection (up/down arrows, start button)
                - Restart buttons for midgame, win screen, and lose screen
            Returns:
                None
        """
        # up arrow
        ButtonClass.ButtonList.append(ButtonClass.ButtonInfo(
            ButtonClass.ButtonTypes.MINE_SELECT_UP_ARROW,
            pygame.image.load("./sprites/start_screen/up_arrow.png").convert_alpha(),
            (3 / 4 * SCREEN_WIDTH, (SCREEN_HEIGHT * 1/2) - 100), GameState.START_SCREEN
        ))
        # down arrow
        ButtonClass.ButtonList.append(ButtonClass.ButtonInfo(
            ButtonClass.ButtonTypes.MINE_SELECT_DOWN_ARROW,
            pygame.image.load("./sprites/start_screen/down_arrow.png").convert_alpha(),
            (3 / 4 * SCREEN_WIDTH, (SCREEN_HEIGHT * 1/2) - 50), GameState.START_SCREEN
        ))
        # start button
        start_img = pygame.image.load("./sprites/start_screen/start_button.png").convert_alpha()
        start_img = pygame.transform.scale_by(start_img, 2)
        ButtonClass.ButtonList.append(ButtonClass.ButtonInfo(
            ButtonClass.ButtonTypes.MINE_SELECT_START, start_img,
            (1 / 2 * SCREEN_WIDTH, 5 / 6 * SCREEN_HEIGHT), GameState.START_SCREEN
        ))

        # lose screen restart
        restart_img = pygame.Surface((200, 40))
        restart_img.fill((200, 0, 0))
        small_font = pygame.font.Font(None, 36)
        label = small_font.render("RESTART", True, WHITE)
        restart_img.blit(label, (40, 10))
        ButtonClass.ButtonList.append(ButtonClass.ButtonInfo(
            ButtonClass.ButtonTypes.LOSE_RESTART_GAME,
            restart_img, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 275), GameState.LOSE_SCREEN
        ))

        # win screen restart
        win_restart_img = pygame.Surface((200, 40))
        win_restart_img.fill((0, 200, 0))
        small_font = pygame.font.Font(None, 36)
        win_label = small_font.render("RESTART", True, WHITE)
        win_restart_img.blit(win_label, (40, 10))
        ButtonClass.ButtonList.append(ButtonClass.ButtonInfo(
            ButtonClass.ButtonTypes.WIN_RESTART_GAME,
            win_restart_img, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 275), GameState.WIN_SCREEN
        ))

        # playing screen restart
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
            (75, 620), GameState.PLAYING
        ))
                
        # Game mode toggle button (on start screen)
        mode_button_img = pygame.Surface((150, 35))
        mode_button_img.fill((100, 150, 255))
        pygame.draw.rect(mode_button_img, (0, 0, 0), mode_button_img.get_rect(), 2)
        mode_font = pygame.font.SysFont(None, 20)
        mode_label = mode_font.render("Single Player", True, (0, 0, 0))
        mode_text_rect = mode_label.get_rect(center=(75, 17))
        mode_button_img.blit(mode_label, mode_text_rect)
        ButtonClass.ButtonList.append(ButtonClass.ButtonInfo(
            ButtonClass.ButtonTypes.GAME_MODE_TOGGLE,
            mode_button_img,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30), GameState.START_SCREEN
        ))
        
        # Initialize bot difficulty dropdown
        from constants import AgentDifficulty
        difficulty_options = [diff.value for diff in AgentDifficulty]
        ButtonClass.agent_difficulty_dropdown = ButtonClass.DropdownInfo(
            difficulty_options, 
            (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 50)
        )
        
        return
    

    def DisplayEndGameBoard(surface: pygame.display, board: Board):
        """Draw the entire board after game over, including headers.
            Args:
                surface (pygame.Surface): Surface to render the board onto.
                board (Board): Board instance containing actual/visible state.
            Returns:
                None
        """
        cell_size = CELL_SIZE
        font = pygame.font.SysFont(None, 24)
        grid_offset_x = GRID_OFFSET_X
        grid_offset_y = GRID_OFFSET_Y
        for r in range(board.board_size):
            for c in range(board.board_size):
                actual = board.actual_board[r][c]
                visible = board.visible_board[r][c]
                rect = pygame.Rect(grid_offset_x + c * cell_size, grid_offset_y + r * cell_size, cell_size, cell_size)
                if actual == BoardPiece.MINE:
                    if visible == BoardPiece.MINE:
                        surface.blit(mine_clicked_img, rect)
                    else:
                        surface.blit(mine_img, rect)
                else:
                    if visible == BoardPiece.FLAG:
                        surface.blit(mine_false_img, rect)
                    else:
                        surface.blit(empty_square, rect)
                        if actual.value > 0:
                            surface.blit(grid_imgs[actual.value], rect)
                pygame.draw.rect(surface, BLACK, rect, 1)
        # headers
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        for r in range(board.board_size):
            row_label = font.render(f"{r+1}", True, BLACK)
            surface.blit(row_label, (10, grid_offset_y + r * cell_size + cell_size // 3))
        for c in range(board.board_size):
            column_label = font.render(letters[c], True, BLACK)
            surface.blit(column_label, (grid_offset_x + c * cell_size + cell_size // 3, 10))

    def UpdateDisplay(surface: pygame.display, board: Board, time):
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
                UIEngine.DisplayWinScreen(surface, board, time)
            case GameState.LOSE_SCREEN:
                UIEngine.DisplayLoseScreen(surface, board, time)

        UIEngine.DisplayButtons(surface, board.state)
        return

    def DisplayStartScreen(surface: pygame.display, board: Board, time):
        """Render the start screen UI.
            Args:
                surface (pygame.Surface): Display surface to draw onto.
                board (Board): Game board for accessing mine count.
                time (int): Elapsed game time (not used on this screen).
            Returns:
                None
        """
        # fill with background color
        surface.fill(START_BG_COLOR)

        # draw border lines to make background look nicer
        line_width = 20
        # weird math with coordinates, i think lines are drawn with x being the pos of the left edge and y being the pos of the middle of the edge ???
        pygame.draw.line(surface, START_DARK_LINE_COLOR, (SCREEN_WIDTH - line_width // 2, 0),
                         (SCREEN_WIDTH - line_width // 2, SCREEN_HEIGHT), line_width)
        pygame.draw.line(surface, START_DARK_LINE_COLOR, (0, SCREEN_HEIGHT - line_width // 2),
                         (SCREEN_WIDTH, SCREEN_HEIGHT - line_width // 2), line_width)
        pygame.draw.line(surface, START_LIGHT_LINE_COLOR, (0, 0 + line_width // 2),
                         (SCREEN_WIDTH + line_width, 0 + line_width // 2), line_width)
        pygame.draw.line(surface, START_LIGHT_LINE_COLOR, (0 + line_width // 2, 0),
                         (0 + line_width // 2, SCREEN_HEIGHT + line_width), line_width)
        # # get bolded font
        header_font_path = "fonts/Handjet-Bold.ttf"
        header_size = 48
        header_font = pygame.font.Font(header_font_path, header_size)
        # get regular font
        reg_font_path = "fonts/Handjet-Regular.ttf"
        reg_font_size = 32
        reg_font = pygame.font.Font(reg_font_path, reg_font_size)
        UIEngine._DrawText(surface, "Choose how many mines: ", reg_font, BLACK, 70, 140)

        # draw minesweeper title on screen
        minesweeper_title = pygame.image.load("./sprites/start_screen/minesweeper_title.png").convert_alpha()
        minesweeper_title = pygame.transform.scale_by(minesweeper_title, .75)
        surface.blit(minesweeper_title, (60, 35))

        pygame.draw.rect(surface, START_LIGHT_LINE_COLOR, pygame.Rect(170, 210, 100, 75))

        num_of_mines = board.mines
        # placeholder to draw number of mines 
        UIEngine._DrawText(surface, str(num_of_mines), header_font, BLACK, 200, 220)
                
        # Update and render game mode components
        UIEngine.UpdateGameModeButton(board)
        UIEngine.RenderDropdown(surface, board)
        
        return

    def DisplayPlayingScreen(surface: pygame.display, board: Board,
                             time):
        '''
        Displays the playing screen for the minesweeper game. Creates the 10x10 board
        and within the board if a square is clicked on it checks the value of that square
        and decides what to do if its a mine, empty sqaure or if the user is placing a flag.
        Also displays the timer, playing status, and allows the user to restart the game if
        choose to
        Params: suface = the pygame display
                board = the board and all its information
                time = the aamount of time that has elapsed 
        '''
        UIEngine.explosion_played = False
        surface.fill(START_BG_COLOR)
        
        # Reset agent position if board hasn't been generated yet (new game)
        if not board.board_generated:
            UIEngine.agent_pos = [30, 30]

        # sets font size, big medium and normal
        font = pygame.font.SysFont("fonts/Handjet-Regular.ttf", 24)  # sets font to size 24
        mid_font = pygame.font.SysFont("fonts/Handjet-Regular.ttf", 40)  # sets font to size 40
        big_font = pygame.font.SysFont("fonts/Handjet-Regular.ttf", 56)  # sets font to size 56
        cell_size = CELL_SIZE

        # offset for row and column headers
        grid_offset_x = GRID_OFFSET_X
        grid_offset_y = GRID_OFFSET_Y

        # this commented code shows the minesweeper title instead of the playing status
        '''
        minesweeper_title = pygame.image.load("./sprites/start_screen/minesweeper_title.png").convert_alpha()
        minesweeper_title = pygame.transform.scale_by(minesweeper_title, .75)
        surface.blit(minesweeper_title, (x_AXIS, (board.board_size * cell_size + 10)))
        '''
        # displays the playing status - show different text for auto-solver
        from constants import GameMode
        if board.game_mode == GameMode.AUTO_SOLVER:
            title = big_font.render("Auto-Solving ...", True, (0, 150, 0))  # Green color for auto-solver
        else:
            title = big_font.render("Playing ...", True, BLACK)
        surface.blit(title, (x_AXIS, board.board_size * cell_size + TEXT_OFFSET_TITLE + grid_offset_y))

        # displays the time
        time_display = big_font.render(f"Time: {time}", True, BLACK)
        surface.blit(time_display, (x_AXIS, board.board_size * cell_size + TEXT_OFFSET_TIME + grid_offset_y))

        # displays the flags left
        mine_display = mid_font.render(f"Flags left: {board.flags}", True, BLACK)
        surface.blit(mine_display, (x_AXIS, board.board_size * cell_size + TEXT_OFFSET_FLAGS + grid_offset_y))

        # emoji
        emoji_rect = emoji_play.get_rect()
        emoji_rect.midleft = (EMOJI_X_OFFSET_PLAYING, board.board_size * cell_size + EMOJI_Y_OFFSET_PLAYING)
        surface.blit(emoji_play, emoji_rect)

        # creates the board by looping through each row and column within the board size
        for r in range(board.board_size):
            for c in range(board.board_size):
                visible_piece = board.visible_board[r][c]  # gets the current position of the visible board at r,c
                actual_piece = board.actual_board[r][c]  # gets the current position of the actual board at r,c
                # creates the cell and shift the grid by an offset
                rect = pygame.Rect(grid_offset_x + c * CELL_SIZE, grid_offset_y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if visible_piece == BoardPiece.FLAG:  # checks if visible piece is a flag
                    surface.blit(filled_square, rect)  # draws a flag
                    surface.blit(flag_img, rect)
                elif visible_piece != BoardPiece.UNKNOWN:  # checks if its been revealed
                    surface.blit(empty_square, rect)
                    # if its not a mine and it has a int assigned to it greater than 0 due to how many mines its touching
                    if actual_piece != BoardPiece.MINE and isinstance(actual_piece.value,
                                                                      int) and actual_piece.value > 0:
                        surface.blit(grid_imgs[actual_piece.value], rect)
                else:
                    # if its not revealed draw a blank square
                    surface.blit(filled_square, rect)

                pygame.draw.rect(surface, BLACK, rect, 1)  # creates cell boarder

        # creates labels
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        # left row headers
        for r in range(board.board_size):
            row_label = font.render(f"{r + 1}", True, BLACK)
            surface.blit(row_label, (10, grid_offset_y + r * cell_size + cell_size // 3))
        # top column headers
        for c in range(board.board_size):
            col_label = font.render(letters[c], True, BLACK)
            surface.blit(col_label, (grid_offset_x + c * cell_size + cell_size // 3, 10))
        if board.prev_click is not None:
            r, c = board.prev_click
            done = UIEngine.move_agent(
                 surface,
                 UIEngine.agent_pos[0], UIEngine.agent_pos[1],
                 r, c
            )
            if done:
                board.RevealSpace((r, c))
                board.prev_click = None  # back to sentinel after we finish the move
                UIEngine._DrawAgent(surface, UIEngine.agent_pos[0], UIEngine.agent_pos[1])
        else:
            UIEngine._DrawAgent(surface, UIEngine.agent_pos[0], UIEngine.agent_pos[1])



    def DisplayWinScreen(surface: pygame.display, board, time):
        """Render the win screen.
            Draws the final board with revealed state and displays a
            congratulatory message.
            Args:
                surface (pygame.Surface): Display surface to draw onto.
                board (Board): Completed board state.
                time (int): Final elapsed time in seconds.
            Returns:
                None
        """
        surface.fill(START_BG_COLOR)
        UIEngine.DisplayEndGameBoard(surface, board)
        WinFont = pygame.font.SysFont(None, 56)
        WinText = 'You WIN!'
        WinTextSurface = WinFont.render(WinText, False, GREEN)
        WinTextSize = WinFont.size(WinText)
        mid_font = pygame.font.SysFont(None, 40)
        time_display = mid_font.render(f"Time: {time} second(s)", True, BLACK)
        time_size = mid_font.size(f"Time: {time} second(s)")
        surface.blit(time_display, (SCREEN_WIDTH / 2 - time_size[0] / 2, SCREEN_HEIGHT / 2 + 200))
        surface.blit(WinTextSurface,
                     (SCREEN_WIDTH / 2 - WinTextSize[0] / 2, SCREEN_HEIGHT / 2 + 200 - WinTextSize[0] / 2))
        """ emoji_rect = emoji_win.get_rect()
        emoji_rect.midleft = (SCREEN_WIDTH - 60, SCREEN_HEIGHT - 40)
        surface.blit(emoji_win, emoji_rect) """
        return

    def DisplayLoseScreen(surface : pygame.display, board, time):
        """Render the lose screen.
            Plays explosion animation (once), draws final board with mines
            revealed, and shows defeat message.
            Args:
                surface (pygame.Surface): Display surface to draw onto.
                board (Board): Completed board state with loss.
                time (int): Final elapsed time in seconds.
            Returns:
                None
        """
        if not UIEngine.explosion_played:
            explosion_animation(surface, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            UIEngine.explosion_played = True

        surface.fill(START_BG_COLOR)
        font = pygame.font.Font(None, 56)
        UIEngine.DisplayEndGameBoard(surface, board);
        text = font.render("You Lose!", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2  + 150))
        mid_font = pygame.font.SysFont(None, 40)
        time_display = mid_font.render(f"Time: {time} second(s)", True, BLACK)
        time_size = mid_font.size(f"Time: {time} second(s)")
        surface.blit(time_display, (SCREEN_WIDTH/2 - time_size[0] / 2, SCREEN_HEIGHT/2  + 200))
        surface.blit(text, text_rect)
        emoji_rect = emoji_lose.get_rect()
        emoji_rect.midleft = (SCREEN_WIDTH - 60, SCREEN_HEIGHT - 40)
        surface.blit(emoji_lose, emoji_rect)
        return

    def DisplayButtons(surface: pygame.display, gameState: GameState):
        """Render buttons appropriate to the current game state.
            Args:
                surface (pygame.Surface): Display surface to draw buttons on.
                gameState (GameState): Current game state to determine which
                                        buttons should be active.
            Returns:
                None
            """
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
        surface.blit(img, (x, y))

    def _DrawAgent(surface: pygame.display, x: int, y: int):
        """
        Function that draws text to the screen
        Params:
            surface: surface to draw agent on
            x: x coordinate for agent to move to
            y: y coordinate for agent to move to
        """
        surface.blit(agent_img, (x, y))

    def get_pixel_coord(r, c):
        return (GRID_OFFSET_X + c * CELL_SIZE, GRID_OFFSET_Y + r * CELL_SIZE)
    
    def move_agent(surface: pygame.display, prev_r: int, prev_c: int, r: int, c: int):
        speed = 10 #wait time for each move
        prev_coords = [prev_r, prev_c]
        coords = list(UIEngine.get_pixel_coord(r, c))
        steps = max(abs(prev_coords[0]-coords[0]), abs(prev_coords[1]-coords[1]))

        #one step
        dx = coords[0] - prev_coords[0]
        dy = coords[1] - prev_coords[1]
        distance = math.sqrt(dx**2 + dy**2) // 1
        done = False

        if distance > 0:
            # Calculate normalized direction vector
            unit_dx = dx / distance
            unit_dy = dy / distance

            # Check if we will overshoot the target
            if speed >= distance:
                done = True
                prev_coords = coords
            else:
                prev_coords[0] += (unit_dx * speed)//1
                prev_coords[1] += (unit_dy * speed)//1
        else:
            done = True
            prev_coords = coords

        UIEngine._DrawAgent(surface, prev_coords[0], prev_coords[1])
        UIEngine.agent_pos = prev_coords
        print(done)
        print(prev_coords)
        return done

    def UpdateGameModeButton(board):
        """Update the game mode button text based on current game mode.
        
        Args:
            board (Board): Board instance containing game mode state.
        """
        # Find the game mode button
        for button in ButtonClass.ButtonList:
            if button.mButtonType == ButtonClass.ButtonTypes.GAME_MODE_TOGGLE:
                # Create new button image with updated text
                mode_button_img = pygame.Surface((150, 35))
                mode_button_img.fill((100, 150, 255))
                pygame.draw.rect(mode_button_img, (0, 0, 0), mode_button_img.get_rect(), 2)
                mode_font = pygame.font.SysFont(None, 20)
                mode_label = mode_font.render(board.game_mode.value, True, (0, 0, 0))
                mode_text_rect = mode_label.get_rect(center=(75, 17))
                mode_button_img.blit(mode_label, mode_text_rect)
                button.mImg = mode_button_img
                break
    
    def RenderDropdown(surface, board):
        """Render the bot difficulty dropdown when appropriate.
        
        Args:
            surface (pygame.Surface): Surface to render on.
            board (Board): Board instance containing game mode state.
        """
        from constants import GameMode
        
        # Only show dropdown for multiplayer and auto solver modes
        if board.game_mode in [GameMode.MULTIPLAYER, GameMode.AUTO_SOLVER]:
            dropdown = ButtonClass.agent_difficulty_dropdown
            if dropdown is not None:
                # Render main dropdown button
                button_color = (200, 200, 200) if not dropdown.is_open else (180, 180, 180)
                pygame.draw.rect(surface, button_color, dropdown.main_rect)
                pygame.draw.rect(surface, (0, 0, 0), dropdown.main_rect, 2)
                
                # Render selected option text
                font = pygame.font.SysFont(None, 20)
                text = font.render(dropdown.selected_option, True, (0, 0, 0))
                text_rect = text.get_rect(center=dropdown.main_rect.center)
                surface.blit(text, text_rect)
                
                # Render dropdown arrow
                # arrow_points = [
                #     (dropdown.main_rect.right - 15, dropdown.main_rect.centery - 3),
                #     (dropdown.main_rect.right - 8, dropdown.main_rect.centery + 3),
                #     (dropdown.main_rect.right - 22, dropdown.main_rect.centery + 3)
                # ]
                # pygame.draw.polygon(surface, (0, 0, 0), arrow_points)
                
                # Render dropdown options if open
                if dropdown.is_open:
                    for i, (option, rect) in enumerate(zip(dropdown.options, dropdown.option_rects)):
                        option_color = (220, 220, 220)
                        pygame.draw.rect(surface, option_color, rect)
                        pygame.draw.rect(surface, (0, 0, 0), rect, 1)
                        
                        option_text = font.render(option, True, (0, 0, 0))
                        option_text_rect = option_text.get_rect(center=rect.center)
                        surface.blit(option_text, option_text_rect)