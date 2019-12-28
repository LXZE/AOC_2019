from copy import copy

# file = open('test_9.txt')
file = open('input_9.txt')
codes = file.readlines()[0][:-1].split(',')
legacy_codes = list(map(int, codes))
print(len(legacy_codes))

def expand_mem(codes, to_idx):
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

			if param_mode_1 == 0:
				to_idx = code_val1
				val1 = codes[code_val1]
			elif param_mode_1 == 1:
				val1 = code_val1
			elif param_mode_1 == 2:
				to_idx = code_val1 + base
				val1 = codes[code_val1 + base]

			if param_mode_2 == 0:
				to_idx = code_val2
				val2 = codes[code_val2]
			elif param_mode_2 == 1:
				val2 = code_val2
			elif param_mode_2 == 2:
				to_idx = code_val2 + base
				val2 = codes[code_val2 + base]

			code_val3 = codes[clock+3]
			codes[code_val3 + base]
		except IndexError:
			codes = expand_mem(codes, max(to_idx, code_val3))

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
			print('read input', read_input)
			target_idx = codes[clock+1]
			if param_mode_1 == 0:
				codes[target_idx] = read_input
			elif param_mode_1 == 2:
				codes[target_idx+base] = read_input
			clock += 2

		elif op == 4:
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



code = copy(legacy_codes)
clock = 0
base = 0
inputs = [1]
output = 0
while output is not None:
	code, clock, base, inputs, output = run_code(code, clock, base, inputs)
	# print(output if output is not None else '')
