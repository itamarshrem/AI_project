import logging

from connect4cube.connect4 import EMPTY
from connect4cube.connect4.board import Board
from connect4cube.connect4.player import Player
from connect4cube.connect4.viewer import BoardViewer

MAX_ROUND = 5 * 5 * 5 - 1
LOG = logging.getLogger(__name__)


class RuleViolation(Exception):
    pass


class Game:
    def __init__(self, player_red: Player, player_blue: Player, viewer: BoardViewer):
        self.players = [player_red, player_blue]
        self.viewer = viewer

    def play(self) -> int:
        board = Board()
        last_x = None
        last_y = None
        while board.round <= MAX_ROUND:
            current_color = board.next_color
            (x, y) = self.players[current_color].play(last_x, last_y)
            if x == -1 and y == -1:
                self.viewer.player_undoes()
                board.undo()
                (last_x, last_y) = (-1, -1)
            else:
                if 0 > x > 4 or 0 > y > 4:
                    raise RuleViolation("out of bounds move")
                if board.field(x, y, 4) != EMPTY:
                    raise RuleViolation("already full at {},{}".format(x, y))
                is_winning = board.move(x, y)
                LOG.debug("player {} plays to {},{}".format(current_color, x, y))
                self.viewer.player_plays(x, y)
                if is_winning:
                    LOG.debug("player {} wins!".format(current_color))
                    self.viewer.finish(board.winning_coords())
                    return current_color
                (last_x, last_y) = (x, y)
        LOG.debug("game ended in a draw")
        self.viewer.finish([])
        return EMPTY
