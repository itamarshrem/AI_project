from collections import defaultdict

from scipy.signal import convolve
import numpy as np
import Constants


def simple_evaluation_function(board, player_index):
    convolved = 0
    for kernel in Constants.KERNELS:
        if board.depth == 1 and kernel.shape[2] > 1:
            continue
        convolved += np.max(convolve((board == player_index).astype(int), kernel, mode='valid'))
    return convolved


def complex_evaluation_function(board, player_index):
    streaks = defaultdict(lambda: 0)
    for kernel in Constants.KERNELS:
        if board.depth == 1 and kernel.shape[2] > 1:
            continue
        convolved = convolve((board == player_index).astype(int), kernel, mode='valid')
        others_convolved = convolve(((board != player_index) & (board != 0)).astype(int), kernel, mode='valid')
        not_blocked_streaks = convolved[others_convolved == 0]
        for streak in not_blocked_streaks:
            streaks[streak] += 1
        max_streak = max(streaks.keys())
    return max_streak * streaks[max_streak]
