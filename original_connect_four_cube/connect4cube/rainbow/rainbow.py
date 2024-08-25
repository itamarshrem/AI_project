import logging
from math import sin, cos
from connect4cube.app import App
from connect4cube.hardware.button_events import ButtonEvents, EventEnum
from connect4cube.hardware.cube import Cube, get_empty_cube_buffer
from connect4cube.hardware.util import is_a_raspberry
from connect4cube.util.color import wheel

if not is_a_raspberry():
    from time import sleep

LOG = logging.getLogger(__name__)
# Choose more or less random values so the two rotations do not repeat regularly.
THETA_D = 0.0121109
PHI_D = 0.0093491
WHEEL_OFFSET_D = 0.5


class Rainbow(App):
    def __init__(self):
        self.button_events = ButtonEvents()
        self.cube = Cube()
        self.cube_buffer = get_empty_cube_buffer()
        self.theta = 0.0
        self.phi = 0.0
        self.wheel_offset = 0.0
        self.theta_d = 0.0
        self.phi_d = 0.0
        self.wheel_offset_d = 0.0

    def run(self):
        try:
            while True:
                self.handle_events()
                v = [sin(self.theta)*cos(self.phi),
                     sin(self.theta)*sin(self.phi),
                     cos(self.theta)]
                self.rainbow(self.cube_buffer, v, self.wheel_offset)
                self.cube.draw(self.cube_buffer)
                self.cube.show()
                # Rotate vector
                self.theta += self.theta_d
                self.phi += self.phi_d
                # Cycle through all colors so the rainbow not only rotates, but also
                # moves through the cube.
                self.wheel_offset += self.wheel_offset_d
                self.wheel_offset %= 256
                if not is_a_raspberry():
                    sleep(0.02)
        except RainbowInterrupted:
            return

    def handle_events(self):
        """
        adjust the rotation settings of the rainbow
        """
        event = self.button_events.get_event(block=False)
        if event:
            if event == EventEnum.UP_PRESSED or event == EventEnum.UP_REPEATED:
                self.theta_d += THETA_D
            elif event == EventEnum.DOWN_PRESSED or event == EventEnum.DOWN_REPEATED:
                self.theta_d -= THETA_D
            elif event == EventEnum.LEFT_PRESSED or event == EventEnum.LEFT_REPEATED:
                self.phi_d -= PHI_D
            elif event == EventEnum.RIGHT_PRESSED or event == EventEnum.RIGHT_REPEATED:
                self.phi_d += PHI_D
            elif event == EventEnum.A_PRESSED:
                self.wheel_offset_d -= WHEEL_OFFSET_D
            elif event == EventEnum.A_REPEATED:
                LOG.debug("interrupting rainbow")
                raise RainbowInterrupted()
            elif event == EventEnum.B_PRESSED:
                self.wheel_offset_d += 0.5
            elif event == EventEnum.B_REPEATED:
                self.theta = 0.0
                self.phi = 0.0
                self.wheel_offset = 0.0
                self.theta_d = 0.0
                self.phi_d = 0.0
                self.wheel_offset_d = 0.0

    def rainbow(self, cube_buffer, v, wheel_offset):
        """
        draw a rainbow across the cube, oriented according to the given vector
        :param cube_buffer: cube buffer to modify
        :param v: vector for rainbow orientation and scaling (unit vector results in one rainbow across the cube)
        :param wheel_offset: color wheel offset
        """
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    dot_product = ((x-2)*v[0] + (y-2)*v[1] + (z-2)*v[2])
                    # 37 is the number to have the full rainbow range from [-2, -2, -2] to [2, 2, 2]
                    # if v is a unit vector.
                    cube_buffer[x][y][z] = wheel(int(dot_product * 37 + wheel_offset))

    def get_preview(self):
        preview = get_empty_cube_buffer()
        self.rainbow(preview, [0.5, 0.5, 0.5], 0)
        return preview

    def get_description(self) -> str:
        return "rainbow"


class RainbowInterrupted(RuntimeError):
    pass
