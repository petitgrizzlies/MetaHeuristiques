cdef class Individu:

    cdef double pm
    cdef str x
    cdef str y
    cdef double pc

    cpdef float callFitness(self)
    cpdef str getX(self)
    cpdef str getY(self)
    cpdef void setX(self, str x)
    cpdef void setY(self, str y)