#! /usr/bin/python3.5
# -* coding:utf-8 -*-

import neuralNet
import numpy as np
import copy
import matplotlib.pyplot as plt
import tqdm


class Particule():
    """
    Il s'agit de la classe particule. Elle dispose de différents attributs:
        - index -> pour identifier de manière unique la particule
        - theta{1,2}_size -> qui donne la taille des matrices theta1 et theta2
        - theta{1,2} -> des arrays numpy
        - v -> notre vecteur vitesse de taille : |v| = |theta1| + |theta2|
        - best -> le meilleur vecteur rencontrer
        - fitnessValue -> la valeur acctuelle pour tetha1,theta2
        - bestValue -> la valeur du vecteur best
    """

    def __init__(self, index, size_theta1, size_theta2, images, labels):
        """Fonction d'initialisation

        La méthode __init__ permet d'initialiser les différents attributs de la classe
        particule.

        Arguments:
            index {int} -- l'index de la particule
            size_theta1 {[int]} -- taille [x,y] de la matrice theta1
            size_theta2 {[int]} -- taille [x,y] de la matrice theta2
            images {np.matrix} -- une matrice contenant toutes les images
            labels {np.matrix} -- une matrice contenant les labels.

        """
        self.index = index
        self.theta1_size = size_theta1
        self.theta2_size = size_theta2
        self.theta1 = (1 - (- 1)) * np.random.random_sample(size_theta1[0] * size_theta1[1]) + -1
        self.theta2 = (1 - (- 1)) * np.random.random_sample(size_theta2[0] * size_theta2[1]) + -1
        self.v = np.random.rand(size_theta1[0] * size_theta1[1] + size_theta2[0] * size_theta2[1])
        self.best = np.append(self.theta1, self.theta2)
        self.fitnessValue = self.fitness(images, labels)
        self.bestValue = self.fitnessBest(images, labels)

    def update(self, omega, c1, r1, c2, r2, bestGlobal, cut_off):
        """Mise à jour de la vitesse et de la position.

        La méthode update va calculer la nouvelle vitesse:
            1. v = omega * v + c1 * r1 * (bestLocal - vecteurLocal) + c2 * r2 * (bestGlobal - vecteurLocal)
        Puis calculer la nouvelle position:
            2. s = s + v

        Arguments:
            omega {float} -- un coefficient multiplicatif
            c1 {int} -- une constante
            r1 {float} -- un nombre aléatoire [0,1]
            c2 {int} -- une constante
            r2 {float} -- un nombre aléatoire [0,1]
            bestGlobal {np.array} -- la position de l'optimum global
            cut_off {bool} -- dit si on applique le cut off ou non
        """
        theta = np.append(self.theta1, self.theta2)
        best = np.append(bestGlobal.theta1, bestGlobal.theta2)
        self.v = omega * self.v + c1 * r1 * (self.best - theta) + c2 * r2 * (best - theta)
        if cut_off:
            self.v = np.where(np.abs(self.v) > 0.5, 0, self.v)
        theta += self.v
        self.theta1 = theta[0: self.theta1_size[0] * self.theta1_size[1]]
        self.theta2 = theta[self.theta1_size[0] * self.theta1_size[1]:]

    def fitness(self, images, labels):
        """Évaluation du réseau avec toutes les images.

        La fitness est juste l'évaluation du réseau de neurone sur toutes les images de l'ensemble d'entrainements.
        Il y a une composition de fonction:
            1. np.where(vecteur >= 0.5, 1, 0) -> met les éléments du vecteur à 1 si  la valeur est >= 0.5 , à 0 sinon.
            2. theta{1,2}.reshape(theta{1,2}_size) -> permet de passer d'un tableau t x 1 à un tableau  m x n. Où m et n sont
                les valeurs définies par tetha{1,2}_size.
            3. np.array(labels) - np.array(liste) -> va soustraire les éléments 1 à 1.
            4. sum([x*x for x in res]) / len(images) -> calcule le carré de chaque éléments puis divise par la longueur.
            5. on assigne la valeur de 4 à l'atribut fitnessValue

        Arguments:
            images {np.matrix} -- la matrice d'image
            labels {np.matrix} -- la matrice des labels

        Returns:
            float -- le nombre d'erreur au carré moyennée.
        """

        liste = np.where(np.array([neuralNet.fitness(self.theta1.reshape(self.theta1_size), self.theta2.reshape(self.theta2_size), 1, x) for x in images]) >= 0.5, 1, 0)
        res = np.array(labels) - np.array(liste)
        self.fitnessValue = sum([x * x for x in res]) / len(images)
        return self.fitnessValue

    def fitnessBest(self, images, labels):
        """Évaluation du réseau avec toutes les images.

        Le code est semblable à la méthode fitness, cependant il faut extraire la valeur de best, qui est un
        tableau en deux tableaux theta{1,2}. Puis même code que fitness, sauf qu'on retourne la valeur calculée.

        Arguments:
            images {np.matrix} -- la matrice d'image
            labels {np.matrix} -- la matrice des labels

        Returns:
        float -- le nombre d'erreur au carré moyennée.
        """

        theta1 = self.best[0: self.theta1_size[0] * self.theta1_size[1]]
        theta2 = self.best[self.theta1_size[0] * self.theta1_size[1]:]
        liste = np.where(np.array([neuralNet.fitness(theta1.reshape(self.theta1_size), theta2.reshape(self.theta2_size), 1, x) for x in images]) >= 0.5, 1, 0)
        res = np.array(labels) - np.array(liste)
        return sum([x * x for x in res]) / len(images)

    def updateBest(self, images, labels):
        """Mise à jour du meilleur résultat rencontré

        On vérifie si la valeur du meilleure est plus grande que la valeur acctuelle. Si oui, on met à jour le meilleur.
        Pour la mise à jour, on copie le vecteur actuel dans le vecteur best, et on met à jour la valeur de l'atribut
        bestValue.

        Arguments:
            images {np.matrix} -- la matrice d'image
            labels {np.matrix} -- la matrice des labels
        """
        if self.fitnessValue < self.bestValue:
            self.best = np.append(self.theta1, self.theta2)
            self.bestValue = copy.deepcopy(self.fitnessValue)


