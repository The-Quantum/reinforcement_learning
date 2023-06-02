
PLAYER_COLOR = [0, 0, 255]
TARGET_COLOR = [0, 255, 0]     
TREASURE_COLOR = [0, 255, 255]   
UNKNOWN_COLOR = [0, 0, 0]
OBSTACLE_COLOR = [1, 1, 1]            
FREE_CELL_COLOR = [255, 255, 255]     

POSSIBLE_ACTIONS = {
	'RIGHT' : [0,1],
	'LEFT'  : [0,-1],
	'UP'    : [-1,0],
	'DOWN'  : [1,0]
}

MAZE_SIZE = 4
GAMMA = 0.9
alpha = 0.5
PLAYER_INITIAL_POSITION = [0, 0]
GOAL_POSITION = [3, 3]

state = 1
ALL_POSITIONS = {}
for x in range(MAZE_SIZE):
  for y in range(MAZE_SIZE):
      ALL_POSITIONS[state] = [x, y]
      state += 1

BLOCKED_SQUARES = [[i, i-1] for i in range(1,3)]

