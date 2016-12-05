package main

import (
	"fmt"
	"gopkg.in/cheggaaa/pb.v1"
	"strconv"
)

const min float64 = -1356.4824368329596
const posX int = 903
const posY int = 917

func main() {

	fmt.Println("Début")
	iterations := 500
	res := make(map[string]float64, 6)
	for _, pm := range []float64{0.1, 0.01} {
		for _, loop := range []int{5, 50, 500} {
			tmp := nTimes(iterations, loop, 5, pm, 0.6, 200, 4)
			c := 0.0
			for _, ele := range tmp {
				if ele == min {
					c += 1
				}
			}
			s := "pm:" + strconv.FormatFloat(pm, 'f', -1, 64) + "| fitness:" + strconv.FormatFloat(float64(loop), 'f', -1, 64)
			res[s] = (c / float64(iterations)) * 100
		}
	}
	for key, ele := range res {
		fmt.Println(key, " = ", ele)
	}
}

func nTimes(n int, loop int, number int, pm float64, pc float64, size int, proc int) []float64 {
	acc := make([]float64, n)
	bar := pb.StartNew(n)
	for i := 0; i < n; i++ {
		bar.Increment()
		acc[i] = iterationMidBreak(loop, number, pm, pc, size, proc)
	}
	return acc
}

func nTimesWithoutCrossover(n int, loop int, number int, pm float64, pc float64, size int, proc int) []float64 {
	acc := make([]float64, n)
	bar := pb.StartNew(n)
	for i := 0; i < n; i++ {
		bar.Increment()
		acc[i] = iteration(loop, number, pm, pc, size, proc)
	}
	return acc
}

func iteration(loop int, number int, pm float64, pc float64, size int, proc int) float64 {
	population := initIndividu(pm, pc, size)
	parallelFitness(population, proc)
	i := 0
	for i < loop {
		i += 1
		tournament(number, population)
		mutation(population)
		parallelFitness(population, proc)
	}
	best := findMin(population)
	if best.f == min {
		return min
	} else {
		return best.f
	}
}

func iterationMidBreak(loop int, number int, pm float64, pc float64, size int, proc int) float64 {
	population := initIndividu(pm, pc, size)
	parallelFitness(population, proc)
	i := 0
	for i < loop {
		i += 1
		tournament(number, population)
		parallelMidPoint(population, proc)
		mutation(population)
		parallelFitness(population, proc)
	}
	best := findMin(population)
	if best.f == min {
		return min
	} else {
		return best.f
	}
	// fmt.Println(best.Fitness())
}
