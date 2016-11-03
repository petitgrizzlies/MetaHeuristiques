package main

import (
	"math"
	"math/rand"
	"time"
)

/*
	The function closestCitie takes:
		cities : a list of citie
		current : the current citie

	And return:
		[][]float64 : the new cities updated
		[]float64 : the closest citie from current

	The goal is to find the closest cite in cities from current.
	We use euclidian distance.
*/
func closestCitie(cities []Ville, current Ville) ([]Ville, Ville) {
	// create the vector with the distance value
	var tmp []float64 = make([]float64, len(cities))

	// loop for computing the distance
	for index, citie := range cities {
		tmp[index] = math.Sqrt(math.Pow(current.x-citie.x, 2) + math.Pow(current.y-citie.y, 2))
	}
	// loop for find the smallest and his index
	smallestIndex := 0
	smallestValue := tmp[0]

	for index, value := range tmp {
		if smallestValue > value {
			smallestIndex = index
			smallestValue = value
		}
	}
	res := cities[smallestIndex]
	// delete the smallest element
	cities = deleteItem(smallestIndex, cities)
	return cities, res
}

/*
	Greedy algorithme. Takes:
		file : path to .dat file, it's a string

	Return:
		[][]float64 : the solution -> an array of cities

	We alwayse choose the closest citie each iteration.
*/
func greedy(file string) []Ville {

	// init the random
	rand.Seed(time.Now().UTC().UnixNano())
	// load the cities from file
	cities := readFile(file)

	// selecte the first random cities
	var n int = rand.Intn(len(cities))
	var solution []Ville = []Ville{}
	solution = append(solution, cities[n])

	cities = deleteItem(n, cities)
	var next Ville

	// while there is some cities, we choose the closest one and add it
	for len(cities) > 0 {
		cities, next = closestCitie(cities, solution[len(solution)-1])
		solution = append(solution, next)
	}
	solution = append(solution, solution[0])
	return solution
}
