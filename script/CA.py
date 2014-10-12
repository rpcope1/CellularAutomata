__version__ = "0.1"
__author__ = "Robert P. Cope"
__application_name__ = "Cellular Automata"

import random
random.seed()


def zeros(l):
    """Takes a length l and returns an array of length l full of zeroes"""
    return [0 for i in range(0, int(l))]


def random_list(l):
    """Takes a length l and returns an array of length l full of random 0s and 1s"""
    return [random.choice(0, 1) for i in range(0, int(l))]


def build_default_start_row(width):
    return [0] * width + [1] + [0] * width


def build_blank_grid(width, height):
    return [[0 for _ in xrange(width)] for _ in xrange(height)]


def load_rules(rulesfile):
    """Takes in a rules file, and returns rules as a dictionary"""
    rules = {}
    NN = None
    with open(rulesfile, 'r') as f:
        for line in f:
            if line[0] == "#" or len(line) == 1:  #For comments in rules file
                pass
            elif line[0:2].upper() == "NN":
                NN = int(line.split()[1])
                if NN % 2 == 1:
                    print "Error specifying number of nearest neighbors"
            elif line[0].upper() == "R":
                rin = line.split(":")[1].split(";")
                rules[tuple([int(i) for i in rin[0].split(",")])] = int(rin[1])

    if NN is None or 2 ** (NN + 1) != len(rules):
        print "Insufficient or too many rules loaded!"
        print "Check rules input!"
    return rules, NN


def evolve_system(l_start, rules):
    """Takes a starting list of states and a rules set, and returns a state one step evolved according to the rules"""
    new_l = zeros(len(l_start))
    NN = rules[1]
    length = len(l_start)
    for i in range(0, len(l_start)):
        entries = []
        for j in range((-NN / 2) + i, (NN / 2) + 1 + i):
            entries.append(l_start[j % length])
        new_l[i] = rules[0][tuple(entries)]
    return new_l


def evolve_system_multi(l_start, rules, iterations):
    grid = [l_start[:]]
    for i in range(0, iterations):
        grid.append(evolve_system(grid[i], rules))
    return grid
