// For comparing to other code \\.
#include <iostream>
#include <algorithm>
#include <cctype>

int main() { 
    std::cout << "Hello, World! (From C++)" << std::endl;

    std::string msg;

    while (true) {
        std::cout << "Say Hi: ";
        std::cin >> msg;

        std::transform(msg.begin(), msg.end(), msg.begin(), [](unsigned char c) { return std::tolower(c); });

        if (msg == "hi") {
            std::cout << "Hello!" << std::endl;
        } else if (msg == "quit") {
            std::cout << "See you later!" << std::endl;
            break;
        } else if (msg == "game"){
            std::cout << "Awe see you lator bestieee" << std::endl;
            break;
        } else {
            std::cout << "Inncorrect" << std::endl;
        }
    }

    return 0;
}
