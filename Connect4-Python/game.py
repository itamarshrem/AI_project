import time
import numpy as np
# from scipy.signal import convolve
from initial_boards import BoardFactory
from user_interface import UIFactory
# from winning_patterns import WinningPatterns


class Game:
    TIE = -1

    def __init__(self, winning_streak, players, sleep_between_actions):
        self.winning_streak = winning_streak
        self.players = players
        self.sleep_between_actions = sleep_between_actions
        self.ui = None
        self.board = None
        self._should_quit = False

    def run(self, display_ui, board_configuration, board_shape):
        self._should_quit = False
        self.board = BoardFactory.get_board(board_configuration, board_shape)
        self.ui = UIFactory.getUI(display_ui, self.board)
        self.ui.display_board(self.board)
        result = self._game_loop()
        self.display_result_in_ui(result)
        return result

    def display_result_in_ui(self, result):
        if result == self.TIE:
            self.ui.print_to_screen("It's a tie!")
        else:
            self.ui.print_to_screen(f"Player {result} wins!")

    def game_finished(self):
        return len(self.board.get_legal_actions()) == 0

    def _game_loop(self):
        player_index = 0
        while not self._should_quit:
            player = self.players[player_index]
            if self.sleep_between_actions:
                time.sleep(1)
            action = player.get_action(self.board, len(self.players), self.winning_streak, self.ui)
            if action is None:
                return
            location = self.board.apply_action(action, player.index)
            self.ui.display_board(self.board)
            if self.winning_move(player, location):
                return player_index
            player_index = (player_index + 1) % len(self.players)
        return self.TIE

    def winning_move(self, current_player, disc_location):
        return self.board.winning_move(current_player.index, disc_location, self.winning_streak)
