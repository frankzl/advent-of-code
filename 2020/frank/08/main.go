package main

import (
    utils "../mylib"
    "fmt"
    "strings"
    "strconv"
)

func split_operation(line string)(string, int){
    command := strings.Split(line, " ")
    function, arg := command[0], command[1]
    arg_val, _ := strconv.Atoi(arg[1:])

    if arg[0] == '-'{
        arg_val *= -1
    }
    return function, arg_val
}

func run_command(line string, instr_ptr int, acc int)(new_instr_ptr, new_acc int){
    new_instr_ptr = instr_ptr
    new_acc = acc
    function, arg_val := split_operation(line)

    switch(function){
    case "acc":
        new_acc += arg_val
        new_instr_ptr += 1
    case "jmp":
        new_instr_ptr += arg_val
    default:
        new_instr_ptr += 1
    }
    return
}

func run(code []string, instr_ptr int, acc int, execution_stack map[int]bool) (int, bool){
    if _, ok := execution_stack[instr_ptr]; ok{
        return acc, false
    }
    if instr_ptr >= len(code) {
        return acc, true
    }
    execution_stack[instr_ptr] = true
    instr_ptr, acc = run_command( code[instr_ptr], instr_ptr, acc )
    return run(code, instr_ptr, acc, execution_stack)
}

func get_line(function string, arg int) string {
    if arg >= 0{
        return fmt.Sprintf(function + " +%d", arg)
    }
    return fmt.Sprintf(function + " %d", arg)
}

func main(){
    code := utils.ReadChallenge(8)
    pt   := utils.ParsePart()

    if pt == 1{
        execution_stack := make(map[int]bool)
        fmt.Println(run(code, 0, 0, execution_stack))
        return
    }

    for i, line := range code{
        function, arg_val := split_operation(line)
        new_line := ""

        if function == "nop"{
            new_line = get_line("jmp", arg_val)
        }else if function == "jmp"{
            new_line = get_line("nop", arg_val)
        }

        if new_line != ""{
            execution_stack := make(map[int]bool)
            code[i] = new_line
            acc, ok := run(code, 0, 0, execution_stack)
            if ok{
                fmt.Println(acc)
                return
            }
            code[i] = line
        }
    }
}
