package utils

import (
    "fmt"
    "os"
    "path"
    "log"
    "bufio"
    "flag"
)

const INPUT_PATH = "input"

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

func ReadChallenge(challenge_id int) []string{
    total_path := path.Join(INPUT_PATH, fmt.Sprintf("%02d", challenge_id))
    return read_file(total_path)
}

func ReadChallengeTest(challenge_id int) []string{
    total_path := path.Join(INPUT_PATH, fmt.Sprintf("%02d_test", challenge_id))
    return read_file(total_path)
}

func ParsePart() int {
    partPtr := flag.Int("part", 1, "selected part")
    flag.Parse()
    return *partPtr
}
