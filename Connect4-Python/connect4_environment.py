# import numpy as np
# from game import Game
#
# class Connect4Env:
#     def __init__(self, game: Game):
#         self.game = game
#         self.state = self.game.board.board
#         self.done = False
#
#     def reset(self):
#         self.game.reset()
#         self.state = self.game.board.board
#         self.done = False
#         return self.state
#
#     def step(self, action):
#         player = self.game.players[self.game.current_player_index]
#         location = self.game.board.apply_action(action, player.index)
#         self.state = self.game.board.board
#         reward = self.get_reward(player, location)
#         self.done = self.game.game_finished()
#         return self.state, reward, self.done
#
#     def get_reward(self, player, location):
#         if self.game.winning_move(player, location):
#             return 1
#         elif self.done:
#             return 0
#         else:
#             return -0.1
#
#     def get_legal_actions(self):
#         return self.game.board.get_legal_actions()