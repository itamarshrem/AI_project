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
        others_convolved = convolve(((board.board != player_index) & (board.board != board.EMPTY_CELL)).astype(int), kernel, mode='valid')
        not_blocked_streaks = convolved[others_convolved == 0]
        for streak in not_blocked_streaks:
            streaks[streak] += 1

    if winning_streak in streaks and streaks[winning_streak] > 0:
        return np.inf, streaks[winning_streak]

    max_streak = max(streaks.keys())
    return 2 ** max_streak, streaks[max_streak]


def all_complex_evaluation_function(board, player_index, num_of_players, winning_streak):
    score = complex_evaluation_function(board, player_index, winning_streak)
    other_players = set(range(num_of_players)) - {player_index}
    max_opponents_streaks = 0
    max_opponents_streaks_appearance = 0
    alpha = 1 / (num_of_players - 1)
    for other_player in other_players:
        max_opponent_streaks, max_opponents_streaks_appearance = complex_evaluation_function(board, other_player, winning_streak)
        max_opponents_streaks += alpha * max_opponent_streaks
        if max_opponent_streaks == score[0]:
            max_opponents_streaks_appearance += max_opponents_streaks_appearance

    return score[0] - max_opponents_streaks, score[1] - max_opponents_streaks_appearance