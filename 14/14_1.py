import math

# infile = open('test_14.txt', 'r')
infile = open('input_14.txt', 'r')
from itertools import chain

requirement = {}

def toKey(e):
	a,b = e.split(' ')
	return (int(a),b)

info = infile.readlines()
for reaction in info:
	body, tail = reaction.strip().split(' => ')
	val, key = toKey(tail)
	# requirement[key] = (val, list(map(toKey, a.split(', ')))
	requirement[key] = (val, {y:x for x,y in list(map(toKey, body.split(', '))) })

got = {k:0 for k in requirement.keys()}
need = {k:0 for k in requirement.keys()}
got['ORE'], need['ORE'] = 0, 0
need['FUEL'] = 1
needs = 1
while needs > 0:
	for substance in need.keys():
		if substance == 'ORE' or need[substance] == 0:
			continue
		require = need[substance] - got[substance]
		if require > 0:
			multiplier = math.ceil(require/requirement[substance][0])
			got[substance] += requirement[substance][0]*multiplier # what we got in cargo
			for key, val in requirement[substance][1].items():
				need[key] += val * multiplier # what we want to add into cargo
				if key != 'ORE': needs += val * multiplier # increase amount of requirement
		got[substance] -= need[substance] # use stuff from cargo
		needs -= need[substance] # decrease amount of requirement
		need[substance] = 0 # don't need it anymore

print(need['ORE'])

