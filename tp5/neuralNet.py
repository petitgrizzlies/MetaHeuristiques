#! /usr/bin/python3.5
# -* coding:utf-8 -*-

import numpy as np


def read_image(pathX, pathY, n):
    """Lire les images et labels depuis un fichier.

    On ouvre les fichiers, on récupère leur contenu. Puis on lis les n premières lignes.
    En prenant garde à la conversion de string à array.

    Arguments:
        pathX {string} -- est un path qui donne le fichier contenant les images.
        pathY {string} -- est un path qui donne le fichier contenant les labels.
        n {int} -- nombre de lignes lues dans les deux fichiers

        Returns:
        images, labels -- des vecteurs numpy qui contiennent les images et leurs labels.
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
    """Calcul d'une couche du réseau de neurones.

    On linéarise la multiplication matricielle et l'application de la fonction:
        1. On ajoute le biais au vecteur et on transpose le résultat
        2. Après avoir transformé le résultat de l'étape 1. en une matrice, on applique la
        multiplication matricielle.
        3. On applique la fonction sigmoîde à tout les éléments du résultat de 2.
        4. On "applatit" la matrice en un vecteur.

    Arguments:
        theta {numpy.matrix} -- est la matrice avec la quelle on va effectuer la multiplication.
        biais {int} -- le biais ajouté au vecteur
        vecteur {numpy.array} -- est le vecteur avec lequel on va effectuer la multiplication

    Returns:
        np.matrix -- retourne le résultat du calcul.
    """
    return np.squeeze(np.asarray(1. / (1 + np.exp(-theta.dot(np.matrix(np.append(vecteur, 1)).transpose())))))


def fitness(theta1, theta2, biais, vecteur):
    """Application du réseau de neurones.

    On a deux matrices (i.e. deux couches), et on les appliques les deux.

    Arguments:
        theta1 {np.matrix} -- la matrice de la première couche.
        theta2 {np.matrix} -- la matrice de la deuxième couche.
        biais {int} -- le biais ajouté à chaque couche.
        vecteur {[type]} -- l'image à laquelle on applique le réseau.

    Returns:
        res.max() -- donne un résultat [0,1]
    """
    res = layout(theta=theta1, biais=biais, vecteur=vecteur)
    res = layout(theta=theta2, biais=biais, vecteur=res)

    return res.max()
