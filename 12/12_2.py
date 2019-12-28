from sympy import lcm
from itertools import chain
import copy
# infile = open('test_12.txt', 'r')
infile = open('input_12.txt', 'r')
moons = []
velos = []
for line in infile.readlines():
	tmp = line.strip()[1:-1].split(', ')
	tmp = list(map(lambda x: x.split('=')[1], tmp))
	tmp = list(map(int, tmp))
	moons.append(tmp)
	velos.append([0]*3)

def print_moon(moons, velos):
	l_m = list(chain(*moons))
	l_v = list(chain(*velos))
	digit = max(len(str(max(l_m)))+1, len(str(max(l_v)))+1)
	for pos, vel in zip(moons, velos):
		print(f'pos=<x={pos[0]:{digit}}, y={pos[1]:{digit}}, z={pos[2]:{digit}}>, ', end='')
		print(f'vel=<x={vel[0]:{digit}}, y={vel[1]:{digit}}, z={vel[2]:{digit}}>')
	print()

def calc_vel(moons, old_vel, idx):
	res = old_vel
	core = moons[idx]
	for i, moon_pos in enumerate(moons):
		for axis, pos  in enumerate(moon_pos):
			if core[axis] < pos:
				res[axis] += 1
			elif core[axis] > pos:
				res[axis] -= 1
	return res

time_step = 0
first_moon_pos = copy.deepcopy(moons)

print(f'step = {time_step}')
print_moon(moons, velos)

def get(moons, velos):
	x,y,z = '','',''
	for pos, vel in zip(moons, velos):
		x += str(pos[0]) + str(vel[0])
		y += str(pos[1]) + str(vel[1])
		z += str(pos[2]) + str(vel[2])
	return x,y,z

uniqX, uniqY, uniqZ = set(), set(), set()
addX, addY, addZ = True, True ,True
onceX, onceY, onceZ = False, False, False
x, y, z = get(moons, velos)
first_x = x
first_y = y
first_z = z
print(x, y, z)
uniqX.add(first_x)
uniqY.add(first_y)
uniqZ.add(first_z)
surp_x, surp_y, surp_z = 0,0,0

while addX or addY or addZ:
	# apply gravity
	for i in range(len(moons)):
		velos[i] = calc_vel(moons, velos[i], i)

	# apply velocity
	for i, vel in enumerate(velos):
		for axis, pos in enumerate(vel):
			moons[i][axis] += pos

	x, y, z = get(moons, velos)
	# print(x, y, z)
	if addX and x not in uniqX:
		uniqX.add(x)
	else:
		if x == first_x:
			if not onceX:
				print('Found X loop')
				print(x, len(uniqX))
				print(f'step = {time_step}')
				print_moon(moons, velos)
				onceX = True
			addX = False
		else:
			if not onceX:
				print('surp x + 1')
				surp_x += 1

	if addY and y not in uniqY:
		uniqY.add(y)
	else:
		if y == first_y:
			if not onceY:
				print('Found Y loop')
				print(y, len(uniqY))
				print(f'step = {time_step}')
				print_moon(moons, velos)
				onceY = True
			addY = False
		else:
			if not onceY:
				print('surp y + 1')
				surp_y += 1

	if addZ and z not in uniqZ:
		uniqZ.add(z)
	else:
		if z == first_z:
			if not onceZ:
				print('Found Z loop')
				print(z, len(uniqZ))
				print(f'step = {time_step}')
				print_moon(moons, velos)
				onceZ = True
			addZ = False
		else:
			if not onceZ:
				print('surp z + 1')
				surp_z += 1

	time_step += 1

print(lcm([len(uniqX)+surp_x, len(uniqY)+surp_y, len(uniqZ)+surp_z]))
