#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <string.h>
#define clear() printf("\033[2J\033[H");

void print_terminal_menu(const char *list[], int list_length, int num, const char *opening, const char *selector) {
    clear();
    printf("%s\n", opening);
    for (int i = 0; i < list_length; i++) {
        printf("  %s%s\n", (num-1 == i ? selector : ""), list[i]);
    }
}

const char* terminal_menu(const char *list[], int list_length, const char *opening, const char *selector) {

    struct termios oldt, newt;
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);

    char c;
    int num = 1;

    print_terminal_menu(list, list_length, num, opening, selector);

    while (read(STDIN_FILENO, &c, 1) == 1) {
        if (c == 'q') {
            tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
            return "None";
            break;
        }

        if (c == 119 || c == 65) {
            num = (num + list_length - 2) % list_length + 1;
        } else if (c == 115 || c == 66) {
            num = num % list_length + 1;
        } else if (c == 10 || c == 67) {
            tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
            return list[num-1];
            break;
        }

        print_terminal_menu(list, list_length, num, opening, selector);
    }

    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
}

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
