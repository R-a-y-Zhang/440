import random

class Node:
    def __init__(self, data, value):
        self.data = data
        self.value = value

class Datastore:
    def __init__(self):
        self.heap = [None]
        self.length = 0
        self.last_i = 0
    
    def insert(self, node):
        self.heap.append(node)
        self.length += 1
        self.last_i += 1
        pi = int(self.length / 2)
        ci = self.length
        while pi > 0:
            if ci % 2 == 0: # does not share parent
                if self.heap[pi].value > self.heap[ci].value: # child is smaller than parent, swap
                    tmp = self.heap[pi]
                    self.heap[pi] = self.heap[ci]
                    self.heap[ci] = tmp
                else:
                    break
            else: # does share parent
                li = ci if self.heap[ci].value < self.heap[ci-1].value else ci-1
                if self.heap[pi].value > self.heap[li].value:
                    tmp = self.heap[pi]
                    self.heap[pi] = self.heap[li]
                    self.heap[li] = tmp
                    ci = li
                else:
                    break
            ci = pi
            pi = int(ci / 2)

    def peek(self):
        return self.heap[0] if self.length > 0 else None

    def pop(self):
        if self.length == 0:
            return None
        hold = self.heap[1]
        self.heap[1] = self.heap[self.length]
        self.heap.pop()
        self.last_i -= 1
        self.length -= 1
        pi = 1
        c1 = pi*2
        c2 = pi*2+1
        while pi <= self.length:
            pNode = self.heap[pi]
            c1Node = self.heap[c1] if c1 <= self.length else None
            c2Node = self.heap[c2] if c2 <= self.length else None
            if c1Node and c2Node:
                sNode = c1 if self.heap[c1].value < self.heap[c2].value else c2 # index of smaller child
                gNode = c2 if sNode == c1 else c1 # index of larger child
                if (pNode.value > self.heap[gNode].value) or (pNode.value > self.heap[sNode].value):
                    tmp = self.heap[pi]
                    self.heap[pi] = self.heap[sNode]
                    self.heap[sNode] = tmp
                    pi = sNode
                else:
                    break
            elif (not c2Node) != (not c1Node):
                c = c1 if c1Node else c2
                cNode = self.heap[c]
                if pNode.value < cNode.value:
                    tmp = self.heap[pi]
                    self.heap[pi] = self.heap[c]
                    self.heap[c] = tmp
                break
            else:
                break
            c1 = pi*2
            c2 = pi*2+1
        return hold
    
    def output(self):
        for i in range(1, len(self.heap)):
            n = self.heap[i]
            print(n.data, n.value)

    def in_bounds(self, v):
        if v < 1 or v > self.length:
            return False
        return True

    def heapify(self, i):
        trees = []
        pi = i
        def get_children(p):
            c1 = p*2
            c2 = p*2+1
            if (not self.in_bounds(c1)) and (not self.in_bounds(c2)):
                return None
            elif c1 and c2:
                return (p, c1, c2)
            return (p, (c1 if self.in_bounds(c1) else c2))
        
        def iterate_parent(p):
            tree = []
            pcTuple = get_children(p)
            if pcTuple:
                trees.append(pcTuple)
                if len(pcTuple) == 3:
                    tree += iterate_parent(pcTuple[1])
                    tree += iterate_parent(pcTuple[2])
                else:
                    tree += iterate_parent(pcTuple[1])
            return tree
        
        trees = iterate_parent(i)
        for i in range(len(trees)-1, -1, -1):
            coll = trees[i]
            p = self.heap[coll[0]]
            c1 = self.heap[coll[1]] 
            c2 = self.heap[coll[2]] if len(coll) > 2 else None
            if c1 and c2 and (p.value > c1.value or p.value > c2.value):
                sNode = coll[1] if c1.value < c2.value else coll[2]
                tmp = self.heap[sNode]
                self.heap[sNode] = self.heap[coll[0]]
                self.heap[coll[0]] = tmp
            else:
                if p.value > c1.value:
                    tmp = self.heap[coll[1]]
                    self.heap[coll[1]] = self.heap[coll[0]]
                    self.heap[coll[0]] = tmp
