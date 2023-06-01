import config


def color_to_char(color):

	color = list(color)
	if color == config.TARGET_COLOR:
		return 'G'
	if color == config.PLAYER_COLOR:
		
		return 'P'
	if color == config.UNKNOWN_COLOR:
		return 'U'
	if color == config.FREE_CELL_COLOR:
		return 'W'
	if color == config.OBSTACLE_COLOR:
		
		return 'B'
	else:
		print('dead color found')
		return 'W'

def manhattan_distance(pointA, pointB):
	x , y = pointA
	x2, y2 = pointB
	return abs(x - x2) + abs(y - y2)


def make_gif(frames, path="output"):

    frame_one = frames[0]
    frame_one.save(path, format="GIF", append_images=frames,
               save_all=True, duration=100, loop=0)

