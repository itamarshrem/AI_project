import datetime

from connect4cube.connect4.ai.board import CBoard
from connect4cube.connect4.ai.perf_testdata_gen import hardname, easyname
from connect4cube.connect4.ai.think_ahead import negamax_full, WIN_SCORE


def run_testset(filename):
    counter, solved, nodes, t, cutoff = 0, 0, 0, 0, 0
    with open(filename) as file:
        for line in file:
            board = CBoard()
            for move_id in map(lambda x: int(x), line.split(",")):
                board.move(move_id)
            start = datetime.datetime.now()
            resut = negamax_full(board, depth=4)
            end = datetime.datetime.now()
            micro = (end - start).microseconds

            # stats
            if abs(resut[0][1]) > WIN_SCORE:
                solved += 1
            counter += 1
            nodes += board.nodes_counter
            cutoff += board.beta_cutoffs
            t += micro
            print("{}/{}: nodes={} cutoffs={} ms={}"
                  .format(counter, solved, round(nodes / counter), round(cutoff / counter), round(t / counter / 100)))


if __name__ == "__main__":
    run_testset(easyname)
    run_testset(hardname)

# alphabeta, depth=4
# 545/545: nodes=225306 cutoffs=15138 ms=1292
# 455/0: nodes=167484 cutoffs=21183 ms=1527

# alphabeta, depth=4, with 2-depth-win-look-ahead
# 545/545: nodes=12333 cutoffs=1156 ms=339
# 455/29: nodes=21533 cutoffs=4638 ms=888
