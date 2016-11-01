package main

import (
	"bufio"
	"fmt"
	"math"
	"math/rand"
	"os"
	"reflect"
	"strconv"
	"time"

	"github.com/gonum/plot"
	"github.com/gonum/plot/plotter"
	"github.com/gonum/plot/vg"

	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func deleteItem(index int, vec [][]float64) [][]float64 {
	vec[len(vec)-1], vec[index] = vec[index], vec[len(vec)-1]
	return vec[:len(vec)-1]
}

func findIndex(item []float64, vec [][]float64) int {
	for index, ele := range vec {
		if reflect.DeepEqual(ele, item) {
			return index
		}
	}
	return -1
}

func plotting(vec [][]float64, title string, axeX string, axeY string, name string) {

	plot, err := plot.New()
	check(err)

	plot.Title.Text = title
	plot.X.Label.Text = axeX
	plot.Y.Label.Text = axeY
	plot.Add(plotter.NewGrid())

	points := convert(vec)
	lLine, lPoint, err := plotter.NewLinePoints(points)

	plot.Add(lLine, lPoint)
	plot.Save(15*vg.Centimeter, 15*vg.Centimeter, name+".png")
}

func convert(vec [][]float64) plotter.XYs {
	res := make(plotter.XYs, len(vec))
	for index := range res {
		res[index].X = vec[index][0]
		res[index].Y = vec[index][1]
	}
	return res
}

func readFile(file string) [][]float64 {

	// we open the file
	f, err := os.Open(file)
	defer f.Close()

	// check the error
	check(err)

	// init new reader on the opened file
	r := bufio.NewReader(f)

	var buffer [][]float64 = [][]float64{}

	// do line
	line, err := r.ReadString('\n')
	for err == nil {
		var splitedLine []string = strings.Fields(line)

		n1, _ := strconv.ParseFloat(splitedLine[1], 32)
		n2, _ := strconv.ParseFloat(splitedLine[2], 32)

		buffer = append(buffer, []float64{n1, n2})
		line, err = r.ReadString('\n')
	}
	return buffer
}

func closestCitie(cities [][]float64, current []float64) ([][]float64, []float64) {
	// create the vector with the distance value
	var tmp []float64 = make([]float64, len(cities))

	// loop for computing the distance
	for index, citie := range cities {
		tmp[index] = math.Sqrt(math.Pow(current[0]-citie[0], 2) + math.Pow(current[1]-citie[1], 2))
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

func norm(vec [][]float64) float64 {
	var res float64 = 0
	var previous []float64 = vec[0]
	for _, ele := range vec[1:] {
		res += math.Sqrt(math.Pow(previous[0]-ele[0], 2) + math.Pow(previous[1]-ele[1], 2))
		previous = ele
	}
	res += math.Sqrt(math.Pow(previous[0]-vec[0][0], 2) + math.Pow(previous[1]-vec[0][1], 2))
	return res
}

func greedy(file string) [][]float64 {

	// init the random
	rand.Seed(time.Now().UTC().UnixNano())
	// load the cities from file
	cities := readFile(file)

	// selecte the first random cities
	var n int = rand.Intn(len(cities))
	var solution [][]float64 = [][]float64{}
	solution = append(solution, cities[n])

	cities = deleteItem(n, cities)
	var next []float64

	// while there is some cities, we choose the closest one and add it
	for len(cities) > 0 {
		cities, next = closestCitie(cities, solution[len(solution)-1])
		solution = append(solution, next)
	}
	solution = append(solution, solution[0])
	return solution
}

func ant(file string) [][]float64 {

	// init the random
	rand.Seed(time.Now().UTC().UnixNano())

	// we get the cities
	var cities [][]float64 = readFile(file)

	// we get the Lnn
	var L float64 = norm(greedy(file))

	// we define ALL the parameters:
	// t_max, alpha, beta, rho
	// m, Q, tau, d, best
	var t_max int = 1000
	var alpha int = 1
	var beta int = 5
	var rho float64 = 0.1
	var m int = 100
	var Q float64 = 1 / L
	fmt.Println(t_max, alpha, beta, rho, m, Q)
	var tau [][]float64 = make([][]float64, len(cities))
	for i, _ := range tau {
		tau[i] = make([]float64, len(cities))
		for j, _ := range tau[i] {
			tau[i][j] = 1 / L
		}
	}

	var d [][]float64 = make([][]float64, len(cities))
	for i, _ := range d {
		d[i] = make([]float64, len(cities))
		for j, _ := range d[i] {
			d[i][j] = math.Sqrt(math.Pow(cities[i][0]-cities[j][0], 2) + math.Pow(cities[i][1]-cities[j][1], 2))
		}
	}

	var best [][]float64 = [][]float64{}
	fmt.Println(best)

	//	// the algo loop
	//	for t_max > 0 {
	//		for m > 0 {
	//			// copy the cities
	//			copy_cities = copy(cities)
	//			// init the solution
	//			var solution [][]float64 = make([][]float64, 0, len(cities))
	//			// choose a random cities
	//			n = rand.Int31n(len(copy_cities))
	//			solution = append(solution, copy_cities[n])
	//		}
	//	}

	return tau
}

func main() {

	ant("cities.dat")
	fmt.Println("Hello World\n")

}
