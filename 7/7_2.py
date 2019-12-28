from itertools import permutations, cycle
from copy import copy

# file = open('test_7.txt')
file = open('input_7.txt')
codes = file.readlines()[0][:-1].split(',')
legacy_codes = list(map(int, codes))
print(len(legacy_codes))

def run_code(codes, clock, inputs):

	final_output = None
	# 0 = position mode
	# 1 = immediate mode
	while codes[clock] != 99:
		current_op = str(codes[clock]).zfill(5)
		op = int(current_op[3:])
		param_mode_1 = int(current_op[2])
		param_mode_2 = int(current_op[1])
		param_mode_3 = int(current_op[0])

		try:
			code_val1 = codes[clock+1]
			code_val2 = codes[clock+2]
			val1 = codes[code_val1] if param_mode_1 == 0 else code_val1
			val2 = codes[code_val2] if param_mode_2 == 0 else code_val2
			code_val3 = codes[clock+3]
		except IndexError:
			pass
		if op == 1:
			tmp = val1 + val2
			if param_mode_3 == 0:
				target_idx = codes[clock+3]
				codes[target_idx] = tmp
			else:
				print('ERROR')
				raise('UNABLE TO HANDLE COMMAND: ', current_op)
			clock += 4

		elif op == 2:
			tmp = val1 * val2
			if param_mode_3 == 0:
				target_idx = codes[clock+3]
				codes[target_idx] = tmp
			else:
				raise('UNABLE TO HANDLE COMMAND: ', current_op)
			clock+=4

		elif op == 3:
			read_input = inputs.pop(0)
			print('read input', read_input)
			target_idx = codes[clock+1]
			codes[target_idx] = read_input
			clock += 2

		elif op == 4:
			print(f'[LOG] Output at index {code_val1} = {val1}')
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
			if param_mode_3 != 0:
				raise('UNABLE TO HANDLE COMMAND: ', current_op)
			codes[code_val3] = 1 if val1 < val2 else 0
			clock += 4

		elif op == 8:
			if param_mode_3 != 0:
				raise('UNABLE TO HANDLE COMMAND: ', current_op)
			codes[code_val3] = 1 if val1 == val2 else 0
			clock += 4

		else:
			raise('UNABLE TO HANDLE COMMAND: ', current_op)

	return codes, clock, inputs, final_output


res = {}
for phases in permutations(list(range(5, 10)), 5):
	last_output = 0
	codes = copy(legacy_codes)
	amps_codes = [copy(codes) for i in phases]
	amps_clock = [0] * len(phases)
	amps_input = [[i] for i in phases]

	result = 0
	while result is not None:
		for i in range(5):
			amps_input[i].append(result)
			amps_codes[i], amps_clock[i], amps_input[i], result = run_code(amps_codes[i], amps_clock[i], amps_input[i])
			if result is not None:
				last_output = result
	res[str(phases)] = last_output

answer = sorted(res.items(), key= lambda kv: kv[1])
print(answer[-1])
