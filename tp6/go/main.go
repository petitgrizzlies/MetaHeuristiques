package main

import (
	"fmt"
	"math/rand"
	"time"
)

func main() {
	rand.Seed(time.Now().UTC().UnixNano())
	iterationOnePoint(100, 5, 0.1, 0.6, 100)
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
	fmt.Println(best.Fitness())
}
