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

# some heuristics
def manhattan(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] + c2[1])

def expManhattan(c1, c2):
    return pow(2, manhattan(c1, c2))

def sqrtManhattan(c1, c2):
    return sqrt(0.5*manhattan(c1, c2))

def crowFlies(c1, c2):
    return sqrt(pow(c1[0] + c2[0], 2) + pow(c1[1] + c2[1], 2))

def solid(c1, c2):
    return 0

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

def aStarSolve(array, start, end, heuristic_fn): # checks out
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
    height = len(array)
    width = len(array[0])
    heuristics.insert(0, manhattan)
    openSets = []
    closedSets = []
    scell = start
    heuristicsMarker = []
    opencells = []
    for h in range(len(heuristics)):
        openSets.append(DS.Datastore())
        snode = CNode(start, heuristics[h](start, end), 0, None)
        openSets[h].insert(DS.Node(snode, snode.g+snode.h))
        closedSets.append(set())
        heuristicsMarker.append(0)
        opencells.append(set())
        opencells[h].add(snode.c)
    nonZeros = len(openSets)
    baseVal = -1
    while nonZeros > 0:
        for i in range(len(openSets)):
            openSet = openSets[i]
            opens = opencells[i]
            closedSet = closedSets[i]
            if openSet.length <= 0: # openSet at i is empty, decrement counter
                nonZeros -= (1 if openSet.length == 0 else 0)
                openSet.length = -1
                continue
            # peeks at the node to fetch, if the g+h value is less than that of the base heuristic, then
            # continue. else, wait until the next round.
            minnode = openSet.peek().data
            if i == 0:
                baseVal = minnode.g + minnode.h
                if 1 in heuristicsMarker: # if other heuristics are better, do not expand
                    continue
            else:
                if baseVal < 0: # should never happen
                    continue
                # if heuristic is better than the base heurisitc, keep iterating over heuristics
                elif baseVal < minnode.g+minnode.h: 
                    heuristicsMarker[i] = 0
                    continue # if baseVal is better than the heuristic, don't proceed with current heuristic
                else:
                    heuristicsMarker[i] = 1
            # continue if only h+g is better than the base heuristic or if is base heuristic.
            # Then just standard A* on it
            node = openSet.pop()
            current = node.data
            cc = current.c
            opens.remove(cc)
            closedSet.add(cc)
            if current.c is end:
                return True # this should also never happen
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
                    for j in range(1, openSet.length+1):
                        if openSet.heap[j].data.c[0] == n[0] and openSet.heap[j].data.c[1] == n[1]:
                            ind = j
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
                    nnode = CNode(n, heuristics[i](start, n), tval, current)
                    openSet.insert(DS.Node(nnode, nnode.g+nnode.h))
                    opens.add(n)

def multiAStarMultiQueue(array, start, end, heuristics):
    height = len(array)
    width = len(array[0])
    heuristics.insert(0, manhattan)
    openSets = []
    opens = []
    closedSet = set()
    for i in range(len(heuristics)):
        openSets.append(DS.Datastore())
        snode = CNode(start, heuristics[i](start, end), 0, None)
        opens.append(set(start))
        openSets[i].insert(DS.Node(snode, snode.g+snode.h))
        closedSet.add(start)
    nonZeros = len(heuristics)
    while nonZeros > 0:
        cExpandVal = -1
        tset = openSets[0]
        ti = 0
        for i in range(len(openSets)):
            if openSets[i].length <= 0:
                nonZeros -= (1 if openSet.length == 0 else 0)
                openSets[i].length = -1
                continue
            pnode = openSets[i].peek().data
            if i == 0: # if is base heuristic, set that as cExpandVal
                cExpandVal = pnode.g + pnode.h
            else:
                if pnode.g + pnode.h < cExpandVal: # if less than base heuristic, set IA as new expansion
                    cExpandVal = pnode.g + pnode.h
                    tset = openSets[i]
                    ti = i
        if openSets[ti].length <= 0:
            return
        current = tset.pop().data
        cc = current.c
        closedSet.add(cc)
        if cc in opens[ti]:
            opens[ti].remove(cc)
        neighbors = list(filter(lambda n: in_bounds(array, n, height, width, 3),
            [sum_tuples(cc, n) for n in neighborOffsets]))
        for n in neighbors:
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
            for i in range(len(openSets)):
                tval = current.g + calculate_travel(cc, n, array[cc[0]][cc[1]], array[n[0]][n[1]])
                if n in opens[i]:
                    ind = -1
                    openSet = openSets[i]
                    for j in range(1, openSet.length+1):
                        if openSet.heap[j].data.c[0] == n[0] and openSet.heap[j].data.c[1] == n[1]:
                            ind = j
                            break
                    if ind == -1:
                        break
                    nodeTup = openSet.heap[ind]
                    nnode = nodeTup.data
                    if tval < nnode.g:
                        nnode.g = tval
                        nnode.p = current
                        nodeTup.value = nnode.g + nnode.h
                else:
                    nnode = CNode(n, heuristics[i](start, n), tval, current)
                    tset.insert(DS.Node(nnode, nnode.g+nnode.h))
                    opens[i].add(n)
