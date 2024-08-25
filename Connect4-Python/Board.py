import pygame
import numpy as np
from Constants import Constants

class Board:
    def __init__(self, rows, cols, depth=1, board=None):
        self.rows = rows
        self.cols = cols
        self.depth = depth
        if board is None:
            self._board = np.zeros((self.rows, self.cols, self.depth))
        else:
            self._board = board

    @property
    def board(self):
        return self._board

    def get_legal_actions(self):
        return np.argwhere(self.board[self.rows - 1, :, :] == 0)

    def apply_action(self, location, player):
        col, depth = location
        assert self._board[self.rows - 1, col, depth] == 0
        row = self.get_next_open_row(location)
        self._board[row][col][depth] = player
        return row, col, depth

    def drop_piece(self, location, player):
        col, depth = location
        row = self.get_next_open_row(col, depth)
        self._board[row][col][depth] = player

    def is_valid_location(self, location):
        col, depth = location
        return self._board[self.rows - 1][col][depth] == 0

    def generate_successor(self, player, location):
        successor = Board(rows=self.rows, cols=self.cols, depth=self.depth, board=self._board.copy())
        successor.apply_action(location, player)
        return successor

    def get_next_open_row(self, location):
        col, depth = location
        for r in range(self.rows):
            if self._board[r][col][depth] == 0:
                return r

    def __str__(self):
        return str(np.flip(self._board.squeeze(), 0))

    def draw(self, screen):
        print(self)
        assert self.depth == 1
        for c in range(self.cols):
            for r in range(self.rows):
                pygame.draw.rect(screen, Constants.BLUE, (c * Constants.SQUARESIZE, r * Constants.SQUARESIZE + Constants.SQUARESIZE, Constants.SQUARESIZE, Constants.SQUARESIZE))
                pygame.draw.circle(screen, Constants.BLACK, (int(c * Constants.SQUARESIZE + Constants.SQUARESIZE / 2), int(r * Constants.SQUARESIZE + Constants.SQUARESIZE + Constants.SQUARESIZE / 2)), Constants.RADIUS)

        for c in range(self.cols):
            for r in range(self.rows):
                if self._board[r][c][0] == 0:
                    continue
                pygame.draw.circle(screen, Constants.PLAYER_COLORS[int(self._board[r][c][0])], (int(c * Constants.SQUARESIZE + Constants.SQUARESIZE / 2), Constants.height - int(r * Constants.SQUARESIZE + Constants.SQUARESIZE / 2)), Constants.RADIUS)
        pygame.display.update()