class Espace():
    """
    Espace est une classe qui contient un ensemble de particule;
        - particule -> un tableau de particules
        - bestGlobal -> le meilleur individu de l'espace
    """

    def __init__(self, size_theta1, size_theta2, number, images, labels):
        """Fonction d'initialisation

        Pour la méthode __init__, on va instancier n particules. cf: méthode __init__ particules.

        Arguments:
            size_theta1 {[int]} -- taille [x,y] de la matrice theta1
            size_theta2 {[int]} -- taille [x,y] de la matrice theta2
            number {int} -- nombre de particule de l'espace
            images {np.matrix} -- la matrice d'image
            labels {np.matrix} -- la matrice des labels
        """
        self.particule = []
        for index in range(number):
            self.particule.append(Particule(index, size_theta1, size_theta2, images, labels))

    def initBest(self):
        """Initialisation du bestGlobal

        On va trouver le min des particules, puis prendre la plus petite particule et la
        copier dans l'attribut bestGlobal
        """
        res = (list(map(lambda x: x.fitnessValue, self.particule)))
        index = res.index(min(res))
        self.bestGlobal = copy.deepcopy(self.particule[index])

    def findBest(self):
        """Mise à jour du bestGlobal

        Même principe que initBest, sauf qu'on vérifie si la valeur du bestGlobal
        est plus grande que celle du meilleur individu courrant de l'espace
        """
        res = [x.bestValue for x in self.particule]
        index = res.index(min(res))
        if self.particule[index].bestValue < self.bestGlobal.bestValue:
            self.bestGlobal = copy.deepcopy(self.particule[index])

    def getFitness(self):
        """
        Permet de récupérer la fitness de toutes les particules de l'espaces

        Returns:
            [float] -- la fitness courrante de chaque particule
        """
        res = [x.fitnessValue for x in self.particule]
        return res


def update(x, omega, c1, c2, bestGlobal, cut_off):
    """Mise à jour d'une particule

    On assume que x est un objet particule. C'est une interface pour appliquer la méthode update
    aux particules

    Arguments:
        x {particule} -- la particule dont on veut mettre à jour les valeurs
        omega {float} -- la valeur de la constante omega
        c1 {int} -- valeur de la constante c1
        c2 {int} -- valeur de la constante c2
        bestGlobal {np.array} -- la postion du meilleur de l'espace
        cut_off {bool} -- applique ou non le cut off
    """

    x.update(omega, c1, np.random.rand(), c2, np.random.rand(), bestGlobal, cut_off)


