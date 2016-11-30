package main

import (
	"fmt"
	"gopkg.in/cheggaaa/pb.v1"
)

const min float64 = -1356.4824368329596
const posX int = 903
const posY int = 917

func main() {
	number := 100
	acc := 0
	bar := pb.StartNew(number)
	for i := 0; i < number; i++ {
		bar.Increment()
		acc += iterationOnePoint(100, 5, 0.1, 0.6, 300)
	}
	bar.FinishPrint("..........................")
	fmt.Printf("Accuracy %f\n", (float64(acc)/float64(number))*100)

}

func iterationOnePoint(loop int, number int, pm float64, pc float64, size int) int {
	population := initIndividu(pm, pc, size)
	fitness(population)
	i := 0
	for i < loop {
		i += 1
		population = tournament(number, population)
		population = crossoverOnePoint(population)
		mutation(population)
		fitness(population)
	}
	best := findMin(population)
	if best.f == min {
		return 1
	} else {
		return 0
	}
	// fmt.Println(best.Fitness())
}

func iterationMidBreak(loop int, number int, pm float64, pc float64, size int) int {
	population := initIndividu(pm, pc, size)
	fitness(population)
	i := 0
	for i < loop {
		i += 1
		population = tournament(number, population)
		population = crossoverMidPoint(population)
		mutation(population)
		fitness(population)
	}
	best := findMin(population)
	if best.f == min {
		return 1
	} else {
		return 0
	}
	// fmt.Println(best.Fitness())
}
