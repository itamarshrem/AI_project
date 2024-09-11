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
    GREEN = (0, 255, 0)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)

class BaseUI:
    def print_to_screen(self, msg, player_index):
        raise NotImplementedError

    def display_board(self, board):
        raise NotImplementedError
    def display_initial_message(self):
        raise NotImplementedError

class UI:
    SQUARESIZE = 100
    RADIUS = int(SQUARESIZE / 2 - 5)
    PLAYER_COLORS = [Color.RED, Color.YELLOW, Color.MAGENTA, Color.GREEN, Color.ORANGE, Color.PURPLE]

    def __init__(self, board: Board):
        self.width = board.cols * self.SQUARESIZE
        self.height = (board.rows + 1) * self.SQUARESIZE
        self.size = (self.width, self.height)
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.myfont = pygame.font.SysFont("monospace", 75)

    def print_to_screen(self, text, player_index):
        label = self.myfont.render(text, 1, UI.PLAYER_COLORS[player_index])
        self.screen.blit(label, (40, 10))
        pygame.display.update()
        pygame.time.wait(3000)
    def display_initial_message(self):
        pass

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

    def print_to_screen(self, msg, player_index):
        pass
    def display_board(self, board):
        pass
    def display_initial_message(self):
        pass

class UI3D(BaseUI):
    def __init__(self, board: Board):
        self.rows, self.cols, self.depth = board.rows, board.cols, board.depth

    def display_initial_message(self):
        print("welcome to 3D connect 4! each board displayed on the screen, represents a depth in the 3D board.\n"
              "So leftmost board is in depth 0, the next one is in depth 1 and so on.\n"
              "In order to play, you need to enter the column and depth you want to play, seperated by coma.\n"
              "for example, in board of shape (6, 7, 5) and winning streak of 4, the next inputs will lead you to win,\n"
              "in case someone else didn't insert disks in the winning pattern:\n"
              "0, 0\n"
              "0, 1\n"
              "0, 2\n"
              "0, 3\n"
              "Good luck!\n")
    def display_board(self, board):
        print(board)
    def get_player_input(self, player_index):
        input_str = input("Enter column and depth, seperated by coma: ")
        input_arr = input_str.replace(" ", "").split(",")
        while len(input_arr) != 2 or not (input_arr[0].isdigit() and input_arr[1].isdigit()):
            input_str = input("Enter column and depth, seperated by coma: ")
            input_arr = input_str.replace(" ", "").split(",")
        column, depth = input_arr[0], input_arr[1]
        return np.array([int(column), int(depth)])
    def print_to_screen(self, msg, player_index):
        print(msg)

class UIFactory:
    @staticmethod
    def getUI(ui_configuration, board):
        if ui_configuration and board.depth > 1:
            return UI3D(board)
        if ui_configuration:
            return UI(board)
        return EmptyUI()