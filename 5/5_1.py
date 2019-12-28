# file = open('test_5.txt')
file = open('input_5.txt')
codes = file.readlines()[0][:-1].split(',')
legacy_codes = list(map(int, codes))
print(len(legacy_codes))

codes = list(legacy_codes)
current_idx = 0
step = 0
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
			print('ERROR')
			raise('UNABLE TO HANDLE COMMAND: ', current_op)
		step = 4

	elif op == 3:
		read_input = int(input('val = ? '))
		target_idx = codes[current_idx+1]
		codes[target_idx] = read_input
		step = 2

	elif op == 4:
		target_idx = codes[current_idx+1]
		print(f'[OP:4] Output at index {target_idx} = {codes[target_idx]}')
		step = 2

	else:
		raise('UNABLE TO HANDLE COMMAND: ', current_op)

	current_idx += step

print(codes)
