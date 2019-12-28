# file = open('test_22.txt', 'r')
file = open('input_22.txt', 'r')
cmds = file.read().split('\n')[:-1]
# print(cmds)

n_card = 10007
wanted = 2019
card = [i for i in range(n_card)]

def dealnewstack(decks):
	return decks[::-1]

def cut(decks, n):
	tmp = decks[n:] + decks[:n]
	return tmp

def dealincrement(decks, n):
	queue = decks[:]
	res = [None] * len(decks)
	i = 0
	while None in res:
		# print(res)
		res[i] = queue.pop(0)
		if i + n >= len(res):
			i = (i+n) - len(res) - n
		if None not in res:
			return res
		i += n

# print(card)
for cmd in cmds:
	# print(cmd)
	if cmd == 'deal into new stack':
		card = dealnewstack(card)
	elif 'cut' in cmd:
		n = int(cmd.split(' ')[-1])
		card = cut(card, n)
	elif 'increment' in cmd:
		n = int(cmd.split(' ')[-1])
		card = dealincrement(card, n)
	# print(card)
# print(card.index(wanted))
print(card[wanted])
