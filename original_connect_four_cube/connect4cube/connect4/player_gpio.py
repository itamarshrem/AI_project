import logging

from connect4cube.connect4 import EMPTY
from connect4cube.connect4.player import BasePlayer
from connect4cube.hardware.button_events import ButtonEvents, EventEnum

LOG = logging.getLogger(__name__)


class GpioPlayer(BasePlayer):
    """
    A binary-joystick controlled player using RasPi GPIOs
    https://gpiozero.readthedocs.io/en/stable/
    """
    def __init__(self, viewer):
        BasePlayer.__init__(self, viewer)
        self.button_events = ButtonEvents()
        self.selected = (2, 2)
        # short timeout after a game starts, it is increased on the first input
        self.timeout = 30
        self.return_position = (None, None)

    def axis_pressed(self, dx, dy):
        LOG.debug("axis button pressed: {} {}".format(dx, dy))
        x, y = self.selected
        x += dx
        y += dy
        if not (0 <= x < 5 and 0 <= y < 5):
            LOG.debug("out of bounds: ignoring {},{}".format(x, y))
            return
        self.selected = (x, y)
        LOG.debug("selected {},{}".format(x, y))
        self.do_select(x, y)

    def drop_pressed(self):
        LOG.debug("drop button pressed")
        if self.board.field(*self.selected, 4) != EMPTY:
            LOG.debug("non playable location, ignoring")
            return
        self.return_position = self.selected

    def undo_pressed(self):
        LOG.debug("undo button pressed")
        self.return_position = (-1, -1)

    def reset_pressed(self):
        LOG.debug("reset button pressed")
        raise PlayerResetError()

    def exit_pressed(self):
        LOG.debug("exit button pressed")
        raise PlayerExitError()

    def do_play(self) -> tuple:
        if self.selected == (-1, -1):
            self.selected = (2, 2)
        self.do_select(*self.selected)  # first show the last selected location
        self.button_events.clear()
        self.return_position = (None, None)
        event_functions = {
            EventEnum.UP_PRESSED: lambda: self.axis_pressed(-1, 0),
            EventEnum.UP_REPEATED: lambda: self.axis_pressed(-1, 0),
            EventEnum.DOWN_PRESSED: lambda: self.axis_pressed(1, 0),
            EventEnum.DOWN_REPEATED: lambda: self.axis_pressed(1, 0),
            EventEnum.LEFT_PRESSED: lambda: self.axis_pressed(0, -1),
            EventEnum.LEFT_REPEATED: lambda: self.axis_pressed(0, -1),
            EventEnum.RIGHT_PRESSED: lambda: self.axis_pressed(0, 1),
            EventEnum.RIGHT_REPEATED: lambda: self.axis_pressed(0, 1),
            EventEnum.A_PRESSED: self.drop_pressed,
            EventEnum.A_REPEATED: self.exit_pressed,
            EventEnum.B_PRESSED: self.undo_pressed,
            EventEnum.B_REPEATED: self.reset_pressed,
        }
        while self.return_position == (None, None):
            event = self.button_events.get_event(timeout=self.timeout)
            if event:
                event_function = event_functions[event]
                if event_function is not None:
                    event_functions[event]()
            else:
                LOG.warning("player idle for too long")
                raise PlayerExitError()

            # increase timeout after first event
            self.timeout = 200
        return self.return_position


class PlayerResetError(InterruptedError):
    pass


class PlayerExitError(InterruptedError):
    pass
