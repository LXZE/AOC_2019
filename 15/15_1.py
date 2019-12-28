from copy import copy
# from collections import defaultdict as ddict
from collections import deque
import random
import intcode
import pickle


file = open('input_15.txt', 'r')
codes = file.readlines()[0][:-1].split(',')
legacy_codes = list(map(int, codes))
print(len(legacy_codes))

# code init
code = copy(legacy_codes)
clock = 0
base = 0
inputs = []
output = 0

start = (0, 0)
visit = {}
visit[start] = '.'
current = [e for e in start]

to_visit = []

output = None
while output is not None:

	# action = random.randrange(1,5)
	# select action from current state and to visit state
	# first check that NEWS are unknown area
	# second add list of unknown area to togo list
	# get action from first

	action = random.randrange(1, 5)
	inputs = [action]
	next_state = move(current, action)

	code, clock, base, inputs, output = intcode.run_code(code, clock, base, inputs)
	if output == 0:
		visit[tuple(next_state)] = '#'
	elif output == 1:
		visit[tuple(next_state)] = '.'
		# add undiscovered nodes
		# if undiscovered nodes not in visited node then add to next list
		current = next_state
	elif output == 2:
		print('found oxygen at', current)
		break
	print('current at ', current, end='\r')
	# visualise visit?

with open('save.pickle', 'rb') as handle:
	visit = pickle.load(handle)

known = []
for key in visit.keys():
	known.append(key)
x = list(map(lambda x: x[0], known))
y = list(map(lambda x: x[1], known))
min_x, max_x = min(x), max(x)
min_y, max_y = min(y), max(y)
offset_x = abs(min_x)
offset_y = abs(min_y)

oxygen = [-14, 11]
start = [0, 0]

screen = []
for i in range(max_x+offset_x+1):
	screen.append([])
	for j in range(max_y+offset_y+1):
		screen[i].append(' ')

for key, val in visit.items():
	screen[key[0]+offset_x][key[1]+offset_y] = '@' if val == '#' else val

screen[start[0]+offset_x][start[1]+offset_y] = 'D'
screen[oxygen[0]+offset_x][oxygen[1]+offset_y] = '*'

grid = []
for row in range(max_y+offset_y+1):
	tmp = ''
	for col in range(max_x+offset_x+1):
		print(screen[col][row], end='')
		tmp += screen[col][row]
	print()
	grid.append(tmp)


def bfs(grid, start):
	queue = deque([[start]])
	seen = set([start])
	while queue:
		path = queue.popleft()
		x, y = path[-1]
		if grid[y][x] == goal:
			return path
		for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
			if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != wall and (x2, y2) not in seen:
				queue.append(path + [(x2, y2)])
				seen.add((x2, y2))

wall, clear, goal = "@", ".", "*"
width, height = max_x+offset_x, max_y+offset_y
# grid = []
# for i in screen:
# 	grid.append(''.join(i))
# print(grid)
path = bfs(grid, (start[0]+offset_x, start[1]+offset_y))
print(len(path))

