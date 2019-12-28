question = list(map(int, '246515-739105'.split('-')))

print(question)

def check(val):
	occur = [0]*10
	prev_digit = '0'
	for digit in str(val):
		if int(prev_digit) > int(digit):
			return False

		if digit == prev_digit:
			occur[int(digit)] += 1

		prev_digit = digit

	return True if 1 in occur else False

res = []
for i in range(question[0], question[1]):
	if check(i):
		res.append(i)

print(res[:10])
print(len(res))
