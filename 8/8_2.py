from copy import copy
from itertools import chain
infile = open('input_8.txt', 'r')
# infile = open('test_8.txt', 'r')
bits = infile.readline()[:-1]

digit_mark = {
	'0': ' ',
	'1': '█'
}

def create_new2dlist(tall, wide):
	tmp = []
	for row in range(tall):
		new = []
		for col in range(wide):
			new.append(0)
		tmp.append(new)
	return tmp

print(bits)

layers = []

# wide = 2
# tall = 2

wide = 25
tall = 6

while len(bits) != 0:
	tmp = create_new2dlist(tall, wide)
	for row in range(tall):
		for col in range(wide):
			print(row, col, bits[0])
			tmp[row][col], bits = bits[0], bits[1:]
	layers.append(tmp)

res = create_new2dlist(tall, wide)
res = copy(layers[-1])
for idx, layer in enumerate(layers[::-1]):
	for row in range(tall):
		for col in range(wide):
			if layer[row][col] != '2':
				res[row][col] = layer[row][col]
print(res)


for row in res:
	for col in row:
		print(digit_mark[col], end='')
	print('')
