from collections import deque as dq
from collections import defaultdict as ddict
import networkx as nx
fset = frozenset

# NOTE: fixing portal GS to GA because conflict with SG
file = open('input_20.txt', 'r')
# file = open('test_20.txt', 'r')
# file = open('test2_20.txt', 'r')
maze = [l[:-1] for l in file.readlines()]
# print(maze)


width, height = len(maze[0]), len(maze)
# start is tuple
def bfs(start, portal_name):
	queue = dq([start])
	distance = {start: 0}
	found = []
	while queue:
		p = queue.popleft()
		for x, y in [
			(p[0]+1, p[1]), (p[0]-1, p[1]),
			(p[0], p[1]+1), (p[0], p[1]-1)
		]:
			if not (0 <= x < width and 0 <= y < height): # maze boundary
				continue
			char = maze[y][x]
			if char == '#': # wall
				continue
			if char == ' ': # space
				continue

			if (x,y) in distance: # founded
				continue
			distance[(x, y)] = distance[p] + 1
			if 'A' <= char <= 'Z':
				found.append( (char, distance[x,y], (x, y)) )
				queue.append((x, y))
			else:
				queue.append((x, y))
	# print(found)
	pair = {}
	while len(found) > 0:
		f_char, f_dist, f_pt = found.pop(0)

		for idx, (key, distance, pt) in enumerate(found): # find in leftover nodes
			if isneighbor(f_pt, pt):
				pair[setkey(f_char, key)] = min(f_dist, distance)-1, findnext(f_pt, pt)
				del found[idx]
				break
		else:
			found.append((f_char, f_dist, f_pt))
		# print(pair, found)
	del pair[portal_name]
	return pair


def isneighbor(p1, p2):
	if abs(p1[0]-p2[0]) == 1 and p1[1] == p2[1]:
		return True
	if abs(p1[1]-p2[1]) == 1 and p1[0] == p2[0]:
		return True
	return False

setkey = lambda x, y: ''.join(sorted([x, y]))

def findnext(p1, p2):
	poss = []
	if p2[1] != p1[1] and p2[0] == p1[0]: # vertical
		poss = [
			(p2[0], max([p1[1], p2[1]])+1),
			(p1[0], min([p1[1], p2[1]])-1)
		]
	elif p2[0] != p1[0] and p2[1] == p1[1]: # horizontal
		poss = [
			(max([p1[0], p2[0]])+1, p2[1]),
			(min([p1[0], p2[0]])-1, p1[1])
		]

	res = []
	for x, y in poss:
		try:
			if maze[y][x] == '.':
				res.append((x,y))
		except IndexError:
			pass

	if len(res) == 1:
		return res[0]
	else:
		print(p1, p2, poss, res)
		print('Error: result should have one but got', len(res))
		raise('error')

def findpos(chars):
	chars = ''.join(sorted(chars))
	found = []

	# check all pos of 1st char
	for idx, row in enumerate(maze):
		tmp = [(i, idx) for i, e in enumerate(row) if e == chars[0]]
		if len(tmp) > 0:
			found.extend(tmp)

	if len(found) == 0:
		return []

	# compare next position with 2nd char
	points = []
	for x, y in found:
		for pt_x, pt_y in [
			(x-1,y),
			(x+1,y),
			(x,y-1),
			(x,y+1)
		]:
			try:
				if maze[pt_y][pt_x] == chars[1] and (pt_x, pt_y) not in points:
					points.extend([
						(x, y),
						(pt_x, pt_y)
					])
			except IndexError:
				pass

	# print(points)
	if len(points) %2 != 0:
		print('pair should be even')
		raise('error')

	# print(start)
	ans = []
	for i in range(0, len(points), 2):
		ans.append(findnext(points[i], points[i+1]))
	return ans

G = {}
queue = dq(['AA'])
travelled = set()
while queue:
	node = queue.popleft()

	start_point = findpos(node)
	# if only one portal in map
	if len(start_point) == 1:
		if (node, start_point[0]) not in G:
			res = bfs(start_point[0], node)
			G[node, start_point[0]] = res
			# retrive node name and position
			found = [(k,v[1]) for k, v in res.items()]
			for s in found:
				if s[0] not in travelled and s[0] not in queue:
					queue.append(s[0])

	# if there are several node
	# elif len(start_point):
	else:
		# then update each node
		for pt in start_point:
			if (node, pt) not in G:
				res = bfs(pt, node)
				G[node, pt] = res
				# retrive node name and position
				found = [(k,v[1]) for k, v in res.items()]
				for s in found:
					if s[0] not in travelled and s[0] not in queue:
						queue.append(s[0])
	travelled.add(node)


def func(u, v, d):
	# print(u,v,d)
	edge_wt = d.get('weight')
	return edge_wt+1

start = 'AA'
target = 'ZZ'
graph = nx.Graph()
added = {}
for k, v in G.items():
	for node_key, (dist, _) in v.items():
		if fset([k[0], node_key]) not in added:
			print(k[0], '<=>', node_key, dist)
			graph.add_edge(k[0], node_key, weight=dist+2)
			added[fset([k[0], node_key])] = dist

def getsteps(res):
	answer = 0
	for i in range(len(res) - 1):
		a, b = res[i], res[i+1]
		# print(a, b, added[fset([a,b])])
		answer += added[fset([a,b])]
		answer += 1 # need to walk through portal
	answer -= 1 # remove surplus step
	return answer

answer = 0
res = nx.dijkstra_path(graph,start,target)
for i in range(len(res) - 1):
	a, b = res[i], res[i+1]
	# print(a, b, added[fset([a,b])])
	answer += added[fset([a,b])]
	answer += 1 # need to walk through portal
answer -= 1 # remove surplus step
print(res, len(res)-1, answer)
