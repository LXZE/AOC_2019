from copy import deepcopy
from itertools import chain
# file = open('test_24.txt', 'r')
file = open('input_24.txt', 'r')
state = file.read().split('\n')[:-1]
print(state)

width, height = len(state[0]), len(state)

def neighbor(p):
	return [(p[0]-1, p[1]), (p[0]+1, p[1]), (p[0], p[1]-1), (p[0], p[1]+1)]

def getnewstate(state, i, j):
	if state[i][j] == '.':
		found = 0
		for px, py in neighbor((i, j)):
			try:
				if 0 <= px < height and 0 <= py < width:
					found = found + 1 if state[px][py] == '#' else found
			except IndexError:
				continue
		return '#' if found in [1, 2] else '.'
	elif state[i][j] == '#':
		found = 0
		for px, py in neighbor((i, j)):
			try:
				if 0 <= px < height and 0 <= py < width:
					found = found + 1 if state[px][py] == '#' else found
			except IndexError:
				continue
		return '#' if found == 1 else '.'

def calc(state):
	tmp = list(chain(*state))
	tmp = [i+1 if e == '#' else 0 for i,e in enumerate(tmp)]
	tmp = [2**(i-1) if i != 0 else 0 for i in tmp]
	# print(tmp)
	return sum(tmp)

def showstate(state):
	tmp = [''.join(row) for row in state]
	print('\n'.join(tmp))
	print()

tmp_state = [list(row) for row in state]
seen = set()
showstate(state)
while True:
# for _ in range(4):
	for i, row in enumerate(state):
		for j, elem in enumerate(row):
			tmp_state[i][j] = getnewstate(state, i, j)
	score = calc(tmp_state)
	if score not in seen:
		seen.add(score)
	else:
		showstate(tmp_state)
		print(score)
		break
	state = deepcopy(tmp_state)
	showstate(state)


