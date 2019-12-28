from collections import deque
file = open('input_18.txt', 'r')
# file = open('test_18.txt', 'r')
maze = file.readlines()
maze = list(map(lambda x: x.strip(), maze))

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

start = (0, 0)
for i, row in enumerate(maze):
	try:
		if row.index('@') > 0:
			# print(i ,row.index('@'))
			start = (i, row.index('@'))
	except ValueError:
		pass

width, height = len(maze[0]), len(maze)
wall = '#'
# credit to stackoverflow
def bfs(grid, start, goal):
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

def checkstep(node_pos, node1, node2):
	pos = node_pos[node1]
	paths = bfs(maze, (pos[1], pos[0]), node2)
	return len(paths)-1

visit = {}
visit[start] = '.'
current = list(start)
queue = [start] # list of tuple

distance = 0
last_state = '@'
memory = {'@':[]}
key_position = {'@':start}
keynode = {start:'@'}

while queue:
	current = queue.pop(0)
	if current in keynode:
		last_state = keynode[current]
	if last_state not in memory:
		memory[last_state] = []
	# print(current, last_state)

	# check around
	tmp = []
	for s in reachable(list(current)):
		if tuple(s) not in visit.keys():
			tmp.append(s)
	togo = tmp

	possible_state = []
	important = []
	for state in togo:
		if tuple(state) not in visit.keys():
			output = maze[state[0]][state[1]]
			if output == '#':
				visit[tuple(state)] = '#'
			else:
				# if not key or door
				if output == '.':
					pass
				# if key
				else:
					key_position[output] = tuple(state)
					keynode[tuple(state)] = output
					memory[last_state].append(output)
				visit[tuple(state)] = output
				possible_state.append(state)

	# have way to go, add the way to go
	if len(possible_state) > 0:
		for state in possible_state:
			queue.insert(0, tuple(state))
			if tuple(state) not in keynode:
				keynode[tuple(state)] = last_state

	# if stuck, start new memory
	# need to find which is the node to back
	else:
		if len(queue) == 0:
			break

def reachable(start, havekeys):
	queue = deque([start])
	distance = {start: 0}
	keys = {}
	while queue:
		p = queue.popleft()
		for x, y in [
			(p[0]+1, p[1]), (p[0]-1, p[1]),
			(p[0], p[1]+1), (p[0], p[1]-1)
		]:
			if not (0 <= x < height and 0 <= y < width):
				continue
			char = maze[x][y]
			if char == '#':
				continue
			if (x,y) in distance:
				continue
			distance[(x, y)] = distance[p] + 1
			if 'A' <= char <= 'Z' and char.lower() not in havekeys:
				continue
			if 'a' <= char <= 'z' and char not in havekeys:
				keys[char] = distance[(x, y)], (x,y)
				# print(queue, keys)
			else:
				queue.append((x, y))
	return keys

seen = {}
def calc(start, havekeys):
	start_key = keynode[start]
	lkeys = ''.join(sorted(havekeys))
	if (start_key, lkeys) in seen:
		return seen[start_key, lkeys]
	# if len(seen) % 10 == 0:
	# 	print(lkeys)
	keys = reachable(start, havekeys)
	# print(start_key, keys)
	if len(keys) == 0:
		ans = 0
	else:
		possible = []
		for ch, (distance, pt) in keys.items():
			# distance = dists[frozenset((start_key, ch))]
			possible.append(distance + calc(pt, havekeys + ch))
			# print(start_key, ch, distance)
		ans = min(possible)
	seen[start_key, lkeys] = ans
	return ans

# print(reachable(start, ''))
print(calc(start, ''))
# print(maze)

# print(key_position)
# all_key = list(filter(lambda x: x.islower(), all_key))
# print(all_key)

# for k,v in dists.items():
# 	print(k, v)
