import numpy as np
from winning_patterns import WinningPatterns

class Board:
    EMPTY_CELL = -1

    def __init__(self, rows, cols, depth=1, num_of_players=2, board=None, conv_res_dict=None, last_disc_location=None):
        if board is None:
            self._board = np.ones((rows, cols, depth)) * self.EMPTY_CELL
            self.rows = rows
            self.cols = cols
            self.depth = depth
            self.last_disc_location = None
        else:
            assert last_disc_location is not None or np.all(board == self.EMPTY_CELL)
            self._board = board
            self.rows, self.cols, self.depth = board.shape
            self.last_disc_location = last_disc_location
        self.num_of_players = num_of_players
        self.conv_res_by_direction = {}
        if conv_res_dict is None:
            self._build_conv_res_by_direction()
        else:
            self.conv_res_by_direction = conv_res_dict

    def _build_conv_res_by_direction(self):
        for direction, res_shape in WinningPatterns.CONV_RES_SHAPES.items():
            rows, cols, depth = res_shape
            self.conv_res_by_direction[direction] = np.zeros((self.num_of_players, rows, cols, depth))

    def __copy__(self):
        b = Board(self.rows, self.cols, self.depth, self.num_of_players, self._board.copy(), {},
                  self.last_disc_location)
        b.conv_res_by_direction = {k: v.copy() for k, v in self.conv_res_by_direction.items()}
        return b

    @property
    def board(self):
        return self._board

    def get_legal_actions(self, winning_streak):
        if self.have_we_won(winning_streak):
            return []
        legal_actions = np.argwhere(self.board[self.rows - 1, :, :] == self.EMPTY_CELL)
        np.random.shuffle(legal_actions)
        return legal_actions.tolist()

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
        if self.depth == 1:
            return str(np.flip(self._board.squeeze(), 0)).replace('.', '.,').replace(']', '],')
        final_board_str = ""
        boards_to_print = []
        for depth in range(self.depth):
            boards_to_print.append(np.flip(self._board[:, :, depth], 0))
        for row in range(self.rows):
            for depth in range(self.depth):
                final_board_str += str(boards_to_print[depth][row]).replace(empty_char, '.,') + "||"
            final_board_str += "\n"
        final_board_str += "**************************************************************************"
        return final_board_str

    def have_we_won(self, winning_streak):
        if self.last_disc_location is None:
            return False

        x, y, z = self.last_disc_location
        current_player_index = self.board[x, y, z]
        for direction, conv_res in self.conv_res_by_direction.items():
            if np.any(conv_res[int(current_player_index), :, :, :] == winning_streak):
                return True
        return False
