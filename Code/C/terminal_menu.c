// I *MIGHT* turn this into a python library and more customizable \\.

#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <string.h>

void clear() {
    printf("\033[2J\033[H");
}

void print_terminal_menu(const char *list[], int list_length, int num) {
    printf("Options:\n");
    for (int i = 0; i < list_length; i++) {
        if (num-1 == i) printf("  > %s", list[i]);
        else printf("  %s", list[i]);
        printf("\n");
    }
}

const char* terminal_menu(const char *list[], int list_length) {

    struct termios oldt, newt;
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;

    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);

    char c;
    int num = 1;

    print_terminal_menu(list, list_length, num);

    while (read(STDIN_FILENO, &c, 1) == 1) {
        if (c == 'q') {
            return NULL;
            break;
        }

        if (c == 119 || c == 65) {
            num = num - 1;
            if (num == 0) num = list_length;
        } else if (c == 115 || c == 66) {
            num = (num % list_length) + 1;
        } else if (c == 10 || c == 67) {
            tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
            return list[num-1];
            break;
        }

        clear();
        print_terminal_menu(list, list_length, num);
    }

    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
}

int main() {
    clear();

    const char *list[] = {
        "Apple",
        "Banana",
        "Orange",
        "Grape",
        "Strawberry",
        "Pancake",
    };

    int list_length = sizeof(list) / sizeof(list[0]);

    const char *picked = terminal_menu(list, list_length);
    printf("You have chosen: %s\n", picked);

    return 0;
}
