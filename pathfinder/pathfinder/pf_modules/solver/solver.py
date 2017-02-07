from math import sqrt

class node:
    # g = travel cost from start, h = heuristic cost
    def __init__(self, c, h, g, p):
        self.c = c
        self.h = h
        self.g = g
        self.p = p
    def equals(n):
        if self.c == n.c and self.h == c.h and self.g == c.g and self.p == c.p:
            return True
        return False

class data:
    def __init__(self, data=None, prev=None, next_=None):
        self.data = data
        self.prev = prev
        self.next = next_
    def match(self, data):
        if self.data == data:
            return True

class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.length = 0

    def insert(self, node):
        if self.length != 0:
            inc = 10
            j = 0
            while True:
                i = j*inc
                if i < self.length:
                    if self.heap[i].data > node.data: # node in heap is greater than node, thus node is in front
                        if inc == 10:
                            inc = 1
                            j = 0
                        else:
                            self.heap[i].prev = node
                            node.next = self.heap[i]
                            self.heap[i].next = node
                            node.prev = self.heap[i]
                            self.heap.insert(i, node)
                            break
                    j += inc
                else:
                    if inc == 10:
                        j -= inc
                        inc = 1
                    else:
                        break
        else:
            self.heap.append(node)
        self.length += 1
    
    def get_min(self):
        self.heap[1].prev = None
        return self.heap.pop(0)

    def find(self, data):
        for i in range(self.length):
            if self.heap[i].match(data):
                return i
        return -1

def testQueue():
    p = PriorityQueue()
    a = [5, 1,2, 5, 1, 3, 34, 7, 2, 1, 2, 6, 3, 1, 2, 100]
    for i in a:
        p.insert(data(i))
    
def in_bounds(array, c, bh, bw, v):
    if c[0] < 0 or c[0] >= bh or c[1] < 0 or c[1] >= bw:
        return False
    if array[c[0]][c[1]] == v:
        return False
    return True

def sum_tuples(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])

def manhattan(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] + c2[1])

def calculate_travel(c1, c2, c1v, c2v):
    deltaH = c1[0] - c2[0]
    deltaW = c1[1] - c2[1]
    if (deltaH == 0 or deltaW == 0) and (deltaH != deltaW): # not diagonal
        if c1v == c2v == 2: # hard to hard
            return 2
        if c1v == c2v == 1: # soft to soft
            return 1
        return 1.5 # mixed
    if deltaH != 0 and deltaW != 0:
        if c1v == c2v == 2:
            return sqrt(8)
        if c1v == c2v == 1:
            return sqrt(2)
        return (sqrt(2) + sqrt(8))/2.0

def find(set_, c):
    for i in range(len(set_)):
        if set_[i].c == c:
            return i
def find_min(openSet):
            chc = openSet[0]
            for c in openSet:
                if c.h+c.g < chc.h+chc.g:
                    chc = c
            return chc
def aStarSolve(array, start, end):
    # testQueue()
    openSet = []
    opens = []
    closedSet = []
    height = len(array)
    width = len(array[0])
    current = node(start, manhattan(start, end), 0, None)
    openSet.append(current)
    opens.append(current.c)
    neighborOffsets = [(1,0), (1,1), (0,1), (-1,0), (-1,1), (-1,-1), (1,-1), (0,-1)]
    while openSet:
        current = find_min(openSet)
        openSet.remove(current)
        cc = current.c
        opens.remove(cc)
        closedSet.append(cc)
        if current.c is end:
            return True
        neighbors = list(filter(lambda n: in_bounds(array, n, height, width, 3),
            [sum_tuples(cc, n) for n in neighborOffsets]))
        for n in neighbors: # n, tuple of the coordinates of the neighbor
            if n == end:
                nc = current
                pathList = [nc.c]
                while nc.p != None:
                    nc = nc.p
                    pathList.insert(0, [nc.c[0], nc.c[1]])
                pathList.append(end)
                return pathList
            if n in closedSet:
                continue
            tval = current.g + calculate_travel(cc, n, array[cc[0]][cc[1]], array[n[0]][n[1]])
            if n in opens:
                nnode = openSet[find(openSet, n)] # finds the node in the openSet
                # calculating travel cost from the start to that cell
                if tval < nnode.g: # if travel cost is better, update
                    nnode.g = tval
                    nnode.p = current
            else: # is not in the openSet
                nnode = node(n, manhattan(start, n), tval, current)
                openSet.append(nnode)
                opens.append(n)
    print("END OO", len(openSet))
