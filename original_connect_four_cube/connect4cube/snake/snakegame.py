import logging
from enum import Enum
from random import randint
from time import monotonic, sleep
from typing import List, Tuple
from connect4cube.app import App
from connect4cube.hardware.button_events import ButtonEvents, EventEnum
from connect4cube.hardware.cube import Cube, CubeType, CoordType, get_empty_cube_buffer
from connect4cube.hardware.util import is_a_raspberry
from connect4cube.util.color import wheel

LOG = logging.getLogger(__name__)
DELAY = 0.5


class SnakeGame(App):
    def __init__(self):
        self.button_events = ButtonEvents()
        self.cube = Cube()
        self.snake = Snake()
        self.apple = Apple()

    def run(self) -> None:
        try:
            last_time = monotonic()
            self.apple.set_random_position(self.snake.snake)
            while True:
                self.handle_events()
                current_time = monotonic()
                if (current_time - last_time) > DELAY:
                    last_time = current_time
                    self.snake.move(self.apple)
                cube_buffer = get_empty_cube_buffer()
                cube_buffer = self.apple.draw(cube_buffer)
                cube_buffer = self.snake.draw(cube_buffer)
                self.cube.draw(cube_buffer)
                self.cube.show()
                if not is_a_raspberry():
                    sleep(0.01)
        except SnakeCollision:
            LOG.debug("collision")
            self.death_animation()
            return
        except SnakeInterrupted:
            return

    def death_animation(self) -> None:
        cube_buffer = get_empty_cube_buffer()
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    cube_buffer[x][y][z] = wheel(85)
        self.cube.draw(cube_buffer)
        self.cube.show()
        sleep(1)

    def handle_events(self) -> None:
        """
        get user input to move snake
        """
        event = self.button_events.get_event(block=False)
        if event:
            if event == EventEnum.UP_PRESSED:
                self.snake.set_direction(Direction.FORWARD.value)
            elif event == EventEnum.DOWN_PRESSED:
                self.snake.set_direction(Direction.BACKWARD.value)
            elif event == EventEnum.LEFT_PRESSED:
                self.snake.set_direction(Direction.LEFT.value)
            elif event == EventEnum.RIGHT_PRESSED:
                self.snake.set_direction(Direction.RIGHT.value)
            elif event == EventEnum.A_PRESSED:
                self.snake.set_direction(Direction.UP.value)
            elif event == EventEnum.A_REPEATED:
                LOG.debug("interrupting snake")
                raise SnakeInterrupted()
            elif event == EventEnum.B_PRESSED:
                self.snake.set_direction(Direction.DOWN.value)

    def get_preview(self) -> CubeType:
        snake = Snake([(4, 4, 0), (4, 3, 0), (4, 2, 0), (4, 2, 1), (4, 2, 2), (3, 2, 2)])
        apple = Apple()
        apple.set_random_position(snake.snake)
        cube_buffer = get_empty_cube_buffer()
        cube_buffer = apple.draw(cube_buffer)
        cube_buffer = snake.draw(cube_buffer)
        return cube_buffer

    def get_description(self) -> str:
        return "snake"


class Apple:
    def __init__(self):
        self.position: CoordType = (0, 0, 0)
        self.color_intensity = 0.8
        self.color_dir = 1

    def draw(self, cube_buffer: CubeType) -> CubeType:
        if self.color_intensity >= 1:
            self.color_dir = -1
        elif self.color_intensity <= 0.5:
            self.color_dir = 1
        self.color_intensity = self.color_intensity + (self.color_dir * 0.05)
        tmp = [int(e * self.color_intensity) for e in wheel(85)]
        # use explicit indices to generate tuple instead of tuple() to satisfy type checker
        color = (tmp[0], tmp[1], tmp[2])
        cube_buffer[self.position[0]][self.position[1]][self.position[2]] = color
        return cube_buffer

    def set_random_position(self, snake: List[Tuple[int, int, int]]) -> None:
        while True:
            position = tuple(randint(0, 4) for _ in range(3))
            if position not in snake:
                LOG.debug("new apple position: {}".format(position))
                self.position = position
                break


class Snake:
    def __init__(self, snake=None):
        if snake is None:
            snake: List[CoordType] = [(4, 2, 2), (3, 2, 2)]
        self.old_direction: CoordType = Direction.FORWARD.value
        self.new_direction: CoordType = Direction.FORWARD.value
        self.snake: List[CoordType] = snake
        self.color = 0

    def draw(self, cube_buffer: CubeType) -> CubeType:
        color = self.color
        for e in self.snake:
            cube_buffer[e[0]][e[1]][e[2]] = wheel(color)
            color = (color + 10) % 256
        self.color = (self.color + 1) % 256
        return cube_buffer

    def move(self, apple: Apple) -> None:
        self.old_direction = self.new_direction
        next_position = self.add_direction(self.snake[-1], self.new_direction)
        # check if apple is consumed
        if next_position == apple.position:
            apple.set_random_position(self.snake)
        else:
            self.snake.pop(0)
        # check for collision
        if next_position in self.snake:
            raise SnakeCollision()
        self.snake.append(next_position)

    def add_direction(self, last: CoordType, direction: CoordType) -> CoordType:
        tmp = [(e0 + e1) % 5 for e0, e1 in zip(last, direction)]
        # use explicit indices to generate tuple instead of tuple() to satisfy type checker
        next_position = (tmp[0], tmp[1], tmp[2])
        return next_position

    def set_direction(self, direction: CoordType) -> None:
        # prevent killing yourself by reversing the direction
        if self.add_direction(self.old_direction, direction) != (0, 0, 0):
            self.new_direction = direction


class Direction(Enum):
    """
    Directions
    """
    UP = (0, 0, 1)
    DOWN = (0, 0, -1)
    LEFT = (0, -1, 0)
    RIGHT = (0, 1, 0)
    BACKWARD = (1, 0, 0)
    FORWARD = (-1, 0, 0)


class SnakeInterrupted(RuntimeError):
    pass


class SnakeCollision(RuntimeError):
    pass
