import os


class Operand:
    def __init__(self, *args):
        self.args = list(args)
        for i, v in enumerate(self.args):
            if isinstance(v, int):
                self.args[i] = Eq(v)


class Eq:
    def __init__(self, idx):
        assert 0 <= idx < 125
        self.idx = idx

    def __str__(self):
        return "c == b[{}]".format(self.idx)


class And(Operand):
    def __str__(self):
        return "(" + " and ".join([str(i) for i in self.args]) + ")"


class Or(Operand):
    def __str__(self):
        return "(" + " or ".join([str(i) for i in self.args]) + ")"


class OrSurround(Operand):
    def __str__(self):
        return " \\\n        or ".join([str(i) for i in self.args])


X = 1
Y = 5
Z = 25


def generate():
    ai_dir = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(ai_dir, "check.py")
    with open(filename, mode='w') as file:
        file.write("""# Generated file
from connect4cube.connect4.ai.board import CBoard


def is_win(board: CBoard, move_id: int) -> bool:
    return checkmap[move_id](board.cube, board.current_player)


""")
        for i in range(125):
            file.write("def is_win{}(b, c):\n".format(i))
            file.write("    return {}\n".format(generate_move(i)))
            file.write("\n")
            file.write("\n")
        file.write("checkmap = [\n")
        for i in range(25):
            file.write("    " + ", ".join(["is_win{}".format(j+5*i) for j in range(5)]) + ",\n")
        file.write("]\n")


def generate_move(idx):
    result = OrSurround()
    x, y, z = to_xyz(idx)
    for d in (
            X, Y, X+Y, Y-X,
            X+Z, Y+Z, X+Y+Z, Y-X+Z,
            X-Z, Y-Z, X+Y-Z, Y-X-Z,
            Z
    ):
        dx, dy, dz = to_xyz(d)
        if abs(dx) > 1 or abs(dy) > 1 or abs(dz) > 1:
            continue
        fw = 1
        while 0 <= x + fw * dx < 5 and 0 <= y + fw * dy < 5 and 0 <= z + fw * dz < 5:
            # still valid
            fw += 1
            assert fw <= 5
        fw -= 1
        if d == Z:
            fw = 0  # must never check upwards
        rw = -1
        while 0 <= x + rw * dx < 5 and 0 <= y + rw * dy < 5 and 0 <= z + rw * dz < 5:
            # still valid
            rw -= 1
            assert rw >= -5
        rw += 1
        if fw - rw < 4:
            continue  # no connect4 possible in this direction
        # extract the line
        line = []
        for i in range(rw, fw + 1):
            line.append(idx + d * i)
        if len(line) == 4:
            # just check the others
            line.remove(idx)
            result.args.append(And(*line))
        elif line[0] == idx:
            result.args.append(And(*line[1:4]))
        elif line[-1] == idx:
            result.args.append(And(*line[-4:-1]))
        else:
            middle = line[1:4]
            middle.remove(idx)
            result.args.append(And(*middle, Or(line[0], line[-1])))
    return result


def to_xyz(i):
    negative = i < 0
    if negative:
        i *= -1
    x = i % 5
    y = (i // 5) % 5
    z = i // 25
    if negative:
        return -x, -y, -z
    return x, y, z


if __name__ == "__main__":
    generate()
