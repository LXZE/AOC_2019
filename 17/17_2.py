from copy import copy
import intcode
import os, time

file = open('input_17.txt', 'r')
codes = file.readlines()[0][:-1].split(',')
legacy_codes = list(map(int, codes))
# print(len(legacy_codes))

# code init
code = copy(legacy_codes)
clock = 0
base = 0
inputs = []
output = 0

# A = R8,L4,R4,R10,R8
# A = R8 L4 R4 R10 R8
# B = L12 L12 R8 R8
# C = R10 R4 R4
# B = L12 L12 R8 R8
# C = R10 R4 R4
# B = L12 L12 R8 R8
# C = R10 R4 R4
# C = R10 R4 R4
# A = R8 L4 R4 R10 R8

cmd = 'A,A,B,C,B,C,B,C,C,A'
a = 'R,8,L,4,R,4,R,10,R,8'
b = 'L,12,L,12,R,8,R,8'
c =	'R,10,R,4,R,4'
feed = 'y'
# feed = 'n'

process = lambda x: list(map(ord, x)) + [10]

cmd = process(cmd)
a = process(a)
b = process(b)
c = process(c)
feed = process(feed)

inputs = cmd+a+b+c+feed

data = [[]]
row = 0
code[0] = 2
while len(inputs) > 0:
	code, clock, base, inputs, output = intcode.run_code(code, clock, base, inputs)

def showscreen(data):
	os.system('clear')
	for ch in data:
		print(ch, end='')

step = 1
count = 1255
inputs = [2]
data = []
last_output = 0
# intcode.code_debug = True
while output is not None:
	code, clock, base, inputs, output = intcode.run_code(code, clock, base, inputs)
	if output is not None:
		if output > 1000:
			print(output)
		data.append(chr(output))
		step += 1
	if step % count == 0:
		showscreen(data)
		data = []
