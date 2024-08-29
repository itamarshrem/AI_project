import abc
import random
import time
from abc import abstractmethod

from evaluation_functions import *
from game import Game
import pickle
import os

def compute_path_to_rl_agent_file(relative_file_name):
    current_directory = os.getcwd()
    return current_directory + "/" + relative_file_name


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


class HumanPlayer(Player):
    def get_action(self, board, num_of_players, winning_streak, ui=None):
        player_input = ui.get_player_input(self.index)
        while not board.is_valid_location(player_input):
            player_input = ui.get_player_input(self.index)
        return player_input


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

    def __init__(self, index, evaluation_function=None, depth=2):
        super(MultiAgentSearchAgent, self).__init__(index)
        self.evaluation_function = evaluation_function
        self.depth = depth
        self.step_times = []
        # if self.index == 0:
        #     self.MAX_PLAYER = 0
        #     self.MIN_PLAYER = 1
        # else:
        #     self.MAX_PLAYER = 1
        #     self.MIN_PLAYER = 0

    def get_action(self, board, num_of_players, winning_streak, ui=None):
        start_time = time.time()
        action = self._get_action(board, num_of_players, winning_streak, ui)
        time_taken = time.time() - start_time
        self.step_times.append(time_taken)
        # print(f"Time taken for move: {time_taken}")
        return action

    @abstractmethod
    def _get_action(self, board, num_of_players, winning_streak, ui=None):
        return

    def get_step_average_time(self):
        return np.mean(self.step_times)



class MinmaxAgent(MultiAgentSearchAgent):

    def _get_action(self, board, num_of_players, winning_streak, ui=None):
        legal_actions = board.get_legal_actions(winning_streak)
        if self.depth == 0 or not legal_actions:
            return None
        max_value_found = self.MIN_SCORE
        action_for_max_value = None
        next_player_index = self.get_next_player(self.index, num_of_players)
        for action in legal_actions:
            successor = board.generate_successor(self.index, location=action, winning_streak=winning_streak)
            successor_value = self.__min_player(successor, self.depth, num_of_players, next_player_index, winning_streak)
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
                successor_value = self.__min_player(successor, cur_depth, num_of_players, next_player_index, winning_streak)
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
            successor_value = self.__min_player(successor, cur_depth, num_of_players, next_player_index, winning_streak)
            if successor_value > max_value_found:
                max_value_found = successor_value
        return max_value_found


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

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
            return self.__max_helper(cur_state, next_player, cur_depth - 1, a, b, num_of_players, legal_actions, winning_streak)
        return self.__min_helper(cur_state, next_player, cur_depth, a, b, num_of_players, legal_actions, winning_streak)

    def __max_helper(self, cur_state, cur_player, cur_depth, a, b, num_of_players, legal_actions, winning_streak):
        max_action = None
        for action in legal_actions:
            successor = cur_state.generate_successor(cur_player, location=action, winning_streak=winning_streak)
            _, new_a = self.__alphabeta_helper(successor, self.get_next_player(cur_player, num_of_players), cur_depth, a, b, num_of_players, winning_streak)
            if new_a > a or max_action is None:
                a = new_a
                max_action = action
            if b <= a:
                break
        return max_action, a

    def __min_helper(self, cur_state, cur_player, cur_depth, a, b, num_of_players, legal_actions, winning_streak):
        min_action = None
        for action in legal_actions:
            successor = cur_state.generate_successor(cur_player, location=action, winning_streak=winning_streak)
            _, new_b = self.__alphabeta_helper(successor, self.get_next_player(cur_player, num_of_players), cur_depth, a, b, num_of_players, winning_streak)
            if new_b < b or min_action is None:
                b = new_b
                min_action = b
            if b <= a:
                break
        return min_action, b


