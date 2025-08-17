#include <iostream>
#include <ctime>
#include <fstream>
using namespace std;

class Math {
public:

    static unsigned int seed;

    static double absNum(double a) {
        return (a < 0) ? -a : a;
    }

    static int randomraw() {
        seed = static_cast<unsigned>(time(0));
        seed = (104240 * seed + 1234245);
        return seed & 0x7FFFFFFF;
    }

    static double sqrt(double number) {
        if (number < 0) return -1;

        double guess = number;
        double accuracy = 0.000001;
        while ((guess * guess - number) > accuracy || (number - guess * guess) > accuracy) {
            guess = (guess + number / guess) / 2;
        }

        return guess;
    }

    static int randomnum(int min, int max) {
        return min + (randomraw() % (max - min + 1));
    }
};

unsigned int Math::seed;

int main() {
    int num;
    string confirm;
    int rannumber = Math::randomnum(10, 20);
    Math::seed = 14;
    ofstream file("ages.txt", ios::app);

    cout << Math::absNum(25) << endl;

    if (!file) {
        cout << "Not a valid file \n";
        return 1;
    }

    cout << "Random Chosen Number: " << rannumber << endl;
    cout << Math::sqrt(rannumber) << endl;
    file << "Random Number: " << rannumber << "\n" << "Random Number Squared: " << Math::sqrt(rannumber);

    cout << "Enter your age please: ";
    cin >> num;

    cout << "Is this your correct age?: " << num << " (Y/N)";
    cin >> confirm;

    file << "AGE: " << num << "\n";
    file << "Confirmed: " << confirm << "\n";

    if (confirm == "Y" || confirm == "y") {
        if (num < 13) {
            cout << "You're a child." << endl;
            file << "Category: Child\n";
        } else if (num > 12 && num < 18) {
            cout << "You're a teenager." << endl;
            file << "Category: Teenager\n";
        } else {
            file << "Category: Adult";
            cout << "You're an adult.\n" << endl;
        }
    } else {
        cout << "Please restart and state your real age." << endl;
        file << "Age not Confirmed\n";
    }

    file << "----\n";
    file.close();

    return 0;
}
