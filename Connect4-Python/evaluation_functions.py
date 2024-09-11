import numpy as np

def calc_max_streak(row):
    max_val = row.max()  # Find the maximum value in the row
    count = np.count_nonzero(row == max_val)  # Count how many times this max value appears
    return [ 2 ** max_val, count]


def update_max_streaks_score(player_streaks, cur_player_index, new_max_score_tuple):
    if cur_player_index not in player_streaks or new_max_score_tuple[0] > player_streaks[cur_player_index][0]:
        player_streaks[cur_player_index] = new_max_score_tuple
    elif new_max_score_tuple[0] == player_streaks[cur_player_index][0]:
        player_streaks[cur_player_index][1] = player_streaks[cur_player_index][1] + new_max_score_tuple[1]


def complex_evaluation_function_helper(board, player_index, num_of_players, winning_streak, depth = 0, complex_mode=False):
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
    max_opponents_streaks = 0
    max_opponents_streaks_appearance = 0
    next_player_index = (player_index + 1) % num_of_players
    while next_player_index != player_index:
        max_opponent_streaks, max_opponent_streaks_appearance = players_streaks[next_player_index]
        if max_opponent_streaks == (2 ** winning_streak) and max_opponent_streaks_appearance > 0:
            max_opponent_streaks = 2 ** (winning_streak + 3)
        max_opponents_streaks += alpha * max_opponent_streaks
        if max_opponent_streaks == cur_player_score[0] or not complex_mode:
            max_opponents_streaks_appearance += max_opponent_streaks_appearance
        next_player_index = (next_player_index + 1) % num_of_players

    if cur_player_score[0] == (2 ** winning_streak) and cur_player_score[1] > 0:
        cur_player_score[0] = 2 ** (winning_streak + 3)
    return cur_player_score[0] - (depth / 100), cur_player_score[1], max_opponents_streaks - (depth / 100), max_opponents_streaks_appearance

def complex_evaluation_function(board, player_index, num_of_players, winning_streak, depth):
    cur_player_max_streak, cur_player_max_streak_app, max_opponents_streaks, max_opponents_streaks_app = \
        complex_evaluation_function_helper(board, player_index, num_of_players, winning_streak, depth, complex_mode=True)

    if cur_player_max_streak == (2 ** (winning_streak + 3)) and cur_player_max_streak_app > 0:
        return cur_player_max_streak, cur_player_max_streak_app

    final_score = (cur_player_max_streak - max_opponents_streaks, cur_player_max_streak_app - max_opponents_streaks_app)
    return final_score


def only_best_opponent_evaluation_function_helper(board, player_index, num_of_players, winning_streak, depth, complex_mode=False):
    players_streaks = {}

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

    opponents_scores = [score for i, score in players_streaks.items() if i != player_index]
    max_opponents_streaks_score = max(opponents_scores, key=lambda x: x[0])
    if max_opponents_streaks_score[0] == (2 ** winning_streak) and max_opponents_streaks_score[1] > 0:
        max_opponents_streaks_score[0] = 2 ** (winning_streak + 3)

    cur_player_score = players_streaks[player_index]
    if cur_player_score[0] == (2 ** winning_streak) and cur_player_score[1] > 0:
        cur_player_score[0] = 2 ** (winning_streak + 3)

    return cur_player_score[0], cur_player_score[1], max_opponents_streaks_score[0], max_opponents_streaks_score[0]


def only_best_opponent_evaluation_function(board, player_index, num_of_players, winning_streak, depth):
    cur_player_max_streak, cur_player_max_streak_app, max_opponents_streaks, max_opponents_streaks_app = \
        only_best_opponent_evaluation_function_helper(board, player_index, num_of_players, winning_streak, complex_mode=True)

    if cur_player_max_streak == (2 ** (winning_streak + 3)) and cur_player_max_streak_app > 0:
        return cur_player_max_streak, cur_player_max_streak_app

    final_score = (cur_player_max_streak - max_opponents_streaks, cur_player_max_streak_app - max_opponents_streaks_app)
    return final_score


def simple_evaluation_function(board, player_index, num_of_players, winning_streak, depth):
    cur_player_max_streak, cur_player_max_streak_app, max_opponents_streaks, max_opponents_streaks_app = \
        complex_evaluation_function_helper(board, player_index, num_of_players, winning_streak)

    return cur_player_max_streak - max_opponents_streaks


def ibef2_evaluation_function(board, player_index, num_of_players, winning_streak, depth):
    assert num_of_players == 2
    cur_streak_sum, opponent_streak_sum = 0, 0

    for direction, conv_res in board.conv_res_by_direction.items():
        mask = (conv_res.sum(axis=0) == conv_res)
        not_blocked_streaks = (conv_res * mask)
        cur_streak_sum += np.sum(2 ** not_blocked_streaks[player_index])
        opponent_streak_sum += np.sum(2 ** not_blocked_streaks[1 - player_index])
    return cur_streak_sum - opponent_streak_sum


def defensive_evaluation_function(board, player_index, num_of_players, winning_streak, depth):
    cur_player_max_streak, cur_player_max_streak_app, max_opponents_streaks, max_opponents_streaks_app = \
        complex_evaluation_function_helper(board, player_index, num_of_players, winning_streak)

    return -combine_scores(max_opponents_streaks, max_opponents_streaks_app)


def offensive_evaluation_function(board, player_index, num_of_players, winning_streak, depth):
    cur_player_max_streak, cur_player_max_streak_app, max_opponents_streaks, max_opponents_streaks_app = \
        complex_evaluation_function_helper(board, player_index, num_of_players, winning_streak)

    return combine_scores(cur_player_max_streak, cur_player_max_streak_app)


def combine_scores(max_streaks, max_streaks_appearance):
    assert max_streaks > 0 and max_streaks_appearance > 0
    shift = 1
    actual_max_streak = np.log2(max_streaks)
    shifted_max_streak = 2 ** (actual_max_streak + shift)
    bind_max_streaks_appearance = min(max_streaks_appearance, shifted_max_streak - 1)
    final_score = shifted_max_streak + bind_max_streaks_appearance
    return final_score
