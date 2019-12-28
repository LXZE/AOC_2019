from copy import copy
import time, os
file = open('input_13.txt', 'r')
codes = file.readlines()[0][:-1].split(',')
legacy_codes = list(map(int, codes))
print(len(legacy_codes))

code_debug = False
# code_debug = True

def expand_mem(codes, to_idx):
	print('mem expanded')
	for i in range(len(codes), to_idx+1):
		codes.append(0)
	return codes

def run_code(codes, clock, base, inputs):

	final_output = None
	# 0 = position mode
	# 1 = immediate mode
	# 2 = relative mode
	while codes[clock] != 99:
		current_op = str(codes[clock]).zfill(5)
		op = int(current_op[3:])
		param_mode_1 = int(current_op[2])
		param_mode_2 = int(current_op[1])
		param_mode_3 = int(current_op[0])
		# print(current_op, codes[clock+1: clock+4])

		try:
			to_idx = 0
			code_val1 = codes[clock+1]
			code_val2 = codes[clock+2]
			code_val3 = codes[clock+3]
			if param_mode_1 == 0:
				val1 = codes[code_val1]
			elif param_mode_1 == 1:
				val1 = code_val1
			elif param_mode_1 == 2:
				val1 = codes[code_val1 + base]

			if param_mode_2 == 0:
				val2 = codes[code_val2]
			elif param_mode_2 == 1:
				val2 = code_val2
			elif param_mode_2 == 2:
				val2 = codes[code_val2 + base]

			to_idx = max([code_val1+base,code_val2+base,code_val3+base])

			codes[to_idx]
		except IndexError:
			codes = expand_mem(codes, to_idx)

		if op == 1:
			tmp = val1 + val2
			target_idx = code_val3
			if param_mode_3 == 0:
				codes[target_idx] = tmp
			elif param_mode_3 == 2:
				target_idx = code_val3
				codes[target_idx+base] = tmp
			else:
				raise('UNABLE TO HANDLE COMMAND: ', current_op)
			clock += 4

		elif op == 2:
			tmp = val1 * val2
			target_idx = code_val3
			if param_mode_3 == 0:
				codes[target_idx] = tmp
			elif param_mode_3 == 2:
				codes[target_idx+base] = tmp
			else:
				raise('UNABLE TO HANDLE COMMAND: ', current_op)
			clock+=4

		elif op == 3:
			read_input = inputs.pop(0)
			if code_debug:
				print('read input', read_input)
			target_idx = codes[clock+1]
			if param_mode_1 == 0:
				codes[target_idx] = read_input
			elif param_mode_1 == 2:
				codes[target_idx+base] = read_input
			clock += 2

		elif op == 4:
			if code_debug:
				if param_mode_1 < 2:
					print(f'[LOG] Output at index {code_val1} = {val1}')
				else:
					print(f'[LOG] Output at relative index {code_val1 + base} = {val1}')
			final_output = val1
			clock+=2
			break

		elif op == 5:
			if val1 != 0:
				clock = val2
			else:
				clock += 3

		elif op == 6:
			if val1 == 0:
				clock = val2
			else:
				clock +=3

		elif op == 7:
			if param_mode_3 == 0:
				codes[code_val3] = 1 if val1 < val2 else 0
			elif param_mode_3 == 1:
				raise('UNABLE TO HANDLE COMMAND: ', current_op)
			elif param_mode_3 == 2:
				codes[code_val3 + base] = 1 if val1 < val2 else 0
			clock += 4

		elif op == 8:
			if param_mode_3 == 0:
				codes[code_val3] = 1 if val1 == val2 else 0
			elif param_mode_3 == 1:
				raise('UNABLE TO HANDLE COMMAND: ', current_op)
			elif param_mode_3 == 2:
				codes[code_val3 + base] = 1 if val1 == val2 else 0
			clock += 4

		elif op == 9:
			base += val1
			clock += 2

		else:
			raise('UNABLE TO HANDLE COMMAND: ', current_op)

	if codes[clock] == 99:
		print('found 99: break')
		final_output = None

	return codes, clock, base, inputs, final_output

def initscreen(screen, max_x, max_y):
	for x in range(max_x):
		screen.append([])
		for y in range(max_y):
			screen[x].append(0)
	return screen

def writescreen(screen, x, y, obj):
	screen[x][y] = obj

def printscreen(screen, score):
	os.system('clear')
	for y in range(len(screen[0])):
		for x in range(len(screen)):
			print( tile_id[str(screen[x][y])], end='')
		print()
	print(f'score = {score}')

tile_id = {
	'0':' ', # empty
	'1':'#', # wall, indestruct
	'2':'@', # block, destruct
	'3':'_', # pad, indestruct
	'4':'O' # ball
}

code = copy(legacy_codes)
clock = 0
base = 0
inputs = []
output = 0

step = 0
score = 0
screen = initscreen([], 40, 21)
paddle_pos = 0
ball_pos = 0
code[0] = 2

cycle = 40*21

while output is not None:
	# time.sleep(1)
	# os.system('clear')
	code, clock, base, inputs, output = run_code(code, clock, base, inputs)

	if (step+1) % 3 == 0: # output 2
		printscreen(screen, score)
		if x == -1 and y == 0:
			score = output if output else score
		else:
			writescreen(screen, x,y, output)

		if output == 3:
			paddle_pos = x
		elif output == 4:
			ball_pos = x

		if ball_pos < paddle_pos:
			cmd = -1
		elif ball_pos > paddle_pos:
			cmd = 1
		else:
			cmd = 0
		inputs = [cmd]
	elif (step+2) % 3 == 0: # output 1
		y = output
	elif (step+3) % 3 == 0: # output 0
		x = output
	step+=1
print(score)
