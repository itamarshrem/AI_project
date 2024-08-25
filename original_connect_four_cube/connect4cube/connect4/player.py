import sys
from random import Random
from time import sleep

from connect4cube.connect4 import EMPTY
from connect4cube.connect4.board import Board


class Player:
    def play(self, other_x, other_y) -> tuple:
        """
        :param other_x: x-coordinate of the previous opponents move or None
        :param other_y: see x
        :return: a tuple (x, y) of the location to play to
        """
        raise NotImplementedError


class BasePlayer(Player):
    """ Abstract player backed by a simple board """
    def __init__(self, viewer):
        self.viewer = viewer
        self.board = Board()
        self.play_both_sides = False

    def play(self, other_x, other_y) -> tuple:
        assert self.board.round < 5 * 5 * 5
        if not self.play_both_sides:
            if other_x is not None and other_y is not None:
                if other_x == -1 and other_y == -1:
                    self.board.undo()
                else:
                    self.board.move(other_x, other_y)
        (x, y) = self.do_play()
        if x == -1 and y == -1:
            self.board.undo()
        else:
            self.board.move(x, y)
        return x, y

    def do_select(self, x, y):
        self.viewer.player_selects(x, y)

    def do_play(self) -> tuple:
        raise NotImplementedError

    def close(self):
        pass


class RandomPlayer(BasePlayer):
    def __init__(self, viewer, seed=None, sleep_sec=0):
        super().__init__(viewer)
        self.rand = Random(seed)
        self.sleep_sec = sleep_sec

    def do_play(self) -> tuple:
        while True:
            # yeah, alternatively we could collect all valid moves and then pick a random one
            x = self.rand.randint(0, 4)
            y = self.rand.randint(0, 4)
            if self.board.field(x, y, 4) == EMPTY:
                sleep(self.sleep_sec/2)
                self.do_select(x, y)
                sleep(self.sleep_sec/2)
                return x, y


class StdinPlayer(BasePlayer):
    def __init__(self, viewer):
        super().__init__(viewer)
        self.selected = (2, 2)

    def do_play(self) -> tuple:
        switcher_2digit = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, '0': 0, '1': 1, '2': 2, '3': 3, '4': 4}
        switcher_1digit = {'d': (0, 0), 'j': (1, 0), 'k': (-1, 0), 'h': (0, -1), 'l': (0, 1)}
        self.do_select(*self.selected)
        while True:
            s = input("move> ").lower()
            if len(s) == 1:
                diff = switcher_1digit.get(s[0], (-1, -1))
                if diff == (-1, -1):
                    sys.stderr.write("invalid digit, 'j'=x+1, 'k'=x-1, 'h'=y-1, 'l'=y+1, 'd'=drop, retry\n")
                    continue
                x = self.selected[0] + diff[0]
                y = self.selected[1] + diff[1]
                if x < 0 or y < 0 or x > 4 or y > 4:
                    continue
                self.selected = (x, y)
                self.do_select(*self.selected)
                # (0, 0) is used to drop
                if diff != (0, 0):
                    continue
            elif len(s) == 2:
                x = switcher_2digit.get(s[0], -1)
                y = switcher_2digit.get(s[1], -1)
                if x < 0 or y < 0:
                    sys.stderr.write("invalid digit, try something like 'A0', retry\n")
                    continue
                self.selected = (x, y)
            else:
                sys.stderr.write("expected one of the following:\n")
                sys.stderr.write("  1 digit, 'j'=x+1, 'k'=x-1, 'h'=y-1, 'l'=y+1, 'd'=drop, retry\n")
                sys.stderr.write("  2 digits, like 'A0', retry\n")
                continue
            if self.board.field(*self.selected, 4) != EMPTY:
                sys.stderr.write("invalid move, column is already full, retry\n")
                continue
            self.do_select(*self.selected)
            return x, y
