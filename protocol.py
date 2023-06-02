import random
import numpy as np

from config import (PLAYER_COLOR, TARGET_COLOR, TREASURE_COLOR, MAZE_SIZE, GOAL_POSITION,
                    UNKNOWN_COLOR, OBSTACLE_COLOR, FREE_CELL_COLOR, POSSIBLE_ACTIONS) 

 

def q(state, action, value_dict):
	result = value_dict.get(state, {}).get(action, 10)
	return result

def update(state, action, value, value_dict):
	state_values = value_dict.get(state, None)
	if state_values:
		state_values[action] = value
	else:
		value_dict[state] = {}
		value_dict[state][action] = value
		
def allowed_actions(input_state):
	
    #zlib.decompress(input_state).decode()
	state = input_state 
	
	allowed = ['UP','DOWN','RIGHT','LEFT']
	last_line = state.split('\n')[-1]
	for c in last_line:
		if c == 'P':
			allowed.remove('DOWN')
	first_line = state.split('\n')[0]
	for c in first_line:
		if c == 'P':
			allowed.remove('UP')
	line_length = MAZE_SIZE+1
	for i in range(MAZE_SIZE):
		if state[line_length*i] == 'P':
			allowed.remove('LEFT')
		if state[line_length*i + line_length - 1] == 'P':
			allowed.remove('RIGHT')

	return allowed
		
def policy(values, state, epsilon = 0.1):
	best_action = None
	best_value = float('-inf')
	
	# filter by possible actions. No bumping into walls.
	allowed = allowed_actions(state) 
	
    # shuffle to avoid bias
	random.shuffle(allowed) 
	for action in allowed:
		if q(state, action, values) > best_value:
			best_value = q(state, action, values)
			best_action = action

	r_var = random.random()
	if r_var < epsilon: #with probability epsilon...
		best_action = random.choice(allowed) #choose at random
		best_value = q(state, best_action, values)

	return best_action, best_value

def state_values(values, mock_env, GOAL_POSITION):
	state_matrix = [[0 for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]

	for i in range(MAZE_SIZE):
		for j in range(MAZE_SIZE):
			
			mock_env.position = np.asarray([i,j])
			mock_env.target_position = np.asarray(GOAL_POSITION)
			
			best_action = None
			state = mock_env.compressed_state_rep()
			best_value = float('-inf')
			allowed = allowed_actions(state)
			for action in allowed:
				if q(state, action, values) > best_value:
					best_value = q(state, action, values)
					best_action = action

			state_matrix[i][j] = round(best_value,1)

	for row in state_matrix:
		print(row)

def unique_starts(i):
	position = [0, 0]
	goal_position = GOAL_POSITION
	'''
	if i%2 == 0:
		position[0] = abs(MAZE_SIZE - position[0]) -1
		position[1] = abs(MAZE_SIZE - position[1]) -1
		goal_position[0] = abs(MAZE_SIZE - goal_position[0]) -1
		goal_position[1] = abs(MAZE_SIZE - goal_position[1]) -1
	
	if (position[0] == MAZE_SIZE//2) and (position[1] == MAZE_SIZE//2):
		position[1]+=1
	'''
	return position, goal_position