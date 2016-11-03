package main

import (
	"fmt"
	"math"
	"math/rand"
	// "strconv"
)

type Ville struct {
	index int
	x, y  float64
}

func chooseCitie(tau [][]float64, etha [][]float64, alpha int, beta int, copyVilles []Ville, current Ville) (Ville, []Ville) {
	var prob []float64 = make([]float64, len(copyVilles))
	var i int = current.index
	var sum float64 = 0.0

	// on calcule les valeurs de tau[i][j]^alpha * etha[i][j]^beta
	for index, ville := range copyVilles {
		prob[index] = math.Pow(tau[i][ville.index], float64(alpha)) * math.Pow(etha[i][ville.index], float64(beta))
		sum += prob[index]
	}

	// on normalise pour avoir des probas
	for index, _ := range copyVilles {
		prob[index] /= sum
	}

	// probability denstiy function
	pcf := prob[0]
	// pour tout le éléments
	for index, _ := range prob {
		// si rand < élément, on le choisit,
		// si non, on calcule la distribution cumulée
		if rand.Float64() < pcf {
			res := copyVilles[index]
			copyVilles = deleteItem(index, copyVilles)

			return res, copyVilles
		}
		if index+1 <= len(prob)+1 {
			pcf += prob[index+1]
		}
	}
	res := copyVilles[len(prob)-1]
	copyVilles = deleteItem(len(prob)-1, copyVilles)

	return res, copyVilles
}

func updateDelta(Q float64, solution []Ville, delta [][]float64) {

	n := len(solution)
	L := norm(solution)

	for index := 1; index < n; index++ {
		i := solution[index-1].index
		j := solution[index].index
		delta[i][j] += Q / L
	}
	i := solution[n-1].index
	j := solution[0].index

	delta[i][j] += Q / L

}

func updatePath(tau [][]float64, delta [][]float64, rho float64) {

	for i, _ := range tau {
		for j, _ := range tau[i] {
			tau[i][j] = (1-rho)*tau[i][j] + delta[i][j]
		}
	}
}

func ant(t_max int, m int, villes []Ville, Q float64) []Ville {
	// first we declare the alpha, beta, tau, rho
	// delta, etha
	alpha := 1
	beta := 5
	rho := 0.1
	var newM int = m

	tau := make([][]float64, len(villes))
	for i, _ := range tau {
		tau[i] = make([]float64, len(villes))
		for j, _ := range tau[i] {
			tau[i][j] = 1 / Q
		}
	}

	etha := make([][]float64, len(villes))
	for i, _ := range etha {
		etha[i] = make([]float64, len(villes))
		for j, _ := range etha[i] {
			etha[i][j] = 1 / math.Sqrt(math.Pow(villes[i].x-villes[j].x, 2)+math.Pow(villes[i].y-villes[j].y, 2))
		}
		etha[i][i] = 0
	}

	delta := make([][]float64, len(villes))
	for i, _ := range delta {
		delta[i] = make([]float64, len(villes))
		for j, _ := range delta[i] {
			delta[i][j] = 0
		}
	}

	var best []Ville = villes

	for t_max > 0 {
		for newM > 0 {
			// on crée une copie des villes
			var copyVilles []Ville = make([]Ville, len(villes))
			copy(copyVilles[:], villes)
			// on crée la solution
			var solution []Ville = make([]Ville, len(villes))
			var i int = 0

			// on choisit le première ville
			// et on supprime l'élément de la copie
			var index int = int(math.Mod(float64(m), float64(len(villes))))
			solution[i] = copyVilles[index]
			copyVilles = deleteItem(index, copyVilles)
			i++

			for len(copyVilles) > 0 {
				// on choisit la ville
				solution[i], copyVilles = chooseCitie(tau, etha, alpha, beta, copyVilles, solution[i-1])
				i++
			}
			// on met à jour les phéromones
			updateDelta(Q, solution, delta)
			// on met à jour le best si il est meilleur que le courrant
			if norm(best) > norm(solution) {
				best = solution
			}
			newM--
		}
		// on met à jour tau
		updatePath(tau, delta, rho)
		newM = m
		t_max--
		// on met delta a 0 pour la nouvelle itération
		for ii, _ := range delta {
			for jj, _ := range delta[ii] {
				delta[ii][jj] = 0.0
			}
		}
	}
	return best
}

func wrapper(file string, t_max int, m int, titre string, out string) {
	villes := readFile(file)
	solution := greedy(file)
	res := ant(t_max, m, villes, norm(solution))
	plotting(res, titre, "X", "Y", out)
}

func wrapper_ten(file string, t_max int, m int) {
	villes := readFile(file)
	solution := greedy(file)
	res := make([]float64, 10)
	for index, _ := range res {
		res[index] = norm(ant(t_max, m, villes, norm(solution)))
	}
	fmt.Print(file + "\t-> mean = ")
	fmt.Print(mean(res))
	fmt.Print("  std = ")
	fmt.Println(stdDev(res, mean(res)))
}

func main() {
	fmt.Println("Start:")
	t_max := 50
	m := 49
	// t_max_s := strconv.FormatInt(int64(t_max), 10)
	// m_s := strconv.FormatInt(int64(m), 10)

	// wrapper("cities.dat", t_max, 50, "Cities.dat with AS\n"+"t_max = "+t_max_s+"\nm = "+m_s, "citieAnt")
	// wrapper("cities2.dat", t_max, 50, "Cities2.dat with AS\n"+"t_max = "+t_max_s+"\nm = "+m_s, "citieAnt2")
	// wrapper("cities50.dat", t_max, 50, "Cities50.dat with AS\n"+"t_max = "+t_max_s+"\nm = "+m_s, "citieAnt50")
	// wrapper("cities60.dat", t_max, 50, "Cities60.dat with AS\n"+"t_max = "+t_max_s+"\nm = "+m_s, "citieAnt60")
	// wrapper("cities80.dat", t_max, 50, "Cities80.dat with AS\n"+"t_max = "+t_max_s+"\nm = "+m_s, "citieAnt80")
	// wrapper("cities100.dat", t_max, 50, "Cities100.dat with AS\n"+"t_max = "+t_max_s+"\nm = "+m_s, "citieAnt100")
	wrapper_ten("cities2.dat", t_max, m)
}