class QLearningPlayer(Player):
    class ActionCreator:
        def __init__(self, board_shape):
            self.board_shape = board_shape

        def __call__(self):
            return np.zeros((self.board_shape[1], self.board_shape[2]))

    def __init__(self, index, board_shape, currently_learning=False, learning_rate=0.1, discount_factor=0.95, exploration_rate=1.0, exploration_decay=1):
        super().__init__(index)
        self.currently_learning = currently_learning
        self.step_times = []
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        action_creator = QLearningPlayer.ActionCreator(board_shape)
        self.q_table = defaultdict(action_creator)

    def set_is_learning(self, is_currently_learning):
        self.currently_learning = is_currently_learning
    def set_exploration_decay(self, exploration_decay):
        self.exploration_decay = exploration_decay

    def get_action(self, board, num_of_players, winning_streak, ui=None):
        start_time = time.time()
        state = self.get_state_representation(board)
        legal_actions = board.get_legal_actions(winning_streak)
        legal_actions_indices = [action[0] for action in legal_actions], [action[1] for action in legal_actions]
        if self.currently_learning:
            if np.random.rand() < self.exploration_rate:
                action = random.choice(legal_actions)
            else:
                q_values = self.q_table[state]
                q_values_for_legal_actions = q_values[legal_actions_indices]
                action = legal_actions[np.argmax(q_values_for_legal_actions)]

            next_board = board.generate_successor(self.index, action, winning_streak)
            reward = self.calculate_reward(next_board, num_of_players, winning_streak)
            self.learn(board, action, reward, next_board)
        else:
            q_values = self.q_table[state]
            q_values_for_legal_actions = q_values[legal_actions_indices]
            action = legal_actions[np.argmax(q_values_for_legal_actions)]
        time_taken = time.time() - start_time
        self.step_times.append(time_taken)
        return action

    def monte_carlo_simulation(self, board, num_of_players, winning_streak, steps=None):
        next_board = board.__copy__()
        cur_player = self.get_next_player(self.index, num_of_players)
        i = 0
        while steps is None or i < steps:
            if next_board.have_we_won(winning_streak):
                return cur_player
            elif next_board.is_board_full():
                return Game.TIE
            legal_actions = next_board.get_legal_actions(winning_streak)
            action = random.choice(legal_actions)
            next_board = next_board.generate_successor(cur_player, location=action, winning_streak=winning_streak)
            cur_player = self.get_next_player(cur_player, num_of_players)
            i += 1

        return Game.TIE

    def calculate_reward(self, board, num_of_players, winning_streak, num_of_simulations=10):
        reward = 0
        for i in range(num_of_simulations):
            result = self.monte_carlo_simulation(board, num_of_players, winning_streak)
            if result == self.index:
                reward += 1000
            elif result == Game.TIE:
                pass
            else:
                reward -= 1000

        return reward / num_of_simulations



    def learn(self, board, action, reward, next_board):
        state = self.get_state_representation(board)
        next_state = self.get_state_representation(next_board)

        # Get max Q-value for the next state
        next_max_q_value = np.max(self.q_table[next_state])

        # Q-learning update rule
        self.q_table[state][action] = (1 - self.learning_rate) * self.q_table[state][action] + \
                                      self.learning_rate * (reward + self.discount_factor * next_max_q_value)

        # Decay exploration rate
        self.exploration_rate *= self.exploration_decay

    def get_state_representation(self, board):
        """
        This method returns a tuple that uniquely represents the state of the 3d board.
        """
        return tuple(board.board.flatten())

    def stop_learning(self):
        self.currently_learning = False

    def get_step_average_time(self):
        return np.mean(self.step_times)


class PlayerFactory:
    @staticmethod
    def get_player(player_type, index, args):
        evaluation_function = PlayerFactory.get_evaluation_function(args.eval_functions[index])
        if player_type == "random":
            return RandomPlayer(index)
        elif player_type == "human":
            return HumanPlayer(index)
        elif player_type == "minmax":
            return MinmaxAgent(index, evaluation_function, args.depths[index])
        elif player_type == "alpha_beta":
            return AlphaBetaAgent(index, evaluation_function, args.depths[index])
        elif player_type == "rl_agent":
            ql_index = 0
            depth = 2
            file_name = f"qlearning_player_ws_{args.winning_streak}_players_2_shape_{args.board_shape}_index_{ql_index}_depth_{depth}.pkl"
            full_path = compute_path_to_rl_agent_file(file_name)
            if args.load_rl_agent:
                with open(full_path, 'rb') as file_object:
                    q_learning_player = pickle.load(file_object)
                    q_learning_player.set_is_learning(False)
                    q_learning_player.set_exploration_decay(0.995)
                    return q_learning_player
            else:
                return QLearningPlayer(index, args.board_shape, currently_learning=False)
        else:
            raise ValueError(f"Unknown player type: {player_type}")

    @staticmethod
    def get_evaluation_function(evaluation_function):
        if evaluation_function == "simple":
            return simple_evaluation_function
        elif evaluation_function == "complex":
            return complex_evaluation_function
        elif evaluation_function == "all_complex":
            return all_complex_evaluation_function
        else:
            return None
