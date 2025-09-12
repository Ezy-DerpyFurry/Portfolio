### I got no clue but my friend told me what he is learning and I was bored so i did it
### Read the readme.md to know what the rules were

BASE_AMOUNT = 8 # <-- dis holds 8 duhhhhhz :3

# does da formulaaaa
def formula(texts: int, minutes: int):
    print("Calculating price of", texts, "texts and", minutes, "minutes") # Dis is fanci debuggy fingy i dunno
    return (minutes*.1) + BASE_AMOUNT + (texts*.05) # Dis just returns the formula lolllll

# Mah pritty custom flooring so python doesnt go 5499999999~ when dealing wif floats
def myFloor(c: int, max_length: int): 
    length = 0 # Base length
    result = "" # Defining the resulterzz
    for character in str(c): # a basic for loop yis :3 is lieekkkk uh go through da number like 5499999 and turns into a stringg to go through
        length = length + 1 # just adds one to da length so it can find out how many numbers to keep
        result = result + character # just appends each character until it breaks 
        if length >= max_length: # This just checks when to
            break                # break ya :D
    return result # returns da precious results

# uhh just loops until u get it right?
while True:
    try: # Try catch so code doesn't break
        minutes, texts = float(input("Minutes: ")), int(input("Texts: ")) # This gets the minutes and texts from da uuuser
        a,b = str(formula(texts, minutes)).split(".") # This turns the formula function into a string so that we can split it to get both sides
        print(f"Your total bill is ${int(a)}.{int(myFloor(b, 2)):02d}") # This prints the total bill tadaaa

        # This is the + strings dunno what you mean by it
        a,b = 1,2 # I know a and b are already used but they're no longer needed here so i just re-use
        print(a + b)
        print("a:", a + b)

        break # Stops the loop once the code finishes
    except ValueError as e: # Catches value error like putting "a" for a number
        print("Both inputs must be a integar (number)") # Just warns the user and re-does da code :3

# TADAAA
# Have an ascii catty :3
#
#
#       |\      _,,,---,,_
#  ZZZzz /,`.-'`'    -.  ;-;;,_
#       |,4-  ) )-,_. ,\ (  `'-'
#      '---''(_/--'  `-'\_)
#
