import time
from Env2048 import Env2048
import random
import numpy as np
from collections import namedtuple, deque
from itertools import count

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
# region New Approach
#   Forget CV. It's surprisingly garbage, (unless we want to train a CNN to extract score using labelled data we collect via the method below)
#   We just go straight for reading the html. Our agent's existence is a webdriver connection, and we use that to read
#   the score field in html to get our reward, and to send the keys for the moves. It's a helluva lot easier.
#   we could train CV out of this by using it to collect labelled image-score pairs, but should I even bother?
#   time will tell, I guess. 
# endregion

# How long to wait between perceptions
# this + processing time determines how long between actions

env = Env2048()
# if gpu is to be used
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


EPISODES = 30
LEARNING_RATE = 0.001
MEM_SIZE = 50000
BATCH_SIZE = 20
GAMMA = 0.999
EXPLORATION_MAX = 0.75
EXPLORATION_DECAY = 0.9
EXPLORATION_MIN = 0
FC1_DIMS = 512
FC2_DIMS = 1024
DEVICE = torch.device("cuda")

class Network(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.input_shape = 16
        self.action_space = 4

        self.fc1 = nn.Linear(self.input_shape, FC1_DIMS)
        self.fc2 = nn.Linear(FC1_DIMS, FC2_DIMS)
        self.fc3 = nn.Linear(FC2_DIMS, 512)
        self.fc4 = nn.Linear(512, self.action_space)

        self.optimizer = optim.Adam(self.parameters(), lr=LEARNING_RATE)
        self.loss = nn.MSELoss()
        self.to(DEVICE)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)

        return x
    
class ReplayBuffer:
    def __init__(self):
        self.mem_count = 0
        
        self.states = np.zeros((MEM_SIZE, 16),dtype=np.float32)
        self.actions = np.zeros(MEM_SIZE, dtype=np.int64)
        self.rewards = np.zeros(MEM_SIZE, dtype=np.float32)
        self.states_ = np.zeros((MEM_SIZE, 16),dtype=np.float32)
        self.dones = np.zeros(MEM_SIZE, dtype=bool)
    
    def add(self, state, action, reward, state_, done):
        mem_index = self.mem_count % MEM_SIZE
        
        self.states[mem_index]  = state
        self.actions[mem_index] = action
        self.rewards[mem_index] = reward
        self.states_[mem_index] = state_
        self.dones[mem_index] =  1 - done

        self.mem_count += 1
    
    def sample(self):
        MEM_MAX = min(self.mem_count, MEM_SIZE)
        batch_indices = np.random.choice(MEM_MAX, BATCH_SIZE, replace=True)
        
        states  = self.states[batch_indices]
        actions = self.actions[batch_indices]
        rewards = self.rewards[batch_indices]
        states_ = self.states_[batch_indices]
        dones   = self.dones[batch_indices]

        return states, actions, rewards, states_, dones
    

class DQN_Solver:
    def __init__(self, network = Network(), exploration_rate = EXPLORATION_MAX):
        self.memory = ReplayBuffer()
        self.exploration_rate = exploration_rate
        self.network = network

    def choose_action(self, observation):
        if random.random() < self.exploration_rate:
            return random.randint(0,len(env.actions)-1)
        
        state = torch.tensor(observation).float().detach()
        state = state.to(DEVICE)
        state = state.unsqueeze(0)
        q_values = self.network(state)
        return torch.argmax(q_values).item()
    
    def learn(self):
        if self.memory.mem_count < BATCH_SIZE:
            return
        
        states, actions, rewards, states_, dones = self.memory.sample()
        states = torch.tensor(states , dtype=torch.float32).to(DEVICE)
        actions = torch.tensor(actions, dtype=torch.long).to(DEVICE)
        rewards = torch.tensor(rewards, dtype=torch.float32).to(DEVICE)
        states_ = torch.tensor(states_, dtype=torch.float32).to(DEVICE)
        dones = torch.tensor(dones, dtype=torch.bool).to(DEVICE)
        batch_indices = np.arange(BATCH_SIZE, dtype=np.int64)

        q_values = self.network(states)
        next_q_values = self.network(states_)
        
        predicted_value_of_now = q_values[batch_indices, actions]
        predicted_value_of_future = torch.max(next_q_values, dim=1)[0]
        
        q_target = rewards + GAMMA * predicted_value_of_future * dones

        loss = self.network.loss(q_target, predicted_value_of_now)
        self.network.optimizer.zero_grad()
        loss.backward()
        self.network.optimizer.step()

        self.exploration_rate *= EXPLORATION_DECAY
        self.exploration_rate = max(EXPLORATION_MIN, self.exploration_rate)

    def returning_epsilon(self):
        return self.exploration_rate
best_reward = 0
best_score = 0
average_reward = 0
episode_number = []
average_reward_number = []
agent = DQN_Solver()
for i in range(1,EPISODES):
    state = env.reset()
    score = 0

    while True:

        action_idx = agent.choose_action(state)
        state_,reward,done = env.step(env.actions[action_idx])
        agent.memory.add(state,action_idx,score+reward,state_,done)
        agent.learn()
        score += reward
        print(f"Score: {score}")
        if done:
            if score > best_reward:
                best_reward = score
            average_reward += score
            print(f"Episode: {i} Avg Reward: {average_reward/i} Best Reward: {best_reward}, Last Reward: {score}, Epsilon: {agent.returning_epsilon()}")
            episode_number.append(i)
            average_reward_number.append(average_reward/i)
            break

            