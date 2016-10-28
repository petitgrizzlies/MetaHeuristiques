#! /usr/bin/python3.5
# -*- coding: utf-8 -*-

import random
import numpy as np
import matplotlib.pyplot as plt


def subdivied(Liste, Size):
    """
    On divise la liste Liste, en :
        sum from i = 1 to N - Size [x_i,x_i+1,...x_i+Size]
    """
    res = []
    # pour chaque éléments de la liste
    for index, ele in enumerate(Liste):
        res_tmp = []
        # on construit une sous-liste si on ne dépasse pas
        if index + Size <= len(Liste):
            for k in range(Size):
                res_tmp.append(Liste[index+k])
            # on ajoute la sous-liste construite au res
            res.append(res_tmp)
            # on retourne le reste
    return res


def fitness(solution, K, dictionnaire):
    """
    solution = un tableau de {0,1} qui représente une solution
    K = le k du problème NK
    dictionnaire = tableau de correspondance entre les suites de bits
    et les valeurs
    """
    # on divisie la liste en sous-liste de taille K+1
    SubListe = subdivied(solution, K+1)
    accumulateur = 0
    # on accumule les résultats des fitness
    for ele in SubListe:
        accumulateur += dictionnaire[tuple(ele)]
    return accumulateur


def Hamming(v1, v2):
    """
        On fait la distance de hamming entre
        v1 et v2
    """
    d = 0
    for index, ele in enumerate(v1):
        d += np.abs(v1[index] - v2[index])
    return d


def random_sequence(Size):
    """
    On génère une séquence aléatoire de bit. Séquence de taille: Size
    """
    res = []
    for ele in range(Size):
        # on utilise le random fourni par python
        if random.random() < 0.5:
            res.append(0)
        else:
            res.append(1)
    return res


def neighbor(solution):
    """
    solution est une solution. donc un vecteur de bit de taille n.
    on veut trouver son voisinage: soit les vecteurs ayant un seul bits de différence avec lui
    """
    res = []
    # pour chaque élément, on va créer un nouveau vecteur, avec un seul bit
    # qui diffère
    for index, ele in enumerate(solution):
        # on ajoute 1 et modulo 2. c'est comme un xor
        ele = (ele + 1) % 2
        # on ajoute la soluton
        res_tmp = list(solution)
        res_tmp[index] = ele
        res.append(res_tmp)
    return res


def choose_neighbor(neighbors, dictionnaire, K, sol_fitness):
    """
    On va choisir le meilleur voisins parmis ceux possibles
    """
    d = {}
    # on calcule toutes les fitness des voisins
    for ele in neighbors:
        d[fitness(ele, K, dictionnaire)] = ele
    # on prend le max s'il est meilleur, et on le retourne
    if max(d) > sol_fitness:
        return [True, d[max(d)]]
    # si non on signifie qu'on s'arrête
    else:
        return [False]


def Hill_Climbing(N, K, dictionnaire):
    """
    K = le k du NK-landscape
    dictionnaire = la table de correspondance
    On va appliquer le hill-climbing
    """
    # on génère une solution aléatoire
    sol = random_sequence(N)
    steps = 0
    # boucle infinie
    while(True):
        # on calcule les voisins
        voisins = neighbor(sol)
        # on choisit le meilleur voisin
        Liste_tmp = choose_neighbor(voisins, dictionnaire, K, fitness(sol, K, dictionnaire))
        # s'il y en a un, on continue
        if Liste_tmp[0]:
            sol = Liste_tmp[1]
            steps += 1
        # sinon on s'arrête et on renvoit le résultat
        else:
            print(sol, ":", fitness(sol, K, dictionnaire))
            return [sol, steps]


def choose_neighbor_probabiliste(voisins, dictionnaire, K, fitness_sol, best_sol):
    """
    Cf énoncé du tp. On utilise un raisonnement probabiliste
    """
    # on calcul la fitness du best
    fitness_best = fitness(best_sol, K, dictionnaire)
    element = [a for a in range(len(voisins))]
    fitness_res = []
    # on calcule la fitness de tout les voisins
    for ele in voisins:
        fitness_res.append(fitness(ele, K, dictionnaire))
    # on regarde s'il y a un meilleur élément absolu
    if max(fitness_res) > fitness_best:
        return [False, voisins[fitness_res.index(max(fitness_res))]]
    # sinon on en choisit un
    else:
        fitness_res = list(map(lambda x: x/sum(fitness_res), fitness_res))
        return [True, voisins[np.random.choice(element, p=fitness_res)]]


def Hill_Climbing_probabiliste(N, K, dictionnaire, Steps):
    """
    On prend les mêmes paramètres que le Hill_Climbing ci dessus
    mais on ajoute le nombre de pas avant la fin
    """
    # on génère une solution aléatoire qui sera notre solution idéale initiale
    sol = random_sequence(N)
    best = list(sol)
    # boucle à condition
    while(Steps > 0):
        # on calcule les voisins
        voisins = neighbor(sol)
        Liste_tmp = choose_neighbor_probabiliste(voisins, dictionnaire, K, fitness(sol, K, dictionnaire), best)
        # si le premier élément est true, alors on a changé de solution, mais
        # ce n'est pas la meilleure
        if Liste_tmp[0]:
            sol = list(Liste_tmp[1])
        # si le premier élément est false, alors on a trouvé un nouveau best,
        else:
            best = list(Liste_tmp[1])
        Steps -= 1
    print(best, ":", fitness(best, K, dictionnaire))
    return best


