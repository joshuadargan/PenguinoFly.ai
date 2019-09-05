import random
import tensorflow as tf
# Helper libraries
import numpy as np


class Brain:

    def __init__(self, learning_rate=0.1, discount=0.95, exploration_rate=1.0, iterations=10000):
        self.learning_rate = learning_rate
        self.discount = discount  # How much we appreciate future reward over current
        self.exploration_rate = exploration_rate  # Initial exploration rate
        self.exploration_delta = 1.0 / iterations  # Shift from exploration to exploitation

        # Input has five neurons, each a different value
        self.input_count = 5
        # Output is one neuron representing whether to flap
        self.output_count = 1

        self.session = tf.Session()
        self.define_model()
        self.session.run(self.initializer)

    # Define tensorflow model graph
    def define_model(self):
        # Input is an array of 5 items (state one-hot)
        # NOTE: In this example we assume no batching.
        self.model_input = tf.placeholder(dtype=tf.float32, shape=[None, self.input_count])

        # Two hidden layers of 16 neurons with sigmoid activation initialized to zero for stability
        fc1 = tf.layers.dense(self.model_input, 16, activation=tf.nn.relu,
                              kernel_initializer=tf.constant_initializer(np.zeros((self.input_count, 16))))
        fc2 = tf.layers.dense(fc1, 16, activation=tf.nn.relu,
                              kernel_initializer=tf.constant_initializer(np.zeros((16, self.output_count))))

        # Output is one value, Q for flapping
        # Output is 2-dimensional, due to possibility of batched training data
        # NOTE: In this example we assume no batching.
        self.model_output = tf.layers.dense(fc2, self.output_count)

        # This is for feeding training output (a.k.a ideal target values)
        self.target_output = tf.placeholder(shape=[None, self.output_count], dtype=tf.float32)
        # Loss is mean squared difference between current output and ideal target values
        loss = tf.losses.mean_squared_error(self.target_output, self.model_output)
        # Optimizer adjusts weights to minimize loss, with the speed of learning_rate
        self.optimizer = tf.train.GradientDescentOptimizer(learning_rate=self.learning_rate).minimize(loss)
        # Initializer to set weights to initial values
        self.initializer = tf.global_variables_initializer()

    # Ask model to estimate Q value for specific state (inference)
    def get_Q(self, state):
        # Model input: Single state represented by array of 5 items (state one-hot)
        # Model output: Array of Q values for single state
        return self.session.run(self.model_output, feed_dict={self.model_input: np.asarray(state)})[0]

    # Turn state into 2d one-hot tensor
    # Example: 3 -> [[0,0,0,1,0]]
    ##def to_one_hot(self, state):
    ##one_hot = np.zeros((1, 5))
    ##one_hot[0, [state]] = 1
    ##return one_hot

    def get_next_action(self, state):
        if random.random() > self.exploration_rate:  # Explore (gamble) or exploit (greedy)
            return self.greedy_action(state)
        else:
            return self.random_action()

    # Which action (FORWARD or BACKWARD) has bigger Q-value, estimated by our model (inference).
    def greedy_action(self, state):
        # argmax picks the higher Q-value and returns the index (FORWARD=0, BACKWARD=1)
        temp = self.get_Q(state)
        print("Testing greedy_action: " + str(temp))
        print("Testing greedy_action [0]:" + str(temp[0]))
        return temp

    def random_action(self):
        return True if random.random() < 0.5 else False

    def train(self, old_state, action, reward, new_state):
        # Ask the model for the Q values of the old state (inference)
        old_state_Q_values = self.get_Q(old_state)

        # Ask the model for the Q values of the new state (inference)
        new_state_Q_values = self.get_Q(new_state)

        # Real Q value for the action we took. This is what we will train towards.
        #[action]
        old_state_Q_values = reward + self.discount * np.amax(new_state_Q_values)

        # Setup training data
        training_input = old_state
        target_output = [old_state_Q_values]
        training_data = {self.model_input: training_input, self.target_output: target_output}

        # Train
        self.session.run(self.optimizer, feed_dict=training_data)

    def update(self, old_state, new_state, action, reward):
        # Train our model with new data
        self.train(old_state, action, reward, new_state)

        # Finally shift our exploration_rate toward zero (less gambling)
        if self.exploration_rate > 0:
            self.exploration_rate -= self.exploration_delta


class BrainControl:
    master_brain = Brain()