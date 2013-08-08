"""
Implementacion del algoritmo de recocido simulado
para la materia electiva Computacion Emergente

@author Yohan Graterol <yograterol@fedoraproject.org> 2013
"""
from collections import deque
from math import exp
try:
    from numpy.random import (permutation, random_sample)
    from numpy import (log, matrix, array, add)
except ImportError:
    from numpypy.random import (permutation, random_sample)
    from numpypy import (log, matrix, array, add)
from copy import deepcopy
from random import randint
from time import time


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
            line = deque(map(lambda x: int(x), line.split()))
            for i in range(total_line - len(line)):
                line.appendleft(0)
            self.matrix.append(list(line))
        self.matrix = array(self.matrix)
        self.matrix = add(self.matrix, self.matrix.transpose())

class SimulatedAnnealing(object):

    __slots__ = ['matrix', 'T', 't', 't_final', 'step', 'cities', 'firts_vc',
                 'Vc', 'Vn', 'Vc_eval', 'Vn_eval', 'alpha']

    def __init__(self, T=1000, alpha=0.9899, t_final=0.001, t=1, cities=29, step=200):
        data = LoadData()
        data.create_matrix()
        self.matrix = data.matrix
        self.T = T
        #self.t = t
        self.t_final = t_final
        self.alpha = alpha
        self.cities = cities
        self.Vc = None
        self.firts_vc = range(self.cities)
        self.step = step
        #import pandas
        #print pandas.DataFrame(self.matrix, range(self.cities), range(self.cities))

    def tsp(self):
        self.Vc = self.generate_solution()
        self.Vc_eval = self.eval_solution(self.Vc)
        while(self.T > self.t_final):
            for i in range(self.step):
                self.Vn = self.generate_solution(self.Vc)
                self.Vn_eval = self.eval_solution(self.Vn)
                delta = self.Vn_eval - self.Vc_eval
                if delta < 0:
                    self.Vc = self.Vn
                    self.Vc_eval = self.Vn_eval
                elif random_sample() < exp(-delta/self.T):
                    self.Vc = self.Vn
                    self.Vc_eval = self.Vn_eval
            self.T *= self.alpha
            #self.T *= self.reduce_temp(self.t)
            #self.t += 1

    def reduce_temp(self, t):
        return self.alpha / log(1 + t)

    def generate_solution(self, Vc=None):
        if Vc is None:
            Vn = list(permutation(self.firts_vc))
            return Vn
        Vn = deepcopy(Vc)
        i1 = randint(0, self.cities - 1)
        i2 = randint(0, self.cities - 1)
        while(i1 == i2):
            i2 = randint(0, self.cities - 1)
        Vn[i1], Vn[i2] = Vn[i2], Vn[i1]
        return Vn

    def eval_solution(self, Vn):
        km = 0
        for c in range(len(Vn) - 1):
            i = Vn[c]
            j = Vn[c + 1]
            km += self.matrix[i][j]
        km += self.matrix[Vn[0]][Vn[self.cities - 1]]
        return km

    def print_result(self):
        print self.Vc
        print self.eval_solution(self.Vc)

if __name__ == '__main__':
    start = time()
    tsp = SimulatedAnnealing()
    tsp.tsp()
    print "Resultado optimo"
    tsp.print_result()
    print "Tiempo: ", time() - start

