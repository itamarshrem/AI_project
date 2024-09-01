import numpy as np
from scipy.signal import convolve

from board import Board
from winning_patterns import WinningPatterns

edge_case1 = np.array(
    [[0., -1., -1., -1., -1., -1., -1.],
     [0., -1., -1., -1.,  1., -1., -1.],
     [1., -1.,  0., -1.,  0., -1., -1.],
     [0., -1.,  1.,  1.,  1., -1., -1.],
     [0., -1.,  0.,  1.,  1., -1., -1.],
     [0., -1.,  0.,  1.,  1.,  1.,  0.]]
)


class BoardFactory:
    @staticmethod
    def get_board(board_configuration, board_shape, num_of_players):
        rows, cols, depth = board_shape
        if board_configuration == "None":
            return Board(rows, cols, depth, num_of_players, None)
        elif board_configuration == "edge_case1":
            return Board(rows, cols, depth, num_of_players, np.flip(np.expand_dims(edge_case1, 2), 0))

    def init_conv_res_for_given_board(self, board, num_of_players):
        conv_res_by_direction = {}
        for direction, res_shape in WinningPatterns.CONV_RES_SHAPES.items():
            rows, cols, depth = res_shape
            conv_res_by_direction[direction] = np.zeros((num_of_players, rows, cols, depth))
            for pla
            conv_res_by_direction[direction] = convolve((board == current_player_index).astype(int), kernel, mode='valid', method='direct')

