"""
Implementacion del algoritmo de recocido simulado
para la materia electiva Computacion Emergente

@author Yohan Graterol <yograterol@fedoraproject.org> 2013
"""
from collections import deque
from math import exp
from numpy.random import (permutation, random_sample)
from numpy import log


class LoadData(object):

    __slots__ = ['data', 'matrix']
    file_name = 'tsp29.txt'

    def __init__(self, file_name=None):
        if file_name:
            self.file_name = file_name
        self.load_data()

    def load_data(self):
        tmp_file = open(self.file_name)
        self.data = tmp_file.readlines()
        self.data.append('0 0')
        tmp_file.close()

    def create_matrix(self):
        self.matrix = list()
        total_line = len(self.data)
        for line in self.data:
            line = line.split()
            line = deque(map(lambda x: int(x), line))
            zero_rest = total_line - len(line)
            for i in range(zero_rest):
                line.appendleft(0)
            self.matrix.append(list(line))

class SimulatedAnnealing(object):

    __slots__ = ['matrix', 'T', 't', 't_final', 'step', 'cities', 'firts_vc',
                 'Vc', 'Vn', 'Vc_eval', 'Vn_eval', 'alpha', 'solutions']

    def __init__(self, T=1000, alpha=0.90, t_final=1, t=1, cities=29, step=200):
        data = LoadData()
        data.create_matrix()
        self.matrix = data.matrix
        self.T = T
        self.t = t
        self.t_final = t_final
        self.alpha = alpha
        self.cities = cities
        self.Vc = None
        self.firts_vc = range(self.cities)
        self.step = step
        self.solutions = list()
        #import pandas
        #print pandas.DataFrame(self.matrix, range(self.cities), range(self.cities))

    def tsp(self):
        self.Vc = self.generate_solution()
        self.Vc_eval = self.eval_solution(self.Vc)

        while(self.T > self.t_final):
            for i in range(self.step):
                self.Vn = self.generate_solution(self.Vc)
                self.Vn_eval = self.eval_solution(self.Vn)
                if self.Vn_eval - self.Vc_eval < 0:
                    self.Vc = self.Vn
                    self.Vc_eval = self.Vn_eval
                elif random_sample() < exp(-(self.Vn_eval - self.Vc_eval)/self.T):
                    self.Vc = self.Vn
                    self.Vc_eval = self.Vn_eval
            self.T *= self.reduce_temp(self.t)
            self.t += 1

    def reduce_temp(self, t):
        return self.alpha / log(1 + t)

    def generate_solution(self, Vc=None):
        if Vc is None:
            Vn = list(permutation(self.firts_vc))
            self.solutions.append(Vn)
            return Vn
        if Vc:
            Vn = list(permutation(Vc))
            while(Vn in self.solutions):
                Vn = permutation(Vc)
            self.solutions.append(Vn)
            return Vn

    def eval_solution(self, Vn, debug=False):
        km = 0
        firts_city = None
        for i in enumerate(Vn):
            if not firts_city:
                firts_city = i
            i = int(i[0])
            j = int(i) + 1
            if j == self.cities:
                i = firts_city[0]
                j -= 1

            i = Vn[i]
            j = Vn[j]

            if i > j:
                i, j = j, i
            if debug:
                print i, j
            km += int(self.matrix[i][j])
        return km

    def print_result(self):
        print self.Vc
        print self.eval_solution(self.Vc)

if __name__ == '__main__':
    tsp = SimulatedAnnealing()
    tsp.tsp()
    print "Resultado optimo"
    print tsp.print_result()

