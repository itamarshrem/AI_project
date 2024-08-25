import logging

from connect4cube.connect4 import RED, BLUE, EMPTY
from connect4cube.connect4.board import Board

LOG = logging.getLogger(__name__)


class BoardViewer:
    def __init__(self):
        self.board = Board()

    def player_plays(self, x, y):
        self.board.move(x, y)

    def player_selects(self, x, y):
        pass

    def player_undoes(self):
        self.board.undo()

    def finish(self, winning_coords):
        pass

    def close(self):
        pass


class StdoutViewer(BoardViewer):
    header = "  Y->         Z1          Z2          Z3            !{} #{}\n"
    value2char = {
        RED: "x ",
        BLUE: "o ",
        EMPTY: ". "
    }

    def select_value(self, value):
        return "[" + value[0] + "]"

    def draw_str(self, select_coords=None):
        LOG.debug("stdoutboard select_coords={}".format(select_coords))
        assert self.board is not None, "board not initialized in viewer"
        s = self.header.format(self.value2char.get(self.board.next_color), self.board.round)
        for x in range(5):
            for z in range(5):
                s += "X " if z == 0 and x == 0 else "  "
                for y in range(5):
                    v = self.board.field(x, y, z)
                    vs = self.value2char.get(v, "{}?".format(v))
                    if select_coords is not None and [x, y, z] in select_coords:
                        s = s[:-1]  # need the previous space
                        vs = self.select_value(vs)
                    s += vs
            s += "\n"
        return s

    def player_plays(self, x, y):
        super().player_plays(x, y)
        z = 4
        while z >= 0 and self.board.field(x, y, z) == EMPTY:
            z -= 1
        print(self.draw_str([[x, y, z]]))

    def player_selects(self, x, y):
        selected = []
        z = 4
        while z >= 0 and self.board.field(x, y, z) == EMPTY:
            selected.append([x, y, z])
            z -= 1
        print(self.draw_str(selected))

    def finish(self, winning_coords):
        print(self.draw_str(winning_coords))


class AnsiStdoutViewer(StdoutViewer):
    header = "  y →         z↑1         z↑2         z↑3          🤔{} #{}\n"
    value2char = {
        RED: '\033[31m○\033[39m ',
        BLUE: '\033[34m●\033[39m ',
        EMPTY: '\033[37m·\033[39m '
    }

    def select_value(self, value):
        return '\033[47m ' + value + '\033[49m'
