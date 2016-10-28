#! /usr/bin/python3.5
# -*- coding: utf-8

import numpy as np
import re


def read_data(file):
    """
    Give a .dat file, we read the:
        - n
        - W
        - D
    """
    opened_file = open(file)
    n = int(opened_file.readline().strip('\n'))
    W = np.zeros((n, n))
    D = np.zeros((n, n))
    opened_file.readline()
    for iterator in range(n):
        # the separator is a space
        line = opened_file.readline().strip('\n').split(' ')
        # we put the reading line in the matrix
        if '' in line:
            line.remove('')
        W[iterator, :] = line
    opened_file.readline()
    for iterator in range(n):
        # i use regex because your way to separate element is aweful
        line = opened_file.readline()
        D[iterator, :] = re.findall(r"[0-9]+", line)
    return [n, W, D]


def fitness(W, D, sol):
    """
    Fitness will compute the value of our solution.
    We assume that:
        - W is the flow matrix
        - D is the distance matrix
        - sol is a solution
    We assume that W,D are some numpy matrix
    Sol is a list.
    """
    res = 0
    for i in range(len(sol)):
        for j in range(i+1, len(sol)):
            # we take the object i in sol and object j
            # we substract 1 beacause we count from 0
            res += W[i, j] * D[sol[i] - 1, sol[j] - 1]
    return 2 * res


def delta(W, D, sol, i, j):
    """
    We compute the delta between two solution.
    We assurme that:
        - W ia the flow matrix
        - D is the distance matrix
        - sol is the solution
        - i is the index of first moved object
        - j is the index of second moved object
    We assume that W,D are numpy matrix
    Sol is a list.
    """
    res = 0
    # we reduce i,j because we count from 0
    j -= 1
    i -= 1
    for k in range(len(sol)):
        if k != i and k != j:
            res += (W[j, k] - W[i, k]) * (D[sol[i] - 1, sol[k] - 1] - D[sol[j] - 1, sol[k] - 1])
    return 2 * res


def generate_neighbor(W, D, sol):
    """
    We generate all solution. We use the same sum as the fitness.
    We have:
        -W : the flow matrix
        -D : the distance matrix
        -sol : a solution
    """
    res = []
    fitness_sol = fitness(W=W, D=D, sol=sol)
    for i in range(len(sol)):
        for j in range(i + 1, len(sol)):
            neighbor = list(sol)
            # we swap the i and j objects
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            # we compute the fitness
            new_fitness_sol = fitness_sol + delta(W=W, D=D, sol=neighbor, i=i, j=j)
            r = i
            s = j
            object_i = sol[r]
            object_j = sol[s]
            res.append([new_fitness_sol, neighbor, object_i, r, object_j, s])
    return res


class ListeTabou:
    """
    It's a matrix to represente the forbbiden assignation.
    It has a size = nxn.
    """

    def __init__(self, listeTabouSize):
        self.listeTabou = np.zeros((listeTabouSize, listeTabouSize))

    def add(self, i, r, j, s, t, l):
        # we decrease i,j because it's some object
        # and the object are 1 to N not 0 to N-1
        i -= 1
        j -= 1
        self.listeTabou[i, r] = t + l
        self.listeTabou[j, r] = t + l

    def permitted(self, i, j, r, s, t):
        return self.listeTabou[i, r] <= t and self.listeTabou[j, s] <= t


def random_solution(W, D, n):
    """
    We generate a solution of size n
    """
    sol = np.random.permutation(n) + 1
    fitness_sol = fitness(W=W, D=D, sol=sol)
    return [fitness_sol, sol]


def choose_neighbor(W, D, sol, best, t, l, listeTabou):
    """
    We choose a neighbor according to tabou liste and asspiraiton
    """
    neighbors = generate_neighbor(W=W, D=D, sol=sol)
    neighbors.sort()
    for ele in neighbors:
        [fitness, sol, i, r, j, s] = ele
        # if we have a new best element
        if ele[0] < best[0]:
            # we add this movement to the matrix
            listeTabou.add(i=i, r=r, j=j, s=s, t=t, l=l)
            best = [fitness, sol]
            return [best, best]
        else:
            if listeTabou.permitted(i=i - 1, j=j - 1, r=r, s=s, t=t):
                listeTabou.add(i=i, r=r, j=j, s=s, t=t, l=l)
                return [best, [fitness, sol]]
    return [best, [fitness(W, D, sol), sol]]


def tabouSearch(file, l, t_max):
    """
    It combines all previous function to build a tabou search
    """
    # read file for n, W, D
    [n, W, D] = read_data(file)
    # generate solution
    sol = random_solution(W=W, D=D, n=n)
    # at begining the best is the sol
    best = list(sol)
    # we define t and l
    t = 0
    if l != 1:
        l = round(l * n)
    # the list tabou
    listeTabou = ListeTabou(n)
    acc = []
    # loop
    while t != t_max:
        # we choose a solution
        [best, sol] = choose_neighbor(W=W, D=D, sol=sol[1], best=best, t=t, l=l, listeTabou=listeTabou)
        acc.append(sol[0])
        t += 1

    return [best, acc]


def runTenTimesDat(file, l, t_max):
    """
    We run ten times the algorithme on a certain problem with
    a certain l and t_max
    """
    acc = []
    best = []
    for ele in range(10):
        res = tabouSearch(file=file, l=l, t_max=t_max)
        acc.append(res[1])
        best.append(res[0])
    print("For l= " + str(l) + "\tBest = " + str(min(best)[0]) + "\tmean = " + str(np.mean(acc)) + "\tstd. dev = " + str(np.sqrt(np.var(acc))))


def generate_data(n):
    """
    We generate data for a QAP problem.
    Two symterical matrix
    """
    # we create the matrix of the right size with random integers
    D = np.random.random_integers(0, 5, size=(n, n))
    W = np.random.random_integers(0, 10, size=(n, n))
    # we create symetrical matrix
    D = np.tril(D) + np.tril(D, -1).T
    W = np.tril(W) + np.tril(W, -1).T
    # we define the diag to 0
    np.fill_diagonal(D, 0)
    np.fill_diagonal(W, 0)

    # we write data in file
    data = open(str(n) + ".dat", 'w+')
    data.write(str(n) + "\n\n")

    # we write the D matrix
    for line in D:
        string = ""
        for ele in line:
            string += str(ele) + " "
        data.write(string + "\n")

    data.write("\n")
    # same thing for the W
    for line in W:
        string = ""
        for ele in line:
            string += str(ele) + " "
        data.write(string + "\n")


if __name__ == '__main__':
    runTenTimesDat(file="1.dat", l=1, t_max=5000)
    runTenTimesDat(file="1.dat", l=0.5, t_max=5000)
    runTenTimesDat(file="1.dat", l=0.9, t_max=5000)

    generate_data(40)
    generate_data(50)
    generate_data(80)
    generate_data(100)
