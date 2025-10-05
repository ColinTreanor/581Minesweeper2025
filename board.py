"""
Minesweeper Game Board Module

Module Name: board.py
Description: Core game logic for Minesweeper including board generation, game state management,
            and player interactions. Handles mine placement, space revelation, flag placement,
            and win/lose conditions.

Inputs: 
    - Player coordinates for space revelation and flag placement
    - Mine count configuration
    - Board size parameters

Outputs:
    - Game board states (visible and actual)
    - Game state transitions (playing, win, lose)
    - Timer functionality for game duration

External Sources: 
    - implementation based on classic Minesweeper game rules
    - Pygame library used for timing functionality
    - Python enum module for type safety

Author: Benjamin Stonestreet
Creation Date: 9/10/2025
"""

from enum import Enum  # Python standard library for enumeration types
import random  # Python standard library for random number generation
from constants import MAX_MINES, MIN_MINES, GameMode, AgentDifficulty  # Local constants module for mine limits
from pygame import time  # Pygame library for game timing functionality
import pygame

# Initialize pygame sound effects 
pygame.mixer.init()
ding = pygame.mixer.Sound("./soundfiles/ding.mp3") 
swoosh = pygame.mixer.Sound("./soundfiles/swoosh.mp3")
swooshReverse = pygame.mixer.Sound("./soundfiles/swooshreverse.mp3")
explosion= pygame.mixer.Sound("./soundfiles/explosion.mp3")
winner=pygame.mixer.Sound("./soundfiles/winner.mp3")
welcome=pygame.mixer.Sound("./soundfiles/gamestart.mp3")
menuSound=pygame.mixer.Sound("./soundfiles/menuselect.mp3")

class BoardPiece(Enum):
    """Enumeration class to represent different types of board spaces
    
    Used to maintain type safety and clear representation of board states.
    Includes both display states (MINE, FLAG, UNKNOWN) and numerical mine counts (0-8).
    """
    MINE = 'M' # Mine indicator for dangerous spaces
    FLAG = 'F' # Flag marker placed by player to indicate suspected mine
    UNKNOWN = 'U' # Unknown/unrevealed space that player hasn't clicked yet

    # Numerical values representing count of adjacent mines
    ZERO = 0      # No adjacent mines - safe space
    ONE = 1       # One adjacent mine
    TWO = 2       # Two adjacent mines
    THREE = 3     # Three adjacent mines
    FOUR = 4      # Four adjacent mines
    FIVE = 5      # Five adjacent mines
    SIX = 6       # Six adjacent mines
    SEVEN = 7     # Seven adjacent mines
    EIGHT = 8     # Eight adjacent mines (maximum possible)

    def __sub__(self, other):
        if isinstance(other, (BoardPiece, int)):
            return self.value - (other.value if isinstance(other, BoardPiece) else other)
        return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, BoardPiece):
            return self.value == other.value
        elif isinstance(other, (int, str)):
            return self.value == other
        return NotImplemented
    
    def increment(self):
        """Increments the numerical value of non-mine spaces
        
        Used during board generation to count adjacent mines for each space.
        Only increments integer values up to maximum of 8.
        
        Returns:
            BoardPiece: Incremented value or self if at maximum or is a mine
        """
        # Check if current value is an integer and can be incremented
        if isinstance(self.value, int) and self.value < 8:
            next_value = self.value + 1  # Increment by 1
            return BoardPiece(next_value)  # Return new BoardPiece with incremented value
        
        # Return unchanged if at maximum value or is a mine
        return self


class GameState(Enum):
    """Enumeration class to represent different game states
    
    Tracks the current phase of the game to control UI display and game logic.
    Ensures proper state transitions and prevents invalid operations.
    """
    START_SCREEN = 1  # Initial state before first move
    PLAYING = 2       # Active gameplay state  
    WIN_SCREEN = 3    # Victory state when all non-mine spaces revealed
    LOSE_SCREEN = 4   # Defeat state when mine is clicked


