import time
import utils

from abc import abstractmethod
from evaluation_functions import *
from board import Board

class Player:
    MIN_SCORE = -np.inf, -np.inf
    MAX_SCORE = np.inf, np.inf

    def __init__(self, index):
        self.index = index

    def get_action(self, board, num_of_players, winning_streak, ui=None):
        raise NotImplementedError()

    def get_step_average_time(self):
        return

    @staticmethod
    def get_next_player(cur_player, num_of_players):
        return (cur_player + 1) % num_of_players



class RandomPlayer(Player):
    def get_action(self, board, num_of_players, winning_streak, ui=None):
        legal_actions = board.get_legal_actions(winning_streak)
        return legal_actions[np.random.choice(len(legal_actions))]

    def __name__(self):
        return "RandomPlayer"


class HumanPlayer(Player):
    def get_action(self, board, num_of_players, winning_streak, ui=None):
        player_input = ui.get_player_input(self.index)
        while not board.is_valid_location(player_input):
            player_input = ui.get_player_input(self.index)
        return player_input

    def __name__(self):
        return "HumanPlayer"


class MultiAgentSearchAgent(Player):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, index, evaluation_function=None, depth=2, eval_func_return_depth=2, gamma=0.0):
        super(MultiAgentSearchAgent, self).__init__(index)
        self.evaluation_function = evaluation_function
        self.depth = depth
        self.gamma = gamma
        self.step_times = []
        if eval_func_return_depth != 2:
            self.MAX_SCORE = tuple([np.inf] * eval_func_return_depth)
            self.MIN_SCORE = tuple([-np.inf] * eval_func_return_depth)



    def get_action(self, board, num_of_players, winning_streak, ui=None):
        start_time = time.time()
        if np.random.rand() >= self.gamma:
            action = self._get_action(board, num_of_players, winning_streak, ui)
        else:
            legal_actions = board.get_legal_actions(winning_streak)
            action = legal_actions[np.random.choice(len(legal_actions))]
        time_taken = time.time() - start_time
        self.step_times.append(time_taken)
        return action

    @abstractmethod
    def _get_action(self, board, num_of_players, winning_streak, ui=None):
        raise NotImplementedError()

    def get_step_average_time(self):
        return np.mean(self.step_times)

class MinmaxAgent(MultiAgentSearchAgent):

    def __name__(self):
        return "MinmaxAgent_" + self.evaluation_function.__name__

    def _get_action(self, board, num_of_players, winning_streak, ui=None):
        legal_actions = board.get_legal_actions(winning_streak)
        if self.depth == 0 or not legal_actions:
            return None
        max_value_found = self.MIN_SCORE
        action_for_max_value = None
        next_player_index = self.get_next_player(self.index, num_of_players)
        for action in legal_actions:
            successor = board.generate_successor(self.index, location=action, winning_streak=winning_streak)
            successor_value = self.__min_player(successor, self.depth - 1, num_of_players, next_player_index, winning_streak)
            if successor_value > max_value_found or action_for_max_value is None:
                max_value_found = successor_value
                action_for_max_value = action
        return action_for_max_value

    def __min_player(self, cur_state, cur_depth, num_of_players, cur_player_idx, winning_streak):
        legal_actions = cur_state.get_legal_actions(winning_streak)
        if cur_depth == 0 or not legal_actions:
            return self.evaluation_function(cur_state, self.index, num_of_players, winning_streak)
        min_value_found = self.MAX_SCORE
        next_player_index = self.get_next_player(cur_player_idx, num_of_players)
        for action in legal_actions:
            successor = cur_state.generate_successor(cur_player_idx, location=action, winning_streak=winning_streak)
            if next_player_index == self.index:
                successor_value = self.__max_player(successor, cur_depth - 1, num_of_players, winning_streak)
            else:
                successor_value = self.__min_player(successor, cur_depth - 1, num_of_players, next_player_index, winning_streak)
            if successor_value < min_value_found:
                min_value_found = successor_value
        return min_value_found

    def __max_player(self, cur_state, cur_depth, num_of_players, winning_streak):
        legal_actions = cur_state.get_legal_actions(winning_streak)
        if cur_depth == 0 or not legal_actions:
            return self.evaluation_function(cur_state, self.index, num_of_players, winning_streak)
        max_value_found = self.MIN_SCORE
        next_player_index = self.get_next_player(self.index, num_of_players)
        for action in legal_actions:
            successor = cur_state.generate_successor(self.index, location=action, winning_streak=winning_streak)
            successor_value = self.__min_player(successor, cur_depth - 1, num_of_players, next_player_index, winning_streak)
            if successor_value > max_value_found:
                max_value_found = successor_value
        return max_value_found


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def __name__(self):
        return "AlphaBetaAgent_" + self.evaluation_function.__name__

    def _get_action(self, board, num_of_players, winning_streak, ui=None):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        action, value = self.__alphabeta_helper(board, self.index, self.depth, self.MIN_SCORE, self.MAX_SCORE, num_of_players, winning_streak)
        return action

    def __alphabeta_helper(self, cur_state, next_player, cur_depth, a, b, num_of_players, winning_streak):
        legal_actions = cur_state.get_legal_actions(winning_streak)
        if cur_depth == 0 or not legal_actions:
            return None, self.evaluation_function(cur_state, self.index, num_of_players, winning_streak)
        if next_player == self.index:
            return self.__max_helper(cur_state, next_player, cur_depth, a, b, num_of_players, legal_actions, winning_streak)
        return self.__min_helper(cur_state, next_player, cur_depth, a, b, num_of_players, legal_actions, winning_streak)

    def __max_helper(self, cur_state, cur_player, cur_depth, a, b, num_of_players, legal_actions, winning_streak):
        max_action = None
        for action in legal_actions:
            successor = cur_state.generate_successor(cur_player, location=action, winning_streak=winning_streak)
            _, new_a = self.__alphabeta_helper(successor, self.get_next_player(cur_player, num_of_players), cur_depth - 1, a, b, num_of_players, winning_streak)
            if new_a > a or max_action is None:
                a = new_a
                max_action = action
            if b <= a:
                break
        return max_action, a

    def __min_helper(self, cur_state, cur_player, cur_depth, a, b, num_of_players, legal_actions, winning_streak):
        if cur_depth == 0 or not legal_actions:
            return None, self.evaluation_function(cur_state, self.index, num_of_players, winning_streak)
        min_action = None
        for action in legal_actions:
            successor = cur_state.generate_successor(cur_player, location=action, winning_streak=winning_streak)
            _, new_b = self.__alphabeta_helper(successor, self.get_next_player(cur_player, num_of_players), cur_depth - 1, a, b, num_of_players, winning_streak)
            if new_b < b or min_action is None:
                b = new_b
                min_action = action
            if b <= a:
                break
        return min_action, b


