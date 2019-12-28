from itertools import permutations

# file = open('test_7.txt')
file = open('input_7.txt')
codes = file.readlines()[0][:-1].split(',')
legacy_codes = list(map(int, codes))
print(len(legacy_codes))

def run_code(codes, phase_set, input_val):

	final_output = 0

	current_idx = 0
	step = 0
	phase_set_bool = False
	input_val_bool = False
	# 0 = position mode
	# 1 = immediate mode
	while codes[current_idx] != 99:
		# print(codes)
		current_op = str(codes[current_idx]).zfill(5)
		op = int(current_op[3:])
		param_mode_1 = int(current_op[2])
		param_mode_2 = int(current_op[1])
		param_mode_3 = int(current_op[0])

		if op == 1:
			code_val1 = codes[current_idx+1]
			code_val2 = codes[current_idx+2]
			val1 = codes[code_val1] if param_mode_1 == 0 else code_val1
			val2 = codes[code_val2] if param_mode_2 == 0 else code_val2
			tmp = val1 + val2
			if param_mode_3 == 0:
				target_idx = codes[current_idx+3]
				codes[target_idx] = tmp
			else:
				print('ERROR')
				raise('UNABLE TO HANDLE COMMAND: ', current_op)
			step = 4

		elif op == 2:
			code_val1 = codes[current_idx+1]
			code_val2 = codes[current_idx+2]
			val1 = codes[code_val1] if param_mode_1 == 0 else code_val1
			val2 = codes[code_val2] if param_mode_2 == 0 else code_val2
			tmp = val1 * val2
			if param_mode_3 == 0:
				target_idx = codes[current_idx+3]
				codes[target_idx] = tmp
			else:
				raise('UNABLE TO HANDLE COMMAND: ', current_op)
			step = 4

		elif op == 3:
			# read_input = int(input('val = ? '))

			if phase_set_bool and input_val_bool:
				print('[ERROR] Ask for val more than 2 times')
				raise('UNABLE TO HANDLE COMMAND: ', current_op)

			if phase_set_bool and not input_val_bool:
				read_input = input_val
				input_val_bool = True


			if not phase_set_bool:
				read_input = phase_set
				phase_set_bool = True

			target_idx = codes[current_idx+1]
			codes[target_idx] = read_input
			step = 2

		elif op == 4:
			# target_idx = codes[current_idx+1]
			code_val1 = codes[current_idx+1]
			val1 = codes[code_val1] if param_mode_1 == 0 else code_val1

			# print(current_op, target_idx)
			print(f'[OP:4] Output at index {target_idx} = {val1}')
			final_output = val1
			step = 2

		elif op == 5:
			code_val1 = codes[current_idx+1]
			code_val2 = codes[current_idx+2]
			val1 = codes[code_val1] if param_mode_1 == 0 else code_val1
			val2 = codes[code_val2] if param_mode_2 == 0 else code_val2

			if val1 != 0:
				current_idx = val2
				# print(f'jumps to {current_idx}')
				step = 0
			else:
				step = 3

		elif op == 6:
			code_val1 = codes[current_idx+1]
			code_val2 = codes[current_idx+2]
			val1 = codes[code_val1] if param_mode_1 == 0 else code_val1
			val2 = codes[code_val2] if param_mode_2 == 0 else code_val2

			if val1 == 0:
				current_idx = val2
				# print(f'jumps to {current_idx}')
				step = 0
			else:
				step = 3

		elif op == 7:
			code_val1 = codes[current_idx+1]
			code_val2 = codes[current_idx+2]
			val1 = codes[code_val1] if param_mode_1 == 0 else code_val1
			val2 = codes[code_val2] if param_mode_2 == 0 else code_val2

			code_val3 = codes[current_idx+3]

			if param_mode_3 != 0:
				raise('UNABLE TO HANDLE COMMAND: ', current_op)

			if val1 < val2:
				codes[code_val3] = 1
			else:
				codes[code_val3] = 0
			step = 4

		elif op == 8:
			code_val1 = codes[current_idx+1]
			code_val2 = codes[current_idx+2]
			val1 = codes[code_val1] if param_mode_1 == 0 else code_val1
			val2 = codes[code_val2] if param_mode_2 == 0 else code_val2

			code_val3 = codes[current_idx+3]

			if param_mode_3 != 0:
				raise('UNABLE TO HANDLE COMMAND: ', current_op)

			if val1 == val2:
				codes[code_val3] = 1
			else:
				codes[code_val3] = 0
			step = 4

		else:
			raise('UNABLE TO HANDLE COMMAND: ', current_op)

		current_idx += step

	return final_output


res = {}
for phases in permutations(list(range(5)), 5):
	last_output = 0
	codes = list(legacy_codes)
	for setting in phases:
		last_output = run_code(codes, setting, last_output)
	res[str(phases)] = last_output
# print(codes)
answer = sorted(res.items(), key= lambda kv: kv[1])
print(answer[-1])
