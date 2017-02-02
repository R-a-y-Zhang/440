def calculate_manhattan(array, target): # calculating manhattan distance
    th = target[0]
    tw = target[1]
    height = len(array)
    width = len(array[0])
    man_arr = [[0 for x in range(width)] for x in range(height)]
    for i in range(height):
        for j in range(width):
            min_arr[i][j] = abs(th - i) + abs(tw - j)
    return man_arr

# vx is the value of a blocked square, any square with that value or which exceeds it is
# considered inaccessible
def check_if_valid(array, s, b0, b1, vx):
    h = s[0]
    w = s[1]
    if array[h][w] >= vx: # if square is "blocked"
        return False
    if h < b0[0] or h >= b1[0] or w < b0[1] or w >= b1[1]: # if square is out of bounds
        return False
    return True

def sum_lists(t1, t2):
    if len(t1) is not len(t2):
        return None
    v = []
    for i in range(len(t1)):
        v.append(t1[i] + t2[i])
    return tuple(v)

def reconstruct_path():
    return True

def A(array, c1, c2, vx):
    # initial setup
    sh = c1[0]
    sw = c1[1]
    th = c2[0]
    tw = c2[1]
    height = len(array)
    width = len(array[0])
    h = calculate_manhattan(array, c2) # the heuristic
    neighbors = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,1), (1,-1), (-1,-1)]
    # calculation start
    openset = [(0, c1)] # list of nodes yet to be examined
    closed = [] # nodes already examined
    paths = []
    while len(nodes) is not 0:
        current = openset.remove[min(openset)] # pulls smallest node
        cpos = current[1] # coordinates of current
        ccost = current[0] # current travel cost from start
        neighbors = map(lambda n: sum_lists(cpos, n), # list of valid neighbors
                     filter(lambda n: check_if_lambda(array, sum_lists(n, cpos), # finds all valid neighbors
                                                (0,0), (height,width), vx), neighbors))
        nclosed = filter(lambda n: n in closed, neighbors) # closed neighbors
        if c2 in neighbors: # found path
            return True
        # getting heuristics
        hv = [h[n[0]][n[1]] for n in neighbors]
        # getting travel cost from cpos
        gv = [ccost + array[n[0]][n[1]] + (4 if ((n[0] != cpos[0]) and (n[1] != cpos[1])) else 0) \
                for n in neighbors]

        openset += list(zip([hv+gv], neighbors)) # adding neighbors to list

