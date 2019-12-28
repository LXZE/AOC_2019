import math
from copy import copy
# infile = open('test_10.txt', 'r')
infile = open('input_10.txt', 'r')

space = []
asteroids = {}
lines = infile.readlines()
for i_y, line in enumerate(lines):
	space.append([])
	for i_x, point in enumerate(list(line.strip())):
		space[-1].append(point)
		if point == '#':
			asteroids[f'{i_x},{i_y}'] = 0

def gcd(x, y):
	while(y):
		x, y = y, x % y
	return x

def diff(point_a, point_b):
	return (int(point_b[0]) - int(point_a[0]), int(point_b[1]) - int(point_a[1]))

for point in asteroids.keys():
	see = set()
	for other_point in asteroids.keys():
		if point != other_point:
			a,b = diff(point.split(','), other_point.split(','))
			divider = abs(gcd(a,b))
			# print(point, other_point, a, b, divider)
			see.add((a/divider, b/divider))
	asteroids[point] = len(see)

res = [(k,v) for k,v in dict(asteroids).items()]
res = sorted(res, key=lambda x:x[1], reverse=True)
best_point = res[0][0]
print('best point', best_point)

asteroids_toclear = copy(asteroids)
del asteroids_toclear[best_point]

# print(asteroids_toclear)

def find_deg(dx,dy):
	return (math.degrees(math.atan2(dy, dx))+180)
def distance(point_a, point_b):
	return sum(abs(int(a) - int(b)) for a,b in zip(point_a, point_b))
def tokey(dx, dy, divider):
	return f'{int(dx/divider)},{int(dy/divider)}'
def pointtokey(point):
	return f'{point[0]},{point[1]}'

to_int_list = lambda x: list(map(int, x.split(',')))
start_point = to_int_list(best_point)

once = True
i = 0
# while once:
while len(asteroids_toclear.keys()) != 0:
	# once = False
	see_direction = set()
	see_point = {}
	for point in asteroids_toclear.keys():
		dx, dy = diff(start_point, point.split(','))
		divider = abs(gcd(dx, dy))
		if (dx/divider, dy/divider) not in see_direction:
			see_direction.add((dx/divider, dy/divider))
			see_point[tokey(dx,dy,divider)] = {}
			see_point[tokey(dx,dy,divider)]['point'] = to_int_list(point)
			# see_point[tokey(dx,dy,divider)]['div'] = divider
		else:
			if distance(start_point, see_point[tokey(dx,dy,divider)]['point']) > distance(start_point, to_int_list(point)):
				see_point[tokey(dx,dy,divider)]['point'] = to_int_list(point)

	for k,v in see_point.items():
		dx, dy = to_int_list(k)
		deg = find_deg(dy, dx)
		see_point[k]['deg'] = deg

	for k,v in sorted(see_point.items(), key=lambda e: e[1]['deg'], reverse=True):
		del asteroids_toclear[pointtokey(v['point'])]
		if i+1 == 200:
			print(f'The {i+1} asteroid to be vaporized is at {pointtokey(v["point"])}.')
			print(f'result = {(v["point"][0] * 100) + v["point"][1]}')
		i+=1
