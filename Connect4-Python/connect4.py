from collections import defaultdict
import time
import numpy as np
from game import Game
from player import PlayerFactory
from winning_patterns import WinningPatterns
import utils
from create_plots import plot_data


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-size', '--board_shape', type=int, nargs=3, required=True, help='size of the board')
    parser.add_argument('-p', '--players', nargs="*", type=str, required=True, choices=["human", "random", "minmax", "alpha_beta", "rl_agent", "baseline"], help='human, random, minmax, alpha_beta, rl_agent, baseline')
    parser.add_argument('-ef', '--eval_functions', nargs="*", required=True, type=str, choices=["simple", "complex",  "defensive", "offensive", "ibef2", "none", 'only_best_opponent'], help='simple, complex, defensive, offensive, ibef2, none, only_best_opponent')
    num_of_players_inputted = len(parser.parse_known_args()[0].players)
    parser.add_argument('-d', '--depths', type=int, nargs="*", default= [2 * num_of_players_inputted] * num_of_players_inputted, help='Depth of the search tree')
    parser.add_argument('-g', '--gamma', type=float, nargs="*", default=[0] * num_of_players_inputted, help='probability of random action of MultiAgentSearchAgent')
    parser.add_argument('-ws', '--winning_streak', type=int, required=True, help='Number of consecutive pieces to win')
    parser.add_argument('-s', '--sleep', action='store_true', help='Sleep between actions')
    parser.add_argument('-lrl', '--load_rl_agent', action='store_true', help='load rl agent from memory')
    parser.add_argument('--rl_currently_learning', action='store_true', help= 'if set, the rl_agent is learning')
    parser.add_argument('-ng', '--num_of_games', type=int, required=True, help='Number of consecutive games')
    parser.add_argument('-ui', '--display_screen', action='store_true', help='if set, ui is displayed')
    parser.add_argument('-bc', '--board_configuration', type=str, default="None", choices=["None", "edge_case1"], help='start a game with a specific board')

    parsed_args = parser.parse_args()
    return parsed_args

def validate_input(args):
    assert len(args.players) > 1, "Number of players should be at least 2"
    assert np.sum(np.array(args.board_shape) > 1) > 1, "Board shape should have at least 2 dimensions"
    minimum_of_board_shape = min(args.board_shape[0], args.board_shape[1], args.board_shape[2] if args.board_shape[2] > 1 else np.inf)
    assert args.winning_streak <= minimum_of_board_shape, "winning streak should be less than the minimum of the board shape"
    assert args.winning_streak > 0, "winning streak should be positive"
    if not len(args.players) == len(args.eval_functions) == len(args.depths) == len(args.gamma):
        raise ValueError("Number of players, evaluation functions, depths and gammas should be the same, non relevant values for different players are ignored")

def create_players(args):
    players = []
    player_index = 0
    for player_type in args.players:
        players.append(PlayerFactory.get_player(player_type, player_index, args))
        player_index += 1
    return players


def print_results(results, num_of_games, game):
    for player, count in results.items():
        if player == Game.TIE:
            print(f"number of ties: {count}, tie percentage: {(count * 100 / num_of_games)}%")
        else:
            print(f"player {game.players[player].__name__()} (index {player}) won {count} games. winning percentage: {count * 100 / num_of_games}%")


def run_all_games(num_of_games, game, display_screen, board_configuration, board_shape, rl_currently_learning):
    victories = []
    results = defaultdict(lambda: 0)
    for i in range(num_of_games):
        start_time = time.time()
        game_result = game.run(display_screen, board_configuration, board_shape)
        results[game_result] += 1
        print(f"player {game.players[game_result].__name__()} with index {game_result} won the game. winning percentage: {results[game_result] * 100 / (i + 1)}%")
        print(f"game {i + 1}: time taken: {time.time() - start_time} seconds")
        if game.players[game_result].__name__() == "QLearningPlayer":
            victories.append(1)
        else:
            victories.append(0)
    if rl_currently_learning:
        np_victories = np.array(victories)
        np_victories = (np.cumsum(np_victories) * 100) / np.arange(1, num_of_games + 1)
        plot_data([np_victories], ["rl agent"], "RL agent winning percentage during training", "game number",
                  "percentage of winning so far")

    print_results(results, num_of_games, game)
    for player in game.players:
        step_time_average = player.get_step_average_time()
        if step_time_average is not None:
            print(f"player {player.index} average step time: {step_time_average}")


def save_rl_agent(args, players):
    ql_index = args.players.index("rl_agent")
    file_name = utils.get_rl_agent_save_path(args.winning_streak, args.board_shape, ql_index)
    utils.save_rl_agent_qtable(file_name, players[ql_index])
    utils.zip_rl_agent_qtable(file_name)


def main(args):
    players = create_players(args)
    game = Game(args.winning_streak, players, sleep_between_actions=args.sleep)
    run_all_games(args.num_of_games, game, args.display_screen, args.board_configuration, args.board_shape, args.rl_currently_learning)
    if args.rl_currently_learning:
        save_rl_agent(args, players)


if __name__ == '__main__':
    args = parse_args()
    validate_input(args)
    WinningPatterns.build_shapes(args.winning_streak, args.board_shape)
    main(args)
