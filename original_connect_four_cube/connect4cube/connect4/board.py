import logging
from itertools import product

from connect4cube.connect4 import RED, BLUE, EMPTY

POS_DIRECTIONS = list(product([-1, 0, 1], repeat=3))
# throw away have of the list since the reverse directions are also checked.
# additionally throw away (0,0,0) since it is not a valid move direction.
POS_DIRECTIONS = POS_DIRECTIONS[len(POS_DIRECTIONS) // 2 + 1:]


class Board:
    LOG = logging.getLogger(__name__)

    def __init__(self):
        self.cube = [[[EMPTY for _ in range(5)] for _ in range(5)] for _ in range(5)]
        self.next_color = RED
        self.round = 0
        self.winning_move = None
        self.history = []

    def change_player(self):
        self.next_color = RED if self.next_color == BLUE else BLUE

    def move(self, x, y) -> bool:
        assert self.winning_move is None
        assert 0 <= x < 5 and 0 <= y < 5
        z = 0
        while z < 5 and self.cube[x][y][z] != EMPTY:
            z += 1
        assert z < 5
        self.history.append((x, y))
        current = self.next_color
        self.cube[x][y][z] = current
        self.change_player()
        self.round += 1
        if self.calc_winning_coords(x, y, z, current) is not None:
            self.winning_move = [x, y, z]
            return True
        return False

    def undo(self):
        if len(self.history) == 0:
            return
        else:
            (x, y) = self.history.pop()
            z = 4
            while self.cube[x][y][z] == EMPTY:
                assert z > 0
                z -= 1
            self.round -= 1
            self.change_player()
            assert self.cube[x][y][z] == self.next_color
            self.cube[x][y][z] = EMPTY
            self.winning_move = None
            return

    def get_last(self):
        if len(self.history) == 0:
            return None, None
        else:
            return self.history[-1]

    def field(self, x, y, z):
        assert 0 <= x < 5 and 0 <= y < 5 and 0 <= z < 5
        return self.cube[x][y][z]

    def winning_coords(self):
        return self.calc_winning_coords(*tuple(self.winning_move), self.field(*tuple(self.winning_move)))

    def calc_winning_coords(self, x0, y0, z0, color):
        for d in POS_DIRECTIONS:
            (x, y, z) = (x0, y0, z0)
            counter = 0
            for counter in range(3):
                (x, y, z) = (x + d[0], y + d[1], z + d[2])
                if 0 > x or 0 > y or 0 > z or x >= 5 or y >= 5 or z >= 5:
                    break  # out of bounds
                if color != self.cube[x][y][z]:
                    break  # another color
                if counter == 2:  # since x0 is the starting point and we iterate 0,1,2
                    return self.four_from(x, y, z, -d[0], -d[1], -d[2])
            (x, y, z) = (x0, y0, z0)
            for counter in range(counter, 3):
                (x, y, z) = (x - d[0], y - d[1], z - d[2])
                if 0 > x or 0 > y or 0 > z or x >= 5 or y >= 5 or z >= 5:
                    break
                if color != self.cube[x][y][z]:
                    break
                if counter == 2:
                    return self.four_from(x, y, z, d[0], d[1], d[2])
        return None

    def four_from(self, x, y, z, dx, dy, dz):
        result = []
        for i in range(4):
            result.append([x + dx * i, y + dy * i, z + dz * i])
        return result
