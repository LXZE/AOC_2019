from copy import deepcopy
from itertools import chain
enum = enumerate
# file = open('test_24.txt', 'r')
file = open('input_24.txt', 'r')
state = file.read().split('\n')[:-1]

def neighbor(p):
	x,y = p
	return [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]

def showstate(state):
	tmp = [''.join(row) for row in state]
	print('\n'.join(tmp))
	print()

print('initial state')
showstate(state)

width, height = len(state[0]), len(state)
template = [list(row) for row in ['.....']*5]
template[2][2] = '?'
# idea: loop through plus and minus level and break on no change
# in case that outer look on -1 level
# inner case look for +1 level
# go deeper and shallower just for +-200 level according to step given by question

inner = {
	(1,2): [(0,0), (0,1), (0,2), (0,3), (0,4)],
	(2,1): [(0,0), (1,0), (2,0), (3,0), (4,0)],
	(2,3): [(0,4), (1,4), (2,4), (3,4), (4,4)],
	(3,2): [(4,0), (4,1), (4,2), (4,3), (4,4)]
}
outer = {
	(0,0): [(1,2), (2,1)],
	(0,1): [(1,2)],
	(0,2): [(1,2)],
	(0,3): [(1,2)],
	(0,4): [(1,2), (2,3)],
	(1,0): [(2,1)],
	(1,4): [(2,3)],
	(2,0): [(2,1)],
	(2,4): [(2,3)],
	(3,0): [(2,1)],
	(3,4): [(2,3)],
	(4,0): [(3,2), (2,1)],
	(4,1): [(3,2)],
	(4,2): [(3,2)],
	(4,3): [(3,2)],
	(4,4): [(3,2), (2,3)]
}

def calctile(basest,inst,outst,i,j, prevtile, tiletype):
	found = 0
	for px, py in neighbor((i, j)):
		try:
			if 0 <= px < height and 0 <= py < width:
				found = found + 1 if basest[px][py] == '#' else found
		except IndexError:
			pass
	if tiletype == 'inner':
		for px, py in inner[(i, j)]:
			found = found + 1 if inst[px][py] == '#' else found
	elif tiletype == 'outer':
		for px, py in outer[(i, j)]:
			found = found + 1 if outst[px][py] == '#' else found

	if prevtile == '.':
		return '#' if found in [1, 2] else '.' # An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
	elif prevtile == '#':
		return '#' if found == 1 else '.' # A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.

def getnewstate(base_state, in_state, out_state, i, j):
	if (i,j) == (2,2):
		return '?'

	if base_state[i][j] == '.': # . case
		if (i,j) in inner: # inner tile that have 8 adjacents
			return calctile(base_state, in_state, out_state,i,j,'.', 'inner')
		elif (i,j) in outer: # outer tile that contact with outer state
			return calctile(base_state, in_state, out_state,i,j,'.', 'outer')
		else:
			return calctile(base_state, in_state, out_state,i,j,'.', '')

	elif base_state[i][j] == '#':
		if (i,j) in inner: # inner tile that have 8 adjacents
			return calctile(base_state, in_state, out_state,i,j,'#', 'inner')
		elif (i,j) in outer: # outer tile that contact with outer state
			return calctile(base_state, in_state, out_state,i,j,'#', 'outer')
		else:
			return calctile(base_state, in_state, out_state,i,j,'#', '')

def update(states, level):
	tmp_state = deepcopy(states[level])
	result_state = deepcopy(states[level])
	outer_state = states[level-1]
	inner_state = states[level+1]

	change = 0
	for i, row in enum(tmp_state):
		for j, elem in enum(row):
			tmp_val = getnewstate(tmp_state, inner_state, outer_state, i, j)
			if tmp_val != tmp_state[i][j]:
				result_state[i][j] = tmp_val
				change += 1

	return result_state, change

state = [list(row) for row in state]
state[2][2] = '?'
levels = {0: state, -1: deepcopy(template), 1: deepcopy(template)}
tmp_levels = deepcopy(levels)
# minute = 10
minute = 200
boundary = minute # bugs actually spread to outer and inner state for minute/2, but I set to minute for assure.
for m in range(minute):
	tmp_levels = deepcopy(levels)
	tmp_levels[0], _ = update(levels, 0) # level 0

	for i in range(1, boundary): # update map for deeper
		if i+1 not in tmp_levels: levels[i+1] = deepcopy(template)
		tmp_levels[i], change = update(levels, i)
		# if change == 0: # no change <- this causes bug as it cut down the update in further step
		# 	break

	for i in range(-1, -boundary, -1): # update map for shallower
		if i-1 not in tmp_levels: levels[i-1] = deepcopy(template)
		tmp_levels[i], change = update(levels, i)
		# if change == 0: # no change <- this causes bug as it cut down the update in further step
		# 	break

	levels = deepcopy(tmp_levels)
	print(m+1)

def count(states):
	result = 0
	for level, state in levels.items():
		tmp = [''.join(row) for row in state]
		tmp = ''.join(tmp)
		result += tmp.count('#')
	return result

for level, state in sorted(levels.items(), key=lambda k: k[0]):
	print(f'Depth {level}:')
	showstate(state)

print(count(levels))
