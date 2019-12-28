question = list(map(int, '246515-739105'.split('-')))

print(question)

def check(val):
	pair = False
	prev_digit = '0'
	for digit in str(val):
		if digit == prev_digit:
			pair = True

		if int(prev_digit) > int(digit):
			return False

		prev_digit = digit

	return True if pair else False

res = []
for i in range(question[0], question[1]):
	if check(i):
		res.append(i)

print(res[:10])
print(len(res))
