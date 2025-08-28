using System;

class Program {
    static void Main() {
        Console.WriteLine("Hello, World! (From C#)");


        while (true) {
            Console.Write("Say Hi: ");
            string msg = Console.ReadLine();

            if (msg == "Hi") {
                Console.WriteLine("Hello!");
            } else if (msg == "Quit") {
                Console.WriteLine("See you later!");
                break;
            } else {
                Console.WriteLine("Inncorrect");
            }
        }
    }
}
