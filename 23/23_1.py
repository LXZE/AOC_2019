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
				print(self.address, self.output)
				self.outputs.append(self.output)
				if len(self.outputs) == 3:
					self.output = self.send()
			return self.output
		
	def send(self):
		data = self.outputs[:]
		self.outputs = []
		if data[0] == 255:
			print(data)
			raise Exception('Found', data)
		else:
			self.network[data[0]].extend(data[1:])
		# print(data)
		
n_pc = 50
queues = {i:[i] for i in range(n_pc)}
PCs = [PC(i, queues[i], queues) for i in range(n_pc)]
while True:
	for pc in PCs:
		pc.run()


# print(queues)
# for pc in PCs:
# 	pc.run()


# while output is not None:
# 	code, clock, base, inputs, output = intcode.run_code(code, clock, base, inputs)
# 	try:
# 		print(chr(output), end = '')
# 	except:
# 		if output != None:
# 			print(output)
