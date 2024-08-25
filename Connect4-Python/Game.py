from Board import Board
from Constants import Constants
import pygame
import time
import numpy as np
from scipy.signal import convolve


class Game:
    def __init__(self, winning_streak, players, sleep_between_actions):
        self.winning_streak = winning_streak
        self.players = players
        self.sleep_between_actions = sleep_between_actions
        self.screen = None
        self.myfont = None
        self.board = None
        self._should_quit = False

    def run(self):
        self._should_quit = False
        self.board = Board(Constants.ROW_COUNT, Constants.COLUMN_COUNT, 1)
        pygame.init()
        self.screen = pygame.display.set_mode(Constants.size)
        self.myfont = pygame.font.SysFont("monospace", 75)
        self.board.draw(self.screen)
        return self._game_loop()

    def game_finished(self):
        return len(self.board.get_legal_actions()) == 0

    def _game_loop(self):
        player_index = 0
        while not self._should_quit:
            player = self.players[player_index]
            if self.sleep_between_actions:
                time.sleep(1)
            action = player.get_action(self.board, self.screen)
            if action is None:
                return
            location = self.board.apply_action(action, player.index)
            self.board.draw(self.screen)
            if self.winning_move(player, location):
                label = self.myfont.render(f"Player {player_index} wins!!", 1, Constants.RED)
                self.screen.blit(label, (40, 10))
                pygame.display.update()
                return
            player_index = (player_index + 1) % len(self.players)
        return

    def winning_move(self, current_player, disc_location):
        # Convolve the board with each kernel and check if any result contains self.winning_streak
        x, y, z = disc_location
        slicing = (
            slice(max(x - (self.winning_streak - 1), 0), min(x + self.winning_streak, self.board.rows)),
            slice(max(y - (self.winning_streak - 1), 0), min(y + self.winning_streak, self.board.cols)),
            slice(max(z - (self.winning_streak - 1), 0), min(z + self.winning_streak, self.board.depth))
        )
        board = self.board.board[slicing]
        for kernel in Constants.KERNELS:
            if self.board.depth == 1 and kernel.shape[2] > 1:
                continue
            convolved = convolve((board == current_player.index).astype(int), kernel, mode='valid')
            if np.any(convolved == self.winning_streak):
                print(True)
                return True
        print(False)
        return False


