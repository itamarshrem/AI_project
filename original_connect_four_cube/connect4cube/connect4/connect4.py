import logging

from connect4cube.app import App
from connect4cube.hardware.cube import get_empty_cube_buffer
from connect4cube.connect4.ai.player_ai_demo import AiDemoPlayer
from connect4cube.connect4.game import Game
from connect4cube.connect4.player_demo import DemoInterrupted
from connect4cube.connect4.player_gpio import GpioPlayer, PlayerExitError, PlayerResetError
from connect4cube.connect4.viewer_led import LedViewer, CYCLE, RAINBOW
from connect4cube.util.color import wheel

LOG = logging.getLogger(__name__)


class Connect4Demo(App):
    def run(self):
        stopped = False
        while not stopped:
            viewer = LedViewer(mode=RAINBOW)
            player = AiDemoPlayer(viewer)
            player.play_both_sides = True
            try:
                Game(player, player, viewer).play()
            except DemoInterrupted:
                stopped = True
            player.close()
            viewer.close()

    def get_preview(self):
        preview = get_empty_cube_buffer()
        preview[4][0][0] = wheel(180)
        preview[4][2][0] = wheel(190)
        preview[4][1][1] = wheel(200)
        preview[4][2][1] = wheel(210)
        preview[4][3][1] = wheel(220)
        preview[4][4][1] = wheel(230)

        preview[4][1][0] = wheel(60)
        preview[4][2][2] = wheel(70)
        preview[4][3][0] = wheel(80)
        preview[4][4][0] = wheel(90)
        preview[4][4][2] = wheel(100)
        return preview

    def get_description(self) -> str:
        return "connect4demo"


class Connect4Human(App):
    def run(self):
        stopped = False
        while not stopped:
            viewer = LedViewer(mode=CYCLE)
            player = GpioPlayer(viewer)
            player.play_both_sides = True
            try:
                Game(player, player, viewer).play()
            except PlayerResetError:
                viewer.finish([])
                LOG.debug("reset game")
            except PlayerExitError:
                viewer.finish([])
                LOG.debug("exit game")
                stopped = True
            player.close()
            viewer.close()

    def get_preview(self):
        preview = get_empty_cube_buffer()
        preview[4][0][0] = wheel(85)
        preview[4][0][1] = wheel(85)
        preview[4][1][0] = wheel(85)
        preview[4][1][1] = wheel(85)
        preview[4][2][0] = wheel(85)
        preview[4][2][2] = wheel(85)
        preview[4][3][1] = wheel(85)
        preview[4][3][3] = wheel(85)

        preview[4][1][0] = wheel(170)
        preview[4][1][2] = wheel(170)
        preview[4][2][1] = wheel(170)
        preview[4][3][0] = wheel(170)
        preview[4][3][2] = wheel(170)
        preview[4][4][0] = wheel(170)
        return preview

    def get_description(self) -> str:
        return "connect4human"
