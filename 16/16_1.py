from itertools import cycle, islice

# infile = open('test_16.txt', 'r')
infile = open('input_16.txt', 'r')
data = infile.readline().strip()
pattern = [0, 1, 0, -1]

def getpattern(size, digit):
	cycled = cycle(pattern)
	base_pattern = list(islice(cycled, None, size+1))
	tmp = [base_pattern] * digit
	res = []
	for items in zip(*tmp):
		for elem in items:
			# print(elem)
			res.append(elem)
		if len(res) > size+1:
			break
	return res[1:size+1]

def calc(signal, pattern):
	res = 0
	for a, b in zip(signal, pattern):
		res += a*b
	return int(str(res)[-1])

phrases = 100
prev_output = [int(i) for i in data]
current_output = prev_output[:]

for phrase in range(phrases):
	for i in range(1, len(data)+1):
		current_pattern = getpattern(len(data), i)
		current_output[i-1] = calc(prev_output, current_pattern)
	prev_output = current_output
	print(phrase, end='\r')

req_digit = 8

print(''.join(map(str, current_output[:req_digit])))
