package main

import (
    utils "../mylib"
    "fmt"
    "strconv"
)

func is_valid(index int, number_buffer []int, valid_range int) bool {
    number := number_buffer[index]
    for j, numberA := range number_buffer[index-valid_range:index]{
        for _, numberB := range number_buffer[index-valid_range+j+1:index]{
            if numberA != numberB && numberA+numberB == number{
                return true
            }
        }
    }
    return false
}
func min(numbers []int)int{
    number := numbers[0]
    if len(numbers) == 1{
        return number
    }
    consec_min := min(numbers[1:len(numbers)])
    if number < consec_min{
        return number
    }else{
        return consec_min
    }
}

func max(numbers []int)int{
    number := numbers[0]
    if len(numbers) == 1{
        return number
    }
    consec_max := max(numbers[1:len(numbers)])
    if number > consec_max{
        return number
    }else{
        return consec_max
    }
}

func main(){
    buffer := utils.ReadChallenge(9)
    valid_range := 25

    var number_buffer []int

    for _, line := range buffer{
        number,_ := strconv.Atoi(line)
        number_buffer = append(number_buffer, number)
    }
    invalid_index := -1
    for i, number := range number_buffer[valid_range:len(number_buffer)]{
        i += valid_range
        if !is_valid(i, number_buffer, valid_range){
            fmt.Printf("Invalid number: %d\n", number)
            invalid_index = i
            break
        }
    }
    invalid_number := number_buffer[invalid_index]

    for i, numberA := range number_buffer[0:invalid_index]{
        sum := numberA
        fmt.Println("------")
        fmt.Println(numberA)
        for j, numberB := range number_buffer[i+1:invalid_index]{
            sum += numberB
            fmt.Println(numberB)
            if sum == invalid_number{
                a := min(number_buffer[i:i+j+1])
                b := max(number_buffer[i:i+j+1])
                fmt.Printf("%d + %d = %d", a,b,a+b)
                return
            }else if sum > invalid_number{
                break
            }
        }
    }
}
