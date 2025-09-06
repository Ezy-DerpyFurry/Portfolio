#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <string.h>

// Defining a basic clear (not a real clear)
#define clear() printf("\033[2J\033[H");

// This is just to print the menu so I don't need to have it clutter the main code
void print_terminal_menu(const char *list[], int list_length, int num, const char *opening, const char *selector) {
    clear();
    printf("%s\n", opening);
    for (int i = 0; i < list_length; i++) {
        printf("  %s%s\n", (num-1 == i ? selector : ""), list[i]);
    }
}

// This is the main code to actually run the terminal
const char* terminal_menu(const char *list[], int list_length, const char *opening, const char *selector) {

    // Changes terminal's attributes like canceling input
    struct termios oldt, newt;
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);

    // Some variables to start with
    char c;
    int num = 1;

    print_terminal_menu(list, list_length, num, opening, selector);

    // Main while loop
    while (read(STDIN_FILENO, &c, 1) == 1) {
        if (c == 'q') {
            tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
            return "None";
            break;
        }

        // First if and else if is just to move up and down on the list
        if (c == 119 || c == 65) {
            num = (num + list_length - 2) % list_length + 1;
        } else if (c == 115 || c == 66) {
            num = num % list_length + 1;
        } else if (c == 10 || c == 67) {
            tcsetattr(STDIN_FILENO, TCSANOW, &oldt); // Resets terminal's attributes to normal once done
            return list[num-1];
            break;
        }

        print_terminal_menu(list, list_length, num, opening, selector);
    }

    tcsetattr(STDIN_FILENO, TCSANOW, &oldt); // Resets terminal's attributes if the function errors or ends wrong
}

// Example code you can mess around with it
int main() {
    const char *list[] = {
        "Apple",
        "Banana",
        "Orange",
        "Grape",
        "Strawberry",
        "Pancake",
    };

    const char *opening = "Choices: ";
    const char *selector = "> ";

    int list_length = sizeof(list) / sizeof(list[0]);

    const char *picked = terminal_menu(list, list_length, opening, selector);
    printf("You have chosen: %s\n", picked);

    return 0;
}
