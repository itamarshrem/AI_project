from connect4cube.connect4 import RED, BLUE, EMPTY
from connect4cube.connect4.board import Board
from connect4cube.connect4.game import Game
from connect4cube.connect4.player import RandomPlayer
from connect4cube.connect4.viewer import StdoutViewer


def test_alternating_players():
    board = Board()
    assert board.field(0, 0, 0) == EMPTY
    assert board.field(1, 1, 0) == EMPTY
    board.move(0, 0)
    assert board.field(0, 0, 0) == RED
    assert board.field(1, 1, 0) == EMPTY
    board.move(1, 1)
    assert board.field(0, 0, 0) == RED
    assert board.field(1, 1, 0) == BLUE
    assert board.round == 2


def test_win_backward1():
    board = Board()
    for i in range(3):
        assert not board.move(i, 0)
        assert not board.move(i, 0)
    assert board.move(3, 0)


def test_win_backward2():
    board = Board()
    for i in range(3):
        assert not board.move(i, 3-i)
        assert not board.move(i, 3-i)
    assert board.move(3, 0)


def test_win_forward1():
    board = Board()
    for i in range(3, 0, -1):
        assert not board.move(i, 0)
        assert not board.move(i, 0)
    assert board.move(0, 0)


def test_win_forward2():
    board = Board()
    for i in range(3, 0, -1):
        assert not board.move(i, 3-i)
        assert not board.move(i, 3-i)
    assert board.move(0, 3)


def test_random_game():
    stdout = StdoutViewer()
    game = Game(RandomPlayer(stdout, 0), RandomPlayer(stdout, 1), stdout)
    assert game.play() == BLUE
    stdout = StdoutViewer()
    game = Game(RandomPlayer(stdout, 0), RandomPlayer(stdout, 4), stdout)
    assert game.play() == RED


def test_draw():
    pass


def test_tostr():
    board = Board()
    board.move(0, 0)
    board.move(0, 0)
    board.move(0, 0)
    board.move(1, 0)
    board.move(3, 3)
    print("\n")
    print(board)
