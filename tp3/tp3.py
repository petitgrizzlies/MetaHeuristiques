#! /usr/bin/python3.5
# -*- coding: utf-8 -*-

import numpy as np
# import matplotlib.pyplot as plt
import ctypes
from numpy.ctypeslib import ndpointer


def chargement_villes(fichier):
    """
    With a string that is the path of cities files.
    We open it and load the cities and return it.
    """
    file = open(fichier, 'r')
    d = {}
    s = []
    for lines in file.readlines():
        numbers = lines.split()[1:]
        numbers = [float(numbers[0]), float(numbers[1])]
        d[lines.split()[0]] = numbers.copy()
        s.append(numbers)
    return [d, s]


def energie(solution):
    """
    With a solution of form:
        - solution = [[1,2],[2,3],[1,100],..]
    We compute the energy of the solution as the norme two
    """
    # n = len(solution)
    # acc = 0
    # for i in range(0, n-1):
    #     acc += np.sqrt(np.power(solution[i][0] - solution[i + 1][0], 2) + np.power(solution[i][1] - solution[i + 1][1], 2))
    # acc += np.sqrt(np.power(solution[n - 1][0] - solution[0][0], 2) + np.power(solution[n - 1][1] - solution[0][1], 2))
    # return acc

    sol = np.array(solution, dtype=np.float32)
    return lib.norm(sol, len(solution))


def generation_solution(villes):
    """
    With the cities as a list, we generate a random permutation of this list
    to create a solution
    """
    return np.random.permutation(villes)


def generation_voisins(solution):
    """
    With a solution we generate a neighbor with one permutaiton
    return a new solution
    """
    value_one = 0
    value_two = 0
    n = len(solution)
    new_solution = solution.copy()
    while(value_one == value_two):
        value_one = np.random.randint(n)
        value_two = np.random.randint(n)

    # the value's swap
    tmp = new_solution[value_one].copy()
    new_solution[value_one] = new_solution[value_two].copy()
    new_solution[value_two] = tmp

    return new_solution.copy()


def temperature_initiale(villes):
    """
    With the list of cities, we do 100 random permutation, and compute the mean.
    Then with this mean we compute the T0 and return it.
    """
    acc = 0
    # generate solution
    solution = generation_solution(villes)
    for _ in range(100):
        acc += energie(generation_voisins(solution))

    mean = acc / 100
    T0 = - mean / np.log(0.5)

    if T0 > 0:
        return T0
    else:
        temperature_initiale(villes)


def test_acceptation(solution, new_solution, T):
    """
    With two solution, we compute if we choose or not the new solution
    """
    energie_old = energie(solution)
    energie_new = energie(new_solution)
    delta = (energie_new - energie_old)

    P = min(1, np.exp(-delta/T))

    if np.random.rand() < P:
        return True
    else:
        return False


def recuit(fichier):
    """
    With a path, we do the recuit
    """
    # we get the dictionnary and the solution
    [d, villes] = chargement_villes(fichier=fichier)

    # init the lib c++ call
    global lib
    lib = ctypes.cdll.LoadLibrary('./libnormcpp.so')
    lib.norm.argtypes = [ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"), ctypes.c_int]
    lib.norm.restype = ctypes.c_float
    lib.acceptation.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float]

    # we compute the temperate
    T = temperature_initiale(villes=villes)

    # creation d'une solution aléatoire
    solution_initiale = generation_solution(villes)

    solution = solution_initiale.copy()
    # condition to stop loop
    condition = True

    cChangement = 0
    cIteration = 0
    cAucunChangement = 0
    n = len(villes)

    while(condition):
        new_solution = generation_voisins(solution)

        # we accept or not the solution generated
        if lib.acceptation(energie(solution), energie(new_solution), T, np.random.rand()):

            cChangement += 1
            solution = new_solution.copy()
        else:
            cIteration += 1

        if cChangement == 12 * n:
            T = 0.9 * T
            cChangement = 0
            cIteration = 0
            cAucunChangement = 0

        elif cIteration == 100 * n:
            T = 0.9 * T
            cChangement = 0
            cIteration = 0
            cAucunChangement += 1

        if cAucunChangement == 3:
            condition = False

    r, s = solution.shape

    res = np.zeros((r+1, s))

    res[0:r] = solution
    res[r] = solution[0]

    return res


def choix_villes(position, villes):
    """
    We choose the closest reming citie
    """
    # we apply the energie to all liste
    valeur = list(map(lambda y: np.sqrt(np.power(position[0] - y[0], 2) + np.power(position[1] - y[1], 2)), villes))
    index = valeur.index(min(valeur))
    ele = villes[index]

    villes.remove(ele)
    return [ele, villes]


def greedy(fichier):
    """
    With a file, we do the greedy algorithme:
        we take the closest remining cities as choosen neighbor
    """
    [d, villes] = chargement_villes(fichier)

    # init the lib c++ call
    global lib
    lib = ctypes.cdll.LoadLibrary('./libnormcpp.so')
    lib.norm.argtypes = [ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"), ctypes.c_int]
    lib.norm.restype = ctypes.c_float
    lib.acceptation.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float]

    solution = [villes[np.random.randint(len(villes))]]
    villes.remove(solution[0])

    while not(villes == []):

        [ville_suivante, villes] = choix_villes(solution[-1], villes)
        solution.append(ville_suivante)
    solution.append(solution[0])

    return solution


def dix_fois(fichier):
    acc_greedy = []
    acc_recuit = []
    for _ in range(10):
        acc_greedy.append(energie(greedy(fichier)))
        acc_recuit.append(energie(recuit(fichier)))
    moyenne_greedy = sum(acc_greedy)/len(acc_greedy)
    moyenne_recuit = sum(acc_recuit)/len(acc_recuit)
    var_greedy = np.var(acc_greedy)
    var_recuit = np.var(acc_recuit)
    print("Moyenne greedy = " + str(moyenne_greedy) + "\t Std = " + str(np.sqrt(var_greedy)))
    print("Moyenne recuit = " + str(moyenne_recuit) + "\t Std = " + str(np.sqrt(var_recuit)))


def cree_cercle(n):
    """
    Give n the number of cities, we create a circle of n cities
    """
    # we compute the angle
    angle = 360.0 / n
    alpha = 0
    liste = []
    # x = cos(alpha)
    # y = sin(alpha)
    while alpha < 360:
        x = np.cos(alpha)
        y = np.sin(alpha)
        liste.append([x, y])
        alpha += angle

    file = open('cities' + str(n) + '.dat', 'w+')
    for i, points in enumerate(liste):
        file.write('c' + str(i) + ' ' + str(points[0]) + ' ' + str(points[1]) + '\n')
    file.close()


if __name__ == '__main__':
    sol = recuit('cities2.dat')
    # m = np.matrix(sol)
    # plt.plot(m[:, 0], m[:, 1])
    # plt.title("$Energie_{solution} = $" + str(energie(sol)))
    # plt.scatter(m[:, 0], m[:, 1])
    # plt.show()
