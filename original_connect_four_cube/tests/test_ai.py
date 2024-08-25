from copy import deepcopy

from connect4cube.connect4.ai.board import CBoard
from connect4cube.connect4.ai.check import is_win
from connect4cube.connect4.ai.think_ahead import negamax_full


def test_check_win():
    board = CBoard()
    board.move(1)
    board.move(6)
    board.move(2)
    board.move(7)
    board.move(3)
    board.move(8)
    assert is_win(board, 0)
    assert is_win(board, 4)


def test_check_no_win():
    board = CBoard()
    board.move(1)
    assert not is_win(board, 0)


def test_undo():
    board = CBoard()
    board.move(1)
    before = deepcopy(board.cube)
    board.move(24)
    board.move(14)
    board.move(5)
    board.undo_move()
    board.undo_move()
    board.undo_move()
    assert before == board.cube


def test_easy_win():
    board = CBoard()
    board.move(1)
    board.move(6)
    board.move(2)
    board.move(7)
    # must now move to 3 for a win
    assert negamax_full(board)[0][0] == 3


def test_easy_prevent():
    board = CBoard()
    board.move(7)
    board.move(24)
    board.move(8)
    # must now move to 6 (or 5 or 9) to prevent a direct loss
    result = negamax_full(board)
    assert result[0][0] in [5, 6, 9]
    assert result[1][0] in [5, 6, 9]
    assert result[2][0] in [5, 6, 9]
