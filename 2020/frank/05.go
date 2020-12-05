package main

import (
    utils "./mylib"
    "fmt"
)

func get_id(min_row int, max_row int,
            min_col int, max_col int,
            seat_encoding string) int{
    if min_row == max_row && min_col == max_col {
        return 8 * min_row + min_col
    } else if len(seat_encoding) == 0{
        return -1
    }
    switch seat_encoding[0]{
    case 'F':
        max_row = min_row + (max_row + 1 - min_row)/2 - 1
    case 'B':
        min_row = min_row + (max_row + 1 - min_row)/2
    case 'L':
        max_col = min_col + (max_col + 1 - min_col)/2 - 1
    case 'R':
        min_col = min_col + (max_col + 1 - min_col)/2
    }
    return get_id(min_row, max_row, min_col, max_col, seat_encoding[1:])
}

func main(){
    buffer := utils.ReadChallenge(5)

    const min_row, max_row = 0,127
    const min_col, max_col = 0,7
    max_id := -1

    var occupancy[8*max_row+1 -1]int

    for _, seat_encoding := range buffer{
        id := get_id(min_row, max_row, min_col, max_col, (seat_encoding))
        if max_id < id{
            max_id = id
        }
        occupancy[id] = 1
    }
    fmt.Println(max_id)

    for i,_ := range occupancy[:len(occupancy)-1]{
        if occupancy[i]==0 && occupancy[i+1] == 1 && occupancy[i-1] == 1{
            fmt.Printf("seat number: %d", i)
        }
    }
}