def Hill_50_times_proba(N, K, dictionnaire, Steps):
    """
    On va lancer 50 fois le hill_climbing probabiliste
    Avec les paramètres fixés du tp. On stock les résultats dans une liste
    """
    a = 50
    final = []
    while(a):
        a -= 1
        # on récupère les résultats au fur et à mesure
        final.append(Hill_Climbing_probabiliste(N, K, dictionnaire, 10*Steps))
    return final


def Hill_50_times(N, K, dictionnaire):
    """
    On va lancer 50 fois le hill_climbing déterministe
    Avec les paramètres fixés du tp. On stock les résultats dans une liste
    """
    a = 50
    final = []
    while(a):
        a -= 1
        # on récupère les résultats
        final.append(Hill_Climbing(N, K, dictionnaire))
    return final


def test_tp1():
    d_k0 = {(0,): 2, (1,): 1}
    d_k1 = {(0, 0): 2, (0, 1): 3, (1, 0): 2, (1, 1): 0}
    d_k2 = {(0, 0, 0): 0, (0, 0, 1): 1, (0, 1, 0): 1, (0, 1, 1): 0, (1, 0, 0): 2, (1, 0, 1): 0, (1, 1, 0): 0, (1, 1, 1): 0}

    final_0 = Hill_50_times(21, 0, d_k0)
    tmp = np.matrix(final_0)
    tmp = sum(tmp[:, 1])
    moyenne_steps_0 = tmp[0, 0] / 50
    print("Moyenne pas K=0 : ", moyenne_steps_0)

    final_1 = Hill_50_times(21, 1, d_k1)
    tmp = np.matrix(final_1)
    tmp = sum(tmp[:, 1])
    moyenne_steps_1 = tmp[0, 0] / 50
    print("Moyenne pas K=1 : ", moyenne_steps_1)

    final_2 = Hill_50_times(21, 2, d_k2)
    tmp = np.matrix(final_2)
    tmp = sum(tmp[:, 1])
    moyenne_steps_2 = tmp[0, 0] / 50
    print("Moyenne pas K=2 : ", moyenne_steps_2)

    final_prob_0 = Hill_50_times_proba(21, 0, d_k0, moyenne_steps_0)
    print("Fin proba K=0")

    final_prob_1 = Hill_50_times_proba(21, 1, d_k1, moyenne_steps_1)
    print("Fin proba K=1")

    final_prob_2 = Hill_50_times_proba(21, 2, d_k2, moyenne_steps_2)
    print("Fin proba K=2")

    # la distance max est de N, donc 21, on crée un dictionnaire de
    # taille 21, on aura plus qu'a incrémenter

    d_d_0 = []
    d_d_1 = []
    d_d_2 = []
    d_p_0 = []
    d_p_1 = []
    d_p_2 = []

    for i in range(50):
        for j in range(50-i):
            d_d_0.append(Hamming(final_0[i][0], final_0[j][0]))
            d_d_1.append(Hamming(final_1[i][0], final_1[j][0]))
            d_d_2.append(Hamming(final_2[i][0], final_2[j][0]))
            d_p_0.append(Hamming(final_prob_0[i], final_prob_0[j]))
            d_p_1.append(Hamming(final_prob_1[i], final_prob_1[j]))
            d_p_2.append(Hamming(final_prob_2[i], final_prob_2[j]))

    plt.hist(d_d_0)
    print("d_d_0")
    plt.show()

    plt.hist(d_d_1)
    print("d_d_1")
    plt.show()

    plt.hist(d_d_2)
    print("d_d_2")
    plt.show()

    plt.hist(d_p_0)
    print("d_p_0")
    plt.show()

    plt.hist(d_p_1)
    print("d_p_1")
    plt.show()

    plt.hist(d_p_2)
    print("d_p_2")
    plt.show()


def interface():
    """
    Il s'agit d'une interface.
    On prend une entrée pour choisir le type e méthode.
    Puis la valeur de K
    """
    # les valeurs des dictionnaires
    d_k0 = {(0,): 2, (1,): 1}
    d_k1 = {(0, 0): 2, (0, 1): 3, (1, 0): 2, (1, 1): 0}
    d_k2 = {(0, 0, 0): 0, (0, 0, 1): 1, (0, 1, 0): 1, (0, 1, 1): 0, (1, 0, 0): 2, (1, 0, 1): 0, (1, 1, 0): 0, (1, 1, 1): 0}

    print("[1] : Hill-Climbing déterministe (default)\n[2] : Hill-Climbing probabiliste\n")
    i = input()
    if i != 2:
        print("Hill-Climbing déterministe")
        k = input("K=")
        if str(k) == '0':
            Hill_Climbing(21, 0, d_k0)
        elif str(k) == '1':
            Hill_Climbing(21, 1, d_k1)
        elif str(k) == '2':
            Hill_Climbing(21, 2, d_k2)
        else:
            print("Erreur\n")
    else:
        print("Hill-Climbing probabiliste")
        k = input("K=")
        if str(k) == '0':
            Hill_Climbing_probabiliste(21, 0, d_k0, 10 * 10)
        elif str(k) == '1':
            Hill_Climbing_probabiliste(21, 1, d_k1, 10 * 6)
        elif str(k) == '2':
            Hill_Climbing_probabiliste(21, 2, d_k2, 10 * 6)
        else:
            print("Erreur\n")


if __name__ == '__main__':
    while(True):
        interface()
