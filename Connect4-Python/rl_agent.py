import numpy as np
import random

class RLAgent:
    def __init__(self, action_size, learning_rate=0.1, discount_factor=0.99, exploration_rate=1.0, exploration_decay=0.995):
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.q_table = {}

    def get_state_key(self, state):
        return str(state)

    def choose_action(self, state, legal_actions):
        if np.random.rand() < self.exploration_rate:
            return random.choice(legal_actions)
        state_key = self.get_state_key(state)
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_size)
        return np.argmax(self.q_table[state_key])

    def learn(self, state, action, reward, next_state, done):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_size)
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = np.zeros(self.action_size)
        q_update = reward
        if not done:
            q_update += self.discount_factor * np.max(self.q_table[next_state_key])
        self.q_table[state_key][action] += self.learning_rate * (q_update - self.q_table[state_key][action])
        if done:
            self.exploration_rate *= self.exploration_decay