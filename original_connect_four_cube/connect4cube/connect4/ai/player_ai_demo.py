import logging
import random

from connect4cube.connect4 import EMPTY
from connect4cube.connect4.ai.board import CBoard
from connect4cube.connect4.ai.think_ahead import negamax_full
from connect4cube.connect4.player_demo import DemoPlayer

LOG = logging.getLogger(__name__)


class AiDemoPlayer(DemoPlayer):
    def best_move(self):
        cboard = self.to_cboard()
        result = negamax_full(cboard)

        LOG.info("negamax result: {}".format(result))
        good_moves = []
        for move_id, score in result:
            if score == result[0][1]:
                good_moves.append(move_id)
        best_move_id = random.choice(good_moves)
        x, y, _ = cboard.to_xyz(best_move_id)
        return x, y

    def to_cboard(self):
        cboard = CBoard()
        for x, y in self.board.history:
            move_id = x + 5 * y
            while cboard.cube[move_id] != EMPTY:
                move_id += 25
            cboard.move(move_id)
        return cboard
