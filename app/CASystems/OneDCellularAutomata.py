__author__ = 'Robert P. Cope'

from BaseSystem import BaseSystem

class OneDimCellularAutomata(BaseSystem):
    def __init__(self):
        BaseSystem.__init__(self)
        self.parameters = {'nn':        ('Nearest Neighbors', 2),
                           'rule_num':  ('Rule Number', 0),
                           'wrap':      ('Grid Wrap', True)}
        self.rule_list = {}
        self.update_rule_list()

    def update_rule_list(self):
        self.rule_list.clear()
        nn = self.parameters['nn'][1]
        rule_num = self.parameters['rule_num'][1]
        for j in xrange(2 ** (nn+1)):
            rule = tuple([self._get_bit(j, n) for n in xrange(nn, -1, 1)])
            self.rule_list[rule] = self._get_bit(rule_num, j)

    @staticmethod
    def _get_bit(number, bit_location):
        if (number & 2 ** bit_location) != 0:
            return 1
        else:
            return 0

    def get_system_params(self):
        return self.parameters

    def set_system_params(self, **kwargs):
        self.parameters.update(kwargs)
        self.update_rule_list()

    def evolve(self, grid):
        new_grid = []
        nn = self.parameters['nn'][1]
        wrap = self.parameters['wrap'][1]
        for row in grid:
            length = len(row)
            if not wrap:
                row = [0 for _ in xrange(nn/2)] + row + [0 for _ in xrange(nn/2)]
            search_len = len(row)
            new_row = [0 for _ in xrange(length)]
            for i in range(0, length):
                entries = []
                for j in range((-nn / 2) + i, (nn / 2) + 1 + i):
                    entries.append(row[j % search_len])
                row[i] = self.rule_list[tuple(entries)]
            new_grid.append(new_row)
        return new_grid