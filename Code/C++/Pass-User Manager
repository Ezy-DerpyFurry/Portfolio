#include <iostream>
#include <fstream>

unsigned int MAX_LINES = 255;

int loadfile(const char* filename, char lines[][300]) {
    std::ifstream file(filename);
    if (!file) {
        std::cout << "File: " << filename << " Not found." << std::endl;
        return 0;
    }

    int count = 0;

    while (count < MAX_LINES && file.getline(lines[count], 300)) {
        count++;
    }

    file.close();
    return count;
}

bool strequals(const char* a, const char* b){
    int i = 0;
    while (a[i] && b[i]) {
        if (a[i] != b[i]) return false;
        i++;
    }
    return a[i] == b[i];
}

int strlength(const char* text) {
    int length = 0;

    while (text[length] != '\0') {
        length++;
    }

    return length;
}

void strsplit(const char* line, char user[][100], char pass[][100], int index) {
    int i = 0;
    int j = 0;

    while (line[i] != ':' && line[i] != '\0') {
        user[index][i] = line[i];
        i++;
    }
    user[index][i] = '\0';

    if (line[i] == ':') i++;

    while (line[i] != '\0') {
        pass[index][j++] = line[i++];
    }
    pass[index][j] = '\0';
}

int main() {
    char filelines[MAX_LINES][300];
    char usernames[MAX_LINES][100];
    char passwords[MAX_LINES][100];

    int linecount = loadfile("users.txt", filelines);

    for (int i = 0; i < linecount; i++) {
        strsplit(filelines[i], usernames, passwords, i);
    }

    char inputUser[100];
    char inputPass[100];

    std::cout << "Enter you username: ";
    std::cin >> inputUser;

    std::cout << "Enter your password: ";
    std::cin >> inputPass;

    bool success = false;

    for (int i = 0; i < linecount; i++) {
        if (strequals(inputUser, usernames[i])) {
            if (strequals(inputPass, passwords[i])) {
                success = true;
                break;
            }
        }
    }

    if (success) {
        std::cout << "You are now logged in." << std::endl;
    } else {
        std::cout << "Login failed please try again." << std::endl;
    }

    return 0;
}
