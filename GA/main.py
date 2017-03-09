import random, sys
import os

var = [False, True]
class Cnf3:
    def __init__(self, x1, x2, x3):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3

    def result(self, values):
        v1 = values[abs(self.x1)]
        v2 = values[abs(self.x2)]
        v3 = values[abs(self.x3)]
        return (v1 if self.x1 > 0 else not v1) or \
                (v2 if self.x2 > 0 else not v2) or \
                 (v3 if self.x3 > 0 else not v3)

    def toString(self):
        return "(x_{} or x_{} or x_{})".format(self.x1, self.x2, self.x3)

class Cnf_group:
    def __init__(self, variables=None, clauses=None):
        if not variables or not clauses:
            return
        self.vars = [None for i in range(variables+1)]
        self.varlen = variables
        self.clen = clauses
        self.clauses = [None for i in range(clauses)]

    def random_populate_cnfs(self): # randomly 
        pvars = [v for v in range(-1*self.varlen, self.varlen+1) if v != 0]
        self.clauses = [Cnf3(random.choice(pvars),
                             random.choice(pvars),
                             random.choice(pvars)) for i in range(self.clen)]

    def populate_cnfs_with_file(fp):
        with open(fp) as f:
            line = f.readline()
            self.varlen = 0
            self.clen = 0
            bucket = []
            self.variables = []
            self.clauses = []
            while line != '':
                if (varcnt == 0) and (clausecnt == 0):
                    words = line.split(' ')
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
                    words = line.split(' ')
                    if words[0] == 'c':
                        continue
                    else:
                        for w in words:
                            if w == 0:
                                if len(bucket) != 3:
                                    sys.stdout.write("ERR: 3-CNF, must contain exactly 3 variables per group")
                                    sys.exit(3)
                                else:
                                    self.clauses.append(Cnf3(bucket[0], bucket[1], bucket[2]))
                                    bucket = []
                            else:
                                if len(bucket) > 3:
                                    sys.stdout.write("ERR: 3-CNF, must contain exactly 3 variables per group")
                                    sys.exit(3)
                                else:
                                    v = int(w)
                                    if abs(v) > self.varlen:
                                        sys.stdout.write("ERR: Variable out of bounds")
                                        sys.exit(4)
                                    else:
                                        bucket.append(v)

    def populate_vars(self):
        for i in range(1, self.varlen+1):
            self.vars[i] = random.choice(var)

    def get_result(self):
        clause_values = []
        for i in range(self.clen):
            clause_values.append(self.clauses[i].result(self.vars))

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

path = sys.argv[1]
if os.path.isdir(path):

elif os.path.isfile(path):
