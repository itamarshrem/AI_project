import logging
import copy
from random import randint

from connect4cube.app import App
from connect4cube.hardware.button_events import ButtonEvents
from connect4cube.hardware.cube import Cube, get_empty_cube_buffer
from connect4cube.hardware.util import is_a_raspberry
from connect4cube.util.color import wheel

if not is_a_raspberry():
    from time import sleep

LOG = logging.getLogger(__name__)


class Random(App):
    """
    fill the cube with random stuff and change it slowly
    """
    def __init__(self):
        self.button_events = ButtonEvents()
        self.cube = Cube()
        self.cube_buffer = get_empty_cube_buffer()
        self.wheel_start = self.get_random_wheel()
        self.wheel_stop = self.get_random_wheel()

    def run(self):
        steps = 100
        try:
            while True:
                self.wheel_stop = self.get_random_wheel()
                for i in range(steps):
                    if self.button_events.get_event(block=False):
                        LOG.debug("button pressed, interrupting rainbow")
                        raise RandomInterrupted()
                    self.step(self.wheel_start, self.wheel_stop, float(i) / steps)
                    self.cube.draw(self.cube_buffer)
                    self.cube.show()
                    if not is_a_raspberry():
                        sleep(0.02)
                self.wheel_start = copy.deepcopy(self.wheel_stop)
        except RandomInterrupted:
            return

    def step(self, start, stop, step):
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    color = wheel(int(start[x][y][z] + (stop[x][y][z] - start[x][y][z]) * step) % 256)
                    self.cube_buffer[x][y][z] = color

    def get_random_wheel(self):
        random_wheel = [[[randint(0, 255) for _ in range(5)] for _ in range(5)] for _ in range(5)]
        return random_wheel

    def get_random_cube(self, cube_buffer):
        random_wheel = self.get_random_wheel()
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    cube_buffer[x][y][z] = wheel(random_wheel[x][y][z])

    def get_preview(self):
        preview = get_empty_cube_buffer()
        self.get_random_cube(preview)
        return preview

    def get_description(self) -> str:
        return "random"


class RandomInterrupted(RuntimeError):
    pass
