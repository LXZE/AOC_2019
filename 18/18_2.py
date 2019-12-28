from collections import deque
file = open('input_18_2.txt', 'r')
# file = open('test_18.txt', 'r')
maze = file.readlines()
maze = list(map(lambda x: x.strip(), maze))

width, height = len(maze[0]), len(maze)
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


def multi_reachable(starts, havekeys):
	keys = {}
	for i, start in enumerate(starts):
		for ch, (distance, pt) in reachable(start, havekeys).items():
			keys[ch] = distance, pt, i
	return keys

seen = {}
def calc(starts, havekeys):
	# start_key = keynode[start]
	lkeys = ''.join(sorted(havekeys))
	if (starts, lkeys) in seen:
		return seen[starts, lkeys]
	if len(seen) % 10 == 0:
		print(lkeys)
	keys = multi_reachable(starts, havekeys)
	if len(keys) == 0:
		ans = 0
	else:
		possible = []
		for ch, (distance, pt, i) in keys.items():
			# distance = dists[frozenset((start_key, ch))]
			start_i = tuple(pt if idx == i else p for idx, p in enumerate(starts))
			# print(start_i)
			possible.append(distance + calc(start_i, havekeys + ch))
			# print(start_key, ch, distance)
		ans = min(possible)
	seen[starts, lkeys] = ans
	return ans

# print(reachable(start, ''))
keynode = {}
unrelated = ['.', '#']
starts = []
for i, row in enumerate(maze):
	for j, elem in enumerate(row):
		if elem not in unrelated:
			keynode[i, j] = elem
		if elem == '@':
			starts.append((i, j))

# start = list(keynode.keys())[list(keynode.values()).index('@')]
print(calc(tuple(starts), ''))
