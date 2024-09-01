import numpy as np
from scipy.signal import convolve
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
# from scipy.special import stats_res
>>>>>>> Stashed changes
=======
# from scipy.special import stats_res
>>>>>>> Stashed changes

from board import Board
from winning_patterns import WinningPatterns

edge_case1 = np.array(
    [[-1., -1., -1., -1., -1., -1., -1.],
     [-1., -1., -1., -1., -1., -1., -1.],
     [-1., -1., -1., -1., -1., -1., -1.],
     [ 1.,  1.,  1., -1., -1.,  1., -1.],
     [ 0.,  0.,  1.,  0., -1.,  0.,  1.],
     [ 0.,  0.,  1.,  1., -1.,  0.,  0.]]
)


class BoardFactory:
    @staticmethod
    def get_board(board_configuration, board_shape, num_of_players):
        rows, cols, depth = board_shape
        if board_configuration == "None":
            return Board(rows, cols, depth, num_of_players, None)
        elif board_configuration == "edge_case1":
<<<<<<< Updated upstream
<<<<<<< Updated upstream
            board = np.flip(np.expand_dims(edge_case1, 2), 0)
=======
            board = np.flip(np.expand_dims(edge_case1, 2))
>>>>>>> Stashed changes
=======
            board = np.flip(np.expand_dims(edge_case1, 2))
>>>>>>> Stashed changes
            conv_res = BoardFactory.init_conv_res_for_given_board(board, num_of_players)
            return Board(rows, cols, depth, num_of_players, np.flip(np.expand_dims(edge_case1, 2), 0), conv_res_dict=conv_res)

    @staticmethod
    def init_conv_res_for_given_board(board, num_of_players):
        conv_res_by_direction = {}
        for direction, res_shape in WinningPatterns.CONV_RES_SHAPES.items():
            rows, cols, depth = res_shape
            kernel = WinningPatterns.PATTERNS[direction]
            conv_res_by_direction[direction] = np.zeros((num_of_players, rows, cols, depth))
            for i in range(num_of_players):
                conv_res_by_direction[direction][i] = convolve((board == i).astype(int), kernel, mode='valid', method='direct')
        return conv_res_by_direction

