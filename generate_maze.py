import numpy as np

from utils import *
from config import (PLAYER_COLOR, TARGET_COLOR, TREASURE_COLOR, 
                    UNKNOWN_COLOR, OBSTACLE_COLOR, POSSIBLE_ACTIONS,
                    FREE_CELL_COLOR)

class Generate_maze():
    def __init__(self, 
                maze_dimensions = [4,4],
                player_position=np.asarray([0,0]),
                target_position = np.asarray([3,3]),
                treasure_position=np.asarray([2,2]), 
                obstacle_positions = []):
        
        self.maze_dimensions = maze_dimensions
        self.player_position = player_position
        self.target_position = target_position
        self.treasure_position = treasure_position
        self.obstacle_positions = obstacle_positions
        self.blocked_map = {str(k): True for k in obstacle_positions}
        self.maze_width = maze_dimensions[0]
        self.maze_height = maze_dimensions[1]
        self.maze_color_mask = np.zeros(
			shape=[self.maze_width, self.maze_height, 3],
	        dtype=np.uint8)
	
        i, j = self.player_position
        for h in range(i-1, i+2):
            for w in range(j-1, j+2):
                if self.bound_check([h,w]):
                    self.maze_color_mask[h][w] = [1,1,1]

    def bound_check(self, coordinates):
        x, y = coordinates
        return (x >= 0 and x < self.maze_height) and (y >= 0 and y < self.maze_width)

    def bump(self, coordinates):
        x, y = coordinates
        return self.blocked_map.get(str([x, y]), False)
    
    def environment_color_map(self): #underlying_scene
        # initialize color map for the maze in white
        maze_color_map = np.ones(
            shape = [self.maze_width, self.maze_height,3], 
            dtype=np.uint8
        )
        maze_color_map = maze_color_map * 255
        
        # Generate the full white canvas
        x, y = self.player_position
        maze_color_map[x][y] = PLAYER_COLOR

        x_target, y_target = self.target_position
        maze_color_map[x_target][y_target] = TARGET_COLOR

        x_treasure, y_treasure = self.treasure_position
        maze_color_map[x_treasure][y_treasure] = TREASURE_COLOR
        
        for blocked_square in self.obstacle_positions:
            maze_color_map[blocked_square[0]][blocked_square[1]] = OBSTACLE_COLOR

        return maze_color_map * self.maze_color_mask

    def visible_scene(self):
      full_scence_picture = self.environment_color_map() 
      return full_scence_picture * self.visible_mask
    
    def color_maze(self):
        # initialized full maze color with colored feature
        maze_feature_color = self.environment_color_map()
        return maze_feature_color * self.maze_color_mask
    
    def make_maze_img(self, fog = True):
        IMG_SCALE_FACTOR = 20
        environment = self.color_maze() if fog else self.environment_color_map()
        environment = environment.repeat(
            IMG_SCALE_FACTOR, axis=0).repeat(IMG_SCALE_FACTOR, axis=1)
         
        return environment

    def sequences(self, steps):

      pictures = [self.make_maze_img()]

      for step in steps:
        self.move(step)
        pictures.append(self.make_maze_img())
      
      return pictures

    def compressed_state_rep(self):

      string_rep = self.current_state_string()
      
      return string_rep #zlib.compress(string_rep.encode('ASCII'))

    def current_state_string(self):
      visible_scene = self.environment_color_map()

      string_representation = ''
      for i in range(self.maze_height):
        for j in range(self.maze_width):
          string_representation += color_to_char(visible_scene[i][j])

        string_representation +='\n'

      return string_representation

    def move(self, direction):
      assert direction in ['UP','DOWN','RIGHT','LEFT']
      new_position = self.player_position + POSSIBLE_ACTIONS[direction]
      reward = 0
      old_position = self.player_position

      if self.bound_check(new_position) and (not self.bump(new_position)):
        self.player_position = new_position
      else:
        reward = -1

      # calculate and store reward
      if (self.player_position[0] == self.target_position[0]) and (self.player_position[1] == self.target_position[1]):
        print("SUCCESSFULL !!!")
        reward = 10 
        self.over = True


      self.rewards.append(reward)
      self.total_reward += reward

      # update visible mask
      i, j = self.player_position
      for h in range(i-1, i+2):
        for w in range(j-1, j+2):
          if self.bound_check([h,w]):
            self.maze_color_mask[h][w] = [1,1,1]

      return reward*1.0

    def reset(self):
        self.target_position = np.random.randint(0, self.maze_width, [2], dtype = np.uint8)
        self.player_position = np.random.randint(0, self.maze_width, [2], dtype = np.uint8)
        self.rewards = []
        self.total_reward = 0
        self.over = False
        self.maze_color_mask = np.zeros(shape = [self.maze_width,self.maze_height, 3], dtype=np.uint8)
        i, j = self.player_position
        for h in range(i-1, i+2):
            for w in range(j-1, j+2):
                if self.bound_check([h,w]):
                    self.maze_color_mask[h][w] = [1,1,1]

        
if __name__ == "__main__":
    maze = Generate_maze()
    env = maze.make_maze_img()
    print(env)
    print(env[:,:,0])