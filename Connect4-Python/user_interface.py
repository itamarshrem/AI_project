import math

import numpy as np
import pygame
from board import Board
import sys

class Color:
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    MAGENTA = (255, 0, 255)

class BaseUI:
    def print_to_screen(self, board):
        raise NotImplementedError

    def display_board(self, board):
        raise NotImplementedError

class UI:
    SQUARESIZE = 100
    RADIUS = int(SQUARESIZE / 2 - 5)
    PLAYER_COLORS = [Color.RED, Color.YELLOW, Color.MAGENTA]

    def __init__(self, board: Board):
        self.width = board.cols * self.SQUARESIZE
        self.height = (board.rows + 1) * self.SQUARESIZE
        self.size = (self.width, self.height)
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.myfont = pygame.font.SysFont("monospace", 75)

    def print_to_screen(self, text):
        label = self.myfont.render(text, 1, Color.RED)
        self.screen.blit(label, (40, 10))
        pygame.display.update()

    def display_board(self, board):
        print(board)
        assert board.depth == 1
        for c in range(board.cols):
            for r in range(board.rows):
                pygame.draw.rect(self.screen, Color.BLUE, (c * self.SQUARESIZE, r * self.SQUARESIZE + self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, Color.BLACK,
                                   (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int(r * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)

        for c in range(board.cols):
            for r in range(board.rows):
                if board.board[r][c][0] == board.EMPTY_CELL:
                    continue
                pygame.draw.circle(self.screen, self.PLAYER_COLORS[int(board.board[r][c][0])],
                                   (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), self.height - int(r * self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)
        pygame.display.update()

    def get_player_input(self, player_index):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, Color.BLACK, (0, 0, self.width, self.SQUARESIZE))
                    posx = event.pos[0]
                    pygame.draw.circle(self.screen, self.PLAYER_COLORS[player_index], (posx, int(self.SQUARESIZE / 2)), self.RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, Color.BLACK, (0, 0, self.width, self.SQUARESIZE))
                    posx = event.pos[0]
                    col = int(math.floor(posx / self.SQUARESIZE))
                    return np.array([col, 0])  # depth is always 0 for the human player



class EmptyUI(BaseUI):
    def __init__(self):
        pass

    def print_to_screen(self, board):
        pass
    def display_board(self, board):
        pass

class UIFactory:
    @staticmethod
    def getUI(ui_configuration, board):
        if ui_configuration:
            return UI(board)
        return EmptyUI()