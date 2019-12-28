# file = open('test_2.txt')
file = open('input_2.txt')
codes = file.readlines()[0][:-1].split(',')
codes = list(map(int, codes))

# question specific
codes[1] = 12
codes[2] = 2

current_idx = 0
while codes[current_idx] != 99:
	print(codes)
	op = codes[current_idx]
	if op == 1:
		idx_val1 = codes[current_idx+1]
		idx_val2 = codes[current_idx+2]
		tmp = codes[idx_val1] + codes[idx_val2]
		target_idx = codes[current_idx+3]
		codes[target_idx] = tmp
	elif op == 2:
		idx_val1 = codes[current_idx+1]
		idx_val2 = codes[current_idx+2]
		tmp = codes[idx_val1] * codes[idx_val2]
		target_idx = codes[current_idx+3]
		codes[target_idx] = tmp
	current_idx += 4

print(codes)
print(codes[0])
