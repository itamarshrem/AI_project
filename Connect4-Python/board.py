import numpy as np
from winning_patterns import WinningPatterns
from scipy.signal import convolve

class Board:
    EMPTY_CELL = -1
    def __init__(self, rows, cols, depth=1, num_of_players=2, board=None, build_conv_res_by_direction=True):
        if board is None:
            self._board = np.ones((rows, cols, depth)) * self.EMPTY_CELL
            self.rows = rows
            self.cols = cols
            self.depth = depth
        else:
            self._board = board
            self.rows, self.cols, self.depth = board.shape
        self.last_disc_location = None
        self.num_of_players = num_of_players
        self.conv_res_by_direction = {}
        if build_conv_res_by_direction:
            self._build_conv_res_by_direction()

    def _build_conv_res_by_direction(self):
        self.conv_res_by_direction = {}
        for direction, res_shape in WinningPatterns.CONV_RES_SHAPES.items():
            rows, cols, depth = res_shape
            self.conv_res_by_direction[direction] = np.zeros((self.num_of_players, rows, cols, depth))

    def __copy__(self):
        b = Board(self.rows, self.cols, self.depth, self.num_of_players, self._board.copy(), False)
        # b.conv_res_by_direction = self.conv_res_by_direction
        # deep copy the conv_res_by_direction
        b.conv_res_by_direction = {k: v.copy() for k, v in self.conv_res_by_direction.items()}
        return b

    @property
    def board(self):
        return self._board

    def get_legal_actions(self, winning_streak):
        if self.have_we_won(winning_streak):
            return []
        return np.argwhere(self.board[self.rows - 1, :, :] == self.EMPTY_CELL).tolist()

    def is_board_full(self):
        return np.all(self.board != self.EMPTY_CELL)

    def apply_action(self, location, player, winning_streak):
        col, depth = location
        assert self._board[self.rows - 1, col, depth] == self.EMPTY_CELL
        row = self.get_next_open_row(location)
        self._board[row, col, depth] = player
        self.last_disc_location = (row, col, depth)
        self._apply_action_on_conv_res((row, col, depth), player, winning_streak)

    def _apply_action_on_conv_res(self, location, player, winning_streak):
        indices_dict = WinningPatterns.build_needed_indices(winning_streak, location)
        for direction, indices in indices_dict.items():
            res = self.conv_res_by_direction[direction]
            # res[player, indices[0, :], indices[1, :], indices[2, :]] += 1
            np.add.at(res[player], (indices[0, :], indices[1, :], indices[2, :]), 1)

    def is_valid_location(self, location):
        col, depth = location
        return self._board[self.rows - 1][col][depth] == self.EMPTY_CELL

    def generate_successor(self, player, location, winning_streak):
        successor = self.__copy__()
        successor.apply_action(location, player, winning_streak)
        return successor

    def get_next_open_row(self, location):
        col, depth = location
        return np.argmax(self._board[:, col, depth] == self.EMPTY_CELL)

    def __repr__(self):
        empty_char = str(self.EMPTY_CELL)
        return str(np.flip(self._board.squeeze(), 0)).replace('.', '.,').replace(']', '],')

    def have_we_won(self, winning_streak):
        if self.last_disc_location is None:
            return False

        x, y, z = self.last_disc_location
        current_player_index = self.board[x, y, z]
        for direction, conv_res in self.conv_res_by_direction.items():
            if np.any(conv_res[int(current_player_index), :, :, :] == winning_streak):
                return True
        return False

    # def have_we_won(self, winning_streak):
    #     if self.last_disc_location is None:
    #         return False
    #     # Convolve the board with each kernel and check if any result contains self.winning_streak
    #     x, y, z = self.last_disc_location
    #     current_player_index = self.board[x, y, z]
    #     slicing = (
    #         slice(max(x - (winning_streak - 1), 0), min(x + winning_streak, self.rows)),
    #         slice(max(y - (winning_streak - 1), 0), min(y + winning_streak, self.cols)),
    #         slice(max(z - (winning_streak - 1), 0), min(z + winning_streak, self.depth))
    #     )
    #     board = self.board[slicing]
    #     for direction, kernel in WinningPatterns.PATTERNS.items():
    #         if self.depth == 1 and kernel.shape[2] > 1:
    #             continue
    #         convolved = convolve((board == current_player_index).astype(int), kernel, mode='valid', method='direct')
    #         current_conv_res =  self.conv_res_by_direction[direction][int(current_player_index), :, :, :]
    #         assert np.all(convolve((self.board == current_player_index).astype(int), kernel, mode='valid', method='direct') == current_conv_res)
    #         assert np.any(convolved == winning_streak) == np.any(current_conv_res[slicing] == winning_streak)
    #         if np.any(convolved == winning_streak):
    #             return True
    #     return False