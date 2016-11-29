package main

import (
	"math"
	"math/rand"
	"strconv"
)

type Individu struct {
	x, y   string
	pm, pc float64
}

func (i Individu) Fitness() float64 {
	tmp_x, _ := strconv.ParseInt(i.x, 2, 32)
	tmp_y, _ := strconv.ParseInt(i.y, 2, 32)
	x := float64(tmp_x) + 0.01
	y := float64(tmp_y) + 0.01

	res := math.Pow(x/1000, 512) + math.Pow(10/x, 4) + math.Pow(y/1000, 512) + math.Pow(10/y, 4) - math.Abs(0.5*x*math.Sin(math.Sqrt(math.Abs(x)))) - math.Abs(y*math.Sin(30*math.Sqrt(math.Abs(x/y))))
	return res
}

func (i *Individu) Mutation() {

	pm := i.pm
	x := i.x
	for index, ele := range i.x {
		if rand.Float64() < pm {
			tmp, _ := strconv.Atoi(string(ele))
			x = x[:index] + string(strconv.FormatFloat(math.Mod(float64(tmp+1), 2), 'f', 1, 64)[0]) + x[index+1:]
		}
	}
	i.x = x

	y := i.y
	for index, ele := range i.y {
		if rand.Float64() < pm {
			tmp, _ := strconv.Atoi(string(ele))
			y = y[:index] + string(strconv.FormatFloat(math.Mod(float64(tmp+1), 2), 'f', 1, 64)[0]) + y[index+1:]
		}
	}
	i.y = y
}

func initIndividu(pm float64, pc float64, size_population int) []Individu {
	res := make([]Individu, size_population)
	iter := size_population - 1
	for iter >= 0 {
		x := int64(10 + rand.Intn(991))
		y := int64(10 + rand.Intn(991))
		res[iter] = Individu{strconv.FormatInt(x, 2), strconv.FormatInt(y, 2), pm, pc}
		iter -= 1
	}
	return res
}

func findMin(population []Individu) Individu {
	min := population[0].Fitness()
	index := 0
	iter := 1
	for iter < len(population) {
		if min > population[iter].Fitness() {
			min = population[iter].Fitness()
			index = iter
		}
		iter += 1
	}
	return population[index]
}

func tournament(number int, population []Individu) []Individu {
	res := make([]Individu, len(population))

	i := 0
	n := len(population)
	iter := 0

	// partie de séléction
	for iter < n {
		tmp := make([]Individu, number)
		// partie de tournois
		for i < number {
			tmp[i] = population[rand.Intn(n)]
			i += 1
		}
		res[iter] = findMin(tmp)
		i = 0
		iter += 1
	}
	return res
}

func mutation(population []Individu) []Individu {
	for index, _ := range population {
		population[index].Mutation()
	}
	return population
}
