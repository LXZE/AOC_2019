import math
# in_file = open('1_test.txt', 'r')
in_file = open('input_1.txt', 'r')
calc = lambda x:math.floor(x/3)-2
res = 0
for line in in_file.readlines():
	val = int(line[:-1])
	# print(calc(val))
	res+=calc(val)

print(res)


