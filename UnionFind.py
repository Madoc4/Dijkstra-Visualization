class UnionFind:
    def __init__(self, edges):
        self.groups = {}
        self.parents = {}
        for i in edges:
            self.parents[i] = i
            self.groups[i] = [i]

    def find(self, node):
            return self.parents[node]

    def union(self, node1, node2):
        # Two types of union: by rank and by size, size is simpler
        if len(self.groups[self.find(node1)]) < len(self.groups[self.find(node2)]):
            for element in self.groups[self.find(node1)]:
                self.groups[self.find(node2)].append(element)
                self.parents[element] = self.parents[node2]
        else:
            for element in self.groups[self.find(node2)]:
                self.groups[self.find(node1)].append(element)
                self.parents[element] = self.parents[node1]
