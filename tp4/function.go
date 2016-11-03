package main

import (
	"bufio"
	"github.com/gonum/plot"
	"github.com/gonum/plot/plotter"
	"github.com/gonum/plot/vg"
	"math"
	"os"
	"strconv"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func mean(vec []float64) float64 {
	total := 0.0
	for _, ele := range vec {
		total += ele
	}
	total /= float64(len(vec))
	return total
}

func stdDev(vec []float64, mean float64) float64 {
	total := 0.0
	for _, ele := range vec {
		total += math.Pow(ele-mean, 2)
	}
	variance := total / float64(len(vec)-1)
	return math.Sqrt(variance)
}

/*
	Given:
		index: the index of item
		vec: the vector

	We return:
		[][]float64: the array without the item at place "index"
*/
func deleteItem(index int, vec []Ville) []Ville {
	vec[len(vec)-1], vec[index] = vec[index], vec[len(vec)-1]
	return vec[:len(vec)-1]
}

/*
	Given some element, it plots the graph
*/
func plotting(vec []Ville, title string, axeX string, axeY string, name string) {

	plot, err := plot.New()
	check(err)
	vec = append(vec, vec[0])

	plot.Title.Text = title + "\n" + strconv.FormatFloat(norm(vec), 'E', -1, 64)
	plot.X.Label.Text = axeX
	plot.Y.Label.Text = axeY
	plot.Add(plotter.NewGrid())

	points := convert(vec)
	lLine, lPoint, err := plotter.NewLinePoints(points)

	plot.Add(lLine, lPoint)
	plot.Save(15*vg.Centimeter, 15*vg.Centimeter, name+".png")
}

/*
	Points conversion for plotting function
*/
func convert(vec []Ville) plotter.XYs {
	res := make(plotter.XYs, len(vec))
	for index := range res {
		res[index].X = vec[index].x
		res[index].Y = vec[index].y
	}
	return res
}

/*
	Given:
		file: a path to .dat

	We read it, and store the date in an array.
	Return:
		[][]float64 : the array with the cities
*/

func readFile(file string) []Ville {

	// we open the file
	f, err := os.Open(file)
	defer f.Close()

	// check the error
	check(err)

	// init new reader on the opened file
	r := bufio.NewReader(f)

	var buffer []Ville = []Ville{}
	var i int = 0

	// do line
	line, err := r.ReadString('\n')
	for err == nil {
		var splitedLine []string = strings.Fields(line)

		n1, _ := strconv.ParseFloat(splitedLine[1], 32)
		n2, _ := strconv.ParseFloat(splitedLine[2], 32)

		buffer = append(buffer, Ville{i, n1, n2})
		i++
		line, err = r.ReadString('\n')
	}
	return buffer
}

/*
	Euclidian norm on a vector of points
*/
func norm(vec []Ville) float64 {
	var res float64 = 0
	var previous Ville = vec[0]
	for _, ele := range vec[1:] {
		res += math.Sqrt(math.Pow(previous.x-ele.x, 2) + math.Pow(previous.y-ele.y, 2))
		previous = ele
	}
	res += math.Sqrt(math.Pow(previous.x-vec[0].x, 2) + math.Pow(previous.y-vec[0].y, 2))
	return res
}
