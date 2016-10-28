#! /usr/bin/python3
# -*- coding:utf-8 -*-

import random as rd
import fractions as fractions
from functools import reduce
import fractions as f


def de_equilibre(N):
    """
    Dé équilibré à N face. On génère un i inclu [0,1),
    On multiplie i par N. On ajoute 1 et on obtient le résultat du dé.
    """
    nombre = rd.random()
    i = round(nombre * N)
    return i


def test_de_equilibre(N, M):
    """
    Test du dé équilibré à N faces, avec M essais
    """
    tableau_res = [0 for i in range(N)]
    while(M):
        res = de_equilibre(6)
        tableau_res[res-1] += 1
        M -= 1
    for index, ele in enumerate(tableau_res):
        print("La face : ", index+1, " est apparue : ", ele)


def ppcm(x, y):
    """
    On calcule le ppcm
    """
    return fractions.gcd(x, y)


def ppcm_list(Liste):
    """
    On applique le ppcm sur toute la liste pour
    obtenir le résultat
    """
    return reduce(ppcm, Liste)


def de_pipe_avec_de(Tableau):
    """
    On lance le dé équilibré sur le tableau du pré-processing
    """
    return Tableau[de_equilibre(len(Tableau))-1]


def pre_processing_de_pipe(P):
    """
    On simule un dé pipé avec un dé équilibré.
    Les deux dés sont à N faces, P représente le tableau de probabilités
    """
    proba_tiroir = ppcm_list(P)
    # tableau_pre_processing = [ele * proba_tiroir for ele in P]
    res = []
    for index, ele in enumerate(P):
        for ele2 in range((proba_tiroir / ele).denominator):
            res.append(index+1)
    return res


def test_de_pipe_avec_de(N, Tableau, M):
    """
    On crée un tableau pour "stocker" les résultats/ les compter.
    On calcule le tableau de pré-processing
    On lance la boucle et on calcule à chaque fois
    """
    tableau_res = [0 for i in range(N)]
    tableau_pre_processing = pre_processing_de_pipe(Tableau)
    while(M):
        res = de_pipe_avec_de(tableau_pre_processing)
        tableau_res[res-1] += 1
        M -= 1
    for index, ele in enumerate(tableau_res):
        print("La face : ", index+1, " est apparue : ", ele)


def pile_face(P):
    """
    Lancer de pièces, avec probabilités P d'avoir p.
    L'autre probabilité est donc 1-p.
    On considère que pile = 1
    Et face = 0
    """
    if rd.random() < P:
        return 1
    else:
        return 0


def de_pipe_avec_piece(Index, Tableau):
    """
    On a que Tableau = le tableau des probabilités.
    Index est la case du tableau que l'on traite.
    """
    Pi = Tableau[0]
    if rd.random() < Pi:
        return Index
    else:
        masse = 1 - Pi
        Tableau_tmp = list(map(lambda x: x / masse, Tableau))
        return de_pipe_avec_piece(Index + 1, Tableau_tmp[1:])


def test_de_pipe_avec_piece(Tableau, M):
    """
    On crée un tableau pour "stocker" les résultats/ les compter.
    On lance la boucle et on calcule à chaque fois
    """
    tableau_res = [0 for i in range(len(Tableau))]
    while(M):
        res = de_pipe_avec_piece(1, Tableau)
        tableau_res[res-1] += 1
        M -= 1
    for index, ele in enumerate(tableau_res):
        print("La face : ", index+1, " est apparue : ", ele)


def calcul_pi_cumul(Tableau):
    """
    On va calculer le tableau des probabilités cumulés.
    La case 0 sera P_0
    La case 1 sera P_0 + P_1
    etc.
    """
    res = [Tableau[0]]
    for ele in Tableau[1:]:
        res.append(ele + res[-1])
    return res


def roulette(Tableau):
    """
    Nous allons faire la recherche linéaire. On va donc comparer 1 à 1.
    """
    r = rd.random()
    for index, ele in enumerate(Tableau):
        if r < ele:
            return index + 1


def test_roulette(Tableau, M):
    """
    Nous allons tester la roulette. Avec le tableau de probabilités Tableau.
    Ainsi que le nombre d'itération M
    """
    tableau_res = [0 for ele in range(6)]
    P = calcul_pi_cumul(Tableau)
    while(M):
        res = roulette(P)
        tableau_res[res - 1] += 1
        M -= 1
    for index, ele in enumerate(tableau_res):
        print("La face : ", index+1, " est apparue : ", ele)


if __name__ == '__main__':
    print("Dé équilibré, 6 faces, 100000 lancés")
    test_de_equilibre(6, 100000)
    print("Dé déséquilibré, 6 faces, 100000 lancés, tableau = [1/4,1/4,1/4,1/8,1/16,1/16]")
    test_de_pipe_avec_de(6, [f.Fraction(1, 4), f.Fraction(1, 4), f.Fraction(1, 4), f.Fraction(1, 8), f.Fraction(1, 16), f.Fraction(1, 16)], 100000)
    print("Dé déséquilibré, 6 faces, 10000 lancés, tableau = [1/4,1/4,1/4,1/8,1/16,1/16]")
    test_de_pipe_avec_piece([f.Fraction(1, 4), f.Fraction(1, 4), f.Fraction(1, 4), f.Fraction(1, 8), f.Fraction(1, 16), f.Fraction(1, 16)], 10000)
    print("Roulette, 50000 lancés, tableau = [1/4,1/4,1/4,1/8,1/16,1/16]")
    test_roulette([f.Fraction(1, 4), f.Fraction(1, 4), f.Fraction(1, 4), f.Fraction(1, 8), f.Fraction(1, 16), f.Fraction(1, 16)], 50000)
