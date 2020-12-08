package main

import (
    utils "../mylib"
    "fmt"
    "strings"
    "regexp"
    "strconv"
)

func extract_info(line string) (string, map[string]int) {
    pair := strings.Split(line[:len(line)-1], " contain ")
    bag := pair[0]
    bag = bag[0:len(bag)-5]

    contents := strings.Split(pair[1], ", ")
    contains := make(map[string]int)

    for _,item := range contents{
        split := strings.Split(item, " ")
        quantity,_ := strconv.Atoi(split[0])
        r, _ := regexp.Compile(`[\d]+ .+ bag`)
        color := r.FindString(item)
        if color == ""{
            break
        }
        color = color[len(split[0]) + 1: len(color)-4]
        contains[color] = quantity
    }
    return bag,contains
}

func contains_bag(quantities map[string]int, bag string) bool{
    for key, _ := range quantities{
        if bag == key{
            return true
        }
    }
    return false
}

func extract(buffer []string) map[string](map[string]int){
    contains := make(map[string](map [string] int))
    for _, line := range buffer{
        c,dict := extract_info(line)
        contains[c] = dict
    }
    return contains
}

func count_bags(lookup map[string](map[string]int), containing []string, checked_off map[string]bool) int {
    wrapper_bags := make(map[string]bool)
    if len(containing) == 0{
        return len(checked_off) - 1
    }
    for _, bag := range containing{
        for color, quantities := range lookup{
            if contains_bag(quantities, bag){
                wrapper_bags[color] = true
            }
        }
    }
    var valid_wrapper []string
    for bag,_ := range wrapper_bags{
        if _, ok := checked_off[bag]; !ok{
            valid_wrapper = append(valid_wrapper, bag)
        }
    }
    fmt.Println("--------")
    for _,bag := range containing{
        checked_off[bag] = true
    }
    for _,k := range valid_wrapper{
        fmt.Println("|"+k+"|")
    }
    return count_bags(lookup, valid_wrapper, checked_off)
}

func count_bags2(lookup map[string](map[string]int), bag string) int{
    quantities, _ := lookup[bag]
    if len(quantities) == 0{
        return 0
    }
    total := 0
    for nested_bag, amount := range quantities{
        total += amount * count_bags2(lookup, nested_bag) + amount
    }
    return total
}

func main(){
    buffer := utils.ReadChallenge(7)
    pt     := utils.ParsePart()
    
    fmt.Println(pt)
    my_bag := []string{"shiny gold"}

    //for _, line := range buffer{
    //    if (contains(line, my_bag)){
    //        count += 1
    //    }
    //    //fmt.Printf("%d "+ line + "\n", i)
    //}
    //fmt.Println(count)
    lookup := extract(buffer)
    checked_off := make(map[string]bool)
    fmt.Println(count_bags(lookup, my_bag, checked_off))
    fmt.Println(count_bags2(lookup, my_bag[0]))
}
