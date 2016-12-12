#! /usr/bin/python3.5
# -*- coding: utf-8 -*-

import random
from copy import copy, deepcopy


class PROG:
    def __init__(self, progLength, functionSet, terminalSet, dataSet, cpu):
        self.prog = randomProg(progLength, functionSet, terminalSet)
        self.fitness = computeFitness(self.prog, cpu, dataSet)

    def __len__(self):
        return len(self.prog)

    def computeFitness(self, cpu, dataSet):
        self.fitness = computeFitness(self.prog, cpu, dataSet)


# This is the machine on which programs are executed
# The output is the value on top of the pile.
class CPU:
    def __init__(self):
        self.pile = []

    def reset(self):
        while len(self.pile) > 0:
            self.pile.pop()


# These are the instructions
def AND(cpu, data):
    # TO DO
    if len(cpu.pile) >= 2:
        b1 = cpu.pile.pop()
        b2 = cpu.pile.pop()
    else:
        return
    cpu.pile.append(b1 and b2)


def OR(cpu, data):
    # TO DO
    if len(cpu.pile) >= 2:
        b1 = cpu.pile.pop()
        b2 = cpu.pile.pop()
    else:
        return
    cpu.pile.append(b1 or b2)


def XOR(cpu, data):
    if len(cpu.pile) >= 2:
        b1 = cpu.pile.pop()
        b2 = cpu.pile.pop()
    else:
        return
    cpu.pile.append(b1 != b2)


def NOT(cpu, data):
    if len(cpu.pile) >= 1:
        b1 = cpu.pile.pop()
    else:
        return
    cpu.pile.append(not(b1))


# Push values of variables on the stack.
def X1(cpu, data):
    # TO DO
    cpu.pile.append(data[0])


def X2(cpu, data):
    # TO DO
    cpu.pile.append(data[1])


def X3(cpu, data):
    # TO DO
    cpu.pile.append(data[2])


def X4(cpu, data):
    # TO DO
    cpu.pile.append(data[3])


# Execute a program
def execute(program, cpu, data):
    # TO DO
    for ele in program:
        eval(ele)(cpu, data)
    try:
        res = cpu.pile[-1]
    except IndexError:
        res = -1
    cpu.reset()
    return res


# Generate a random program
def randomProg(length, functionSet, terminalSet):
    # TO DO
    prog = []
    for ele in range(length - 1):
        if random.random() > 0.66:
            # sélection terminal
            prog.append(functionSet[random.randint(0, len(functionSet) - 1)])
        else:
            # sélection de function
            prog.append(terminalSet[random.randint(0, len(terminalSet) - 1)])
    prog.append(functionSet[random.randint(0, len(functionSet) - 1)])
    return prog


# Computes the fitness of a program.
# The fitness counts how many instances of data in dataSet are correctly computed by the program
def computeFitness(prog, cpu, dataSet):
    # TO DO
    return (sum([1 if x[-1] == execute(prog, cpu, x) else 0 for x in dataSet]))


# Selection using 2-tournament.
def selection(Population, cpu, dataSet):
    newPopulation = []
    n = len(Population)
    for i in range(n):
        i1 = random.randint(0, n - 1)
        i2 = random.randint(0, n - 1)
        if Population[i1].fitness > Population[i2].fitness:
            newPopulation.append(Population[i1])
        else:
            newPopulation.append(Population[i2])
    return newPopulation


def crossover(Population, p_c):
    newPopulation = []
    n = len(Population)
    i = 0
    while(i < n):
        p1 = deepcopy(Population[i])
        p2 = deepcopy(Population[(i + 1) % n])
        m = len(p1)
        if random.random() < p_c:  # crossover
            k = random.randint(1, m - 1)
            newP1 = p1.prog[0:k] + p2.prog[k:m]
            newP2 = p2.prog[0:k] + p1.prog[k:m]
            p1.prog = copy(newP1)
            p2.prog = copy(newP2)
        newPopulation.append(p1)
        newPopulation.append(p2)
        i += 2
    return newPopulation


def fitness(population, cpu, dataSet):
    for ele in population:
        ele.computeFitness(cpu, dataSet)
    return population


def mutation(Population, p_m, terminalSet, functionSet):
    newPopulation = []
    nT = len(terminalSet) - 1
    nF = len(functionSet) - 1
    for p in Population:
        for i in range(len(p)):
            if random.random() > p_m:
                continue
            if random.random() < 0.5:
                p.prog[i] = terminalSet[random.randint(0, nT)]
            else:
                p.prog[i] = functionSet[random.randint(0, nF)]
        newPopulation.append(deepcopy(p))
    return newPopulation


def genetique(dataSet, functionSet, terminalSet, pm, pc, size, loop):
    cpu = CPU()
    progLength = 6
    population = [PROG(progLength, functionSet, terminalSet, dataSet, cpu) for x in range(size)]
    while loop > 0:
        population = selection(population, cpu, dataSet)
        population = crossover(population, pc)
        population = mutation(population, pc, terminalSet, functionSet)
        population = fitness(population, cpu, dataSet)
        loop -= 1
    res = [computeFitness(x.prog, cpu, dataSet) for x in population]
    return population[res.index(max(res))]

# -------------------------------------

# LOOK-UP TABLE YOU HAVE TO REPRODUCE.
if __name__ == '__main__':
    nbVar = 4
    cpu = CPU()
    dataSet = [[0, 0, 0, 0, 0], [0, 0, 0, 1, 1], [0, 0, 1, 0, 0], [0, 0, 1, 1, 0],
    [0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 1, 1, 0, 0], [0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0], [1, 0, 0, 1, 1], [1, 0, 1, 0, 0], [1, 0, 1, 1, 0],
    [1, 1, 0, 0, 0], [1, 1, 0, 1, 0], [1, 1, 1, 0, 0], [1, 1, 1, 1, 0]]
    for ele in dataSet:
        print(ele)

    # Function and terminal sets.
    pm = 0.1
    pc = 0.6
    functionSet = ["AND", "OR", "NOT", "XOR"]
    terminalSet = ["X1", "X2", "X3", "X4"]
    res = genetique(dataSet, functionSet, terminalSet, pm, pc, 20, 100)
    print("resultat : ", res.prog)
    print("fitness(resultat) = ", computeFitness(res.prog, cpu, dataSet))
