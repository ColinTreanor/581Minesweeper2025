"""
Minesweeper Event Handling Module

Module Name: event_handler.py
Description: Handles user input and translates events into game actions.
             Processes mouse clicks, button presses, and quit events.
             Communicates between Pygame's event system and the Board's
             game logic.

Inputs:
    - Pygame events (mouse clicks, quit)
    - Current Board instance (state, mine/flag counts, etc.)

Outputs:
    - Updates to Board state (revealing spaces, placing flags, resetting)
    - Updates to mine/flag counts when adjusting game difficulty
    - State transitions (start → playing, playing → win/lose, etc.)

External Sources:
    - Pygame event system for capturing user input
    - Python sys library for application termination

Author: Team 17
Creation Date: 9/3/2025
"""
import pygame, sys
from pygame.locals import *
from board import *
import button as ButtonClass
from constants import CELL_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, MAX_MINES, MIN_MINES
from time import sleep as sleep
import agents

#TODO add way to select agent difficulty
#TODO add way to select if playing vs agent or auto-solve

class EventHandler:
    """Handles Pygame events and dispatches game actions."""
    # Thinking no member variables, just member functions to implement functionality

    def HandleEvent(event: pygame.event, game: Board):
        """Process a single Pygame event and apply changes to the game state.
            Responsibilities:
                - Handle quit events and terminate the program
                - Handle mouse clicks for:
                    * Interacting with on-screen buttons
                    * Revealing spaces on the board
                    * Placing/removing flags on the board
                - Enforce board offsets so clicks align with the grid
                - Update mine counts through arrow buttons on the start screen
                - Transition game state from start → playing when beginning a game
            Args:
                event (pygame.event.Event): A Pygame event to process (mouse, quit, etc.)
                game (Board): The current game board instance whose state may be updated.
            Returns:
                None
        """
        '''
        will do one of the following:
            - close the game
            - tell BoardEngine to return to StartScreen
            - tell BoardEngine to make new game with certain mines
            - tell BoardEngine to register click if it is users turn (use bool to keep track of that)
        probably using a switch statement
        '''
        if event.type == MOUSEBUTTONDOWN:
            # put in event handler
            leftMousePressed = pygame.mouse.get_pressed()[0]
            rightMousePressed = pygame.mouse.get_pressed()[2]
            position = pygame.mouse.get_pos()

            if (leftMousePressed):
                for button in ButtonClass.ButtonList:
                    if (button.mRect.collidepoint(position) and button.mOnState == game.state):
                        # TODO: implement other button functionality
                        # print(f"Button Type: {button.mButtonType}")
                        match button.mButtonType:
                            case ButtonClass.ButtonTypes.WIN_RESTART_GAME | ButtonClass.ButtonTypes.LOSE_RESTART_GAME | ButtonClass.ButtonTypes.MIDGAME_RESTART_GAME:
                                game.ResetBoard()
                                #game.move_agent((0,0)) #reset agent position
                            case ButtonClass.ButtonTypes.MINE_SELECT_UP_ARROW:
                                # only update mines if it is less than max mines value
                                if game.mines < MAX_MINES:
                                    game.IncrementMines()
                            case ButtonClass.ButtonTypes.MINE_SELECT_DOWN_ARROW:
                                # only update mines if there are more than min mines value
                                if game.mines > MIN_MINES:
                                    game.DecrementMines()
                            case ButtonClass.ButtonTypes.MINE_SELECT_START:
                                game.state = GameState.PLAYING 
                                game.active_agent = True #COMMENT OUT IF YOU WANT TO PLAY WITHOUT AGENT
                        break

                if ( game.state == GameState.PLAYING and game.active_agent):
                    x, y = pygame.mouse.get_pos()
                    gx = x - GRID_OFFSET_X  # Adjust board for x offset
                    gy = y - GRID_OFFSET_Y  # Adjust board for y offset
                    # Only process clicks from inside the grid
                    if 0 <= gx < game.board_size * CELL_SIZE and 0 <= gy < game.board_size * CELL_SIZE:
                        c = gx // CELL_SIZE
                        r = gy // CELL_SIZE
                        space_revealed = game.RevealSpace((r, c))
                        if space_revealed:
                            agent_move = agents.Agent(2).run_agent(game)
                            if agent_move:  # Check if agent found a valid move
                                x_agent, y_agent = agent_move
                                game.move_agent((x_agent, y_agent))
                                game.RevealSpace((x_agent, y_agent))


                if (game.state == GameState.PLAYING):
                    x, y = pygame.mouse.get_pos()
                    gx = x - GRID_OFFSET_X  # Adjust board for x offset
                    gy = y - GRID_OFFSET_Y  # Adjust board for y offset
                    # Only process clicks from inside the grid
                    if 0 <= gx < game.board_size * CELL_SIZE and 0 <= gy < game.board_size * CELL_SIZE:
                        c = gx // CELL_SIZE
                        r = gy // CELL_SIZE
                        game.RevealSpace((r, c))

            elif (rightMousePressed): # Same logic for reveal space upon left click to adjust for offset
                if (game.state == GameState.PLAYING):
                    x, y = pygame.mouse.get_pos()
                    gx = x - GRID_OFFSET_X
                    gy = y - GRID_OFFSET_Y
                    if 0 <= gx < game.board_size * CELL_SIZE and 0 <= gy < game.board_size * CELL_SIZE:
                        c = gx // CELL_SIZE
                        r = gy // CELL_SIZE
                        game.PlaceFlag((r, c))

        if event.type == QUIT:
            # end pygame
            pygame.quit()
            # end python script
            sys.exit()
        return
