from typing import List, Tuple
from connect4cube.hardware.util import is_a_raspberry

if is_a_raspberry():
    from connect4cube.hardware.cube_led import LedCube
else:
    from connect4cube.hardware.cube_vpython import VPythonCube

CubeType = List[List[List[Tuple[int, int, int]]]]
CoordType = Tuple[int, int, int]


class Cube:
    """
    Singleton class of an LED cube. Depending on the target the real LED cube or a vpython mockup is used.
    """
    instance = None

    class __Cube:
        cube = None

        def __init__(self):
            if is_a_raspberry():
                self.cube = LedCube()
            else:
                self.cube = VPythonCube()

        def set_color(self, x: int, y: int, z: int, r: int, g: int, b: int) -> None:
            self.cube.set_color(x, y, z, r, g, b)

        def draw(self, cube_buffer: CubeType) -> None:
            for x in range(5):
                for y in range(5):
                    for z in range(5):
                        self.cube.set_color(x, y, z, *cube_buffer[x][y][z])

        def show(self) -> None:
            self.cube.show()

    def __init__(self):
        if not Cube.instance:
            Cube.instance = Cube.__Cube()

    def __getattr__(self, name):
        return getattr(self.instance, name)


def get_empty_cube_buffer() -> CubeType:
    cube_buffer = [[[(0, 0, 0) for _ in range(5)] for _ in range(5)] for _ in range(5)]
    return cube_buffer
