import abc
from evaluation_functions import *


class Player:
    MIN_SCORE = -np.inf, -np.inf
    MAX_SCORE = np.inf, np.inf

    def __init__(self, index):
        self.index = index

    def get_action(self, board, num_of_players, winning_streak, ui=None):
        raise NotImplementedError()


class RandomPlayer(Player):
    def get_action(self, board, num_of_players, winning_streak, ui=None):
        legal_actions = board.get_legal_actions()
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
        if self.index == 0:
            self.MAX_PLAYER = 0
            self.MIN_PLAYER = 1
        else:
            self.MAX_PLAYER = 1
            self.MIN_PLAYER = 0

    @abc.abstractmethod
    def get_action(self, board, num_of_players, winning_streak, ui=None):
        return


class MinmaxAgent(MultiAgentSearchAgent):

    def get_action(self, board, num_of_players, winning_streak, ui=None):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """
        legal_actions = board.get_legal_actions()
        if self.depth == 0 or not legal_actions:
            return None
        max_value_found = self.MIN_SCORE
        action_for_max_value = None
        for action in legal_actions:
            successor = board.generate_successor(self.MAX_PLAYER, location=action)
            successor_value = self.__min_player(successor, self.depth - 1, winning_streak)
            if successor_value > max_value_found:
                max_value_found = successor_value
                action_for_max_value = action
        return action_for_max_value

    def __min_player(self, cur_state, cur_depth, winning_streak):
        legal_actions = cur_state.get_legal_actions()
        if cur_depth == 0 or not legal_actions:
            return self.evaluation_function(cur_state, self.MAX_PLAYER, self.MIN_PLAYER, winning_streak)
        min_value_found = self.MAX_SCORE
        for action in legal_actions:
            successor = cur_state.generate_successor(self.MIN_PLAYER, location=action)
            successor_value = self.__max_player(successor, cur_depth, winning_streak)
            if successor_value < min_value_found:
                min_value_found = successor_value
        return min_value_found

    def __max_player(self, cur_state, cur_depth, winning_streak):
        legal_actions = cur_state.get_legal_actions()
        if cur_depth == 0 or not legal_actions:
            return self.evaluation_function(cur_state, self.MAX_PLAYER, self.MIN_PLAYER, winning_streak)
        max_value_found = self.MIN_SCORE
        for action in legal_actions:
            successor = cur_state.generate_successor(self.MAX_PLAYER, location=action)
            successor_value = self.__min_player(successor, cur_depth - 1, winning_streak)
            if successor_value > max_value_found:
                max_value_found = successor_value
        return max_value_found


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, board, num_of_players, winning_streak, ui=None):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        action, value = self.__alphabeta_helper(board, self.MAX_PLAYER, 0, self.MIN_SCORE, self.MAX_SCORE, winning_streak)
        return action

    def __alphabeta_helper(self, cur_state, cur_player, cur_depth, a, b, winning_streak):
        legal_actions = cur_state.get_legal_actions(cur_player)
        if cur_depth == self.depth or not legal_actions:
            return None, self.evaluation_function(cur_state, self.MAX_PLAYER, self.MIN_PLAYER, winning_streak)
        if cur_player == self.MAX_PLAYER:
            return self.__max_helper(cur_state, cur_player, cur_depth, a, b, legal_actions, winning_streak)
        return self.__min_helper(cur_state, cur_player, cur_depth, a, b, legal_actions, winning_streak)

    def __max_helper(self, cur_state, cur_player, cur_depth, a, b, legal_actions, winning_streak):
        max_action = None
        for action in legal_actions:
            successor = cur_state.generate_successor(cur_player, location=action)
            _, new_a = self.__alphabeta_helper(successor, 1 - cur_player, cur_depth + cur_player, a, b, winning_streak)
            if new_a > a:
                a = new_a
                max_action = action
            if b <= a:
                break
        return max_action, a

    def __min_helper(self, cur_state, cur_player, cur_depth, a, b, legal_actions, winning_streak):
        min_action = None
        for action in legal_actions:
            successor = cur_state.generate_successor(cur_player, location=action)
            _, new_b = self.__alphabeta_helper(successor, 1 - cur_player, cur_depth + cur_player, a, b, winning_streak)
            if new_b < b:
                b = new_b
                min_action = b
            if b <= a:
                break
        return min_action, b


class PlayerFactory:
    @staticmethod
    def get_player(player_type, index, evaluation_function_name="", depth=2):
        evaluation_function = PlayerFactory.get_evaluation_function(evaluation_function_name)
        if player_type == "random":
            return RandomPlayer(index)
        elif player_type == "human":
            return HumanPlayer(index)
        elif player_type == "minmax":
            return MinmaxAgent(index, evaluation_function, depth)
        elif player_type == "alpha_beta":
            return AlphaBetaAgent(index)
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
