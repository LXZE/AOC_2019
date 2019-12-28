infile = open('input_3.txt','r')
# infile = open('test_3.txt','r')
wire1 = infile.readline()[:-1].split(',')
wire2 = infile.readline()[:-1].split(',')

start = (0,0)
point_wire1 = [start]
point_wire2 = [start]


def distance(point):
	return abs(point[0]) + abs(point[1])

def intersection(lst1, lst2):
	return list(set(lst1) & set(lst2))

def onpoint(startpoint, line):
	direction = line[0]
	length = int(line[1:])

	res = []
	if direction == 'U':
		res += [(i, startpoint[1]) for i in range(startpoint[0], startpoint[0]+length+1)]
	elif direction == 'D':
		res += [(i, startpoint[1]) for i in range(startpoint[0], startpoint[0]-length-1, -1)]
	elif direction == 'L':
		res += [(startpoint[0], i) for i in range(startpoint[1], startpoint[1]-length-1, -1)]
	elif direction == 'R':
		res += [(startpoint[0], i) for i in range(startpoint[1], startpoint[1]+length+1)]

	return res[1:]

for cmd in wire1:
	point_wire1 += onpoint(point_wire1[-1], cmd)

for cmd in wire2:
	point_wire2 += onpoint(point_wire2[-1], cmd)

intersect = intersection(point_wire1[1:], point_wire2[1:])
vals = []
for p in intersect:
	step_wire1 = point_wire1.index(p)
	step_wire2 = point_wire2.index(p)
	vals.append(step_wire1+step_wire2)
	print(step_wire1, step_wire2, step_wire1+step_wire2)

print(min(vals))
