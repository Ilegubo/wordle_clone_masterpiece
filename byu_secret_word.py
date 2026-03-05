#code is organized in functions to make more readable and maintainable
#number of attempts is limited to 6
def user_input(default_word:str):
    while True:
        guess = input("Word: ")
        if len(default_word) != len(guess):
            print("Invalid input size")
            continue
        
        return guess


def initialize_game(default_word:str, guess:str):
    container = ["_"] * len(guess)
    matches = [False] * len(guess)
    if guess == default_word:
        print("Correct")
        return guess

    for idx, letter in enumerate(default_word):
        if guess[idx].lower() == letter:
            container[idx] = letter.upper()
            matches[idx] = True

    for n_idx, letter in enumerate(default_word):
        if container[n_idx] ==  "_" and matches[n_idx] == False:
            for i, j in enumerate(guess):
                if j.lower() == letter:
                    container[i] = letter.lower()

    return ' '.join(container)


print("Welcome to the guessing game")
default_word = "mosiah"
hint = "_ " * len(default_word)
print(f"Hint: {hint}")

response = input("Would you like to play the guessing game? (yes/no) ")
while True:
    if response.lower() == "yes":
        attempts = 0
        while True:
            guess = user_input(default_word)
            attempts += 1
            start_game = initialize_game(default_word, guess)
            print(start_game)
            hint = start_game
            if guess.lower() == default_word:
                print(f"Congratulations! You guessed the word in {attempts} attempts.")
                break
            if attempts >= 6:
                print(f"Out of attempts. The word was: {default_word}")
                break
        break
    elif response.lower() == "no":
        print("Exiting...")
        break
    else:
        print("Invalid input")
        response = input("Would you like to play the guessing game? (yes/no) ")