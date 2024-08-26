import pygame
import numpy as np

class Board:
    EMPTY_CELL = -1
    def __init__(self, rows, cols, depth=1, board=None):
        if board is None:
            self._board = np.ones((rows, cols, depth)) * self.EMPTY_CELL
            self.rows = rows
            self.cols = cols
            self.depth = depth
        else:
            self._board = board
            self.rows, self.cols, self.depth = board.shape

    @property
    def board(self):
        return self._board

    def get_legal_actions(self):
        return np.argwhere(self.board[self.rows - 1, :, :] == self.EMPTY_CELL).tolist()

    def apply_action(self, location, player):
        col, depth = location
        assert self._board[self.rows - 1, col, depth] == self.EMPTY_CELL
        row = self.get_next_open_row(location)
        self._board[row][col][depth] = player
        return row, col, depth

    def drop_piece(self, location, player):
        col, depth = location
        row = self.get_next_open_row(col, depth)
        self._board[row][col][depth] = player

    def is_valid_location(self, location):
        col, depth = location
        return self._board[self.rows - 1][col][depth] == self.EMPTY_CELL

    def generate_successor(self, player, location):
        successor = Board(rows=self.rows, cols=self.cols, depth=self.depth, board=self._board.copy())
        successor.apply_action(location, player)
        return successor

    def get_next_open_row(self, location):
        col, depth = location
        for r in range(self.rows):
            if self._board[r][col][depth] == self.EMPTY_CELL:
                return r

    def __repr__(self):
        empty_char = str(self.EMPTY_CELL)
        return str(np.flip(self._board.squeeze(), 0)).replace('.', '.,').replace(']', '],')