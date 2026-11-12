import numpy as np
import random
import os
import joblib

class DQNTrafficBrain:
    """
    Advanced Reinforcement Learning Agent (Q-Learning / Neural Approximation) 
    for Adaptive Traffic Signal Timing Optimization.
    """
    def __init__(self, state_size=4, action_size=3):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = 0.95      # Discount factor
        self.epsilon = 1.0     # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        
        # Initialize lightweight Q-table weights for edge/low-resource execution
        self.q_table = np.zeros((10, 10, 10, 10, action_size))

    def discretize_state(self, state):
        """Discretize continuous traffic telemetry into state bins."""
        return tuple(min(9, max(0, int(val // 5))) for val in state)

    def act(self, state):
        """Select action using Epsilon-Greedy policy."""
        s_bin = self.discretize_state(state)
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        return np.argmax(self.q_table[s_bin])

    def train_step(self, state, action, reward, next_state):
        """Perform a single Q-learning update step."""
        s_bin = self.discretize_state(state)
        next_s_bin = self.discretize_state(next_state)
        
        target = reward + self.gamma * np.amax(self.q_table[next_s_bin])
        self.q_table[s_bin][action] += self.learning_rate * (target - self.q_table[s_bin][action])
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save_model(self, filepath="model.pkl"):
        joblib.dump(self.q_table, filepath)

    def load_model(self, filepath="model.pkl"):
        if os.path.exists(filepath):
            self.q_table = joblib.load(filepath)

if __name__ == "__main__":
    brain = DQNTrafficBrain()
    print("DATG Reinforcement Learning Brain Initialized Successfully.")
    
