import pygame
from Game import Game
from Constants import Constants
from Players import PlayerFactory


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    default_players_num = 2
    parser.add_argument('-p', '--players', nargs="*", type=str, default=["human"] * default_players_num, choices=["human", "random", "minmax", "alpha_beta"], help='human, random')
    parser.add_argument('-ef', '--eval_function', nargs="*", default=["None"] * default_players_num, type=str, choices=["simple", "complex", "None"], help='simple, complex, None')
    parser.add_argument('-d', '--depth', type=int, nargs="*", default=[2] * default_players_num, help='Depth of the search tree')
    parser.add_argument('-ws', '--winning_streak', type=int, default=4, help='Number of consecutive pieces to win')
    parser.add_argument('-s', '--sleep', action='store_true', help='Sleep between actions')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    Constants.set_winning_streak(args.winning_streak)
    print(Constants.WINNING_STREAK, Constants.KERNELS[0].shape)
    players = []
    player_index = 0
    for player_type in args.players:
        players.append(PlayerFactory.get_player(player_type, player_index, args.eval_function))
        player_index += 1
    game = Game(Constants.WINNING_STREAK, players, sleep_between_actions=args.sleep)
    game.run()
    pygame.time.wait(3000)










