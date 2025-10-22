### PLEASE DO NOT USE THIS FOR BAD ###
# Anything done with this is not my fault and I will not be help accountable for it
# This is simply here so you can check your password to see if its out there or not
# This also depends on the machine how fast it can loop
# Also no this doesn't leak any passwords but it will append every password you put in to the passwords.txt for later use if you want it off change append to False
# ^^ It's only locally

### SIDE NOTE ###
# This code uses relative paths so things like vs code can use it
# I'm pretty proud of this if im being honest, I think it's really really cool!
# But please don't use it for bad, not that it's capable of anything there's no username input, it's more so for checking if your password is leaked or how crackable it is.

# Imports
import os
import string
import itertools
import random
import time
import threading
import asyncio
from pathlib import Path
from typing import AsyncIterator

# Variables and options
APPEND = False # Appends the password you put for next time if you want
LOGBRUTEFORCE = False # Logs the brute force attempts
MAXSAFECOUNT = 5_000_000 # If it is above this number
CHECKADDEDLISTS = True # If you don't want it to loop through your files just set to False

# Don't touch variables
chars = string.ascii_letters + string.digits + string.punctuation # Total brute force tries every combonation using these
nums = string.digits # For number only combonations
customPasswordPath = Path(r'CustomPasswordLists') # This is a relative path by da way so I don't know if it will work on everything

def clearTerm() -> None: print("\033[2J\033[H", end="") # Fake terminal clear to make it look nice but really just moves text up and resets your cursor to the top

def loadFile(path: str) -> list: # A safer file loader thingy I made
    output = []

    targetFile = os.path.abspath(path)

    try:
        with open(targetFile, "r") as file:
            for password in file:
                output.append(password.strip('\n'))
    except FileNotFoundError:
        print("File path not found please enter a valid path")
    except PermissionError:
        print(f"You do not have permission to read and/or write to {targetFile}")
    except ValueError as error:
        print(f"ERROR: {error}")
    
    return output

def formatTime(seconds: float) -> str: # Formats seconds from using time.perf_counter() for time elapsed
    ms = int((seconds - int(seconds)) * 1000)
    s = int(seconds) % 60
    m = (int(seconds) // 60) % 60
    h = int(seconds) // 3600
    if h:
        return f"{h}:{m:02d}:{s:02d}.{ms:03d}"
    if m:
        return f"{m:02d}:{s:02d}.{ms:03d}"
    return f"{s:02d}.{ms:03d}"

def loadAddedPasswordLists() -> list: # Handles loading passwords from the lists you add
    output = []
    start = time.perf_counter()

    for addPath in customPasswordPath.glob('*.add'):
        output.append(loadFile(addPath))
    
    print(f"Loaded all password lists in {formatTime(time.perf_counter() - start)} \nformat(hh:mm:ss.ms)")
    return output


def finalBruteForce(amount: int) -> AsyncIterator[str]: # Loops through all combonations possible using eat digit starting at 1, 2 ect.
    numCheck = True
    for a in range(1, amount + 1):
        print("Attempting numbers only first.")
        for b in itertools.product(nums, repeat = a):
            yield ''.join(b)
    for a in range(1, amount + 1):
        print("Full combonations now.")
        for b in itertools.product(chars, repeat = a):
            yield ''.join(b)

defaultPasswords = loadFile("passwords.txt")
if CHECKADDEDLISTS: AddedPasswords = loadAddedPasswordLists()

while True: # Main loop
    found = False
    yourPassword = input("Please enter a password to check: ").strip() # YES IT STRIPS SPACES most passwords don't allow spaces but you can remove it if you want...

    for word in defaultPasswords: # Checks passwords.txt (The default)
        if yourPassword == word:
            print("Your password has been found, not recommended to use!")
            found = True
            break

    if found: break
    for word in AddedPasswords: # Checks the lists you added
        if yourPassword == word:
            print("Your password has been found, not recommended to use!")
            found = True
            break

    if found: break
    choice = input("Your password has not been found!\nWould you like to try a more rough form of brute forcing? (Y/n) ")

    if choice.lower() != "y":
        print("Exiting. . .")
        break

    clearTerm()
    try:
        amt = int(input("Enter how many characters long you would like it (ex. 1): "))
    except ValueError:
        print("Not a valid number defaulting to 1")
        amt = 1

    confirmationNumber = random.randint(1,40)
    attempts = len(chars)**amt
    choice = input(f"Are you sure you are about to load/try {format(attempts, ",")} times. type 'YES {str(confirmationNumber)}'  ") # Confirms you actually wanna run it

    if choice != f"YES {confirmationNumber}":
        print("Not the correct confirmation exiting. . .")
        break

    start = time.perf_counter()
    
    if attempts > MAXSAFECOUNT:
        print(f"WARNING: OVER MAX SAFE COUNT {format(attempts, ",")}. Program will slowdown to keep it from crashing")

    with open("finalBruteForceLog.txt", "w") as file: # Main loop that compares passwords/logs attempts for brute force
        for combo in finalBruteForce(amt):
            print("BruteForce attempting >> ", combo)
            
            if LOGBRUTEFORCE:
                print("BruteForce log adding >> ", combo)
                file.write('\n' + combo)

            if yourPassword == combo:
                print(f"BruteForce attempt successful your password is: {combo}")
                break
                
            print("Unsuccessful retrying")

            if len(combo) > 5 and attempts > MAXSAFECOUNT:
                time.sleep(0.001)
        
        print(f"Total time elapsed: {formatTime(time.perf_counter() - start)} \nformat is (hh:mm:ss.ms)")

    if APPEND and yourPassword not in defaultPasswords: # This handles appending the password you put in to a txt for later so you don't reuse passwords
        with open("passwords.txt", "a") as file:
            file.write('\n' + yourPassword)
