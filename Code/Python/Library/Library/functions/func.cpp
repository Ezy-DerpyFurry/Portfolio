#include <ctime>
#include <filesystem>
#include <iostream>
#include <chrono>
#include <thread>
#include <vector>
#include <string>
#include <cstring>
#include <X11/Xlib.h>
#include <X11/keysym.h>
#include <cstdio>
#include <utility>
#include <cctype>

int seed2 = time(0);

namespace fs = std::filesystem;

// Exterior Functions \\.

double to_int(const std::string& string) {
    double num = 0.0;
    double frac = 0.0;
    int sign = 1;
    bool decimal_found = false;
    double divisor = 10.0;

    size_t i = 0;

    while (i < string.size() && string[i] == ' ') i++;

    if (i < string.size() && (string[i] == '+' || string[i] == '-')) {
        if (string[i] == '-') sign = -1;
        i++;
    }

    while (i < string.size()) {
        if (isdigit(string[i])) {
            if (!decimal_found) {
                num = num * 10 + (string[i] - '0');
            } else {
                frac += (string[i] - '0') / divisor;
                divisor *= 10;
            }
        } else if (string[i] == '.' && !decimal_found) {
            decimal_found = true;
        } else {
            break;
        }
        i++;
    }

    return (num + frac) * sign;
}

/* My precious was replaced :/
bool contains(const std::string& string, const std::string& value) {
    if (value.empty() || value.size() < string.size()) return false;

    for (int i = 0; i < string.size() - value.size(); i++) {
        if (string.substr(i, value.size()) == value) {
            return true;
        }
    }
    return false;
}*/

extern "C" {
    bool debug = false;
    bool animate = false;
    bool dis_intro = false;

    int add(int a, int b) {
        return a + b;
    }

    double circlearea(double value, int type, int shape) {
        const double pi = 3.1416;
        double radius, area = 0.0;

        if (type == 0) {
            radius = value;
        } else {
            radius = value / 2.0;
        }
        if (shape == 0) {
            area = pi * radius * radius;
        } else if (shape == 1) {
            area = 4 * pi * radius * radius;
        }

        return area;
    }

    double squarearea(double side) {
        return side * side;
    } 

    void sleep(double seconds) {
        std::this_thread::sleep_for(std::chrono::duration<double>(seconds));
    }

    double to_int_converted(const char* string) {
        if (!string) return 0.0;
        std::string str(string);
        return to_int(str);
    }

    int defloat_int_c(const char* string) {
        if (!string) return 0;

        std::string str(string);
        int defloated_num = 0;

        for (int i = 0; i < str.size(); i++) {
            if (str[i] == '.') break;
            defloated_num = defloated_num * 10 + (str[i] - '0');
        }
        return defloated_num;
    }

    int defloat_int_double(double num) {
        return static_cast<int>(num);
    }

    /* Old Sleep function R.I.P

    void sleep(double seconds) {
        std::time_t start = std::time(0);
        while (std::time(0) - start < seconds) {
            // Wait code!!! :3
        } 
    } */

    void delete_file(const char* path) {
        
        if (std::remove(path) == 0) {
            if (debug) {
                std::cout << "File removed successfully." << "\n";
            }
        } else {
            std::perror("Error deleting file");
        }

    }

    void downloadanim() {
        const char* dots[] = {"   ", ".  ", ".. ", "..."};
        const int numDots = 4;
        int i = 0;

        while (animate) {
            i++;
            std::cout << "\rDownloading" << dots[i % numDots] << std::flush;
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
        } 

        std::cout << "Done" << '\n';
    }

    void set_intro(bool val) {
        dis_intro = val;
    }

    bool get_intro_state() {
        return dis_intro;
    }

    int randomraw() {
        int seed = static_cast<unsigned>(time(0));
        seed2++;
        seed = (seed2 * seed + 54325435);
        return seed & 0x7FFFFFFF;
    }

    bool contains_c(const char* string, const char* value) {
        if (!string || !value) return false;
        std::string s(string);
        std::string v(value);
        return s.find(v) != std::string::npos;
    }

    int mrandom(int min, int max) {
        if (max < min) return min;
        return min + (randomraw() % (max - min));
    }

    int filecount(const char* path_cstr) {
        int count = 0;

        try {
            std::string path(path_cstr);
            if (debug) {
                std::cout << path << '\n';
            }
            for (const auto& entry : fs::directory_iterator(path)) {
                if (fs::is_regular_file(entry.path())) {
                    count++;
                }
            }
        }
        catch (const fs::filesystem_error& e) {
            std::cerr << "Error: " << e.what() << std::endl;
        }

        return count;
    }

    const char* randomsong(std::string path) {
        static std::string chosensong;

        std::string folder = path;
        int total = filecount("Library");
        if (total <= 0) {
            return "";
        }

        int targetIndex = mrandom(0, total);

        size_t count = 0;
        try {
            for (const auto& entry : fs::directory_iterator(folder)) {
                if (fs::is_regular_file(entry.path()) && entry.path().extension() == ".mp3") {
                    if (count == static_cast<size_t>(targetIndex)) {
                        chosensong = entry.path().string();
                        return chosensong.c_str();
                    }
                    count++;
                }
            }
        }
        catch (const fs::filesystem_error& e) {
            std::cerr << "Error: " << e.what() << std::endl;
            return "";
        }

        return "";
    }

}

// Testing Code vv (To test directly)

int main() {
    std::string path = "../temp";
    size_t filecount = 0;

    try {
        for (const auto& entry : fs::directory_iterator(path)) {
            if (fs::is_regular_file(entry.path())) {
                filecount++;
                std::cout << "File Path" << entry.path() << "\n";
            }
        }

        std::cout << "File amount: " << filecount << "\n";

    }
    catch (const fs::filesystem_error& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    return 0;
}
