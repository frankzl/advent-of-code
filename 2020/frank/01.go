package main

import (
    "fmt"
    "os"
    "log"
    "bufio"
    "strconv"
    "flag"
)

func main(){
    partPtr := flag.Int("part", 1, "selected part")
    flag.Parse()

    file, err := os.Open("input/01")
    if err != nil {
        log.Fatal(err)
    }
    defer file.Close()
    
    scanner := bufio.NewScanner(file)

    var buffer []int
    for scanner.Scan(){
        i, _ := strconv.Atoi(scanner.Text())
        buffer = append(buffer, i)
    }

    if *partPtr == 1 {
        for i, u := range buffer{
            numberA := int(u)
            for _, v := range buffer[i+1:]{
                numberB := int(v)
                if (numberA + numberB == 2020){
                    fmt.Printf("%d * %d = %d",
                                numberA,
                                numberB,
                                numberA*numberB)
                    return
                }
            }
        }
    }else if *partPtr == 2{
        for i, u := range buffer{
            numberA := int(u)
            for _, v := range buffer[i+1:]{
                numberB := int(v)
                for _, w := range buffer[i+2:]{
                    numberC := int(w)
                    if (numberA + numberB +numberC == 2020){
                        fmt.Printf("%d * %d * %d = %d", 
                                    numberA, 
                                    numberB, 
                                    numberC, 
                                    numberA*numberB*numberC)
                        return
                    }
                }
            }
        }
    }
}
