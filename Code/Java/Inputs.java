import java.util.HashMap;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World! (From java)");

        HashMap<String, String> responses = new HashMap<>();
        responses.put("hi", "Hello!");
        responses.put("bye", "Why are you leaving?");

        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.print("Say Hi: ");
            String msg = scanner.nextLine().toLowerCase();

            if (responses.containsKey(msg)) {
                System.out.println(responses.get(msg));
            } else if (msg.equals("quit")) {
                System.out.println("See you later!");
                break;
            } else {
                System.out.println("I don't understand what you mean.");
            }
        }
    }
}
