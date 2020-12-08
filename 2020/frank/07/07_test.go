package main

import (
    "testing"
    "strings"
    "fmt"
)

func TestOutput(t *testing.T){

    input := `light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.`

    buffer := strings.Split(input, "\n")

    lookup := extract(buffer)
    my_bag := []string{"shiny gold"}
    checked_off := make(map[string]bool)
    res := count_bags(lookup, my_bag, checked_off)
    if (res) != 4{
        t.Errorf("incorrect result %d", res)
    }
}

func TestOutput2(t *testing.T){

    input := `light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.`

    buffer := strings.Split(input, "\n")
    lookup := extract(buffer)
    my_bag := "shiny gold"
    res := count_bags2(lookup, my_bag)
    fmt.Println(res)
    if (res) != 32{
        t.Errorf("incorrect result %d",res)
    }
}


