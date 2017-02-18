from math import sqrt
from . import datastore as DS

class CNode:
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

def testQueue():
    d = DS()
    
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

def uniform_cost(c1, c2):
    return 0

def weighted_manhattan(c1, c2):
    return manhattan(c1, c2)*2

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

neighborOffsets = [(1,0), (1,1), (0,1), (-1,0), (-1,1), (-1,-1), (1,-1), (0,-1)]

def aStarSolve(array, start, end, heuristic_fn):
    openSet = DS.Datastore()
    opens = set()
    closedSet = set()
    height = len(array)
    width = len(array[0])
    current = CNode(start, heuristic_fn(start, end), 0, None)
    openSet.insert(DS.Node(current, current.g+current.h))
    opens.add(current.c)
    while openSet.length > 0:
        node = openSet.pop()
        current = node.data
        cc = current.c
        opens.remove(cc)
        closedSet.add(cc)
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
                ind = -1
                for i in range(1, openSet.length+1):
                    if openSet.heap[i].data.c[0] == n[0] and openSet.heap[i].data.c[1] == n[1]:
                        ind = i
                        break
                nodeTup = openSet.heap[ind]
                nnode = nodeTup.data
               # calculating travel cost from the start to that cell
                if tval < nnode.g: # if travel cost is better, update
                    nnode.g = tval
                    nnode.p = current
                    nodeTup.value = nnode.g + nnode.h
                    openSet.heapify(ind)
            else: # is not in the openSet
                nnode = CNode(n, heuristic_fn(start, n), tval, current)
                openSet.insert(DS.Node(nnode, nnode.g+nnode.h))
                opens.add(n)
    print("NONE")

def multiAStar(array, start, end, heuristics):
    hlen = len(heuristics)
    heuristics.insert(manhattan, 0)
    openSets = []
    openCells = []
    closedSet = []
    # initializing all heuristics including root
    for heuristic in heuristics:
        oSet = DS.Datastore()
        current = CNode(start, heuristic(start, end), 0, None)
        oSet.insert(DS.Node(current, current.g+current.h))
        if start not in openCells:
            openCells.append(start)
        openSets.append(oSet)
        openCells.append(set())
        closedSet.append(set())
    while heuristics[0].length > 0:
        dCel = heuristics[0].pop().data
        dV = dCel.g + dCel.h
        neighbors = list(filter(lambda n: in_bounds(array, n, height, width, 3),
            [sum_tuples(dCel.c, n) for n in neighborOffsets]))
        for n in neighbors:
            if n in closedSet[0]:
                pass
            elif:
                cc = dCel.c
                tval = dCel.g + calculate_travel(cc, n, array[cc[0]][cc[1]], array[n[0]][n[1]])
                nnode = CNode(n, heuristic[0](start, n), tval, dCel)
                openSets[0].insert(DS.Node(nnode, nnode.g+nnode.h))
                openCells[0].add(n)
            for i in range(1, hlen):
                hCell = heuristics[i].pop().data
                if hCell.c in openCells[i]:
                    continue
                neighbors = list(filter(lambda n: in_bounds(array, n, height, width, 3),
                    [sum_tuples(hCell.c, n), for n in neighborOffsets]))
                for n in neighbors:
                cc = hCell.c
                tval = dCel.g + calculate_travel(cc, n, array[cc[0]][cc[1]], array[n[0]][n[1]])
                nnode = CNode(n, heuristic[i](start, n), tval, hCell)
                openSets[i].insert(DS.Node(nnode, nnode.g+nnode.h))
                openCells[i].add(n)

