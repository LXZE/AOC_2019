from copy import copy
import intcode

file = open('input_21.txt', 'r')
codes = file.readlines()[0][:-1].split(',')
legacy_codes = list(map(int, codes))

cmd = '\n'.join([
'NOT A J',
'NOT C T',
'AND H T',
'OR T J',
'NOT B T',
'AND A T',
'AND C T',
'OR T J',
'AND D J',
'RUN\n'
])
cmd = list(map(ord, cmd))
inputs = cmd

code = copy(legacy_codes)
clock = 0
base = 0
output = 0
while output is not None:
	code, clock, base, inputs, output = intcode.run_code(code, clock, base, inputs)
	try:
		print(chr(output), end = '')
	except:
		if output != None:
			print(output)
