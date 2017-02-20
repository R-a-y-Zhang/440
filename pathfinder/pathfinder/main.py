import sys, os
import random as rand
from flask import Flask, render_template, request

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
    width = request.args.get("width")
    height = request.args.get('height')
    o_width = request.args.get("o_width")
    o_height = request.args.get("o_height")
    o_count = request.args.get("o_count")
    print(width, height)
    global path
    global array
    w = int(width) if width and width.strip() != "" else 160
    h = int(height) if height and height.strip() != "" else 100
    ow = int(o_width) if o_width and o_width.strip() != "" else 31
    oh = int(o_height) if o_height and o_height.strip() != "" else 31
    oc = int(o_count) if o_count and o_count.strip() != "" else 6
    algo = request.args.get('algo')
    if not algo:
        algo = 'a-star'
    if not w or not h:
        path = [[]]
        array = [[]]
        return render_template('index.html')

    array = setup.init_board(w, h, 1)
    array = setup.generate_obstacles(setup.generate_hards(array, oc, ow, oh, 2), 3, 0.2)
    r1_w = rand.randint(0, 5)
    r1_h = rand.randint(0, 5)
    print("START", r1_h, r1_w)
    r2_w = rand.randint(w-10, w-1)
    r2_h = rand.randint(h-10, h-1)
    print("END", r2_h, r2_w)
    path = None
    def run_with_algo(algo, heurs):
        return algo(array, (r1_h, r1_w), (r2_h, r2_w), heurs)

    if algo == 'a-multi-single' or algo == 'a-multi-multi':
        path = run_with_algo(solver.multiAStar if algo == 'a-multi-single' else solver.multiAStarMultiQueue,
                [solver.manhattan, solver.weighted_manhattan, solver.sqrtManhattan,
                    solver.crowFlies, solver.expManhattan])
    else:
        if algo == 'uniform':
            path = run_with_algo(solver.aStarSolve, solver.uniform_cost)
        elif algo == 'weighted':
            path = run_with_algo(solver.aStarSolve, solver.weighted_manhattan)
        else:
            path = run_with_algo(solver.aStarSolve, solver.manhattan)
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
    global array
    global path
    if not path:
        path = [[]]
    return render_template("main.js", rows=array, path=path)

app.run(debug=True)
