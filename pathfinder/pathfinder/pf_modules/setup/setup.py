import random

def init_board(width, height, v):
    return [[v for x in range(width)] for x in range(height)]

def generate_obstacles(arr, v, fill):
    array = arr
    height = len(array)
    width = len(array[0])
    pick_cnt = height*width*fill
    i = 0
    while i < v:
        w = random.randint(0, width-1)
        h = random.randint(0, height-1)
        if (array[h][w] != v):
            array[h][w] = v
            i += 1
    return array

def check_bounds(b0, b1, v):
    if v >= b0 and v < b1:
        return True
    return False

def generate_hards(arr, cnt, hard_w, hard_h, v):
    array = arr
    height = len(array)
    width = len(array[0])
    half_w = hard_w / 2
    half_h = hard_h / 2
    roffset = half_w - (1 if (hard_w % 2 == 0) else 0)
    boffset = half_h - (1 if (hard_h % 2 == 0) else 0)
    loffset = half_w
    toffset = half_h
    for i in range(cnt):
        w = random.randint(0, width)
        h = random.randint(0, height)
        scell_h = h - toffset
        scell_w = w - loffset
        for i in range(hard_h):
            sh = i + h
            if (check_bounds(0, height, sh)):
                for j in range(hard_w):
                    sw = j + w
                    if (check_bounds(0, width, sw)):
                        array[sh][sw] += v
    return array

def generate_rivers(array, v): # to be implemented
    return array
