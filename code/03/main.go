package main

import (
    "fmt"
    "os"
    "log"
    "bufio"
    "flag"
)

func read_file(file_name string) []string{
    file, err := os.Open(file_name)
    if err != nil {
        log.Fatal(err)
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)

    var buffer []string
    for scanner.Scan(){
        i := scanner.Text()
        buffer = append(buffer, i)
    }
    return buffer
}

func is_tree(x int, y int, buffer []string) bool{
    line_width := len(buffer[0])

    x_pos := x % line_width
    y_pos := y
    return buffer[y_pos][x_pos] == '#'
}

func main(){
    partPtr := flag.Int("part", 1, "selected part")
    flag.Parse()

    buffer := read_file("input/03")
    
    var step [][2]int
    if *partPtr == 1{
        step = [][2]int{
            {3,1},
        }
    }else{
        step = [][2]int{
            {1,1},
            {3,1},
            {5,1},
            {7,1},
            {1,2},
        }
    }

    tree_product := 1

    for _, step_size := range step{
        x,y := 0,0
        tree_count := 0
        for y < len(buffer) {
            if is_tree(x,y, buffer){
                tree_count += 1
            }
            x += step_size[0]
            y += step_size[1]
        }
        tree_product *= tree_count
    }
    fmt.Println(tree_product)
}
