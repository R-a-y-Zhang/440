from flask import Flask, request
import sys

app = Flask(__name__)

def unflatten(flat, width, height):
    array = []
    buf = []
    c = 0
    for i in range(height):
        for j in range(width):
            buf.append(flat[c])
            c += 1
        array.append(buf)
        buf = []
    return array

class Session:
    def __init__(self, sid):
        self.sid = sid

    def set_field(self, flattened_map, width, height):
        self.width = width
        self.height = height
        self.field = unflatten(flattened_map, self.width, self.height)
    
    def output_status(self):
        print("SESSION ID {}\nGRID DIMS:\nWIDTH {}\nHEIGHT {}".format(self.sid, self.width, self.height))

    def output_grid(self):
        for row in self.field:
            print(row)

sessions = []

@app.route('/init_session')
def init_session():
    print("init session")
    session = Session(len(sessions))
    sessions.append(session)
    return str(session.sid)

@app.route('/setup', methods=['POST'])
def setup_field():
    req = request.get_json()
    sid = int(req['id'])
    session = sessions[sid]
    session.set_field([int(x) for x in req['flattened_array']], req['width'], req['height'])
    session.output_grid()
    return "OK"

app.run(debug=True)
