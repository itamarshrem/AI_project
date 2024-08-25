import logging
import random
from queue import Empty

from connect4cube.connect4 import EMPTY
from connect4cube.connect4.player_gpio import GpioPlayer

LOG = logging.getLogger(__name__)


class DemoPlayer(GpioPlayer):
    def sleep_or_die(self):
        try:
            self.button_events.event_queue.get(timeout=(random.random()+0.5))
            self.button_events.event_queue.task_done()
            LOG.debug("button pressed, interrupting demo")
            raise DemoInterrupted()
        except Empty:
            pass

    def get_valid_moves(self):
        valid_moves = []
        for x in range(5):
            for y in range(5):
                if self.board.field(x, y, 4) == EMPTY:
                    valid_moves.append((x, y))
        return valid_moves

    def best_move(self):
        valid_moves = self.get_valid_moves()

        # if we can win, we do it
        for x, y in valid_moves:
            is_win = self.board.move(x, y)
            self.board.undo()
            if is_win:
                return x, y

        # if the other could win, we prevent it (or at least on of 'em)
        self.board.change_player()
        for x, y in valid_moves:
            is_win = self.board.move(x, y)
            self.board.undo()
            if is_win:
                self.board.change_player()
                return x, y
        self.board.change_player()

        return random.choice(valid_moves)

    def do_play(self) -> tuple:
        self.button_events.clear()
        x, y = self.best_move()
        sx, sy = self.selected
        self.do_select(sx, sy)
        while sx != x:
            sx += 1 if x > sx else -1
            self.sleep_or_die()
            self.do_select(sx, sy)
        while sy != y:
            sy += 1 if y > sy else -1
            self.sleep_or_die()
            self.do_select(sx, sy)
        self.selected = (sx, sy)
        self.sleep_or_die()
        return x, y


class DemoInterrupted(RuntimeError):
    pass
