import sys, os
import random as rand
from flask import Flask, render_template

sys.path.append(os.path.join(os.path.dirname("."), "pf_modules"))

from setup import setup
from solver import solver
from termcolor import colored

app = Flask(__name__, static_folder="./pf_modules/visualizer/statics",
        template_folder="./pf_modules/visualizer/statics")
path = [[]]
array = [[]]

@app.route('/')
def run():
    global path
    w = 120
    h = 160
    global array
    array = setup.init_board(w, h, 1)
    array = setup.generate_obstacles(setup.generate_hards(array, 8, 31, 31, 2), 3, 0.2)
    r1_w = rand.randint(0, 10)
    r1_h = rand.randint(0, 10)
    print("START", r1_h, r1_w)
    r2_w = rand.randint(w-10, w-1)
    r2_h = rand.randint(h-10, h-1)
    print("END", r2_h, r2_w)
    path = solver.aStarSolve(array, (r1_h, r1_w), (r2_h, r2_w))
    '''
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
    '''
    return render_template("index.html")

@app.route("/main.js")
def get_mainjs():
    return render_template("main.js", rows=array, path=path)

app.run(debug=True)
