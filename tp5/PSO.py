#! /usr/bin/python3.5
# -* coding:utf-8 -*-

import neuralNet
import numpy as np
import copy
import matplotlib.pyplot as plt


def floor(number):
    if number >= 0.5:
        return 1
    return 0


class Particule():

    def __init__(self, index, size_theta1, size_theta2, images, labels):
        self.index = index
        self.theta1_size = size_theta1
        self.theta2_size = size_theta2
        self.theta1 = (1-(-1)) * np.random.random_sample(size_theta1[0] * size_theta1[1]) + -1
        self.theta2 = (1-(-1)) * np.random.random_sample(size_theta2[0] * size_theta2[1]) + -1
        self.v = np.random.rand(size_theta1[0] * size_theta1[1] + size_theta2[0] * size_theta2[1])
        self.best = np.append(self.theta1, self.theta2)
        self.fitnessValue = self.fitness(images, labels)
        self.bestValue = self.fitnessBest(images, labels)

    def update(self, omega, c1, r1, c2, r2, bestGlobal):
        theta = np.array(self.theta1_size[0] * self.theta1_size[1] + self.theta2_size[0] * self.theta2_size[1])
        theta = np.append(self.theta1, self.theta2)
        self.v = omega * self.v + c1 * r1 * (self.best - theta) + c2 * r2 * (bestGlobal.best - theta)
        theta += self.v
        self.theta1 = theta[0: self.theta1_size[0] * self.theta1_size[1]]
        self.theta2 = theta[self.theta1_size[0] * self.theta1_size[1]:]

    def fitness(self, images, labels):
        liste = [floor(neuralNet.fitness(self.theta1.reshape(self.theta1_size), self.theta2.reshape(self.theta2_size), 1, x)) for x in images]
        res = np.array(labels) - np.array(liste)
        self.fitnessValue = sum([x*x for x in res])
        return self.fitnessValue

    def fitnessBest(self, images, labels):
        theta1 = self.best[0: self.theta1_size[0] * self.theta1_size[1]]
        theta2 = self.best[self.theta1_size[0] * self.theta1_size[1]:]
        liste = [floor(neuralNet.fitness(theta1.reshape(self.theta1_size), theta2.reshape(self.theta2_size), 1, x)) for x in images]
        res = np.array(labels) - np.array(liste)
        return sum([x*x for x in res])

    def updateBest(self, images, labels):
        if self.fitnessValue < self.bestValue:
            self.best = np.append(self.theta1, self.theta2)
            self.bestValue = copy.deepcopy(self.fitnessValue)


class Espace():

    def __init__(self, size_theta1, size_theta2, number, images, labels):
        self.particule = []
        for index in range(number):
            self.particule.append(Particule(index, size_theta1, size_theta2, images, labels))

    def initBest(self):
        res = (list(map(lambda x: x.fitnessValue, self.particule)))
        index = res.index(min(res))
        self.bestGlobal = self.particule[index]

    def findBest(self):
        res = [x.fitnessValue for x in self.particule]
        index = res.index(max(res))
        if self.particule[index].fitnessValue < self.bestGlobal.fitnessValue:
            self.bestGlobal = copy.deepcopy(self.particule[index])


def update(x, omega, c1, c2, bestGlobal):
    """
    On assume que x est un objet particule
    """
    x.update(omega, c1, np.random.rand(), c2, np.random.rand(), bestGlobal)


def main(particuleNumbers, xPath, yPath, t1, t2, t_max):
    # on initialise le tout
    images, labels = neuralNet.read_image(xPath, yPath, 200)
    e = Espace(t1, t2, particuleNumbers, images, labels)
    e.initBest()
    res = [e.bestGlobal.fitnessValue]
    # init constante
    omega = 0.9
    c1 = 2
    c2 = 2

    while(t_max > 0):
        # calculate its fitness
        [x.fitness(images, labels) for x in e.particule]
        # update the best
        [x.updateBest(images, labels) for x in e.particule]
        # find the absolute best
        e.findBest()
        res.append(e.bestGlobal.fitnessValue)
        [update(x, omega, c1, c2, e.bestGlobal) for x in e.particule]
        t_max -= 1
        print(t_max)

    return res

if __name__ == '__main__':
    res = main(particuleNumbers=5, xPath='X.data', yPath='Y.data', t1=[25, 401], t2=[1, 26], t_max=30)
    # plt.plot(res)
    # plt.show()
