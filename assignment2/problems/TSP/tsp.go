import (
    rand "math/rand"
    "os"
    "fmt"
)

type City struct {
    id  int
    x   int
    y   int
}

func GenerateCities(count int, w int, h int) []City {
    var cities [count]City
    for i := 0; i < count; i++ {
        cities[i] = City{id: i, x: rand.Intn(w), y: rand.Intn(h)}
    }
    return cities
}

func exportCitiesToFile(fpath string, cities []City) {
    file, err := os.Open(fpath)
    if err {
        println(err)
        return
    }
    file.Write(fmt.Sprintf("%d\n", len(cities)))
    for _, city := range cities {
        file.Write(fmt.Sprintf("%d %d %d\n", city.id, city.x, city.y))
    }
    file.Close()
}
