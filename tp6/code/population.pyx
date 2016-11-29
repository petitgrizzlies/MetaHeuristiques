#!python
#population.pyx
#cython: profile=True

from individu cimport Individu
from libc.stdlib cimport rand, RAND_MAX

import numpy as np
cimport numpy as np
from libc.math cimport fmod

from copy import deepcopy
from copy import copy
import math
import time


DOUBLE = np.double
ctypedef np.double_t DOUBLE_t

cdef double MIN = -1356.48243686

def getKey(item):
    return item.callFitness()


cdef class Population:

    cdef int size
    cpdef public individus
    cdef double pc

    def __init__(self, pm, pc, size_population):
        self.individus = []
        self.size = size_population
        self.pc = pc

        cdef int iter = size_population
        cdef int zero = 0
        while(iter > 0):
            x = np.random.randint(10, 1001)
            y = np.random.randint(10, 1001)
            self.individus.append(Individu(bin(x)[2:], bin(y)[2:], pm, pc))
            iter = iter - 1


    cdef Individu tournament(self, number):
        cdef int i = 0
        cdef int n = len(self.individus)
        choosen = []
        while(i < number):
            i = i + 1
            choosen.append(self.individus[<int>fmod(rand(),n)])
        sorted(choosen, key=getKey)
        return choosen[0]

    cpdef void selection(self, number):
        cdef int iter = self.size -1 
        cdef int zero = 0
        individus = [0] * self.size
        while(iter >= 0):
            individus[iter] = self.tournament(number)
            iter = iter - 1
        self.individus = individus

    cpdef void mutation(self):
        cdef int iter = 0
        while(iter < self.size):
            self.individus[iter].callMutation()
            iter = iter + 1

    cpdef void crossover(self, int choice):
        cdef int iter = 0
        if choice == 0:
            while(iter < self.size-1):
                onePointCrossover(self.individus[iter], self.individus[iter + 1], self.pc)
                iter = iter + 2
        else:
            while(iter < self.size-1):
                midBreak(self.individus[iter], self.individus[iter + 1], self.pc)
                iter = iter + 2
    
    cdef Individu getMin(self):
        cdef int i = 0
        cdef double minimum = self.individus[0].callFitness()
        cdef int index = 0
        while(i < self.size):
            if self.individus[i].callFitness() < minimum:
                minimum = self.individus[i].callFitness()
                index = i
            i = i + 1
        return self.individus[index]

    cpdef Individu main(self, int loop, int number, int choice):
        cdef int i = 0
        while (i < loop):
            i = i + 1
            self.selection(number)
            self.crossover(0)
            self.mutation()
        cdef Individu best = self.getMin()
        return best

cpdef void onePointCrossover(Individu i1, Individu i2, pc):

    if pc > np.random.rand():
        x = str(i1.getX())
        y = str(i1.getY())

        new_x = str(i2.getX())
        new_y = str(i2.getY())

        if len(new_x) >= len(x):
            x = (len(new_x) - len(x)) * "0" + x
        else:
            new_x = (len(x) - len(new_x)) * "0" + new_x

        if len(new_y) >= len(y):
                y = (len(new_y) - len(y)) * "0" + y
        else:
            new_y = (len(y) - len(new_y)) * "0" + new_y

        point = np.random.randint(len(x))

        tmpX = copy(x[point:])
        tmpY = copy(x[point:])

        i1.setX(x[:point] + new_x[point:])
        i1.setY(y[:point] + new_y[point:])
        i2.setX(new_x[:point] + tmpX)
        i2.setY(new_y[:point] + tmpY)

cpdef void midBreak(Individu i1, Individu i2, pc):
    if pc > np.random.rand():
        x = str(i1.getX())
        y = str(i1.getY())

        new_x = str(i2.getX())
        new_y = str(i2.getY())

        if len(new_x) >= len(x):
            x = (len(new_x) - len(x)) * "0" + x
        else:
            new_x = (len(x) - len(new_x)) * "0" + new_x

        if len(new_y) >= len(y):
                y = (len(new_y) - len(y)) * "0" + y
        else:
            new_y = (len(y) - len(new_y)) * "0" + new_y

        point = math.floor(len(x)/2)

        tmpX = copy(x[point:])
        tmpY = copy(x[point:])

        i1.setX(x[:point] + new_x[point:])
        i1.setY(y[:point] + new_y[point:])
        i2.setX(new_x[:point] + tmpX)
        i2.setY(new_y[:point] + tmpY)