from termcolor import colored

code_debug = False
# code_debug = True

def expand_mem(codes, to_idx):
	# print('mem expanded')
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
		final_output = final_output if final_output != None else None

	return codes, clock, base, inputs, final_output

def onscreen(visit, current):
	known = []
	for key in visit.keys():
		known.append(key)
	x = list(map(lambda x: x[0], known))
	y = list(map(lambda x: x[1], known))
	min_x, max_x = min(x), max(x)
	min_y, max_y = min(y), max(y)
	offset_x = abs(min_x)
	offset_y = abs(min_y)

	oxygen = [-14, 12]
	start = [0, 0]

	screen = []
	for i in range(max_x+offset_x+1):
		screen.append([])
		for j in range(max_y+offset_y+1):
			screen[i].append(' ')

	for key, val in visit.items():
		screen[key[0]+offset_x][key[1]+offset_y] = '@' if val == '#' else colored(val,'red')

	screen[start[0]+offset_x][start[1]+offset_y] = 'S'
	screen[current[0]+offset_x][current[1]+offset_y] = colored('+', 'green')
	try:
		screen[oxygen[0]+offset_x][oxygen[1]+offset_y] = colored('*', 'yellow')
	except:
		pass

	# grid = []
	for row in range(max_y+offset_y+1):
		tmp = ''
		for col in range(max_x+offset_x+1):
			print(screen[col][row], end='')
			# tmp += screen[col][row]
		print()
