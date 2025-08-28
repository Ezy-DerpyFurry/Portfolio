#include <stdio.h>
#include <string.h>

int main() {
    printf("Hello, World! (From C)\n");

    char msg[10];

    while (true) {
        printf("Say Hi: ");
        fgets(msg, sizeof(msg), stdin);
        msg[strcspn(msg, "\n")] = 0;

        if (strcmp(msg, "Hi") == 0) {
            printf("Hello!\n");
        } else if (strcmp(msg, "Quit") == 0) {
            printf("See you later!\n");
            break;
        } else {
            printf("Inncorrect\n");
        }
    }

    return 0;
}
