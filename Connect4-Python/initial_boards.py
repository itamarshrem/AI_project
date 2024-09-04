import numpy as np
from scipy.signal import convolve
import random

from board import Board
from winning_patterns import WinningPatterns

edge_case1 = np.array(
    [[-1., -1., -1., -1., -1, -1., -1., ],
     [-1., -1., -1., -1., -1., -1., -1., ],
     [-1., -1., -1., -1., -1., -1., -1., ],
     [-1., -1., -1., -1., -1., -1., -1., ],
     [-1., -1., -1., 1., -1., -1., -1., ],
     [-1., -1., -1., 0., -1., -1., -1., ], ]
)


class BoardFactory:
    @staticmethod
    def get_board(board_configuration, board_shape, num_of_players):
        rows, cols, depth = board_shape
        if board_configuration == "None":
            return Board(rows, cols, depth, num_of_players, None)
        elif board_configuration == "edge_case1":
            random.seed(0)
            np.random.seed(0)
            board = np.flip(np.expand_dims(edge_case1, 2), 0)
            conv_res = BoardFactory.init_conv_res_for_given_board(board, num_of_players)
            return Board(rows, cols, depth, num_of_players, board, conv_res_dict=conv_res, last_disc_location=(1, 3, 0))

    @staticmethod
    def init_conv_res_for_given_board(board, num_of_players):
        conv_res_by_direction = {}
        for direction, res_shape in WinningPatterns.CONV_RES_SHAPES.items():
            rows, cols, depth = res_shape
            kernel = WinningPatterns.PATTERNS[direction]
            conv_res_by_direction[direction] = np.zeros((num_of_players, rows, cols, depth))
            for i in range(num_of_players):
                conv_res_by_direction[direction][i] = convolve((board == i).astype(int), kernel, mode='valid',
                                                               method='direct')
        return conv_res_by_direction
