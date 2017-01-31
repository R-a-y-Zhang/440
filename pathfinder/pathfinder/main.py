import sys, os

sys.path.append(os.path.join(os.path.dirname("."), "pf_modules"))
print(sys.path)

from setup import setup

array = setup.init_board(60, 60, 1)
array = setup.generate_hards(setup.generate_obstacles(array, 500, 0.2), 8, 31, 31, 5)
for h in array:
    print('.'.join(map(str, h)))

