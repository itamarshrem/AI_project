import numpy as np
from board import Board
edge_case1 = np.array(
    [[ -1., -1., -1., -1., -1., -1., -1.],
     [ -1., -1., -1., -1., -1.,  1., -1.],
     [ -1., -1., -1., -1.,  1.,  0., -1.],
     [  1., -1.,  1.,  1.,  1.,  0., -1.],
     [  0., -1.,  1.,  0.,  0.,  0., -1.]]
)


class BoardFactory:
    @staticmethod
    def get_board(board_configuration, board_shape):
        rows, cols, depth = board_shape
        if board_configuration == "None":
            return Board(rows, cols, depth, None)
        elif board_configuration == "edge_case1":
            return Board(rows, cols, depth, np.flip(np.expand_dims(edge_case1, 2), 0))
