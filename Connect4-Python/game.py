import time
from initial_boards import BoardFactory
from user_interface import UIFactory
from player import Player

class Game:
    TIE = -1

    def __init__(self, winning_streak, players, sleep_between_actions):
        self.winning_streak = winning_streak
        self.players = players
        self.sleep_between_actions = sleep_between_actions
        self.ui = None
        self.board = None
        self._should_quit = False

    def does_players_contain_rl(self):
        for index, player in enumerate(self.players):
            if player.__name__() == "QLearningPlayer":
                return index
        return -1

    def run(self, display_ui, board_configuration, board_shape):
        self._should_quit = False
        self.board = BoardFactory.get_board(board_configuration, board_shape, len(self.players))
        self.ui = UIFactory.getUI(display_ui, self.board, len(self.players))
        self.ui.display_initial_message()
        self.ui.display_board(self.board)
        rl_index = self.does_players_contain_rl()
        if rl_index != -1 and self.players[rl_index].is_currently_learning():
            result = self._rl_game_loop(rl_index, len(self.players))
        else:
            result = self._game_loop()
        self.display_result_in_ui(result)
        return result

    def display_result_in_ui(self, result):
        if result == self.TIE:
            msg = "It's a tie!"
            result = 0
        else:
            msg = f"Player {result} wins!"
        self.ui.print_to_screen(msg, player_index=result)


    def _game_loop(self):
        player_index = 0
        while not self.board.is_board_full():
            player = self.players[player_index]
            if self.sleep_between_actions:
                time.sleep(1)
            action = player.get_action(self.board, len(self.players), self.winning_streak, self.ui)
            self.board.apply_action(action, player.index, self.winning_streak)
            self.ui.display_board(self.board)
            if self.board.have_we_won(self.winning_streak):
                return player_index
            player_index = (player_index + 1) % len(self.players)
        return self.TIE

    def _rl_game_loop(self, rl_index, num_of_players):
        rl_player = self.players[rl_index]
        cur_player_index = 0
        winning_player = self.TIE
        while cur_player_index != rl_index and winning_player == self.TIE and not self.board.is_board_full():
            winning_player, _ = self.play_turn(cur_player_index)
            cur_player_index = Player.get_next_player(cur_player_index, num_of_players)

        while winning_player == self.TIE and not self.board.is_board_full():
            board_before_rl = self.board.__copy__()
            winning_player, rl_action = self.play_turn(rl_index)
            board_after_rl = self.board.__copy__()
            cur_player_index = Player.get_next_player(cur_player_index, num_of_players)
            while cur_player_index != rl_index and (not self.board.is_board_full() and winning_player == self.TIE):
                winning_player, _ = self.play_turn(cur_player_index)
                cur_player_index = Player.get_next_player(cur_player_index, num_of_players)
            rl_player.update_q_table(board_before_rl, rl_action, board_after_rl, self.board, self.winning_streak)
        return winning_player

    def play_turn(self, player_index):
        player = self.players[player_index]
        action = player.get_action(self.board, len(self.players), self.winning_streak, self.ui)
        self.board.apply_action(action, player.index, self.winning_streak)
        self.ui.display_board(self.board)
        if self.board.have_we_won(self.winning_streak):
            return player_index, action
        return self.TIE, action

