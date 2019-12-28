import networkx as nx
# infile = open('test_6.txt','r')
infile = open('input_6.txt','r')

target = 'SAN'
meta = 'YOU'

data = list(map(lambda x: x.strip(), infile.readlines()))
orbits = nx.DiGraph()
for orbit in data:
	a,b = orbit.split(')')
	orbits.add_nodes_from([a,b])
	orbits.add_edge(b,a)

# print(f'#amount orbits = {len(orbits.nodes())}')

def calc(graph, node):
	com = list(graph.successors(node))
	if len(com) != 0:
		return f'->{com[0]}' + calc(graph, com[0])
	return ''

tmp = {}
tmp[target] = calc(orbits, target).split('->')[1:][::-1]
tmp[meta] = calc(orbits, meta).split('->')[1:][::-1]

for i in range(max(len(tmp[meta]), len(tmp[target]))):
	if tmp[meta][i] != tmp[target][i]:
		break
print(tmp[target][i-1:],len(tmp[target][i-1:]))
print(tmp[meta][i-1:],len(tmp[meta][i-1:]))

meta_side_len = len(tmp[meta][i-1:])
target_len = len(tmp[target][i-1:])-2 # -1 for same link node, -1 for target orbit

print(meta_side_len+target_len)
