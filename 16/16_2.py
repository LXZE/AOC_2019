from itertools import cycle, islice
import time, math

# infile = open('test_16.txt', 'r')
infile = open('input_16.txt', 'r')
data = infile.readline().strip()
pattern = [0, 1, 0, -1]

lookup_patterns = {}
def getpattern(size, digit):
	global lookup_patterns
	if digit not in lookup_patterns:
		cycled = cycle(pattern)
		base_pattern = list(islice(cycled, None, size+1))
		tmp = [base_pattern] * digit
		res = []
		for items in zip(*tmp):
			for elem in items:
				res.append(elem)
			if len(res) > size+1:
				break
		lookup_patterns[digit] = res[1:size+1]
	return lookup_patterns[digit]

# def calc(signal, pattern):
# 	res = 0
# 	for a, b in zip(signal, pattern):
# 		res += a*b
# 	return int(str(res)[-1])
# simplified version for part 2
def calc(signal, offset):
	res = sum(signal[offset:])
	return res%10

data *= 10000
msg_off = int(data[:7])
req_digit = 8

print('message_offset = ', msg_off)
print('message len = ', len(data))

phrases = 100
prev_output = [int(i) for i in data[msg_off:]]
current_output = prev_output[:]
print(len(current_output))

# init
# for i in range(msg_off, len(data)+1):
# 	lookup_patterns[i] = [0]*(i-msg_off) + [1]*(len(data)-i+1)
# print(lookup_patterns[msg_off+1][:req_digit])

for phrase in range(phrases):
	# for i in range(msg_off, len(data)):
	# 	idx = i-msg_off
	# 	# current_pattern = getpattern(len(data), i+1)
	# 	current_output[idx] = calc(prev_output, idx)
	# 	print(i, end='\r')
	tmp = 0
	for i in range(len(data)-1, msg_off-1, -1):
			idx = i-msg_off
			tmp += prev_output.pop(-1)
			current_output[idx] = tmp%10
			# print(idx)
	prev_output = current_output[:]
	print(phrase, prev_output[:req_digit])

print(''.join(map(str, current_output[:req_digit])))
