# individu.pyx
# cython: profile=True

import cython
import numpy as np
import math

cimport numpy as np
from libc.math cimport fabs
from libc.math cimport sin
from libc.math cimport sqrt
from libc.math cimport pow
from libc.math cimport fmod

INT = np.int
ctypedef np.int_t INT_t

DOUBLE = np.double
ctypedef np.double_t DOUBLE_t


cdef class Individu:

    def __init__(self, str x, str y, double pm, double pc):
        if len(x) > len(y):
            y = (len(x) - len(y)) * "0" + y

        elif len(y) > len(x):
            x = (len(y) - len(x)) * "0" + x
        self.x = x
        self.y = y
        self.pm = pm
        self.pc = pc

    cpdef float callFitness(self):
        return fitness(int(self.x, 2), int(self.y, 2))

    def callMutation(self):
        self.x = ''.join(str(x) for x in mutation(self.pm, np.array(list(self.x), dtype=np.int)))
        self.y = ''.join(str(x) for x in mutation(self.pm, np.array(list(self.y), dtype=np.int)))

    cpdef str getX(self):
        return self.x

    cpdef str getY(self):
        return self.y

    cpdef void setX(self, str x):
        self.x = x

    cpdef void setY(self, str y):
        self.y = y


cdef np.ndarray[INT_t, ndim=1] mutation(double pm, np.ndarray[INT_t, ndim=1] x):
    cdef int lx = x.size
    cdef np.ndarray[DOUBLE_t, ndim=1] prob = np.random.rand(lx)
    cdef int acc = 0

    while(acc < lx):
        if pm > prob[acc]:
            x[acc] = <int>fmod(x[acc] + 1, 2)
        acc = acc + 1
    return x


@cython.cdivision(True)
cdef float fitness(int x, int y):
    cdef double noXZero = fabs(x + 0.001)
    cdef double noYZero = fabs(y + 0.001)

    return + pow(x / 1000, 512) +\
    pow(10 / noXZero, 4) +\
    pow(y / 1000, 512) +\
    pow(10 / noXZero, 4) -\
    fabs(0.5 * x * sin(sqrt(fabs(x)))) - fabs(y * sin(30 * sqrt(fabs(x / noYZero))))