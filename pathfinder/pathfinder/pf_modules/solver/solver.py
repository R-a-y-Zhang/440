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

def A(array, c1, c2):
    sh = c1[0]
    sw = c1[1]
    th = c2[0]
    tw = c2[1]
    h = calculate_manhattan(array, c2)
    closed_set = []
    open_set = [c1]

