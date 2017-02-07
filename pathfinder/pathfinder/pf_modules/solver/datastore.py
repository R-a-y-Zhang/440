class Node:
    def __init__(self, data, value):
        self.data = data
        self.value = value

class Datastore:
    def __init__(self):
        self.heaps = []

    def insert(self, node):
        if not len(self.heaps):
            self.heaps.append([])
            self.heaps[0].append(node)
        else:
            j = -1
            for i in range(len(self.heaps)):
                if self.heaps[i][0].value > node.value:
                    j = i - 1 if i > 0 else 0
                    break
            for i in range(len(self.heaps[j])-1, -1, -1:
