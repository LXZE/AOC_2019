from copy import copy
import intcode
import os, time

file = open('input_17.txt', 'r')
codes = file.readlines()[0][:-1].split(',')
legacy_codes = list(map(int, codes))
print(len(legacy_codes))

# code init
code = copy(legacy_codes)
clock = 0
base = 0
inputs = []
output = 0

data = [[]]
row = 0
while output is not None:
	code, clock, base, inputs, output = intcode.run_code(code, clock, base, inputs)
	if output == 10:
		data.append([])
		row+=1
	else:
		if type(output) == int:
			data[row].append(chr(output))
	# print(output, chr(output))

data = data[:-2]

# for row in data:
# 	for col in row:
# 		print(col, end='')
# 	print()

x_len = len(data[0])
y_len = len(data)

res = 0
for y in range(1, y_len-1):
	for x in range(1, x_len-1):
		if data[y][x] == '#' and \
			data[y-1][x] == data[y][x] and \
			data[y+1][x] == data[y][x] and \
			data[y][x-1] == data[y][x] and \
			data[y][x+1] == data[y][x]:
			print(x, y, x*y)
			res+= x*y
			data[y][x] = 'O'


for row in data:
	for col in row:
		print(col, end='')
	print()
print(res)
