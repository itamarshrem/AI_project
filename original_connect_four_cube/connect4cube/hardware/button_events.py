import logging
from enum import Enum, auto
from queue import Queue, Empty
from threading import Lock
from time import time
from gpiozero import Button

from connect4cube.hardware.util import is_a_raspberry
if not is_a_raspberry():
    from gpiozero.pins.mock import MockFactory
    from gpiozero import Device

LOG = logging.getLogger(__name__)
DEBOUNCE_TIME = 0.01
DEBOUNCE_TIME_REVERSE_DIR = 0.1


class ButtonEvents:
    """
    Singleton class for button events, because the hardware can only be accessed by one.
    """
    instance = None

    class __ButtonEvents:
        def __init__(self, axis_up=19, axis_down=26, axis_left=6, axis_right=13, button_a=12, button_b=16):
            """
            all pin numbers in BMC, see https://pinout.xyz/
            """
            if not is_a_raspberry():
                Device.pin_factory = MockFactory()

            pin2fn = {
                axis_up: (
                    lambda: self.button_pressed_dir(EventEnum.UP_PRESSED),
                    lambda: self.button_repeated(EventEnum.UP_REPEATED),
                    lambda: self.button_released(EventEnum.UP_PRESSED)
                ),
                axis_down: (
                    lambda: self.button_pressed_dir(EventEnum.DOWN_PRESSED),
                    lambda: self.button_repeated(EventEnum.DOWN_REPEATED),
                    lambda: self.button_released(EventEnum.DOWN_PRESSED)
                ),
                axis_left: (
                    lambda: self.button_pressed_dir(EventEnum.LEFT_PRESSED),
                    lambda: self.button_repeated(EventEnum.LEFT_REPEATED),
                    lambda: self.button_released(EventEnum.LEFT_PRESSED)
                ),
                axis_right: (
                    lambda: self.button_pressed_dir(EventEnum.RIGHT_PRESSED),
                    lambda: self.button_repeated(EventEnum.RIGHT_REPEATED),
                    lambda: self.button_released(EventEnum.RIGHT_PRESSED)
                ),
                button_a: (
                    lambda: self.button_pressed(EventEnum.A_PRESSED),
                    lambda: self.button_repeated(EventEnum.A_REPEATED),
                    lambda: self.button_released(EventEnum.A_PRESSED)
                ),
                button_b: (
                    lambda: self.button_pressed(EventEnum.B_PRESSED),
                    lambda: self.button_repeated(EventEnum.B_REPEATED),
                    lambda: self.button_released(EventEnum.B_PRESSED)
                ),
            }
            self.buttons = []
            for pin, fns in pin2fn.items():
                # Debouncing function of Button (argument bounce_time) is broken and is not usable.
                button = Button(pin, hold_repeat=True, hold_time=1)
                button.when_pressed = fns[0]
                button.when_held = fns[1]
                button.when_released = fns[2]
                self.buttons.append(button)

            self.last_up_time = self.LastEventTime()
            self.last_down_time = self.LastEventTime()
            self.last_left_time = self.LastEventTime()
            self.last_right_time = self.LastEventTime()
            self.last_a_time = self.LastEventTime()
            self.last_b_time = self.LastEventTime()
            self.last_event_times = {
                EventEnum.UP_PRESSED: self.last_up_time,
                EventEnum.DOWN_PRESSED: self.last_down_time,
                EventEnum.LEFT_PRESSED: self.last_left_time,
                EventEnum.RIGHT_PRESSED: self.last_right_time,
                EventEnum.A_PRESSED: self.last_a_time,
                EventEnum.B_PRESSED: self.last_b_time
            }
            # Dictionary to get the event times of the reverse direction.
            # Used for additional debouncing of joystick.
            self.last_reverse_dir_event_times = {
                EventEnum.UP_PRESSED: self.last_down_time,
                EventEnum.DOWN_PRESSED: self.last_up_time,
                EventEnum.LEFT_PRESSED: self.last_right_time,
                EventEnum.RIGHT_PRESSED: self.last_left_time
            }

            self.lock = Lock()
            self.event_queue = Queue()

        def button_pressed_dir(self, event):
            """
            If the joystick is released it tends to jump back and activate the reversed direction.
            Suppress this reverse activation in addition to the normal debouncing.
            """
            LOG.debug("button event: {}".format(event))
            with self.lock:
                diff = time() - self.last_event_times[event].last_event_time
                if diff < DEBOUNCE_TIME:
                    LOG.debug("debounce: ignoring input")
                    return
                reverse_dir_diff = time() - self.last_reverse_dir_event_times[event].last_event_time
                if reverse_dir_diff < DEBOUNCE_TIME_REVERSE_DIR:
                    LOG.debug("debounce reverse dir: ignoring input")
                    return
                self.last_event_times[event].last_event_time = time()
            self.event_queue.put(event)

        def button_pressed(self, event):
            """
            Debounce the button by checking the last event time of this button.
            """
            LOG.debug("button event: {}".format(event))
            with self.lock:
                if time() - self.last_event_times[event].last_event_time < DEBOUNCE_TIME:
                    LOG.debug("debounce: ignoring input")
                    return
                self.last_event_times[event].last_event_time = time()
            self.event_queue.put(event)

        def button_repeated(self, event):
            LOG.debug("button event: {}".format(event))
            self.event_queue.put(event)

        def button_released(self, event):
            """
            Reset debounce time on release.
            """
            LOG.debug("button released: {}".format(event))
            with self.lock:
                self.last_event_times[event].last_event_time = time()

        def get_event(self, block=True, timeout=None):
            try:
                event = self.event_queue.get(block=block, timeout=timeout)
                self.event_queue.task_done()
                return event
            except Empty:
                return None

        def clear(self):
            """
            consume all events which are still in the queue
            """
            try:
                while self.event_queue.get(block=False):
                    self.event_queue.task_done()
            except Empty:
                pass

        def close(self):
            """
            close any GPIO ports or creating a new instance will fail until the garbage collector runs
            """
            for button in self.buttons:
                button.close()

        class LastEventTime:
            """
            Class to store the last event time.
            Separate class so it can be used from multiple dictionaries.
            """
            def __init__(self, last_event_time=0):
                self.last_event_time = last_event_time

    def __init__(self):
        if not ButtonEvents.instance:
            ButtonEvents.instance = ButtonEvents.__ButtonEvents()

    def __getattr__(self, name):
        return getattr(self.instance, name)


class EventEnum(Enum):
    """
    Button event identifiers to send via a queue to consumers.
    """
    UP_PRESSED = auto()
    DOWN_PRESSED = auto()
    LEFT_PRESSED = auto()
    RIGHT_PRESSED = auto()
    A_PRESSED = auto()
    B_PRESSED = auto()
    UP_REPEATED = auto()
    DOWN_REPEATED = auto()
    LEFT_REPEATED = auto()
    RIGHT_REPEATED = auto()
    A_REPEATED = auto()
    B_REPEATED = auto()
