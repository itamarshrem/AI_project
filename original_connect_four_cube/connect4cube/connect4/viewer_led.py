from queue import Queue, Empty
from random import Random
from threading import Thread, Event

from connect4cube.connect4 import RED, BLUE, EMPTY
from connect4cube.connect4.viewer import BoardViewer
from connect4cube.hardware.cube import Cube, get_empty_cube_buffer
from connect4cube.hardware.util import is_a_raspberry
from connect4cube.util.color import wheel

if not is_a_raspberry():
    from time import sleep

SELECT = 0
PLAY = 1
UNDO = 2
FINISH = 3

CYCLE = 0
RAINBOW = 1


class LedViewer(BoardViewer):
    def __init__(self, mode=CYCLE):
        super().__init__()
        self.cube = Cube()
        self.queue = Queue()
        self.mode = mode
        self.animation_thread = StoppableThread(target=self.animation)
        self.animation_thread.setDaemon(True)
        self.animation_thread.start()

    def player_plays(self, x, y):
        self.queue.put((PLAY, x, y))

    def player_undoes(self):
        last_move = self.board.get_last()
        self.board.undo()
        if last_move != (None, None):
            self.queue.put((UNDO, *last_move))

    def player_selects(self, x, y):
        self.queue.put((SELECT, x, y))

    def finish(self, winning_coords):
        self.queue.put((FINISH, winning_coords))

    def close(self):
        self.animation_thread.stop()
        self.animation_thread.join()

    def animation(self):
        animation_state = AnimationState(self.mode)
        animation_list = [FieldColorsAnimation(animation_state, self.board.field)]
        while not self.animation_thread.stopped() or animation_list[-1].is_blocking() or not self.queue.empty():
            if not animation_list[-1].is_blocking():
                try:
                    event = self.queue.get_nowait()
                    # some animations have to stop when a new one is started
                    animation_list[-1].new_animation_available()
                    if event[0] == PLAY:
                        super().player_plays(*event[1:3])
                        animation_list.append(PlayAnimation(animation_state))
                    elif event[0] == UNDO:
                        x = event[1]
                        y = event[2]
                        z = self.get_z(x, y)
                        c = self.board.next_color
                        animation_list.append(UndoAnimation(animation_state, x, y, z, c))
                    elif event[0] == SELECT:
                        x = event[1]
                        y = event[2]
                        z = self.get_z(x, y)
                        c = self.board.next_color
                        top = self.board.field(x, y, z) is not EMPTY
                        animation_list.append(SelectAnimation(animation_state, x, y, z, c, top))
                    elif event[0] == FINISH:
                        c = RED
                        if self.board.next_color == RED:
                            c = BLUE
                        animation_list.append(FinishAnimation(animation_state, event[1], c))
                except Empty:
                    pass

            cube_buffer = get_empty_cube_buffer()
            for a in animation_list:
                a.animate(cube_buffer)

            # remove completed animations from list
            animation_list[:] = [a for a in animation_list if not a.is_done()]

            # draw the completed cube
            self.cube.draw(cube_buffer)
            self.cube.show()

            animation_state.update()

            if not is_a_raspberry():
                sleep(0.01)

    def get_z(self, x, y):
        z = 4
        while z > 0 and self.board.field(x, y, z - 1) == EMPTY:
            z -= 1
        return z