class Board:
    #will store mines, state, board list(s) and size
    board_size: int = 10

    def __init__(self):
        self.ResetBoard() # set board to default values
        self.prev_click = None

    def ResetBoard(self):
        # sets b
        self.mines: int = 10
        self.flags: int = 10
        self.state: GameState = GameState.START_SCREEN
        self.active_agent: bool = False
        self.StartTime = 0
        self.board_generated: bool = False
        self.visible_board: list = [[BoardPiece.UNKNOWN for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.actual_board: list = [[BoardPiece.ZERO for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.auto_solve_timer: int = 0  # Timer for auto-solve mode delays 
        self.auto_solve_delay: int = 1 
        self.prev_click = None
        # Game mode settings
        self.game_mode: GameMode = GameMode.SINGLE_PLAYER
        self.agent_difficulty: AgentDifficulty = AgentDifficulty.EASY
        self.ai_turn = False
        
        # Reset the UI dropdown to match the reset difficulty
        import button as ButtonClass
        if ButtonClass.agent_difficulty_dropdown is not None:
            ButtonClass.agent_difficulty_dropdown.selected_option = AgentDifficulty.EASY.value
        
        # Reset agent position in UI
        import UI_engine
        UI_engine.UIEngine.agent_pos = [30, 30]
        UI_engine.UIEngine.explosion_played = False

    def CalculateDuration(self):
        if not self.board_generated:
            return 0
        elif self.state == GameState.PLAYING:
            return (time.get_ticks() - self.StartTime) // 1000
        else:
            return self.StartTime // 1000 #used to store game time after win
            

    def GenerateBoard(self, startIdx: tuple):
        """Generate the actual board with mines and numbers
        
        Creates mine layout ensuring the starting position is safe.
        Places mines randomly then calculates adjacent mine counts for all spaces.
        
        Args:
            startIdx (tuple): (row, col) coordinates of player's first click
        """
        # Change game state to active playing
        self.state = GameState.PLAYING
        # Mark board as generated to enable timer
        self.board_generated = True
        
        # Generate board based on player's first click (ensure first click is safe)
        mines_placed: int = 0
        # Continue until all mines are placed
        while(mines_placed < self.mines):
            # Generate random coordinates for mine placement
            rand_x = random.randint(0, self.board_size - 1)
            rand_y = random.randint(0, self.board_size - 1)
            # Only place mine if not on starting position and space is empty
            if (startIdx != (rand_x, rand_y) and self.actual_board[rand_x][rand_y] != BoardPiece.MINE):
                # Place mine at random location
                self.actual_board[rand_x][rand_y] = BoardPiece.MINE
                mines_placed += 1 
            
                # Update adjacent spaces' mine counts
                # Iterate through 3x3 grid around the mine
                for x in range(max(0, rand_x - 1), min(rand_x + 2, self.board_size)):
                    for y in range(max(0, rand_y - 1), min(rand_y + 2, self.board_size)):
                        # Increment count for non-mine spaces
                        if(self.actual_board[x][y] != BoardPiece.MINE):
                            self.actual_board[x][y] = self.actual_board[x][y].increment()
                        

    def GetValue(self, spaceIdx: tuple):
        """Get the actual value at a specific board position
        
        Args:
            spaceIdx (tuple): (row, col) coordinates to check
            
        Returns:
            BoardPiece: The actual piece at the specified location
        """
        return self.actual_board[spaceIdx[0]][spaceIdx[1]]

    def PrintActualBoard(self):
        """Print the actual board state for debugging purposes
        
        Displays all mines and numbers in their true positions.
        Used for development and testing - not shown to players.
        """
        # Iterate through each row
        for x in range(self.board_size):
            # Iterate through each column in the row
            for y in range(self.board_size):
                # Print 'M' for mines
                if(self.actual_board[x][y] == BoardPiece.MINE):
                    print('M', end =' ')
                    continue
                # Print numerical value for non-mine spaces
                print(self.actual_board[x][y].value, end=' ')
            print()  # New line after each row

    def PrintVisibleBoard(self):
        """Print the board as seen by the player
        
        Shows only revealed spaces, flags, and unknown areas.
        Used for debugging the player's view of the game state.
        """
        # Iterate through each row
        for x in range(self.board_size):
            # Iterate through each column in the row
            for y in range(self.board_size):
                # Print 'U' for unrevealed spaces
                if(self.visible_board[x][y] == BoardPiece.UNKNOWN):
                    print('U', end = ' ')
                    continue
                # Print 'F' for flagged spaces
                if(self.visible_board[x][y] == BoardPiece.FLAG):
                    print('F', end = ' ')
                    continue
                # Print actual value for revealed spaces
                else: 
                    # Handle both BoardPiece enum values and direct integer values
                    if hasattr(self.visible_board[x][y], 'value'):
                        print(self.visible_board[x][y].value, end = ' ')
                    else:
                        print(self.visible_board[x][y], end = ' ')

            print()  # New line after each row

    def PlaceFlag(self, spaceIdx: tuple):
        """Toggle flag placement at specified coordinates
        
        Allows player to mark suspected mine locations with flags.
        Removes flag if already present, places flag if space is unknown.
        Updates available flag count accordingly.
        
        Args:
            spaceIdx (tuple): (row, col) coordinates to flag/unflag
        """
        r, c = spaceIdx  # Extract row and column from tuple
        # If space is already flagged, remove the flag
        if self.visible_board[r][c] == BoardPiece.FLAG:
            self.visible_board[r][c] = BoardPiece.UNKNOWN  # Return to unknown state
            self.flags += 1  # Increment available flags
            swooshReverse.play() # Sound effect for removing a flag
        # If space is unknown, place a flag
        elif self.visible_board[r][c] == BoardPiece.UNKNOWN:
            self.visible_board[r][c] = BoardPiece.FLAG  # Mark with flag
            self.flags -= 1  # Decrement available flags
            swoosh.play() # Sound effect for placing a flag 

    def RevealSpace(self, spaceIdx: tuple):
        """Reveal a space on the board and handle game logic
        
        Core game method that handles player clicks. Generates board on first move,
        reveals spaces, handles mine explosions, auto-reveals adjacent empty spaces,
        and checks for win conditions.
        
        Args:
            spaceIdx (tuple): (row, col) coordinates to reveal
            
        Returns:
            bool: True if space was successfully revealed, False if already revealed/flagged or invalid coordinates
        """
        r, c = spaceIdx  # Extract row and column coordinates

        # Validate coordinates are within board bounds
        if not (0 <= r < self.board_size and 0 <= c < self.board_size):
            return False  # Return False if coordinates are invalid

        # Get the actual content at the specified location
        revealedSpace = self.actual_board[r][c]
        # Generate board on first move to ensure starting position is safe
        if(not self.board_generated):
            self.GenerateBoard(spaceIdx)  # Create mine layout avoiding starting position
            self.StartTime = time.get_ticks()  # Start game timer

        # Re-get the space value after potential board generation
        revealedSpace = self.actual_board[spaceIdx[0]][spaceIdx[1]]

        # Only reveal unknown spaces (ignore already revealed or flagged spaces)
        if(self.visible_board[spaceIdx[0]][spaceIdx[1]] != BoardPiece.UNKNOWN):
            return False  # Return False if space is already revealed or flagged

        # Handle different types of revealed spaces
        match revealedSpace:
            
            case BoardPiece.MINE:
                # Player hit a mine - game over
                self.visible_board[spaceIdx[0]][spaceIdx[1]] = BoardPiece.MINE  # Show the mine
                self.StartTime = time.get_ticks() - self.StartTime  # Calculate final game time
                if self.game_mode == GameMode.SINGLE_PLAYER or self.game_mode == GameMode.AUTO_SOLVER:
                    self.state = GameState.LOSE_SCREEN  # Set game state to loss
                    explosion.play() # sound when user clicks on a bomb tile
                else:
                    if self.ai_turn:
                        self.state = GameState.WIN_SCREEN
                    else:
                        self.state = GameState.LOSE_SCREEN
                        explosion.play() # sound when user clicks on a bomb tile
                return True  # Return True indicating successful reveal (even though it's a mine)
                
            case BoardPiece.ZERO:
                # Empty space with no adjacent mines - auto-reveal surrounding area
                self.visible_board[spaceIdx[0]][spaceIdx[1]] = 0  # Show as empty space
                #safe tile 
                ding.play() # plays when clicking on a safe tile (blank)

                # Recursively reveal all adjacent spaces (flood fill algorithm)
                for x in range(max(0, spaceIdx[0] - 1), min(spaceIdx[0] + 2, self.board_size)):
                    for y in range(max(0, spaceIdx[1] - 1), min(spaceIdx[1] + 2, self.board_size)):
                        self.RevealSpace((x, y))  # Recursive call for each adjacent space

                # Check if revealing this area completed the game
                if(self.CheckWin()):
                    if self.game_mode == GameMode.SINGLE_PLAYER or self.game_mode == GameMode.AUTO_SOLVER:
                        self.state = GameState.WIN_SCREEN  # Set game state to victory
                    else:
                        if self.ai_turn:
                            self.state = GameState.LOSE_SCREEN
                        else:
                            self.state = GameState.WIN_SCREEN
                    self.StartTime = time.get_ticks() - self.StartTime  # Calculate final game time
                    winner.play() # this plays with the "you win" message 
                    return True  # Return True indicating successful reveal
                return True  # Return True indicating successful reveal

            case _:  # Default case - numbered space (1-8 adjacent mines)
                # Reveal the number of adjacent mines
                self.visible_board[spaceIdx[0]][spaceIdx[1]] = revealedSpace

                # Check if this revelation completed the game
                if(self.CheckWin()):
                    if self.game_mode == GameMode.SINGLE_PLAYER or self.game_mode == GameMode.AUTO_SOLVER:
                        self.state = GameState.WIN_SCREEN  # Set game state to victory
                    else:
                        if self.ai_turn:
                            self.state = GameState.LOSE_SCREEN
                        else:
                            self.state = GameState.WIN_SCREEN
                    self.StartTime = time.get_ticks() - self.StartTime  # Calculate final game time
                    winner.play() # plays when user wins the games
                    return True  # Return True indicating successful reveal
                ding.play() # Sound effect for selecting safe tile / number tile 
                return True  # Return True indicating successful reveal


    def ReturnVisableBoard(self):
        """Return the current visible board state
        
        Returns:
            list: 2D array representing what the player can currently see
        """
        return self.visible_board

    def SetMines(self, mines: int):
        """Set the number of mines for the game
        
        Updates both mine count and available flag count to match.
        
        Args:
            mines (int): Number of mines to place on the board
        """
        self.mines = mines    # Set mine count
        self.flags = mines    # Set flag count to match mine count

    def IncrementMines(self):
        """Increase mine and flag count by 1
        
        Used for difficulty adjustment during game setup.
        """
        self.mines += 1  # Increment mine count
        self.flags += 1  # Increment available flags to match

    def DecrementMines(self):
        """Decrease mine and flag count by 1
        
        Used for difficulty adjustment during game setup.
        """
        self.mines -= 1  # Decrement mine count
        self.flags -= 1  # Decrement available flags to match

    def CheckWin(self):
        """Check if player has won the game
        
        Victory condition: All non-mine spaces must be revealed.
        Flags on mines don't affect win condition - only revelation matters.
        
        Returns:
            bool: True if player has won, False otherwise
        """
        # Check every space on the board
        for x in range(0, self.board_size):
            for y in range(0, self.board_size):
                # If any non-mine space is still unknown or flagged, game continues
                if(self.actual_board[x][y] != BoardPiece.MINE and 
                   (self.visible_board[x][y] == BoardPiece.UNKNOWN or 
                    self.visible_board[x][y] == BoardPiece.FLAG)):
                    return False  # Win condition not met
                
        return True  # All non-mine spaces revealed - player wins!
    
    def move_agent(self, rc):
        r, c = rc
        self.prev_click = [r, c]

    # def UpdateAutoSolve(self): 
    #     """Handle auto-solve mode AI moves with timing. 
         
    #     Returns: 
    #         bool: True if an AI move was made, False otherwise 
    #     """         
    #     if (self.state == GameState.PLAYING and  
    #         self.active_agent and  
    #         self.game_mode == GameMode.AUTO_SOLVER): 
    #         print("Auto-solve mode active")
    #         current_time = time.get_ticks() 
    #         if current_time - self.auto_solve_timer >= self.auto_solve_delay: 
    #             # Import here to avoid circular import 
    #             import agents 

    #             agent_move = agents.Agent(self.agent_difficulty).run_agent(self)
    #             if agent_move:  # Check if agent found a valid move
    #                 x_agent, y_agent = agent_move
    #                 self.move_agent((x_agent, y_agent)) 
    #                 self.auto_solve_timer = current_time 
    #                 return True 
    #     return False