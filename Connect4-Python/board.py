import pygame
import numpy as np
from winning_patterns import WinningPatterns
from scipy.signal import convolve

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

    def __copy__(self):
        return Board(self.rows, self.cols, self.depth, self._board.copy())

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

    #todo it seems that we doesn't use the following function:
    # def drop_piece(self, location, player):
    #     col, depth = location
    #     row = self.get_next_open_row((col, depth))
    #     self._board[row][col][depth] = player

    def is_valid_location(self, location):
        col, depth = location
        return self._board[self.rows - 1][col][depth] == self.EMPTY_CELL

    def generate_successor(self, player, location):
        successor = self.__copy__()
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

    def winning_move(self, current_player_index, disc_location, winning_streak):
        # Convolve the board with each kernel and check if any result contains self.winning_streak
        x, y, z = disc_location
        slicing = (
            slice(max(x - (winning_streak - 1), 0), min(x + winning_streak, self.rows)),
            slice(max(y - (winning_streak - 1), 0), min(y + winning_streak, self.cols)),
            slice(max(z - (winning_streak - 1), 0), min(z + winning_streak, self.depth))
        )
        board = self.board[slicing]
        for kernel in WinningPatterns.PATTERNS:
            if self.depth == 1 and kernel.shape[2] > 1:
                continue
            convolved = convolve((board == current_player_index).astype(int), kernel, mode='valid')
            if np.any(convolved == winning_streak):
                return True
        return False