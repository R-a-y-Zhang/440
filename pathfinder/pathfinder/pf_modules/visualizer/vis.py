from flask import Flask, render_template
import random as rand

app = Flask(__name__, static_folder="./statics", template_folder="./statics")

array = [[]]
path = []

def set_array(arr):
    global array
    array = arr

def set_path(p):
    global path
    path = p

def run():

    @app.route('/')
    def run():
        return render_template("index.html")

    @app.route("/main.js")
    def get_main_js():
        ## array = [[rand.randint(1, 3) for n in range(100)] for n in range(100)]
        print(path)
        return render_template("main.js", rows=array, path=path)

    print("RUNNING")
    app.run(debug=True)
