package main

import (
	"fmt"
	"math/rand"
	"time"
)

func main() {
	rand.Seed(time.Now().UTC().UnixNano())
	population := initIndividu(0.1, 0.6, 100)
	i := population[0]
	fmt.Println(i.Fitness())
	i = population[1]
	fmt.Println(i.Fitness())
	// population = tournament(5, population)
	population = mutation(population)
	i = population[0]
	fmt.Println(i.Fitness())
	i = population[1]
	fmt.Println(i.Fitness())
}
