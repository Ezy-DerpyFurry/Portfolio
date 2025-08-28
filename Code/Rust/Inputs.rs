use std::collections::HashMap;
use std::io::{self, Write};

fn readint(prompt: &str) -> i32 {
    print!("{}", prompt);
    io::stdout().flush().unwrap();

    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("Can't read line");
    input.trim().parse().expect("Please enter a Integer")
}

fn readstr(prompt: &str) -> String {
    print!("{}", prompt);
    io::stdout().flush().unwrap();

    let mut msg = String::new();
    io::stdin().read_line(&mut msg).expect("Can't read line");

    msg.trim().to_lowercase()
}

fn main() {
    println!("Hello, World! (From rust)");

    let mut responses = HashMap::new();
    responses.insert("hi", "Hello!");
    responses.insert("bye", "Why are you leaving?");

    /*for (key, value) in &responses {
        println!("{}: {}", key, value);
    }*/

    loop {
        let msg = readstr("Say Hi: ");

        if let Some(reply) = responses.get(msg.as_str()) {
            println!("{}", reply);
        } else if msg == "quit" {
            println!("See you later!");
            break;
        } else if msg == "math" {
            let msg2 = readstr("Add/Subtract/Multiply/Divide: ");
            let num1 = readint("First number: ");
            let num2 = readint("Second number: ");

                if msg2 == "add" {println!("{} + {} = {}", num1, num2, num1 + num2);}
                else if msg2 == "subtract" {println!("{} - {} = {}", num1, num2, num1 - num2);}
                else if msg2 == "multiply" {println!("{} x {} = {}", num1, num2, num1 * num2);}
                else if msg2 == "divide" {println!("{} / {} = {}", num1, num2, num1 / num2);}
        } else {
            println!("I don't understand what you mean.");
        }
    }
}
