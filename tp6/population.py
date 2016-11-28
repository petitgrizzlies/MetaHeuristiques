#! /usr/bin/python3.5
# -*- coding:utf-8 -*-

from individu import Individu
import numpy as np


class Population():

    def __init__(self, pm, pc, size_population):
        self.individus = []
        for ele in range(size_population):
            x = np.random.randint(10, 1001)
            y = np.random.randint(10, 1001)
            self.individus.append(Individu(bin(x)[2:], bin(y)[2:], pm, pc))

    def tournament(self, number):
        x = number
        return x
