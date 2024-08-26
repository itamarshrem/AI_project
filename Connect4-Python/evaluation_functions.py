from collections import defaultdict
from winning_patterns import WinningPatterns
from scipy.signal import convolve
import numpy as np


def simple_evaluation_function(board, player_index):
    convolved = 0
    for kernel in WinningPatterns.PATTERNS:
        if board.depth == 1 and kernel.shape[2] > 1:
            continue
        convolved = max(convolved, np.max(convolve((board == player_index).astype(int), kernel, mode='valid')))
    return convolved


def complex_evaluation_function(board, player_index, winning_streak):
    streaks = defaultdict(lambda: 0)
    streaks[0] = 0
    for kernel in WinningPatterns.PATTERNS:
        if board.depth == 1 and kernel.shape[2] > 1:
            continue
        convolved = convolve((board.board == player_index).astype(int), kernel, mode='valid')
        if np.any(convolved >= winning_streak):
            return np.inf, np.inf
        others_convolved = convolve(((board.board != player_index) & (board.board != board.EMPTY_CELL)).astype(int), kernel, mode='valid')
        not_blocked_streaks = convolved[others_convolved == 0]
        for streak in not_blocked_streaks:
            streaks[streak] += 1
    max_streak = max(streaks.keys())
    return 2 ** max_streak, streaks[max_streak]
    # shift = min(max(board.rows, board.cols, board.depth), 32) - winning_streak
    # return 2**(max_streak + shift) + min(2**(max_streak + shift) - 1, streaks[max_streak])


def all_complex_evaluation_function(board, player_index, opponent_index, winning_streak):
    score = complex_evaluation_function(board, player_index, winning_streak)
    opponent_score = complex_evaluation_function(board, opponent_index, winning_streak)
    if score[0] != opponent_score[0]:
        return score[0] - opponent_score[0], score[1]
    return 0, score[1] - opponent_score[1]

