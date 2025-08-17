#include <iostream>
#include <fstream>
using namespace std;

const int MAX_LINES = 256;
const int MAX_LENGTH = 256;

class functions {
public:
    static int loadfile(const char* filename, char lines[][MAX_LENGTH]) {
        ifstream file(filename);
        if (!file) {
            cout << "Sorry, could not find that file." << endl;
            return 0;
        }

        int count = 0;
        while (count < MAX_LINES && file.getline(lines[count], MAX_LENGTH)) {
            count++;
        }

        file.close();
        return count;
    }

    static bool contains(const char* haystack, const char* needle) {
        if (!*needle) return true;

        for (int i = 0; haystack[i]; i++) {
            int j = 0;
            while (needle[j] && haystack[i + j] == needle[j]) {
                ++j;
            }

            if (!needle[j]) return true;
        }

        return false;
    }
};

int main() {
    char filelines[MAX_LINES][MAX_LENGTH];

    int linecount = functions::loadfile("users.txt", filelines);

    for (int i = 0; i < linecount; i++) {
        cout << "Line - " << i + 1 << ": " << filelines[i] << endl;
    }

    char buffer[100];

    cout << "Please type what you want to search: " << endl;
    cin >> buffer;

    const char* target = buffer;
    bool success = false;
    int line;

    for (int i = 0; i < linecount; i++) {
        if (functions::contains(filelines[i], target)) {
            success = false;
            line = i + 1;
        }
    }
    if (!success) {
        cout << target << " not found, please try again." << endl;
    } else {
        cout << "Target found, Line = " << line << endl;
    }

}
