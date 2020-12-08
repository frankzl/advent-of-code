package main

import (
    "fmt"
    "os"
    "log"
    "bufio"
    "strings"
    "strconv"
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

func extract_info(line string) (int, int, string, string){
    split := strings.Split(line, ": ")

    occurence, password := split[0], split[1]

    split = strings.Split(occurence, " ")
    num_occurence, letter := split[0], split[1]

    split = strings.Split(num_occurence, "-")
    lower, _ := strconv.Atoi(split[0])
    upper, _ := strconv.Atoi(split[1])

    return lower, upper, letter, password
}

func is_valid(lower int, upper int, letter string, password string) bool{
    count := 0
    for _, char := range password {
        if byte(char) == letter[0] {
            count += 1
        }
    }
    return (count >= lower && count <= upper)
}

func is_valid2(lower int, upper int, letter string, password string) bool{
    condA := (password[lower-1] == letter[0])
    condB := (password[upper-1] == letter[0])
    return condA != condB
}
func main(){
    partPtr := flag.Int("part", 1, "selected part")
    flag.Parse()

    var is_valid_check func(int,int,string,string) bool

    if *partPtr == 1{
        is_valid_check = is_valid
    }else{
        is_valid_check = is_valid2
    }

    buffer := read_file("input/02")

    count := 0

    for _, line := range buffer {
        lower, upper, letter, password := extract_info(line)
        if is_valid_check(lower, upper, letter, password){
            count += 1
        }
    }
    fmt.Println(count)
}
