#!/usr/bin/env python3
import string
import sys
import os
from colorama import init, Fore, Back, Style
from random import randint

init()  # Enables colorama for Windows
MAX_TRIES = 6
num_of_tries = 0
HANGMAN_ASCII_ART = (r"""
  /\  /\__ _ _ __   __ _ _ __ ___   __ _ _ __
 / /_/ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \
/ __  / (_| | | | | (_| | | | | | | (_| | | | |
\/ /_/ \__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                   |___/
""")


HANGMAN_PHOTOS = {
    0: (Fore.RED + r"""x-------x """),
    1: Fore.RED + (r"""
     x-------x
     |
     |
     |
     |
     |

"""),
    2: (Fore.GREEN + r"""
     x-------x
     |       |
     |       0
     |
     |a
     |
"""),
    3: (Fore.BLUE + r"""
     x-------x
     |       |
     |       0
     |       |
     |
     |
"""),
    4: (Fore.CYAN + r"""
     x-------x
     |       |
     |       0
     |      /|\
     |
     |
"""),
    5: Fore.RED + r"""
x-------x
|       |
|       0
|      /|\
|      /
|
""",
    6: Fore.LIGHTMAGENTA_EX + r"""
    x-------x
    |       |
    |       0
    |      /|\
    |      / \
    |
""",
}


def open_screen():
    print(f'{HANGMAN_ASCII_ART}\n Max Tries: {MAX_TRIES}')


def choose_word(file_path, index):
    """Choosing word from a text file.
    :param file_path: file's path location
    :param index: selected word's index
    :type file_path: string
    :type index: int
    :return: The selected word
    :rtype: string
    """
    try:
        with open(file_path, 'r') as words:
            word_list = words.readlines()
            if index.lower() == 'random':
                index = randint(0, len(word_list) - 1)
                print(index)
                chosen_word = word_list[index].replace('\n', '')
            else:
                chosen_word = word_list[int(index)].replace('\n', '')
        return chosen_word
    except IndexError:
        print('index out of range, chose the first word')
        index = 0
        with open(file_path, 'r') as words:
            chosen_word = words.readlines()[index].replace('\n', '')
        return chosen_word
    except OSError:
        print(
            Back.RED +
            'error was found, please enter correct path' +
            Back.RESET)
        main()
    except ValueError:
        print(
            Back.RED +
            'error was found, please enter correct index' +
            Back.RESET)
        main()


def check_valid_input(letter_guessed, old_letters_guessed,secret_word):
    """input vaildateor.
    :param letter_guessed: user's input letter
    :param old_letters_guessed: List of guessed letters
    :type letter_guessed: string(char)
    :type old_letters_guessed: list
    :return: True/False
    :rtype: Boolean
    """
    letter_guessed = letter_guessed.lower()
    if letter_guessed in string.ascii_letters or letter_guessed == secret_word:
        if letter_guessed not in old_letters_guessed or letter_guessed == 'clear':
            return True
    else:
        return False


def try_update_letter_guessed(
        letter_guessed,
        old_letters_guessed,
        secret_word):
    """append the user's input.
    :param letter_guessed: user's input letter
    :param old_letters_guessed: List of guessed letters
    :param secret_word: user's chosen word
    :type letter_guessed: string(char)
    :type old_letters_guessed: list
    :type secret_word: string
    :return: True/False
    :rtype: Boolean
    """
    if not check_valid_input(letter_guessed, old_letters_guessed,secret_word):
        print('Invaild letter\n' + ' -> '.join(sorted(old_letters_guessed)))
    elif letter_guessed == 'clear':
        clear_screen()
    else:
        global num_of_tries
        if letter_guessed.lower() not in secret_word:
            old_letters_guessed.append(letter_guessed.lower())
            num_of_tries += 1
            print('Wrong :(')
            print(print_hangman(num_of_tries))
            print(show_hidden_word(secret_word, old_letters_guessed))

        else:
            if len(letter_guessed) > 1 and letter_guessed == secret_word:
                new_list = [char for char in letter_guessed]
                for item in new_list:
                    old_letters_guessed.append(item)
            old_letters_guessed.append(letter_guessed.lower())
            print(show_hidden_word(secret_word, old_letters_guessed))
            

def print_hangman(num_of_tries):
    return (HANGMAN_PHOTOS[num_of_tries])


def show_hidden_word(secret_word, old_letters_guessed):
    """show the status of the hidden word.
    :param secret_word: user's chosen word
    :param old_letters_guessed: List of guessed letters
    :type secret_word: string
    :type old_letters_guessed: list
    :return: variable "result" which contain the satus
    :rtype: string
    """
    secret_word_progress = ['']
    for letter in secret_word:
        if letter in old_letters_guessed:
            secret_word_progress.append(letter + " ")
        else:
            secret_word_progress.append("_ ")
    result = ''.join(secret_word_progress)
    return result


def check_win(secret_word, old_letters_guessed):
    if ''.join(show_hidden_word(secret_word, old_letters_guessed).split()) in secret_word:
        print('win')
        return True
    return False


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def Instructions():
    print("""
        Instructions
-------------------------------
""", Style.BRIGHT + """Type wordlist path
Type random in index for random word or specific index.""", Style.RESET_ALL + """
// Commands
clear - for cleaning the screen
Ctrl+C - For exiting.
-------------------------------\n""")

open_screen()
Instructions()
def main():
    try:
        file_path = input(r"Enter file path :")
        file_index = input("Enter index: ").lower()
        secret_word = choose_word(file_path, file_index)
        old_letters_guessed = []
        print(f""" Let’s start! {print_hangman(num_of_tries)}""")
    except KeyboardInterrupt:
        print('\n', 'Ctrl+C was clicked --> Exiting...')
        sys.exit()

    try:
        while num_of_tries < MAX_TRIES:
            try_update_letter_guessed(input("Enter a letter: "), old_letters_guessed, secret_word)
            game_status = check_win(secret_word, old_letters_guessed)
            if game_status:
                break
        if not game_status:
            print('GAME OVER')
    except (KeyboardInterrupt):
        print('\n', 'Ctrl+C was clicked --> Exiting...')
    except EOFError:
        print('\n', 'Ctrl+Z was clicked --> Exiting...')


if __name__ == "__main__":

    main()