class StoppableThread(Thread):
    """
    A normal thread with a stop event.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stop_event = Event()

    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()


class AnimationBase:
    def __init__(self, state):
        self.state = state

    def animate(self, cube_buffer):
        # modify the cube with an animation
        pass

    def is_done(self) -> bool:
        # animation is removed from the list once this is true
        return True

    def new_animation_available(self):
        # some animations must terminate when a new one arrives
        pass

    def is_blocking(self) -> bool:
        # blocking animations must be completed before a next animation is started
        return False


class SelectAnimation(AnimationBase):
    def __init__(self, state, x, y, z, c, top):
        super().__init__(state)
        self.done = False
        self.x = x
        self.y = y
        self.z = z
        self.c = c
        self.z_a = 5.
        self.top = top

    def animate(self, cube_buffer):
        if not self.done:
            player_color = self.state.get_color(self.c)

            for z in range(self.z, 5):
                diff = abs(self.z_a - z)
                draw_color = player_color
                min_dim = 0.1
                # the one on the bottom is glowing white, except when there is no space left
                if z == self.z and not self.top:
                    min_dim = 0.3
                    dim = max(0., 1-diff)
                    dimmed_color = tuple(map(lambda c, w: int(c * min_dim + (w - c * min_dim) * dim),
                                             draw_color, (255, 255, 255)))
                else:
                    # always show a minimum of color on the selected line
                    dim = max((1.-diff), min_dim)
                    dimmed_color = tuple(map(lambda c: int(c * dim), draw_color))
                cube_buffer[self.x][self.y][z] = dimmed_color
            self.z_a -= 0.1
            if self.z_a < self.z - 1:
                self.z_a = 5.

    def is_done(self) -> bool:
        return self.done

    def new_animation_available(self):
        self.done = True


class FinishAnimation(AnimationBase):
    FLASH_TIME = 60
    BLINK_TIME = 50
    BLINK_COUNT = 6

    class State:
        FLASH = 0
        BLINK = 1

    def __init__(self, state, winning_coords, c):
        super().__init__(state)
        self.done = False
        self.winning_coords = winning_coords
        self.c = c
        self.finish_state = self.State.FLASH
        self.counter = 0

    def animate(self, cube_buffer):
        if not self.done:
            color = self.state.get_color(self.c)
            if not self.winning_coords:
                color = [255, 255, 255]
            if self.finish_state == self.State.FLASH:
                color = tuple(map(lambda c: int(c - self.counter * (c / self.FLASH_TIME)), color))
                for x in range(5):
                    for y in range(5):
                        for z in range(5):
                            cube_buffer[x][y][z] = color
                if self.counter >= self.FLASH_TIME:
                    if not self.winning_coords:
                        self.done = True
                    else:
                        self.counter = -1
                        self.finish_state = self.State.BLINK
            elif self.finish_state == self.State.BLINK:
                color = tuple(map(lambda c: int(c - self.counter % self.BLINK_TIME * (c / self.BLINK_TIME)), color))
                for coords in self.winning_coords:
                    cube_buffer[coords[0]][coords[1]][coords[2]] = color
                if self.counter >= self.BLINK_COUNT * self.BLINK_TIME - 1:
                    self.done = True
            self.counter += 1

    def is_done(self) -> bool:
        return self.done

    def is_blocking(self):
        return True


class PlayAnimation(AnimationBase):
    def __init__(self, state):
        super().__init__(state)

    def animate(self, cube_buffer):
        pass

    def is_done(self) -> bool:
        return True


class UndoAnimation(AnimationBase):
    def __init__(self, state, x, y, z, c):
        super().__init__(state)
        self.done = False
        self.x = x
        self.y = y
        self.z = z
        self.c = c
        self.z_a = z

    def animate(self, cube_buffer):
        if not self.done:
            player_color = self.state.get_color(self.c)
            for z in range(self.z, 5):
                diff = abs(self.z_a - z)
                dimmed_color = (0, 0, 0)
                if diff <= 1:
                    dimmed_color = tuple(map(lambda c: int(c * (1 - diff)), player_color))
                cube_buffer[self.x][self.y][z] = dimmed_color
            self.z_a += 0.1
            if self.z_a >= 5:
                self.done = True

    def is_done(self) -> bool:
        return self.done

    def is_blocking(self):
        return True


class FieldColorsAnimation(AnimationBase):
    def __init__(self, state, field):
        super().__init__(state)
        self.field = field

    def animate(self, cube_buffer):
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    value = self.field(x, y, z)
                    color = self.state.get_color(value)
                    cube_buffer[x][y][z] = color

    def is_done(self) -> bool:
        return False


class AnimationState:
    def __init__(self, mode):
        self.start = Random().randint(0, 255)
        self.variance = 15
        self.color = self.start
        self.dir = 1
        self.mode = mode

    def get_color(self, c) -> tuple:
        if c == RED:
            return wheel(self.color)
        elif c == BLUE:
            return wheel((self.color + 128) % 256)
        else:
            return 0, 0, 0

    def update(self):
        self.color = (self.color + self.dir) % 256
        if self.mode == CYCLE:
            if self.color == (self.start + self.variance) % 256 or self.color == (self.start - self.variance) % 256:
                self.dir = -self.dir
        elif self.mode == RAINBOW:
            self.color = (self.color + 1) % 256