class BaselinePlayer(MultiAgentSearchAgent):

    def __name__(self):
        return "BaselinePlayer_" + self.evaluation_function.__name__

    def __init__(self, index, evaluation_function=None):
        super().__init__(index, evaluation_function)
        self.step_times = []

    def _get_action(self, board, num_of_players, winning_streak, ui=None):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        legal_actions = board.get_legal_actions(winning_streak)
        if not legal_actions:
            return None, self.evaluation_function(board, self.index, num_of_players, winning_streak)

        actions_values = []
        for action in legal_actions:
            successor = board.generate_successor(self.index, location=action, winning_streak=winning_streak)
            value = self.evaluation_function(successor, self.index, num_of_players, winning_streak)
            actions_values.append(value)

        actions_values = np.array(actions_values)
        min_value = np.min(actions_values)
        if min_value < 0:
            actions_values -= min_value
        if np.sum(actions_values) == 0:
            actions_values = np.ones(len(actions_values))
        # apply softmax on the values and choose a random action based on the probabilities
        probabilities = actions_values / np.sum(actions_values)
        action = legal_actions[np.random.choice(len(legal_actions), p=probabilities)]
        return action


class QLearningPlayer(Player):

    def __name__(self):
        return "QLearningPlayer"

    def __init__(self, index, board_shape, num_of_players, with_master=True, currently_learning=False, q_table=None, learning_rate=0.1, discount_factor=0.8, exploration_rate=1, exploration_decay=0.9999539):
        super().__init__(index)
        self.currently_learning = currently_learning
        self.step_times = []
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.board_shape = board_shape
        self.num_of_players = num_of_players
        if with_master:
            evaluation_function = PlayerFactory.get_evaluation_function("all_complex")
            self.master = AlphaBetaAgent(index, evaluation_function, 2, 2, 0)
        else:
            self.master = RandomPlayer(index)
        if q_table is None:
            self.q_table = {}
        else:
            self.q_table = q_table

    def is_currently_learning(self):
        return self.currently_learning


    def get_q_values(self, state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros((self.board_shape[1], self.board_shape[2]))
        return self.q_table[state]

    def get_q_value(self, state, action):
        return self.get_q_values(state)[action]

    def get_action(self, board: Board, num_of_players, winning_streak, ui=None):
        start_time = time.time()
        state = self.get_state_representation(board)
        legal_actions = board.get_legal_actions(winning_streak)
        legal_actions_indices = [action[0] for action in legal_actions], [action[1] for action in legal_actions]
        if self.currently_learning:
            if np.random.rand() < self.exploration_rate:
                action = self.master.get_action(board, num_of_players, winning_streak)
            else:
                q_values = self.get_q_values(state)
                q_values_for_legal_actions = q_values[legal_actions_indices]
                action = legal_actions[np.argmax(q_values_for_legal_actions)]

        else:
            q_values = self.get_q_values(state)
            q_values_for_legal_actions = q_values[legal_actions_indices]
            action = legal_actions[np.argmax(q_values_for_legal_actions)]
        time_taken = time.time() - start_time
        self.step_times.append(time_taken)
        return action


    def update_q_table(self, board_before_rl, rl_action, board_after_rl, board_after_opponents, winning_streak):
        reward = self.calculate_reward(board_after_rl, board_after_opponents, winning_streak)
        self.learn(board_before_rl, rl_action, reward, board_after_opponents)


    def calculate_reward(self, board_after_rl, board_after_opponents, winning_streak):
        if board_after_rl.have_we_won(winning_streak):
            return 500
        if board_after_opponents.have_we_won(winning_streak):
            number_of_steps = np.ceil(np.sum(board_after_opponents.board != -1) / self.num_of_players)
            return -500 + number_of_steps
        if board_after_rl.is_board_full() or board_after_opponents.is_board_full():
            return 200
        return -1


    def learn(self, board, action, reward, next_board):
        action = tuple(action)
        state = self.get_state_representation(board)
        next_state = self.get_state_representation(next_board)

        next_q_values = self.get_q_values(next_state)
        next_max_q_value = np.max(next_q_values)

        cur_q_value = self.get_q_value(state, action)
        self.q_table[state][action] = (
                (1 - self.learning_rate) * cur_q_value + self.learning_rate * (reward + self.discount_factor * next_max_q_value)
        )

        self.exploration_rate *= self.exploration_decay

    def get_state_representation(self, board):
        """
        This method returns a tuple that uniquely represents the state of the 3d board.
        """
        sum_per_column = np.sum(board.board != Board.EMPTY_CELL, axis=0)
        not_blocked_streaks = []
        for conv_res in board.conv_res_by_direction.values():
            mask = (conv_res.sum(axis=0) == conv_res)
            not_blocked_streaks.append((conv_res * mask).flatten())
        state = tuple(sum_per_column.flatten()) + tuple(np.concatenate(not_blocked_streaks))
        return state


    def get_step_average_time(self):
        return np.mean(self.step_times)

class PlayerFactory:
    @staticmethod
    def get_player(player_type, index, args):
        evaluation_function = PlayerFactory.get_evaluation_function(args.eval_functions[index])
        eval_func_return_depth = 1 if args.eval_functions[index] in {'simple', 'ibef2'} else 2
        if player_type == "random":
            return RandomPlayer(index)
        elif player_type == "human":
            return HumanPlayer(index)
        elif player_type == "minmax":
            return MinmaxAgent(index, evaluation_function, args.depths[index], eval_func_return_depth, args.gamma[index])
        elif player_type == "alpha_beta":
            return AlphaBetaAgent(index, evaluation_function, args.depths[index], eval_func_return_depth, args.gamma[index])
        elif player_type == "rl_agent":
            return PlayerFactory.create_rl_agent(args, index)
        elif player_type == "baseline":
            return BaselinePlayer(index, evaluation_function)
        else:
            raise ValueError(f"Unknown player type: {player_type}")

    @staticmethod
    def create_rl_agent(args, index):
        if args.load_rl_agent:
            full_path_filename = utils.get_rl_agent_save_path(args.winning_streak, args.board_shape, index)
            utils.extract_files_from_zip(args.winning_streak, args.board_shape, index)
            q_table = utils.get_qtable_from_file(full_path_filename)
            return QLearningPlayer(index, args.board_shape, len(args.players), currently_learning=args.rl_currently_learning, q_table=q_table)

        return QLearningPlayer(index, args.board_shape, len(args.players), currently_learning=args.rl_currently_learning, q_table=None)
    
    @staticmethod
    def get_evaluation_function(evaluation_function):
        if evaluation_function == "simple":
            return simple_evaluation_function
        elif evaluation_function == "all_complex":
            return all_complex_evaluation_function
        elif evaluation_function == "defensive":
            return defensive_evaluation_function
        elif evaluation_function == "offensive":
            return offensive_evaluation_function
        elif evaluation_function == "ibef2":
            return ibef2_evaluation_function
        elif evaluation_function == "only_best_opponent":
            return only_best_opponent_evaluation_function
        else:
            return None
