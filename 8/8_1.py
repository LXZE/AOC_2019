from itertools import chain
infile = open('input_8.txt', 'r')
# infile = open('test_8.txt', 'r')
bits = infile.readline()[:-1]

print(bits)

layers = []

# wide = 3
# tall = 2

wide = 25
tall = 6

while len(bits) != 0:
	tmp = []
	for row in range(tall):
		new = []
		for col in range(wide):
			new.append(0)
		tmp.append(new)

	for row in range(tall):
		for col in range(wide):
			print(row, col, bits[0])
			tmp[row][col], bits = bits[0], bits[1:]
	layers.append(tmp)

res = []
for idx, layer in enumerate(layers):
	all_digit = list(chain(*layer))
	print(all_digit)
	res.append({
		'idx': idx,
		'#0': all_digit.count('0'),
		'#1': all_digit.count('1'),
		'#2': all_digit.count('2'),
	})
res = sorted(res, key = lambda x: x['#0'])
print(res[0]['#1'])
print(res[0]['#2'])
print(int(res[0]['#1']) * int(res[0]['#2']))
# print(layers)
# wide = 25
# tall = 6
