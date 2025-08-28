#include <iostream>
#include <vector>
using namespace std;

const int SIZE = 3;
char current_p = 'x';

char board[3][3] = {
    {'-', '-', '-'},
    {'-', '-', '-'},
    {'-', '-', '-'}
};

bool print_board() {
    cout << "- 0 1 2\n";
    for (int i = 0; i < SIZE; i++) {
        cout << i << " ";
        for (int j = 0; j < SIZE; j++) {
            cout << board[i][j] << " ";
        }
        cout << endl;
    }
    cout << current_p << "'s turn" << endl;
    return true;
}

bool validate_move(int row, int column) {
    return board[row][column] == '-';
}

void clear_console() {
    cout << "\033[2J\033[1;1H";
}

char check_win() {

    for (int i = 0; i < SIZE; i++) {
        if (board[i][0] != '-' && board[i][0] == board[i][1] && board[i][1] == board[i][2]) {
            return board[i][0];
        }
    }

    for (int j = 0; j < SIZE; j++) {
        if (board[0][j] != '-' && board[0][j] == board[1][j] && board[1][j] == board[2][j]) {
            return board[0][j];
        }
    }

    if (board[0][0] != '-' && board[0][0] == board[1][1] && board[1][1] == board[2][2])
        return board[0][0];
    if (board[2][0] != '-' && board[2][0] == board[1][1] && board[1][1] == board[0][2])
        return board[2][0];

    return '-';
}

bool is_filled() {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            if (board[i][j] == '-')
                return false;
        }
    }
    return true;
}

int main() {
    string none;
    char choice;
    int row;
    int column;

    cout << "Welcome to tic tac toe (C++ version)" << endl;
    cout << "Enter any key to start: ";
    cin >> none;

    while (true) {
        
        if (is_filled()) {
            clear_console();
            cout << "Tie! No one won." << endl;
        } else {
            cout << "Not Tie!";
        }

        cout << "Enter a row and column (ex 0 1): ";
        cin >> row >> column;

        clear_console();

        if (validate_move(row, column)) {
            board[row][column] = current_p;
            cout << check_win() << endl;
            current_p = (current_p == 'x') ? 'o' : 'x';
            if (check_win() != '-') {
                clear_console();
                cout << "Player " << check_win() << " has won!\n";
                break;
                /* Doesn't work :p
                cout << "Would you like to restart (Y/N): " << endl;
                cin >> choice;
                if (choice == 'y') {
                    char board[3][3] = {
                        {'-', '-', '-'},
                        {'-', '-', '-'},
                        {'-', '-', '-'}
                    };
                }*/
            }
        } else {
            cout << "Can't go there!" << endl;
        }
        print_board();
    }

    return 0;
}
