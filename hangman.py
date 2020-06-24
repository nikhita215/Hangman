from random import choice
from string import ascii_lowercase
# Part 1/8 Hello, Hangman
def greeting():
    print("H A N G M A N")
    ##print("The game will be available soon.")

# Part 2/8 I want to play a game
def result(win=False):
    if win:
        print("You guessed the word!")
        print("You survived!")
    else:
        print("You are hanged!")

# Part 3/8 Make Your Choice    
def new_game():
    hangman_word_list = 'python', 'java', 'kotlin', 'javascript'
    return choice(hangman_word_list), list(), ''


# Part 6/8 The Value of a Life
def game_round(correct, number_of_lives=8, correctly_guessed_letters=set(), entered_letters=set()):
    progress = ""
    for letter in correct:
        if letter not in correctly_guessed_letters:
            progress += "-"
        else:
            progress += letter
    print()
    print(progress)  # Something like --v- is output
    if progress != correct:
        letter = input("Input a letter: ")
        if len(letter)==1:
            if letter in ascii_lowercase:
                if letter in entered_letters:
                    print("You already typed this letter")
                else:
                    entered_letters.add(letter)
                    if letter in correct:
                        correctly_guessed_letters.add(letter)
                    else:
                        number_of_lives -= 1
                        print("No such letter in the word")
            else:
                print("It is not an ASCII lowercase letter")
        else:
            print("You should input a single letter")
    return number_of_lives, correctly_guessed_letters, progress, entered_letters

greeting()
while 1:
    game = input('Type "play" to play the game, "exit" to quit: ')
    if game == "play":
        chosen_word, correctly_guessed, progression = new_game()
        lives, correctly_guessed, progression, entered_letters = game_round(chosen_word)

        while lives:
            if progression == chosen_word:
                break
            lives, correctly_guessed, progression, entered_letters = game_round(chosen_word, lives, correctly_guessed, entered_letters)
        else:
            result()

        if progression == chosen_word:
            result(True)
    elif game == "exit":
        break


