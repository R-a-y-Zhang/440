import random, sys
import os
import re

var = [False, True]

def reduce(fn, arr, acc=None):
    s = 0
    if acc is None:
        acc = arr[0]
        s = 1
    for i in range(s, len(arr)):
        acc = fn(acc, arr[i])
    return acc
   
class Cnf3:
    def __init__(self, xvar):
        self.vars = xvar

    def result(self, values):
        def get_boolean(b):
            v = values[b]
            return (v if b < 0 else not v)
        return reduce(lambda acc, v: acc or v, [get_boolean(b) for b in self.vars])

    def toString(self):
        out = ''
        for i in range(len(self.vars)):
            out += 'x_{}'.format(self.vars[i])
            if i != (len(self.vars)-1):
                out += ' '
        return out

class Cnf_group:
    def __init__(self, variables=None, clauses=None):
        if not variables or not clauses:
            return
        self.varlen = variables
        self.clen = clauses
        self.clauses = [None for i in range(clauses)]

    def random_populate_cnfs(self): # randomly 
        pvars = [v for v in range(-1*self.varlen, self.varlen+1) if v != 0]
        self.clauses = [Cnf3(random.choice(pvars),
                             random.choice(pvars),
                             random.choice(pvars)) for i in range(self.clen)]

    def populate_cnfs_with_file(self, fp):
        with open(fp) as f:
            line = f.readline()
            self.varlen = 0
            self.clen = 0
            bucket = []
            self.clauses = []
            for line in f:
                if (self.varlen == 0) and (self.clen == 0):
                    words = re.split(' +', line)
                    if words[0] == 'p':
                        if words[1] != 'cnf':
                            sys.stdout.write("ERR: p line must specify cnf as format")
                            sys.exit(1)
                        else:
                            try:
                                self.varlen = int(words[2])
                                self.clen = int(words[3])
                            except:
                                sys.stdout.write("ERR: p line must contain a count of variable and clauses")
                                sys.exit(2)
                    else:
                        continue
                else:
                    words = re.split(' +', line)
                    words = list(filter(lambda n: n != '', [w.strip() for w in words]))
                    if words[0] == 'c':
                        continue
                    else:
                        for w in words:
                            if w == '%':
                                return
                            if int(w) == 0:
                                if len(bucket) != 3:
                                    sys.stdout.write("ERR: 3-CNF, must contain exactly 3 variables per group")
                                    print()
                                    sys.exit(3)
                                else:
                                    self.clauses.append(Cnf3([bucket[0], bucket[1], bucket[2]]))
                                    bucket.clear()
                            else:
                                if len(bucket) > 3:
                                    sys.stdout.write("ERR: 3-CNF, must contain exactly 3 variables per group")
                                    print()
                                    sys.exit(3)
                                else:
                                    v = int(w)
                                    if abs(v) > self.varlen:
                                        sys.stdout.write("ERR: Variable out of bounds")
                                        print()
                                        sys.exit(4)
                                    else:
                                        bucket.append(v)

    def populate_vars(self):
        self.variables = [None]
        for i in range(1, self.varlen+1):
            self.variables.append(random.choice(var))

    def get_result(self):
        clause_values = []
        for i in range(self.clen):
            clause_values.append(self.clauses[i].result(self.variables))
        return clause_values

    def output_cnfs(self):
        for cnf in self.clauses:
            print(cnf.toString())

    def output_vars(self):
        for i in range(1, self.varlen+1):
            sys.stdout.write("x_{} {} ".format(i, 'T' if self.vars[i] else 'F'))
        print()
'''
cnf = Cnf_group(30, 30)
cnf.random_populate_cnfs()
cnf.populate_vars()
cnf.output_cnfs()
cnf.output_vars()
print(cnf.get_result())
'''

def basic_fitness(res):
    return res.count(True)

def process_cnf_file(fp):
    cnf = Cnf_group()
    cnf.populate_cnfs_with_file(fp)
    return cnf

def solve_cnf(cnf):
    cnf.populate_vars()
    return cnf.get_result()

def cum_results(res):
    return reduce(lambda acc, n: acc and n, res)

## processing command-line arguments
path = sys.argv[1]
if os.path.isdir(path):
    for f in os.listdir(path):
        process_cnf_file(f)

elif os.path.isfile(path):
    cnf = process_cnf_file(path)
    for i in range(10):
        res = solve_cnf(cnf)
        print(basic_fitness(res), cum_results(res))
