import networkx as nx
# infile = open('test_6.txt','r')
infile = open('input_6.txt','r')

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
		return 1 + calc(graph, com[0])
	return 0

tmp = {}
for idx, node in enumerate(orbits.nodes()):
	print(idx, end=' ')
	tmp[node] = calc(orbits, node)
print()
print(sum(tmp.values()))
