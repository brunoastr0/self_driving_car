import numpy as np

class QLearning:
    def __init__(self, num_states, num_actions, learning_rate=0.1, discount_factor=0.9, exploration_prob=0.1):
        self.num_states = num_states
        self.num_actions = num_actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_prob = exploration_prob

        # Initialize Q-values to zeros
        self.q_values = np.zeros((num_states, num_actions))

    def select_action(self, state):
        # Epsilon-greedy policy for action selection
        if np.random.rand() < self.exploration_prob:
            # Explore: Randomly choose an action
            action = np.random.randint(self.num_actions)
        else:
            # Exploit: Choose the action with the highest Q-value
            action = np.argmax(self.q_values[state])

        return action

    def update_q_values(self, state, action, reward, next_state):
        # Q-learning update rule
        current_q_value = self.q_values[state, action]
        best_next_q_value = np.max(self.q_values[next_state])
        new_q_value = current_q_value + self.learning_rate * (reward + self.discount_factor * best_next_q_value - current_q_value)
        self.q_values[state, action] = new_q_value
