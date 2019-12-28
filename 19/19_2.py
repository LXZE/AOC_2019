from copy import copy
from itertools import cycle, islice
import intcode
import os, time
import pickle

file = open('input_19.txt', 'r')
codes = file.readlines()[0][:-1].split(',')
legacy_codes = list(map(int, codes))
# print(len(legacy_codes))

def get_output(x, y):
	code = copy(legacy_codes)
	clock = 0
	base = 0
	inputs = [x, y]
	output = 0
	while output is not None:
		code, clock, base, inputs, output = intcode.run_code(code, clock, base, inputs)
		return output if output is not None else None

x = 0
x1, x2 = 0, 0
y = 10000
while not get_output(x, y):
	x+=1
x1 = x
while get_output(x, y):
	x+=1
x2 = x


m1, m2 = y/x2, y/x1
x2 = ((m1 * 99) + 99) / (m2 - m1)
y1 = (m2 * x2) - 99
# print(x2, y1)

x2 = abs(round(x2))
y1 = abs(round(y1))
print(x2*10000+y1)
# print(round(x2), round(y1))

# top_x = []
# bot_x = []

# top_x = [902, 904, 906, 908, 911, 913, 915, 917, 919, 922, 924, 926, 928, 931, 933, 935, 937, 939, 942, 944, 946, 948, 950, 953, 955, 957, 959, 962, 964, 966, 968, 970, 973, 975, 977, 979, 981, 984, 986, 988, 990, 993, 995, 997, 999, 1001, 1004, 1006, 1008, 1010, 1013, 1015, 1017, 1019, 1021, 1024, 1026, 1028, 1030, 1032, 1035, 1037, 1039, 1041, 1044, 1046, 1048, 1050, 1052, 1055, 1057, 1059, 1061, 1064, 1066, 1068, 1070, 1072, 1075, 1077, 1079, 1081, 1083, 1086, 1088, 1090, 1092, 1095]
# bot_x = [0, 2, 4, 6, 7, 9, 11, 12, 14, 16, 17, 19, 21, 22, 24, 26, 27, 29, 31, 32, 34, 36, 37, 39, 41, 42, 44, 46, 47, 49, 51, 52, 54, 56, 57, 59, 61, 62, 64, 66, 67, 69, 71, 72, 74, 76, 77, 79, 81, 82, 84, 86, 87, 89, 91, 92, 94, 96, 97, 99, 101, 102, 104, 106, 107, 109, 111, 112, 114, 116, 117, 119, 121, 122, 124, 126, 128, 129, 131, 133, 134, 136, 138, 139, 141, 143, 144, 146, 148, 149]

# tmp = []
# # tmp2 = []
# for i in range(1, len(top_x)):
# 	tmp.append(top_x[i] - top_x[i-1])
# # for i in range(1, len(bot_x)):
# # 	tmp2.append(bot_x[i] - bot_x[i-1])
# print(tmp)
# print(tmp2)
# res = []
# min_y = 400
# for y in range(400,600):
# # for y in range(400,450):
# 	res.append([])
# 	start, end = int(1e5), 0
# 	for x in range(900, 1100):
# 	# for x in range(900, 910):
# 		tmp = get_output(x, y)
# 		if tmp == 1:
# 			if x > start:
# 				start = x
# 			if end < x:
# 				end = x
# 		res[y-min_y].append(tmp)
# 	if 1 in res[y-min_y]:
# 		top_x.append((end, y))
# 		bot_x.append((start, y))
# print(top_x, bot_x)

# pickle.dump(res, 'space.pkl')
# res_top = (0, 0)
# res_bot = (0, 0)
# for (x, y) in bot_x:
# 	tmp = (x+100, y-100)
# 	if tmp in top_x:
# 		print('found')
# 		print((x, y), tmp)
# 		res_top = tmp
# 		res_bot = (x, y)
# 		break
# print(res_top, res_bot)
# for row in res:
# 	for e in row:
# 		print('#' if e == 1 else '.', end='')
# 	print()


# generate a, b as a cycle
# for i, (a,b) in enumerate(zip(top_boundary, bottom_boundary)):
# 	print(a, i, b)
# start at seq 1
# top = 2,4,6,8,1,3,5,7,9 # 2223 22223 2223 22223
# bottom = 2,4,6,7,9,11,12,14,16,17 # 2 221 221 221 221
# large = 1200
# top = [2]
# bot = [2]
# a = [2,2,2,3]
# b = [2,2,2,2,3]
# top_cycle = cycle([*a, *b, *a, *b, *b, *a, *b, *b])
# top_cycle = list(islice(top_cycle, large))
# bot_cycle = cycle([2,2,1])
# bot_cycle = list(islice(bot_cycle, large))

# for i in range(1, large+1):
# 	# for top, just apply with top cycle
# 	tmp = top[-1] + top_cycle[i-1]
# 	top.append(tmp)

# 	# for bottom, apply 2 once then cycle after that
# 	tmp = bot[-1] + bot_cycle[i-1]
# 	bot.append(tmp)

# print(top)
# top = list(map(lambda x: (x[1], x[0]+1), enumerate(top)))
# bot = list(map(lambda x: (x[1], x[0]+1), enumerate(bot)))
# # print(top)
# # print(bot)

# res_top = (0, 0)
# res_bot = (0, 0)
# for (x, y) in bot:
# 	tmp = (x+100, y-100)
# 	if tmp in top:
# 		# print((x, y), tmp)
# 		res_top = tmp
# 		res_bot = (x, y)
# 		break
# print(res_top, res_bot)
# print()

# res_top = (0, 0)
# res_bot = (0, 0)
# for (x, y) in top:
# 	tmp = (x-100, y+100)
# 	if tmp in top:
# 		# print((x, y), tmp)
# 		res_top = tmp
# 		res_bot = (x, y)
# 		break
# print(res_top, res_bot)
# answer = res_bot[0]*10000 + res_top[1]
# print(answer)
