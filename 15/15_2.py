from copy import copy
# from collections import defaultdict as ddict
from collections import deque
import random
import intcode
import pickle
import os, time

display_time = 0.03

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

def move(tmp_pos, action):
	current_pos = list(tmp_pos)
	if action == 1:
		current_pos[1] -= 1
	elif action == 2:
		current_pos[1] += 1
	elif action == 3:
		current_pos[0] -= 1
	elif action == 4:
		current_pos[0] += 1
	return current_pos

def reachable(current):
	res = []
	for i in range(1, 5):
		res.append(move(current, i))
	return res

def getaction(current, state):
	dx = current[0] - state[0]
	dy = current[1] - state[1]
	if dy == 1 and dx == 0:
		return 1
	elif dy == -1 and dx == 0:
		return 2
	elif dx == 1 and dy == 0:
		return 3
	elif dx == -1 and dy == 0:
		return 4

def swap(cmd):
	if cmd == 1:
		return 2
	elif cmd == 2:
		return 1
	elif cmd == 3:
		return 4
	elif cmd == 4:
		return 3

start = (0, 0)
visit = {}
visit[start] = '.'
current = [e for e in start]
queue = [start] # list of tuple

walk_history = []
oxygen = ''
while queue:
	new_current = queue.pop(0)
	# move to new place
	if tuple(current) != new_current:
		action = getaction(current, new_current)
		if action is None:
			# something wrong
			raise('error')
		inputs = [action]
		code, clock, base, inputs, output = intcode.run_code(code, clock, base, inputs)
		walk_history.append(action)

	current = new_current

	# check around
	tmp = []
	for s in reachable(list(current)):
		if tuple(s) not in visit.keys():
			tmp.append(s)
	togo = tmp

	possible_state = []
	for state in togo:
		if tuple(state) not in visit.keys():
			# check state result
			action = getaction(current, state)
			inputs = [action]
			code, clock, base, inputs, output = intcode.run_code(code, clock, base, inputs)
			if output == 0:
				visit[tuple(state)] = '#'
			elif output == 1 :
				visit[tuple(state)] = '.'
				possible_state.append(state)
				# return old position
				inputs = [swap(action)]
				code, clock, base, inputs, output = intcode.run_code(code, clock, base, inputs)
			else:
				visit[tuple(state)] = '*'
				oxygen = tuple(state)
				possible_state.append(state)
				inputs = [swap(action)]
				code, clock, base, inputs, output = intcode.run_code(code, clock, base, inputs)

	if len(possible_state) > 0:
		for state in possible_state:
			queue.insert(0, tuple(state))
	else: # current state is stuck need to go back
		if len(queue) == 0:
			break
		while getaction(current, queue[0]) is None:
			action = swap(walk_history.pop(-1))
			inputs = [action]
			code, clock, base, inputs, output = intcode.run_code(code, clock, base, inputs)
			if output != 1:
				# something wrong should break
				raise('break')
			current = move(current, action)
			# print('return to', current)
		# print(walk_history)

	os.system('clear')
	intcode.onscreen(visit, current)
	time.sleep(display_time)

visit[oxygen] = 'O'
visit[start] = '.'
# while still . in visit
	# for key that contain O
	# check surround that contain .
		# if contain . = change
			# add to list for apply in next step
	# apply O in list to visit
	# count minute ++
# print minute

minute = 0
current = start
while '.' in visit.values():
	apply = []
	for key, val in visit.items():
		if val == 'O':
			checkList = reachable(key)
			for state in checkList:
				if visit[tuple(state)] == '.':
					apply.append(tuple(state))
	for state in apply:
		visit[state] = 'O'
	os.system('clear')
	intcode.onscreen(visit, current)
	time.sleep(display_time)
	minute += 1

print(minute)
