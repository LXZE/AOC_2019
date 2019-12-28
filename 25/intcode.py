from termcolor import colored

code_debug = False
# code_debug = True

def expand_mem(codes, to_idx):
	if to_idx > len(codes)*2: # prevent mem over extended for question 25
		to_idx = len(codes)
	if code_debug:
		print(f'mem expanded to {to_idx}')
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
			code_val1 = codes[clock+1]
			code_val2 = codes[clock+2]
			code_val3 = codes[clock+3]
			to_idx = max([code_val1+base,code_val2+base,code_val3+base])

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
			try:
				read_input = inputs.pop(0)
			except IndexError:
				final_output = 'need input'
				break
				# print(inputs)
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
		if code_debug:
			print('found 99: break')

	return codes, clock, base, inputs, final_output
