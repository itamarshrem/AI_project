from connect4cube.connect4 import EMPTY


class CBoard:
    def __init__(self):
        self.cube = [EMPTY for _ in range(125)]
        self.valid_moves = [i for i in range(25)]
        self.round = 0
        self.history = [-1 for _ in range(125)]
        self.current_player = 0
        # stats
        self.nodes_counter = 0
        self.beta_cutoffs = 0

    def move(self, move_id):
        assert self.cube[move_id] == EMPTY
        self.cube[move_id] = self.current_player
        self.valid_moves[move_id % 25] += 25
        self.history[self.round] = move_id
        self.round += 1
        self.current_player ^= 1

    def undo_move(self):
        self.current_player ^= 1
        self.round -= 1
        move_id = self.history[self.round]
        self.valid_moves[move_id % 25] -= 25
        self.cube[move_id] = EMPTY

    def get_valid_moves(self):
        return list(filter(lambda x: x < 125, self.valid_moves))

    def to_xyz(self, i):
        x = i % 5
        y = (i // 5) % 5
        z = i // 25
        return x, y, z

    def __str__(self):
        s = ""
        for x in range(5):
            for z in range(5):
                s += "  "
                for y in range(5):
                    i = x + y * 5 + z * 25
                    s += {
                        0: "x ",
                        1: "o ",
                        EMPTY: ". "
                    }.get(self.cube[i])
            s += "\n"
        s += "valid_moves={}\n".format([int(x) for x in self.valid_moves])
        s += "history={}\n".format([int(x) for x in self.history])
        s += "round={}\n".format(self.round)
        s += "current_player={}\n".format(self.current_player)
        return s
