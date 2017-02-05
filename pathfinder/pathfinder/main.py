import sys, os
import random as rand

sys.path.append(os.path.join(os.path.dirname("."), "pf_modules"))

from setup import setup
from solver import solver
from termcolor import colored

array = setup.init_board(200, 200, 1)
array = setup.generate_obstacles(setup.generate_hards(array, 6, 15, 15, 2), 3, 0.2)
r1_w = rand.randint(0, 20)
r1_h = rand.randint(0, 20)
array[r1_h][r1_w] = 'S'
print("START", r1_h, r1_w)
r2_w = rand.randint(180, 199)
r2_h = rand.randint(180, 199)
print("END", r2_h, r2_w)
array[r2_h][r2_w] = 'E'
path = solver.aStarSolve(array, (r1_h, r1_w), (r2_h, r2_w))

for h in range(len(array)):
    for v in range(len(array[0])):
        if (h,v) in path:
            sys.stdout.write("{}".format(colored(array[h][v], 'green')))
        else:
            vv = array[h][v]
            if vv is 1:
                sys.stdout.write('{}'.format(colored(vv, 'white')))
            elif vv is 2:
                sys.stdout.write('{}'.format(colored(vv, 'yellow')))
            elif vv is 3:
                sys.stdout.write('{}'.format(colored(vv, 'red')))
    print()

