#! /usr/bin/python3.5
# -*- coding:utf-8 -*-

from population import Population
import numpy as np
import math
import tqdm


MIN = -1356.48243686

if __name__ == '__main__':
    diff = []
    best = 0
    for ele in tqdm.tqdm(range(100)):
        p = Population(0.1, 0.6, 100)
        i = p.main(100, 5, 0)
        diff.append(math.fabs(i.callFitness() - MIN))
        if best > i.callFitness():
            best = i.callFitness()
    print(np.mean(diff))
    print(best)
