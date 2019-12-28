from copy import copy
import intcode

file = open('input_23.txt', 'r')
codes = file.readlines()[0][:-1].split(',')
legacy_codes = list(map(int, codes))

code = copy(legacy_codes)
clock = 0
base = 0
inputs = [0]
output = 0

# intcode.code_debug = True

class PC:
	def __init__(self, address, queue, network):
		self.address = address
		self.network = network

		self.code = legacy_codes[:]
		self.clock = 0
		self.base = 0
		self.inputs = queue
		self.output = 0

		self.outputs = []

		tmp = self.run()
		# if tmp != 'need input':
			# print(address)

	def run(self):
		self.code, self.clock, self.base, self.inputs, self.output = intcode.run_code(self.code, self.clock, self.base, self.inputs)
		if self.output != None:
			if self.output == 'need input':
				self.inputs.append(-1)
			else:
				# print(self.address, self.output)
				self.outputs.append(self.output)
				if len(self.outputs) == 3:
					self.output = self.send()
			return self.output

	def send(self):
		data = self.outputs[:]
		self.outputs = []
		if data[0] == 255: # to nat
			# print(data)
			self.network[255] = data[1:] # always override
			# raise Exception('Found', data)
		else:
			self.network[data[0]].extend(data[1:])
		# print(data)

prev = []

def clearidle(prev, queues):

	if all([queues[255] == data for data in prev]) and len(queues[255]) != 0:
		# print(queues[255])
		print(queues[255][1])
		raise Exception('Found', queues[255])
	# print(queues[255])
	queues[0].extend(queues[255])
	return queues[255]

n_pc = 50
queues = {i:[i] for i in range(n_pc)}
queues[255] = []
PCs = [PC(i, queues[i], queues) for i in range(n_pc)]

limit = 1000

once = False
while True:
	tmp = []
	for pc in PCs:
		tmp.append(pc.run())
		if all([status == 'need input' for status in tmp]) and not once:
			once = True
		elif all([status == 'need input' for status in tmp]) and once:
			prev.append(clearidle(prev, queues))
			if len(prev) > limit:
				prev = prev[-limit:]
			once = False
