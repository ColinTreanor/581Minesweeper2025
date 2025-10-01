"""
ai_solver.py
------------
AI Solver module for Minesweeper (Project 2: EECS 581).

This file implements automated players that interact with the Board.
Includes:
    - Easy AI: Randomly uncovers a cell (may hit a mine).
    - Hard AI: Cheats by always picking a safe non-mine cell.

Classes:
    AISolver: Provides Easy and Hard AI solvers.
"""

import random
from board import Board, BoardPiece


class AISolver:
    """Minesweeper AI Solver class."""

    def __init__(self, board: Board):
        self.board = board

    def move_easy(self):
        """Easy AI: Picks a random covered/unflagged cell (may hit a mine)."""
        candidates = []
        for r in range(self.board.board_size):
            for c in range(self.board.board_size):
                if self.board.visible_board[r][c] == BoardPiece.UNKNOWN:
                    candidates.append((r, c))

        if not candidates:
            return None

        r, c = random.choice(candidates)
        self.board.RevealSpace((r, c))
        return (r, c)

    def move_hard(self):
        """Hard AI: Always picks a safe non-mine covered cell."""
        candidates = []
        for r in range(self.board.board_size):
            for c in range(self.board.board_size):
                if (self.board.visible_board[r][c] == BoardPiece.UNKNOWN
                        and self.board.actual_board[r][c] != BoardPiece.MINE):
                    candidates.append((r, c))

        if not candidates:
            return None

        r, c = random.choice(candidates)
        self.board.RevealSpace((r, c))
        return (r, c)
