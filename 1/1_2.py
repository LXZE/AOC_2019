import math
# in_file = open('1_test.txt', 'r')
in_file = open('input_1.txt', 'r')
calc = lambda x:math.floor(x/3)-2

def rec(val):
	addi = calc(val)
	return 0 if addi <= 0 else addi+rec(addi)

res = 0
for line in in_file.readlines():
	val = int(line[:-1])
	tmp = rec(val)
	# print(tmp)
	res+=tmp

print(res)
