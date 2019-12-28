# file = open('test_2.txt')
file = open('input_2.txt')
codes = file.readlines()[0][:-1].split(',')
legacy_codes = list(map(int, codes))
print(len(legacy_codes))

magic_num = 19690720
ans_noun, ans_verb = 0,0
found = False
for noun in range(0,100):
	for verb in range(0, 100):
		if found:
			continue
		codes = list(legacy_codes)
		codes[1] = noun
		codes[2] = verb

		current_idx = 0
		print(noun, verb)
		while codes[current_idx] != 99:
			# print(codes)
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

		if codes[0] == magic_num:
			ans_noun, ans_verb = noun, verb
			found = True

calc = lambda noun, verb: (100*noun) + verb
print(codes)
print(codes[0], ans_noun, ans_verb, calc(ans_noun,ans_verb))


