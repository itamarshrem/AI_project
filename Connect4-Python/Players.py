import numpy as np
import pygame
from Constants import Constants
import math
import sys
import abc
from EvaluationFunctions import simple_evaluation_function, complex_evaluation_function

class Player:
    def __init__(self, index, color):
        self.index = index
        self.color = color

    def get_action(self, board, screen=None):
        raise NotImplementedError()


class RandomPlayer(Player):
    def get_action(self, board, screen=None):
        legal_actions = board.get_legal_actions()
        return legal_actions[np.random.choice(len(legal_actions))]


class HumanPlayer(Player):

    def get_action(self, board, screen=None):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, Constants.BLACK, (0, 0, Constants.width, Constants.SQUARESIZE))
                    posx = event.pos[0]
                    pygame.draw.circle(screen, self.color, (posx, int(Constants.SQUARESIZE / 2)), Constants.RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, Constants.BLACK, (0, 0, Constants.width, Constants.SQUARESIZE))
                    # print(event.pos)
                    posx = event.pos[0]
                    col = int(math.floor(posx / Constants.SQUARESIZE))
                    location = np.array([col, 0]) # depth is always 0 for the human player
                    if board.is_valid_location(location):
                        return location


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

    def __init__(self, index, color, evaluation_function=None, depth=2):
        super(MultiAgentSearchAgent, self).__init__(index, color)
        self.evaluation_function = evaluation_function
        self.depth = depth
        if self.index == 1:
            self.MAX_PLAYER = 1
            self.MIN_PLAYER = 2
        else:
            self.MAX_PLAYER = 2
            self.MIN_PLAYER = 1

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):
    MAX_PLAYER = 0
    MIN_PLAYER = 1

    def get_action(self, game_state):
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
        legal_actions = game_state.get_legal_actions(self.MAX_PLAYER)
        if self.depth == 0 or not legal_actions:
            return None
        max_value_found = -np.inf
        action_for_max_value = None
        for action in legal_actions:
            successor = game_state.generate_successor(self.MAX_PLAYER, location=action)
            successor_value = self.__min_player(successor, self.depth - 1)
            if successor_value > max_value_found:
                max_value_found = successor_value
                action_for_max_value = action
        return action_for_max_value

    def __min_player(self, cur_state, cur_depth):
        legal_actions = cur_state.get_legal_actions(self.MIN_PLAYER)
        if cur_depth == 0 or not legal_actions:
            return self.evaluation_function(cur_state, self.MIN_PLAYER)
        min_value_found = np.inf
        for action in legal_actions:
            successor = cur_state.generate_successor(self.MIN_PLAYER, location=action)
            successor_value = self.__max_player(successor, cur_depth)
            if successor_value < min_value_found:
                min_value_found = successor_value
        return min_value_found

    def __max_player(self, cur_state, cur_depth):
        legal_actions = cur_state.get_legal_actions(self.MAX_PLAYER)
        if cur_depth == 0 or not legal_actions:
            return self.evaluation_function(cur_state, self.MAX_PLAYER)
        max_value_found = -np.inf
        for action in legal_actions:
            successor = cur_state.generate_successor(self.MAX_PLAYER, location=action)
            successor_value = self.__min_player(successor, cur_depth - 1)
            if successor_value > max_value_found:
                max_value_found = successor_value
        return max_value_found


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    MAX_PLAYER = 0
    MIN_PLAYER = 1

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        action, value = self.__alphabeta_helper(game_state, 0, 0, -np.inf, np.inf)
        # print(f"alphabeta value is: {value}")
        return action

    def __alphabeta_helper(self, cur_state, cur_player, cur_depth, a, b):
        legal_actions = cur_state.get_legal_actions(cur_player)
        if cur_depth == self.depth or not legal_actions:
            return None, self.evaluation_function(cur_state)
        if cur_player == self.MAX_PLAYER:
            return self.__max_helper(cur_state, cur_player, cur_depth, a, b, legal_actions)
        return self.__min_helper(cur_state, cur_player, cur_depth, a, b, legal_actions)

    def __max_helper(self, cur_state, cur_player, cur_depth, a, b, legal_actions):
        max_action = None
        for action in legal_actions:
            successor = cur_state.generate_successor(cur_player, location=action)
            _, new_a = self.__alphabeta_helper(successor, 1 - cur_player, cur_depth + cur_player, a, b)
            if new_a > a:
                a = new_a
                max_action = action
            if b <= a:
                break
        return max_action, a

    def __min_helper(self, cur_state, cur_player, cur_depth, a, b, legal_actions):
        min_action = None
        for action in legal_actions:
            successor = cur_state.generate_successor(cur_player, location=action)
            _, new_b = self.__alphabeta_helper(successor, 1 - cur_player, cur_depth + cur_player, a, b)
            if new_b < b:
                b = new_b
                min_action = b
            if b <= a:
                break
        return min_action, b



class PlayerFactory:
    @staticmethod
    def get_player(player_type, index, evaluation_function_name="", depth=2):
        color = Constants.PLAYER_COLORS[index - 1]
        evaluation_function = PlayerFactory().get_evaluation_function(evaluation_function_name)
        if player_type == "random":
            return RandomPlayer(index, color)
        elif player_type == "human":
            return HumanPlayer(index, color)
        elif player_type == "minmax":
            return MinmaxAgent(index, color, evaluation_function, depth)
        elif player_type == "alpha_beta":
            return AlphaBetaAgent(index, color)
        else:
            raise ValueError(f"Unknown player type: {player_type}")

    def get_evaluation_function(self, evaluation_function):
        if evaluation_function == "simple":
            return simpleEvaluationFunction
        elif evaluation_function == "complex":
            return complexEvaluationFunction
        else:
            return None