import numpy as np
from PIL import Image

from make_maze import Generate_maze
from protocol import *
import config

def train(env, EPISODES=100, save_to = 'models/model3.dump'):
	env.reset()
	values = {}
	rewards_list = []
	steps_list = []
	step = 0
	last_path = []
	first_path = []
	for episoden in range(EPISODES):
		env.reset()
		position, goal_position = [0, 0], [3, 3]

		start_position = position
		env.position = np.asarray(position)
		env.target_position = np.asarray(goal_position)
		current_state = env.compressed_state_rep()
		use_epsilon = 0.1
		if episoden > 200:
			use_epsilon = 0.0
		action, action_v = policy(values, current_state, epsilon = use_epsilon)
		total_reward = 0
		#step = 0
		deltas = []

		while (not env.over):
			if episoden == 299:
				print(f'state: \n{current_state}')
				print(f'action chosen: {(action, action_v)}')
				last_path.append(action)
			if episoden == 0:
				first_path.append(action)
				

			step +=1
			reward = env.move(action)
			total_reward += reward
			next_state = env.compressed_state_rep()

			next_action, next_action_v = policy(values, next_state, epsilon = use_epsilon)
			

			if env.over: #one can only win.
				next_action_v = 100
				total_reward+=100

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

	env.reset()
	position, goal_position = [0, 0], config.GOAL_POSITION
	start_position = position
	env.position = np.asarray(position)
	env.target_position = np.asarray(goal_position)
	boards = env.sequences(last_path)
	frames = [Image.fromarray(frame, 'RGB') for frame in boards]
	path = 'media/last_iter_5.gif'
	
if __name__ == "__main__":
	blocked_squares = [[i, i-1] for i in range(1,3)]
	environment = Generate_maze(maze_dimensions = [MAZE_SIZE, MAZE_SIZE], 
	                    obstacle_positions = blocked_squares)
	train(env)
