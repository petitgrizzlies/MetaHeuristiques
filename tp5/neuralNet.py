#! /usr/bin/python3.5
# -* coding:utf-8 -*-

import numpy as np
from numba import *


def read_image(pathX, pathY, n):
    """
    Depuis le path des données, ainsi que le path des labels, et le nombre de lignes
    On charge tout dans deux matrices.
    Une d'image et une de label
    """
    fileX = open(pathX, 'r')
    fileY = open(pathY, 'r')

    dataX = fileX.readlines()
    dataY = fileY.readlines()

    images = [0] * n
    labels = [0] * n
    for index in range(n):
        images[index] = np.array(dataX[index].strip('\n').split(','), dtype=np.float32)
        labels[index] = int(dataY[index].strip('\n'))

    fileX.close()
    fileY.close()
    return images, labels


def layout(theta, biais, vecteur):
    """
    On prend la matrice theta, on ajoute le biais à vecteur. On fait la
    multiplication matricielle. On retourne le résultat après y avoir appliqué la fonction g.
    """
    return np.squeeze(np.asarray(1./(1 + np.exp(-theta.dot(np.matrix(np.append(vecteur, 1)).transpose())))))


def fitness(theta1, theta2, biais, vecteur):
    """
    On simule des layouts.
    """
    res = layout(theta=theta1, biais=biais, vecteur=vecteur)
    res = layout(theta=theta2, biais=biais, vecteur=res)

    return res.max()
