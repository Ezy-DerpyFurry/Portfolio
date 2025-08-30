package main

import (
	"fmt"
	"os"
	"bufio"
	"strings"
	"strconv"
)

var board = [6][7]rune {
	{'-','-','-','-','-','-','-'},
	{'-','-','-','-','-','-','-'},
	{'-','-','-','-','-','-','-'},
	{'-','-','-','-','-','-','-'},
	{'-','-','-','-','-','-','-'},
	{'-','-','-','-','-','-','-'},
}

var current_p = 'x'

func print_board() {
	fmt.Println("0 1 2 3 4 5 6")
	for i := 0; i < 6; i++{
		for j := 0; j < 7; j++ {
        	fmt.Print(string(board[i][j]), " ")
    	}
		fmt.Println()
	}
}

func input(msg string) string {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print(msg)
	text, _ := reader.ReadString('\n')
	text = strings.TrimSpace(text)

	return text
} 

func toggle_player() {
	if current_p == 'x' {
		current_p = 'o'
	} else {
		current_p = 'x'
	}
}

func validate_move(column int) int {
	for i := 0; i < 6; i++ {
		if board[i][column] != '-' {
			return i - 1
		}
	}

	return 5
}

// Check win functions was mostly chatgpt I didn't know da algorithm (I'm coping, I'm just bad at this.)

func check_win() rune {
    directions := [][2]int{
        {0, 1},
        {1, 0},
        {1, 1},
        {1, -1},
    }

    for i := 0; i < 6; i++ {
        for j := 0; j < 7; j++ {
            player := board[i][j]
            if player == '-' {
                continue
            }

            for _, d := range directions {
                count := 1

                r, c := i+d[0], j+d[1]
                for r >= 0 && r < 6 && c >= 0 && c < 7 && board[r][c] == player {
                    count++
                    r += d[0]
                    c += d[1]
                }

                if count >= 4 {
                    return player
                }
            }
        }
    }
    return '-'
}


func main() {

	for {
		msg := input("Pick a column. (0-6): ")
		column_num, _ := strconv.Atoi(msg)

		if column_num < -1 || column_num > 6 {
			fmt.Println("You can't go there")
		} else {

			row := validate_move(column_num)

			if row == -1 {
				fmt.Println("You can't make a move there")
				print_board()
			} else {
				board[row][column_num] = current_p
				print_board()
				if check_win() != '-' {
					if check_win() == "111" {
						fmt.Println("Player (o) won!")
					} else {
						fmt.Println("Player (x) won!")
					}
				}
			}

			toggle_player()

		}
	}

}
