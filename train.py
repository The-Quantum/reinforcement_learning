import numpy as np
from PIL import Image

from generate_maze import Generate_maze
from protocol import *
import config
import utils

def train(environment, EPISODES=300, binary_path = 'models/model3.dump'):
	environment.reset()
	values = {}
	rewards_list = []
	steps_list = []
	step = 0
	last_path = []
	first_path = []
	for episoden in range(EPISODES):
		environment.reset()
		position, goal_position = config.PLAYER_INITIAL_POSITION, config.GOAL_POSITION

		environment.player_position = np.asarray(position)
		environment.target_position = np.asarray(goal_position)
		current_state = environment.compressed_state_rep()
		use_epsilon = 0.1
		if episoden > 200:
			use_epsilon = 0.0

		action, action_v = policy(
			values, current_state, epsilon = use_epsilon
			)
		
		total_reward = 0
		
		deltas = []

		while (not environment.over):
			if episoden == 299:
				print(f'state: \n{current_state}')
				print(f'action chosen: {(action, action_v)}')
				last_path.append(action)
			if episoden == 0:
				first_path.append(action)
				
			step +=1
			reward = environment.move(action)
			total_reward += reward
			next_state = environment.compressed_state_rep()

			next_action, next_action_v = policy(values, next_state, epsilon = use_epsilon)
			

			if environment.over: #one can only win.
				next_action_v = 100
				total_reward += 100

			delta = next_action_v * config.GAMMA + reward - action_v
			deltas.append(delta)
			new_value = action_v + delta * config.alpha
			update(current_state, action, new_value, values)
			current_state = next_state
			action = next_action
			action_v = next_action_v


		rewards_list.append(total_reward)
		steps_list.append(step)

	with open('steps.txt', 'w') as f:
		output = str(steps_list)+'\n'+str(values)
		f.write(output)

	environment.reset()
	position, goal_position = [0, 0], config.GOAL_POSITION

	start_position = position
	environment.player_position = np.asarray(position)
	environment.target_position = np.asarray(goal_position)
	boards = environment.sequences(last_path)
	frames = [Image.fromarray(frame, 'RGB') for frame in boards]

	path = 'output/Output.gif'
	utils.make_gif(frames, path)
	
if __name__ == "__main__":

	blocked_squares = [[i, i-1] for i in range(1,3)]

	environment = Generate_maze(
		maze_dimensions = [MAZE_SIZE, MAZE_SIZE], 
	    obstacle_positions = blocked_squares
		)
	
	train(environment)