def main(particuleNumbers, xPath, yPath, t1, t2, t_max, cut_off):
    """Algorithme PSO

    Applique l'algorithme PSO sur les paramètres.

    Arguments:
        particuleNumbers {int} -- nombre de particules
        xPath {string} -- un chemin jusqu'au fichier
        yPath {string} -- un chemin jusqu'au fichier
        t1 {[int]} -- taille de la matrice theta1
        t2 {[int]} -- taille de la matrice theta2
        t_max {int} -- nombre d'itération
        cut_off {bool} -- dis s'il y a un cut off ou non

    Returns:
        [],np.array,np.array -- donne une liste avec la valeur de la fitness du global best,
        ainsi que les meilleures theta{1,2}
    """

    # on initialise les images et les labels depuis les fichiers.
    images, labels = neuralNet.read_image(xPath, yPath, 200)
    # on crée l'espace des particules
    e = Espace(t1, t2, particuleNumbers, images, labels)
    # on trouve le best global
    e.initBest()
    res = []
    # init constante
    omega = 0.75
    c1 = 2
    c2 = 2

    for x in tqdm.tqdm(range(t_max)):
        # calculate its fitness
        [x.fitness(images, labels) for x in e.particule]
        # update the best
        [x.updateBest(images, labels) for x in e.particule]
        # find the absolute best
        e.findBest()
        res.append(e.bestGlobal.fitnessValue)
        # mise à jour de la vitesse
        [update(x, omega, c1, c2, e.bestGlobal, cut_off) for x in e.particule]

    # on retourne les meilleures matrices pour faire des tests
    theta1 = e.bestGlobal.best[0: e.bestGlobal.theta1_size[0] * e.bestGlobal.theta1_size[1]].reshape(e.bestGlobal.theta1_size)
    theta2 = e.bestGlobal.best[e.bestGlobal.theta1_size[0] * e.bestGlobal.theta1_size[1]:].reshape(e.bestGlobal.theta2_size)
    return res, theta1, theta2


def print_data(array):
    """Afficher des données

    Afficher le min, le max, la moyenne et la déviation standard.

    Arguments:
        array {np.arry} -- le vecteur numpy dont on veut les infos
    """
    print("Min : " + str(array.min()))
    print("Max : " + str(array.max()))
    print("Mean: " + str(array.mean()))
    print("Std : " + str(array.std()))


def plot(boolean):
    """Plot
    Simple fonction qui lance le PSO, et qui plot les résultats
    """
    n = 40
    t_max = 70
    res, theta1, theta2 = main(particuleNumbers=n, xPath='X.data', yPath='Y.data', t1=[25, 401], t2=[1, 26], t_max=t_max, cut_off=boolean)
    plt.plot(res, label="Fitness")
    plt.ylabel("$J(\Theta^{(1)},\Theta^{(2)})$")
    plt.xlabel("Itérations")
    plt.title("$t_{max} = " + str(t_max) + "$, et " + str(n) + " particules")
    plt.show()

    print("Theta1 : ")
    print_data(theta1)
    print("\nTheta2:")
    print_data(theta2)

    images, labels = neuralNet.read_image('X.data', 'Y.data', 200)
    new_res = np.where(np.array([neuralNet.fitness(theta1, theta2, 1, x) for x in images]) >= 0.5, 1, 0) - np.array(labels)
    new_res = 100 - (np.sum(np.abs(new_res)) / 200) * 100
    print("Accuracy : " + str(new_res) + "%")


def ten_times(boolean):
    """Lance 10 fois l'algorithme PSO

    On va lancer 10 fois l'algorithme, en récupérant la fitness du best à chaque fois.
    On print ces valeurs
    """
    n = 30
    liste = []
    res2 = []
    for x in range(10):
        print("Itération : " + str(x))
        res, _, _ = main(particuleNumbers=n, xPath='X.data', yPath='Y.data', t1=[25, 401], t2=[1, 26], t_max=40, cut_off=boolean)
        liste.append(res)

    for ele in liste:
        res2.append(min(ele))
    print(res2)


if __name__ == '__main__':
    # plot(False)
    ten_times(False)
