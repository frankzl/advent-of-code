package main

import (
    utils "./mylib"
    "fmt"
)

func is_occupied(row int, col int, board map[int]rune, width int, height int)bool{
    if row < 0 || row >= height || col < 0 || col >= width{
        return false
    }
    seat_idx := row*width+col
    if state, ok := board[seat_idx]; ok{
        return state == '#'
    }
    return false
}

func get_num_neighbors(row int, col int, board map[int] rune, width int, height int) int {
    occupied := is_occupied(row, col, board, width, height)
    num_neighbors := 0
    if occupied{
        num_neighbors = -1
    }
    for i := -1; i<=1; i++{
        for j := -1; j<=1; j++{
            if is_occupied(row+i,col+j,board,width, height){
                num_neighbors += 1
            }
        }
    }
    return num_neighbors
}

func is_direction_occupied(row int, col int, i int,j int, board map[int]rune, width int, height int) bool {
    new_row := row + i
    new_col := col + j
    for (new_row >= 0 && new_row < height && new_col >= 0 && new_col < width ) {
        seat_idx := new_row*width + new_col
        if val, ok := board[seat_idx]; ok{
            if val == '#'{
                return true
            }
            if val == 'L'{
                return false
            }
        }else{
            return false
        }
        new_row += i
        new_col += j
    }
    return false
}

func get_num_neighbors2(row int, col int, board map[int] rune, width int, height int) int {
    num_neighbors := 0
    for i := -1; i<=1; i++{
        for j := -1; j<=1; j++{
            if !(i == 0  && j==0){
                if is_direction_occupied(row, col, i,j,board,width, height){
                    num_neighbors += 1
                }
            }
        }
    }
    return num_neighbors
}


func get_seat_update(row int, col int, board map[int]rune, width int, height int, occupation_threshold int, get_num_neighbors func(int, int, map[int] rune, int, int)int) rune {
    seat_idx := row*width+col
    if board[seat_idx] == '.'{
        return '.'
    }

    num_neighbors := get_num_neighbors(row, col, board, width, height)
    occupied := is_occupied(row, col, board, width, height)
    if !occupied && num_neighbors == 0{
        return '#'
    }
    if occupied && num_neighbors >= occupation_threshold{
        return 'L'
    }
    return board[seat_idx]
}

func get_update_board(board map[int]rune, width int, height int, occupation_threshold int,
        get_num_neighbors func(int, int, map[int] rune, int, int)int)(map[int]rune, bool){
    update_board := make(map[int]rune)
    changed := false

    for row :=0; row < height; row++{
        for col :=0; col < width; col++{
            seat_idx := row*width + col
            update_board[seat_idx] = get_seat_update(row, col, board, width, height, occupation_threshold, get_num_neighbors)
            if board[seat_idx] != update_board[seat_idx]{
                changed = true
            }
        }
    }
    return update_board, changed
}

func print_board(board map[int]rune, width int, height int){
    for i:=0;i<height;i++{
        for j:=0;j<width;j++{
            fmt.Printf("%c",board[i*width + j])
        }
        fmt.Printf("\n")
    }
}

func main(){
    buffer := utils.ReadChallenge(11)
    // pt := utils.ParsePart()

    width := len(buffer[0])
    height := len(buffer)

    occupation_threshold := 5
    my_get_neighbors := get_num_neighbors2

    board := make(map[int]rune)

    for i, row := range buffer{
        for j, val := range row{
            board[i*width + j] = val
        }
    }

    //fmt.Printf("%c \n", get_seat_update(0, 2, board, width, height, occupation_threshold, my_get_neighbors))
    updated_board, changed := get_update_board(board, width, height, occupation_threshold, my_get_neighbors)
    //print_board(updated_board, width, height)

    for changed {
        updated_board, changed = get_update_board(updated_board, width, height, occupation_threshold, my_get_neighbors)
    }
    count := 0
    for _, val := range updated_board{
        if val == '#'{
            count ++
        }
    }
    fmt.Println(count)
}
