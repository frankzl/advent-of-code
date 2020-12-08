package main

import (
    utils "./mylib"
    "fmt"
)

func update_questions(line string, questions map[rune]int){
    for _, token := range line{
        if _, ok := questions[token]; !ok{
            questions[token] = 0
        }
        questions[token] += 1
    }
}

func countpt1(questions map[rune]int, group_size int) int{
    return len(questions)
}

func countpt2(questions map[rune]int, group_size int) int{
    count := 0
    for _, val := range questions{
        if val == group_size{
            count += 1
        }
    }
    return count
}

func main(){
    buffer := utils.ReadChallenge(6)
    pt := utils.ParsePart()

    questions := make(map[rune]int)
    count := 0
    var count_func func(map[rune]int, int) int

    if pt == 1{
        count_func = countpt1
    }else{
        count_func = countpt2
    }

    group_size := 0
    for _, line := range buffer{
        if line != "" {
            update_questions(line, questions)
            group_size += 1
        }else{
            count += count_func(questions, group_size)
            questions = make(map[rune]int)
            group_size = 0
        }
    }
    fmt.Printf("%d \n", count + count_func(questions, group_size))
}
