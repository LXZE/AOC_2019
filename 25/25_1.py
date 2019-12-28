from itertools import chain, combinations
from copy import copy
import intcode

file = open('input_25.txt', 'r')
codes = file.readlines()[0][:-1].split(',')
legacy_codes = list(map(int, codes))

code = copy(legacy_codes)
clock = 0
base = 0
inputs = []
output = 0

# NOTE: this part has been solved manually.

cmds = [
	'north', # Warp Drive Maintenance
	'west', # Passages
	'take mug',
	'west', # Hot Chocolate Fountain
	'take easter egg',
	'east', # Passages
	'east', # Warp Drive Maintenance
	'south', # Hull Breach
	'south', # Gift Wrapping Center
	'take asterisk',

	'south', # Stables
	'west', # Kitchen
	'north', # Hallway
	'take jam',
	'south', # Kitchen
	'east',
	'north', # Gift wrap

	'east', # Holodeck
	'take klein bottle',
	'south', # sick bay
	'west', # navigation
	'take tambourine',
	'west', # Observatory
	'take cake',
	'east', # Navigation
	'south', # Arcade
	'east', # Storage
	'take polygon',
	'north', # Security Checkpoint
]

inv = [
	# 'asterisk',
	'easter egg',
	'jam',
	'mug',
	'klein bottle',
	'cake',
	'tambourine',
	'polygon',
]

tointlist = lambda txt: [ord(c) for c in txt+'\n']

def powerset(iterable):
	s = list(iterable)
	return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def bruteforce():
	bfitems = list(powerset(inv))[1:]
	for itemlst in bfitems:
		cmd = []
		for item in itemlst:
			cmd.append('drop ' + item)
			# cmd.append(tointlist('drop ' + item))
		cmd.append('east')
		for item in itemlst:
			cmd.append('take ' + item)
		tmp = list(map(tointlist, cmd))
		yield list(chain(*tmp))

cmds = list(map(tointlist, cmds))
cmds = list(chain(*cmds))
# print(cmds)
inputs = cmds

# intcode.code_debug = True
bf_cmds = [cmd for cmd in bruteforce()]

while output is not None:
	code, clock, base, inputs, output = intcode.run_code(code, clock, base, inputs)
	try:
		print(chr(output), end = '')
	except:
		if output != None:
			if output == 'need input':
				# cmd = input('-> ')
				cmd = 'bf' # answer found, no need to ask for cmd anymore
				if cmd != 'bf':
					inputs = tointlist(cmd)
				else:
					# inputs = bf_cmds.pop(0)
					inputs = list(chain(*bf_cmds))
			else:
				print(output)
