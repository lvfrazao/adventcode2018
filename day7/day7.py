import re
import bisect


class Graph(object):
    def __init__(self, instructions):
        self.instructions = instructions
        self._origin = None
        self.unique_nodes = set()
        for node in self.instructions:
            self.unique_nodes.add(node[0])
            self.unique_nodes.add(node[1])
        self.nodes = self.build_graph()
        self._traverse = None

    def build_graph(self):
        nodes = []
        for origin, destination in self.instructions:
            if origin in nodes:
                index = nodes.index(origin)
                nodes[index].add_connection(to=destination)
            else:
                nodes.append(Node(origin, to=destination))

            if destination in nodes:
                index = nodes.index(destination)
                nodes[index].add_connection(fr=origin)
            else:
                nodes.append(Node(destination, fr=origin))
        return nodes

    @property
    def origin(self):
        if self._origin is not None:
            pass
        else:
            self._origin = []
            to_nodes = {node[1] for node in self.instructions}
            for node in self.unique_nodes:
                if node not in to_nodes:
                    self._origin.append(node)
            self._origin = sorted(self._origin)
        return self._origin
    
    @property
    def traverse(self):
        if self._traverse is not None:
            return self._traverse
        indexes = [self.nodes.index(origin) for origin in self.origin]
        nodes = sorted([self.nodes[index] for index in indexes])

        travelled = []
        while nodes:
            next_nodes = []
            for i, node in enumerate(nodes):
                if all([(n in travelled) for n in node.fr]):
                    node = nodes.pop(i)
                    break
            travelled.append(node)
            next_nodes = node.to

            for node in next_nodes:
                index = self.nodes.index(node)
                if node not in nodes:
                    bisect.insort(nodes, self.nodes[index])

            # de-dup and sort
            # nodes = sorted(set(nodes))
        self._traverse = "".join([i.id for i in travelled]) 
        return self._traverse


class Node(object):
    def __init__(self, identifier, fr=None, to=None):
        self.id = identifier
        self.init_fr = fr
        self.init_to = to
        self.fr = []
        self.to = []
        if fr:
            self.fr = [fr]
        else:
            self.to = [to]
    
    def add_connection(self, fr=None, to=None):
        if fr:
            self.fr.append(fr)
        else:
            self.to.append(to)
    
    def __eq__(self, other):
        return self.id == other
    
    def __lt__(self, other):
        return self.id < other.id

    def __hash__(self):
        return hash((self.id, tuple(self.fr), tuple(self.to)))
    
    def __repr__(self):
        return f"Node({self.id}, fr={self.init_fr}, to={self.init_to})"
    
    def __str__(self):
        return f"{self.id}: From: {self.fr} // To: {self.to}"


class InstructionsReader(object):
    def __init__(self, file):
        self.fname = file
        self.instructions = open(file).read().split("\n")

    def __iter__(self):
        pattern = re.compile(r'Step (\w) must be finished before step (\w) can begin.')
        for instruction in self.instructions:
            fr, to = pattern.findall(instruction)[0]
            yield (fr, to)
    
    def __repr__(self):
        return f"InstructionsReader({self.fname})"


filepath = 'input.txt'
#filepath = 'input_example.txt'

g1 = Graph(InstructionsReader(filepath))
origin = g1.origin
for node in g1.nodes:
    pass

print(g1.unique_nodes)
print(g1.origin)
print(*g1.nodes, sep="\n")
print("The fully traversed chain is:", g1.traverse)
