# file = open('test_22.txt', 'r')
file = open('input_22.txt', 'r')
cmds = file.read().split('\n')[:-1]
# print(cmds)
# card = [i for i in range(n_card)]

n_card = 119315717514047
wanted = 2020
repeat = 101741582076661

# n_card = 10007
# wanted = 2019
# repeat = 1

# new idea -> find mx + c % n which x is for certain number
# 1. change cmd to linear polynomial
m, c = 1, 0
for cmd in cmds[::-1]:
	if cmd == 'deal into new stack':
		m = -m % n_card
		c = (n_card - c - 1) % n_card
	elif 'cut' in cmd:
		n = int(cmd.split(' ')[-1])
		c = (c + n) % n_card
	elif 'increment' in cmd:
		n = int(cmd.split(' ')[-1])
		z = pow(n, n_card-2, n_card) # MAGIC: == modinv(n, L)
		m = (m*z) % n_card
		c = (c*z) % n_card
print(m, c)

# 2. modpow polynomial (ax+b)^m % n
# f(x) = ax+b
# g(x) = cx+d
# f^2(x) = a(ax+b)+b = aax + ab+b
# f(g(x)) = a(cx+d)+b = acx + ad+b
def polynompow(a, b, multiplier):
	if multiplier == 0:
		return 1, 0
	if multiplier % 2 == 0:
		return polynompow((a*a) % n_card, ((a*b)+b) % n_card, multiplier//2)
	else:
		c, d = polynompow(a, b, multiplier-1)
		return (a*c) % n_card, ((a*d)+b) % n_card

m, c = polynompow(m, c, repeat)
print(m, c)
print(((m * wanted) + c) % n_card)
