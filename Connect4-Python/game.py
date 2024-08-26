import time
import numpy as np
from scipy.signal import convolve
from initial_boards import BoardFactory
from user_interface import UIFactory
from winning_patterns import WinningPatterns


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
        # Convolve the board with each kernel and check if any result contains self.winning_streak
        x, y, z = disc_location
        slicing = (
            slice(max(x - (self.winning_streak - 1), 0), min(x + self.winning_streak, self.board.rows)),
            slice(max(y - (self.winning_streak - 1), 0), min(y + self.winning_streak, self.board.cols)),
            slice(max(z - (self.winning_streak - 1), 0), min(z + self.winning_streak, self.board.depth))
        )
        board = self.board.board[slicing]
        for kernel in WinningPatterns.PATTERNS:
            if self.board.depth == 1 and kernel.shape[2] > 1:
                continue
            convolved = convolve((board == current_player.index).astype(int), kernel, mode='valid')
            if np.any(convolved == self.winning_streak):
                return True
        return False
