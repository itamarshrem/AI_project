import logging

from connect4cube.connect4.connect4 import Connect4Demo, Connect4Human
from connect4cube.hardware.button_events import ButtonEvents, EventEnum
from connect4cube.hardware.cube import Cube
from connect4cube.rainbow.rainbow import Rainbow
from connect4cube.random.random import Random
from connect4cube.snake.snakegame import SnakeGame

LOG = logging.getLogger(__name__)


class Selector:
    """
    App selector to show previews and run apps
    """
    def __init__(self):
        self.cube = Cube()
        self.button_events = ButtonEvents()
        self.apps = [Rainbow(), Random(), Connect4Demo(), Connect4Human(), SnakeGame()]
        self.selected = 0
        self.show_preview()

    def run(self):
        event = self.button_events.get_event()
        if event == EventEnum.UP_PRESSED or event == EventEnum.LEFT_PRESSED:
            self.selected = (self.selected - 1) % len(self.apps)
            self.show_preview()
        elif event == EventEnum.DOWN_PRESSED or event == EventEnum.RIGHT_PRESSED:
            self.selected = (self.selected + 1) % len(self.apps)
            self.show_preview()
        elif event == EventEnum.A_PRESSED:
            # create new instance
            self.apps[self.selected] = type(self.apps[self.selected])()
            self.apps[self.selected].run()
            self.show_preview()

    def show_preview(self):
        preview = self.apps[self.selected].get_preview()
        self.cube.draw(preview)
        self.cube.show()
