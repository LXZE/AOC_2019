import networkx as nx
fset = frozenset

# NOTE: fixing portal GS to GA because conflict with SG
file = open('input_20.txt', 'r')
maze = [l[:-1] for l in file.readlines()]
# print(maze)

# 1: scan through map for location of portal and walkable floor
# 2: create graph for every walkable path with addition level and distance
# 3: bfs

def neighbors(p):
	return [(p[0]-1, p[1]), (p[0]+1, p[1]), (p[0], p[1]-1), (p[0], p[1]+1)]

width, height = len(maze[0]), len(maze)
floor, gates = set(), {}
for idx_row in range(height):
	for idx_col in range(width):
		if maze[idx_row][idx_col] == '.':
			floor.add((idx_row, idx_col))
		elif maze[idx_row][idx_col].isupper(): # A-Z
			if idx_row < height-1 and maze[idx_row+1][idx_col].isupper():  # vertical
				tmp = (idx_row-1, idx_col) if maze[idx_row-1][idx_col] == '.' else (idx_row+2, idx_col) # check if where is floor
				if maze[idx_row][idx_col]+maze[idx_row+1][idx_col] in gates: # if gate once found, append
					gates[maze[idx_row][idx_col]+maze[idx_row+1][idx_col]].append(tmp)
				else:
					gates[maze[idx_row][idx_col]+maze[idx_row+1][idx_col]] = [tmp]
			elif idx_col < width-1 and maze[idx_row][idx_col+1].isupper():  # horizontal
				tmp = (idx_row, idx_col-1) if maze[idx_row][idx_col-1] == '.' else (idx_row, idx_col+2) # check floor direction
				if maze[idx_row][idx_col]+maze[idx_row][idx_col+1] in gates: # if gate once found, append
					gates[maze[idx_row][idx_col]+maze[idx_row][idx_col+1]].append(tmp)
				else:
					gates[maze[idx_row][idx_col]+maze[idx_row][idx_col+1]] = [tmp]

# for k,v in gates.items():
# 	print(k ,v)

G = {}
for node in floor:
	neighbor = []
	for pt in neighbors(node):
		if pt in floor:
			neighbor.append((pt, 0)) # no add level
	for gate in gates.values(): # gate node
		if len(gate) == 2 and node in gate:
			if node[0] in [2, height-3] or node[1] in [2, width-3]: # at outer bound
				neighbor.append((gate[(gate.index(node)+1) % 2], -1)) # use outer bound -1 with link to other node
			else:
				neighbor.append((gate[(gate.index(node)+1) % 2], 1)) # use inter bound +1 with link to other node
	G[node] = neighbor

# print(G)


def bfs(graph, start, end):
	queue = [(start, 0, 0)]
	seen = set([(start, 0)])
	while queue:
		v = queue.pop(0)
		if v[0] == end and v[1] == 0:
			return v[2]
		for n in graph[v[0]]:
			if v[1] + n[1] < 0:
				continue
			if (n[0], v[1]+n[1]) not in seen:
				queue.append((n[0], v[1]+n[1], v[2]+1))
				seen.add((n[0], v[1]+n[1]))
print(bfs(G, gates['AA'][0], gates['ZZ'][0]))
