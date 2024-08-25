import os
from random import Random

from connect4cube.connect4.ai.board import CBoard
from connect4cube.connect4.ai.check import is_win
from connect4cube.connect4.ai.think_ahead import negamax_full, WIN_SCORE

ai_dir = os.path.dirname(os.path.realpath(__file__))
easyname = os.path.join(ai_dir, "easy.csv")
hardname = os.path.join(ai_dir, "hard.csv")


def generator():
    easy = open(easyname, mode='w')
    hard = open(hardname, mode='w')
    counter = 0
    seed = -1
    while counter < 1000:
        seed += 1
        rand = Random(seed)
        board = CBoard()
        gameover = False
        for i in range(rand.randint(8, 18)):
            move_id = rand.choice(list(board.get_valid_moves()))
            if is_win(board, move_id):
                gameover = True
                break
            board.move(move_id)
        if gameover:
            continue
        for _ in range(1):
            move_id = rand.choice(list(board.get_valid_moves()))
            if is_win(board, move_id):
                break
            board.move(move_id)
            results = negamax_full(board, 4)
            file = hard if abs(results[0][1]) < WIN_SCORE else easy
            counter += 1
            line = ",".join([str(x) for x in board.history[0:board.round]])
            print("{} @{}".format(line, counter))
            file.write(line + "\n")
    easy.close()
    hard.close()


if __name__ == "__main__":
    generator()
