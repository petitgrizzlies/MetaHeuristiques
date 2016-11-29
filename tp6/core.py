#! /usr/bin/python3.5
# -*- coding:utf-8 -*-

from population import Population
import numpy as np
import math
import tqdm


MIN = -1356.48243686


def f(x,y):
    x = x + 0.01
    y = y + 0.01
    return math.pow(x/1000,512) + math.pow(10 / x,8) + math.pow( y/1000,512)\
     + math.pow(10/y,8) - math.fabs(0.5 * x *\
         math.sin(math.sqrt(math.fabs(x)))) - math.fabs(y * math.sin(30 * math.sqrt(math.fabs(x/y))))


def findMin():
    x = np.arange(0, 1200)
    y = np.arange(0, 1200)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros(Y.shape)
    for i in range(len(y)):
        for j in range(len(y)):
            Z[i, j] = f(X[i, j], Y[i, j])
    print(Z.min())


if __name__ == '__main__':
    diff = []
    for ele in tqdm.tqdm(range(100)):
        p = Population(0.1, 0.6, 100)
        i = p.main(1, 5, 0)
        diff.append(math.fabs(i.callFitness() - MIN))
    print(np.mean(diff))
