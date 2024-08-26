from collections import defaultdict

import pygame
from game import Game
from player import PlayerFactory
from winning_patterns import WinningPatterns


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    default_players_num = 2
    parser.add_argument('-size', '--board_shape', type=int, nargs=3, default=[5, 7, 1], help='size of the board')
    parser.add_argument('-p', '--players', nargs="*", type=str, default=["human"] * default_players_num, choices=["human", "random", "minmax", "alpha_beta"], help='human, random')
    parser.add_argument('-ef', '--eval_functions', nargs="*", default=["None"] * default_players_num, type=str, choices=["simple", "complex", "all_complex", "None"], help='simple, complex, None')
    parser.add_argument('-d', '--depths', type=int, nargs="*", default=[2] * default_players_num, help='Depth of the search tree')
    parser.add_argument('-ws', '--winning_streak', type=int, default=4, help='Number of consecutive pieces to win')
    parser.add_argument('-s', '--sleep', action='store_true', help='Sleep between actions')
    parser.add_argument('-ng', '--num_of_games', type=int, default=1, help='Number of consecutive games')
    parser.add_argument('-ui', '--display_screen', action='store_true', help='if set, ui is displayed')
    parser.add_argument('-bc', '--board_configuration', type=str, default="None", choices=["None", "edge_case1"], help='start a game with a specific board')

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
        players.append(PlayerFactory.get_player(player_type, player_index, args.eval_functions[player_index], args.depths[player_index]))
        player_index += 1
    return players


def print_results(results):
    for player, count in results.items():
        if player == Game.TIE:
            print(f"number of ties: {count}")
        print(f"player {player} won {count} games")


def run_all_games(num_of_games, game, display_screen, board_configuration, board_shape):
    results = defaultdict(lambda: 0)
    for i in range(num_of_games):
        game_result = game.run(display_screen, board_configuration, board_shape)
        pygame.time.wait(3000)
        results[game_result] += 1
    print_results(results)


if __name__ == '__main__':
    args = parse_args()
    validate_input(args)
    WinningPatterns.build_patterns(args.winning_streak)
    players = create_players(args)
    game = Game(args.winning_streak, players, sleep_between_actions=args.sleep)
    run_all_games(args.num_of_games, game, args.display_screen, args.board_configuration, args.board_shape)
