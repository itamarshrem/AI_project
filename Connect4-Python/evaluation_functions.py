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
    for kernel in WinningPatterns.PATTERNS.values():
        if board.depth == 1 and kernel.shape[2] > 1:
            continue
        convolved = convolve((board.board == player_index).astype(int), kernel, mode='valid', method='direct')
        others_convolved = convolve(((board.board != player_index) & (board.board != board.EMPTY_CELL)).astype(int), kernel, mode='valid', method='direct')
        not_blocked_streaks = convolved[others_convolved == 0]
        for streak in not_blocked_streaks:
            streaks[streak] += 1

    if winning_streak in streaks and streaks[winning_streak] > 0:
        return np.inf, streaks[winning_streak]

    max_streak = max(streaks.keys())
    return 2 ** max_streak, streaks[max_streak]

def _all_complex_evaluation_function(board, player_index, num_of_players, winning_streak):
    score = complex_evaluation_function(board, player_index, winning_streak)
    other_players = set(range(num_of_players)) - {player_index}
    max_opponents_streaks = 0
    max_opponents_streaks_appearance = 0
    alpha = 1 / (num_of_players - 1)
    for other_player in other_players:
        max_opponent_streaks, max_opponent_streaks_appearance = complex_evaluation_function(board, other_player, winning_streak)
        max_opponents_streaks += alpha * max_opponent_streaks
        if max_opponent_streaks == score[0]:
            max_opponents_streaks_appearance += max_opponent_streaks_appearance

    score_ = (score[0] - max_opponents_streaks, score[1] - max_opponents_streaks_appearance)
    return score_


def calc_max_streak(row):
    max_val = row.max()  # Find the maximum value in the row
    count = np.count_nonzero(row == max_val)  # Count how many times this max value appears
    return [ 2 ** max_val, count]

def update_max_streaks_score(player_streaks, cur_player_index, new_max_score_tuple):
    if cur_player_index not in player_streaks or new_max_score_tuple[0] > player_streaks[cur_player_index][0]:
        player_streaks[cur_player_index] = new_max_score_tuple
    elif new_max_score_tuple[0] == player_streaks[cur_player_index][0]:
        player_streaks[cur_player_index][1] = player_streaks[cur_player_index][1] + new_max_score_tuple[1]

def all_complex_evaluation_function(board, player_index, num_of_players, winning_streak):
    players_streaks = {}
    alpha = 1 / (num_of_players - 1)

    for direction, conv_res in board.conv_res_by_direction.items():
        mask = (conv_res.sum(axis=0) == conv_res)
        not_blocked_streaks = (conv_res * mask)
        new_max_score = calc_max_streak(not_blocked_streaks[player_index])
        update_max_streaks_score(players_streaks, player_index, new_max_score)

        next_player_index = (player_index + 1) % num_of_players
        while next_player_index != player_index:
            new_player_score = calc_max_streak(not_blocked_streaks[next_player_index])
            update_max_streaks_score(players_streaks, next_player_index, new_player_score)
            next_player_index = (next_player_index + 1) % num_of_players

    cur_player_score = players_streaks[player_index]
    if cur_player_score[0] == (2 ** winning_streak) and cur_player_score[1] > 0:
        score = (np.inf, players_streaks[player_index][1])
        # assert score == _all_complex_evaluation_function(board, player_index, num_of_players, winning_streak)
        return score

    max_opponents_streaks = 0
    max_opponents_streaks_appearance = 0
    next_player_index = (player_index + 1) % num_of_players
    while next_player_index != player_index:
        max_opponent_streaks, max_opponent_streaks_appearance = players_streaks[next_player_index]
        if max_opponent_streaks == (2 ** winning_streak) and max_opponent_streaks_appearance > 0:
            max_opponent_streaks = np.inf
        max_opponents_streaks += alpha * max_opponent_streaks
        if max_opponent_streaks == cur_player_score[0]:
            max_opponents_streaks_appearance += max_opponent_streaks_appearance
        next_player_index = (next_player_index + 1) % num_of_players

    final_score = (cur_player_score[0] - max_opponents_streaks, cur_player_score[1] - max_opponents_streaks_appearance)
    # assert final_score == _all_complex_evaluation_function(board, player_index, num_of_players, winning_streak)
    return final_score



    # if score[0] > opponent_score[0]:
    #     return score[0] - opponent_score[0], score[1]
    # return score[0] - opponent_scores[0], score[1] - opponent_scores[1]
