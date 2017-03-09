import random
ops = ['and', 'or'];
vals = [True, False];
links = linker([Node(random.choice(ops), random.choice(vals)) for n in range(100)])
links.run()
