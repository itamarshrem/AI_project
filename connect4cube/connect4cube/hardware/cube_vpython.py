import logging
from time import sleep

from gpiozero import Device
from vpython import sphere, vector, canvas, color

LOG = logging.getLogger(__name__)


class VPythonCube:
    """
    A Mockup class for local pingpong LED debugging
    """
    no_color = color.white * 0.2

    def __init__(self):
        self.canvas = canvas(width=1900, height=900)
        self.pixels = [sphere] * 125
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    pxid = self.xyz2pxid(x, y, z)
                    led = sphere(canvas=self.canvas,
                                 pos=vector(y - 2, z - 2, x - 2),
                                 radius=0.2,  # pingpong ball diameter is 40mm, distance between 'em 100mm
                                 color=self.no_color,
                                 emissive=True)
                    # noinspection PyTypeChecker
                    self.pixels[pxid] = led
        self.canvas.camera.rotate(angle=0.1, axis=vector(1, 1, 0), origin=self.canvas.center)
        self.canvas.center = vector(0, 0, 0)
        self.canvas.bind("keydown", handle_mock_gpio)  # handle keypresses

    def xyz2pxid(self, x, y, z) -> int:
        return x + y * 5 + z * 25

    def set_color(self, x, y, z, r, g, b):
        pxid = self.xyz2pxid(x, y, z)
        self.pixels[pxid].color = vector(r / 256.0, g / 256.0, b / 256.0) * 0.8 + self.no_color

    def show(self):
        pass


def handle_mock_gpio(event):
    pressed = 0
    repeat = 1
    LOG.debug("keydown {}".format(event.key))
    pin = {
        "up": (19, pressed),
        "down": (26, pressed),
        "left": (6, pressed),
        "right": (13, pressed),
        " ": (12, pressed),
        "\n": (12, pressed),
        "a": (12, pressed),
        "A": (12, repeat),
        "u": (16, pressed),  # undo
        "r": (16, repeat),  # reset
        "b": (16, pressed),
        "B": (16, repeat)
    }.get(event.key, (0, 0))
    if pin != (0, 0):
        pin_dev = Device.pin_factory.pin(pin[0])
        pin_dev.drive_low()
        if pin[1] == pressed:
            sleep(0.1)
        else:
            sleep(1.5)
        pin_dev.drive_high()
