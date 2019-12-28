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
	return (int(point_a[0]) - int(point_b[0]), int(point_a[1]) - int(point_b[1]))

for point in asteroids.keys():
	see = set()
	for other_point in asteroids.keys():
		if point != other_point:
			a,b = diff(point.split(','), other_point.split(','))
			divider = abs(gcd(a,b))
			# print(point, other_point, a, b, divider)
			see.add((a/divider, b/divider))
	asteroids[point] = len(see)

print(max(dict(asteroids).values()))
# for row in space:
# 	print(''.join(row))
