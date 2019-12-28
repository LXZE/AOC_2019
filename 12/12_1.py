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
	# digit = max(len(str(max(moons))))
	digit = 3
	for pos, vel in zip(moons, velos):
		print(f'pos=<x={pos[0]:{digit}}, y={pos[1]:{digit}}, z={pos[2]:{digit}}>, ', end='')
		print(f'vel=<x={vel[0]:{digit}}, y={vel[1]:{digit}}, z={vel[2]:{digit}}>')
	print()

time_step = 0
max_time_step = 1000

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

def calc_energy(moons, velos):
	res = 0
	for pos, vel in zip(moons, velos):
		res += sum(map(abs,pos)) * sum(map(abs, vel))
	return res

print(f'step = {time_step}')
print_moon(moons, velos)
while time_step < max_time_step:
	# apply gravity
	for i in range(len(moons)):
		velos[i] = calc_vel(moons, velos[i], i)

	# apply velocity
	for i, vel in enumerate(velos):
		for axis, pos in enumerate(vel):
			moons[i][axis] += pos

	time_step += 1
	print(f'step = {time_step}')
	print_moon(moons, velos)
print('energy = ', calc_energy(moons, velos))
