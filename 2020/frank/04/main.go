package main

import (
    "fmt"
    "os"
    "log"
    "bufio"
    "strings"
    "strconv"
    "unicode"
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

func add_attributes(line string, dict map[string]string) map[string]string {
    pairs := strings.Split(line, " ")
    for _, pair := range pairs{
        split_pair := strings.Split(pair, ":")
        dict[split_pair[0]] = split_pair[1]
    }
    return dict
}

func contains(list []string, field string) bool {
    for _, item := range list{
        if item == field{
            return true
        }
    }
    return false
}

func is_valid(passport map[string]string, required_fields []string, 
                check func(string,string) bool) bool {
    for _, field := range required_fields{
        if val, ok := passport[field]; !ok {
            return false
        }else if !check(field, val){
            return false
        }
    }
    return true
}

func no_check(field string, value string) bool {return true}

var valid_ecls map[string]int

func value_check(field string, value string) bool {
    switch field{
    case "byr":
        i, err := strconv.Atoi(value)
        if err == nil{
            return (i >= 1920 && i <= 2002)
        }
    case "iyr":
        i, err := strconv.Atoi(value)
        if err == nil{
            return (i >= 2010 && i <= 2020)
        }
    case "eyr":
        i, err := strconv.Atoi(value)
        if err == nil{
            return (i >= 2020 && i <= 2030)
        }
    case "hgt":
        i, err := strconv.Atoi(value[0:len(value)-2])
        unit := value[len(value)-2:]
        if err == nil{
            if unit == "cm" {
                return (i >= 150 && i <= 193)
            }else if unit == "in"{
                return (i >= 59 && i <= 76)
            }
        }
    case "hcl":
        if value[0] != '#'{
            return false
        }else if len(value) == 7{
            for _, char := range value[1:]{
                if !unicode.IsDigit(char) && !unicode.IsLetter(char) {
                    return false
                }
            }
            return true
        }
    case "ecl":
        _, ok := valid_ecls[value]
        return ok
    case "pid":
        for _, char := range value{
            if !unicode.IsDigit(char){
                return false
            }
        }
        return len(value) == 9
    default:
        return true
    }
    return false
}

func main(){
    partPtr := flag.Int("part", 1, "selected part")
    flag.Parse()

    var check func(string, string) bool

    if *partPtr == 2{
        check = value_check
    }else{
        check = no_check
    }

    valid_ecls = map[string]int{
        "amb":0,"blu":0,"brn":0,"gry":0,"grn":0,"hzl":0,"oth":0,
    }

    buffer := read_file("input/04")
    required_fields := []string{"byr","iyr","eyr","hgt","hcl","ecl","pid"}
    valids := 0
    total := 0

    current_passport := make(map[string]string)

    for _, line := range buffer{
        if line != ""{
            add_attributes(line, current_passport)
        }else{
            if is_valid(current_passport, required_fields, check) {
                valids += 1
            }
            current_passport = make(map[string]string)
            total += 1
        }
    }

    if len(current_passport)!=0{
        if is_valid(current_passport, required_fields, check){
            valids += 1 
        }
        total += 1
    }

    fmt.Printf("num valid passports %d/%d", valids, total)
}
