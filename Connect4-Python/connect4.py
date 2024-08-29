from collections import defaultdict

import time
import random

import numpy as np
from game import Game
from player import PlayerFactory
from winning_patterns import WinningPatterns
import pickle


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    default_players_num = 2
    parser.add_argument('-size', '--board_shape', type=int, nargs=3, default=[6, 7, 1], help='size of the board')
    parser.add_argument('-p', '--players', nargs="*", type=str, default=["human"] * default_players_num,
                        choices=["human", "random", "minmax", "alpha_beta", "rl_agent"], help='human, random')
    parser.add_argument('-ef', '--eval_functions', nargs="*", default=["none"] * default_players_num, type=str,
                        choices=["simple", "complex", "all_complex", "none"], help='simple, complex, None')
    parser.add_argument('-d', '--depths', type=int, nargs="*", default=[2] * default_players_num,
                        help='Depth of the search tree')
    parser.add_argument('-ws', '--winning_streak', type=int, default=4, help='Number of consecutive pieces to win')
    parser.add_argument('-s', '--sleep', action='store_true', help='Sleep between actions')
    parser.add_argument('-lrl', '--load_rl_agent', action='store_true', help='load rl agent from memory')
    parser.add_argument('-ng', '--num_of_games', type=int, default=1, help='Number of consecutive games')
    parser.add_argument('-ui', '--display_screen', action='store_true', help='if set, ui is displayed')
    parser.add_argument('-bc', '--board_configuration', type=str, default="None", choices=["None", "edge_case1"],
                        help='start a game with a specific board')

    return parser.parse_args()


def validate_input(args):
    if len(args.players) != len(args.eval_functions):
        raise ValueError("Number of players and evaluation functions should be the same")
    if len(args.players) != len(args.depths):
        raise ValueError("Number of players and depths should be the same")


def create_players(args):
    players = []
    player_index = 0
    for player_type in args.players:
        players.append(PlayerFactory.get_player(player_type, player_index, args))
        player_index += 1
    return players


def print_results(results, num_of_games):
    for player, count in results.items():
        if player == Game.TIE:
            print(f"number of ties: {count}, tie percentage: {(count * 100 / num_of_games)}%")
        else:
            print(f"player {player} won {count} games, winning percentage: {count * 100 / num_of_games}%")


def run_all_games(num_of_games, game, display_screen, board_configuration, board_shape):
    results = defaultdict(lambda: 0)
    for i in range(num_of_games):
        # save time
        start_time = time.time()
        game_result = game.run(display_screen, board_configuration, board_shape)
        results[game_result] += 1
        print(
            f"game {i + 1}: player {game_result} won!! he has winning percentage of {results[game_result] * 100 / (i + 1)}%")
        print(f"game {i + 1}: time taken: {time.time() - start_time} seconds")
    print_results(results, num_of_games)
    for player in game.players:
        step_time_average = player.get_step_average_time()
        if step_time_average is not None:
            print(f"player {player.index} average step time: {step_time_average}")


def train_qlearning_player(num_of_games, board_shape, winning_streak, load_qlearning_player=False):
    ql_index = 0
    depth = 2
    qlearning_player = PlayerFactory.create_rl_agent(winning_streak, board_shape, ql_index, depth, load_qlearning_player)
    minmax_player = PlayerFactory.get_player("minmax", 1 - ql_index, args)
    players = [qlearning_player, minmax_player]
    game = Game(winning_streak, players, sleep_between_actions=False)
    run_all_games(num_of_games, game, False, "None", board_shape)
    # save the qlearning player
    file_name = PlayerFactory.get_rl_agent_save_path(winning_streak, board_shape, ql_index, depth)
    with open(file_name, 'wb') as file_object:
        pickle.dump(qlearning_player.q_table, file_object)




def main(args):
    players = create_players(args)
    game = Game(args.winning_streak, players, sleep_between_actions=args.sleep)
    run_all_games(args.num_of_games, game, args.display_screen, args.board_configuration, args.board_shape)


if __name__ == '__main__':
    random.seed(0)
    np.random.seed(0)
    args = parse_args()
    validate_input(args)
    WinningPatterns.build_shapes(args.winning_streak, args.board_shape)
    main(args)
    # train_qlearning_player(args.num_of_games, args.board_shape, args.winning_streak, load_qlearning_player=False)
