from copy import copy
import intcode
import os, time

file = open('input_19.txt', 'r')
codes = file.readlines()[0][:-1].split(',')
legacy_codes = list(map(int, codes))
# print(len(legacy_codes))

def get_output(x, y):
	code = copy(legacy_codes)
	clock = 0
	base = 0
	inputs = [x, y]
	output = 0
	while output is not None:
		code, clock, base, inputs, output = intcode.run_code(code, clock, base, inputs)
		return output if output is not None else None


res = []
count = 0
# intcode.code_debug = True
for y in range(0, 50):
	res.append([])
	for x in range(0, 50):
		tmp = get_output(x, y)
		res[y].append(tmp)
		if tmp == 1:
			count+=1

# print(res)
print(count)
