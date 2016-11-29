package main

import (
	"fmt"
)

const min float64 = -1356.4824368329596
const posX int = 903
const posY int = 917

func main() {
	for i := 0; i < 100; i++ {
		iterationOnePoint(100, 5, 0.1, 0.6, 100)
	}
}

func iterationOnePoint(loop int, number int, pm float64, pc float64, size int) {
	population := initIndividu(pm, pc, size)
	i := 0
	for i < loop {
		i += 1
		population = tournament(number, population)
		population = crossoverOnePoint(population)
		population = mutation(population)
	}
	best := findMin(population)
	if best.Fitness() == min {
		fmt.Println("Fin min")
	}
	// fmt.Println(best.Fitness())
}
