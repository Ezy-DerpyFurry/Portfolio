package main

import (
	"fmt"
	"os"
	"strings"
	"bufio"
	"math/rand"
	"time"
)

func main() {
    fmt.Println("Hello, World! (From go)")

	reader := bufio.NewReader(os.Stdin)

	for {
		fmt.Print("Say Hi: ")
		msg, _ := reader.ReadString('\n')
		
		msg = strings.TrimSpace(msg)
		msg = strings.ToLower(msg)

		if msg == "hi" {
			fmt.Println("Hello!")
		} else if msg == "game" {
			var num int
			for {
				rand.Seed(time.Now().UnixNano())
				guess := rand.Intn(10) + 1

				fmt.Print("Guess the number (1-10 [0 = quit]): ")
				fmt.Scan(&num)

				if num == guess {
					fmt.Println("Good job you got it right!")
				} else if num == 0 {
					break
				} else {
					fmt.Println("Incorrect please try again.")
				}
			}
		} else if msg == "quit" {
			fmt.Println("See you later!")
			break
		} else {
			fmt.Println("Inncorrect")
		}
	}
}
