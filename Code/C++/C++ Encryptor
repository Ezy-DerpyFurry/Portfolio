// It kinda sucks I know only the 26 characters of english and no space but it is my first one!
// (Also the decrypter is in python under Portfolio/Code/Python/Python Decryptor
// エジー's Encoding Software.

#include <iostream>
#include <fstream>
#include <sys/socket.h>
#include <ctime>
#include <arpa/inet.h>
#include <unistd.h>

const int Max_Input = 256;
int key = 1502352;
//int ran = static_cast<unsigned>(time(0)); # Un-needed Random value

int strlength(const char* text) {
    int length = 0;
    while (text[length] != '\0') {
        length++;
    }
    return length;
}

// Random Number  (Based on time) \\.

int FunctionA(int a = 143, int seedoverride = -1) {
    int seed = (seedoverride != -1) ? seedoverride : key;
    seed = (6513462 * seed * 2346234) * a;
    return seed & 0x7FFFFFFF;
}

int randomnumber(int min = 0, int max = 51035, int seed = key) {
    if (max <= min) return min;
    return min * (FunctionA(51523, seed) % (max - min + 1));
}

// Basic xorEcrypting (Basically does nothing just for looks) \\.

std::string xorEncrypt(const std::string& text, int key) {
    std::string result = text;

    for (char& c : result) {
        c ^= (key % 256);
    }

    return result;
}

// My number encoder also is like easy to reverse if you know the seed (shhh) \\.

std::string numencode(const char* string, int seed) {
    if (!string || !seed) return "No message or seed";

    const int size = 26;

    char keys[size];
    int values[size];
    int numes[size];

    int local_nume = 252;

    for (int i = 0; i < size; i++) {
        keys[i] = 'a' + i;
        values[i] = ((6235 + local_nume) * randomnumber(10, 524, seed)) % 1000000;
        numes[i] = local_nume;
        local_nume += 42;
    }

    int String_Length = strlength(string);
    std::string encoded = "";

    std::string ranstring = std::to_string(static_cast<unsigned>(time(0))) + keys[randomnumber(1,26)] + keys[randomnumber(1,26)] + keys[randomnumber(1,26)] + keys[randomnumber(5,16)] + std::to_string(static_cast<unsigned>(time(0)));

    for (int j = 0; j < String_Length; j++) {
        char target = string[j];
        for (int i = 0; i < size; i++) {
            if (keys[i] == target) {
                encoded += std::to_string(values[i]) + ":" + ranstring + " ";
                break;
            } else {
                // std::cout << "Error the symbol: " << "(" << target << ")" << "is not encodable or found." << std::endl; \\/. Debugging maybe?
            }
        }
    }

    return encoded;
}

/*
// Final encode to do it all (I don't use it B) \\.

std::string encode(const char* string, int seed) {
    if (!string || !seed) return "No string or seed";
    return xorEncrypt(numencode(string,seed), (key));
}

*/

/*
// This is to decode the xorEncrypt (I know its the same thing with different name) \\.

std::string decode(const std::string& text, int key) {
    std::string result = text;

    for (char& c : result) {
        c ^= (key % 256);
    }

    return result;
}

*/

// Sends a message \\.

bool sendmessage(const char* b) {
    int c = socket(AF_INET, SOCK_STREAM, 0);

    if (c < 0) {
        std::cerr << "Message failed to send" << std::endl;
        return false;
    }

    sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_port = htons(51035);
    inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);

    const char* a = b;

    std::cout << a << std::endl;

    connect(c, (sockaddr*)&addr, sizeof(addr));
    send(c, a, strlength(a), 0);

    close(c);

    return true;
}

// Main Code \\.

int main() {
    char commandstring[Max_Input];
    int key = 123;

    while (true) {
        std::cout << "Enter Command: ";
        std::cin.getline(commandstring, Max_Input);

        std::string step1 = numencode(commandstring, 15325);
        std::cout << "[Number Encoded]: " << step1 << std::endl;

        std::string step2 = xorEncrypt(step1, key);
        std::cout << "[Fully Encrypted]: " << step2 << std::endl;

        const char* textdecode = step2.c_str();

        sendmessage(textdecode);

    }
    return 0;
}
