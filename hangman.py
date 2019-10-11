#!/usr/bin/env python3
import string
import sys
import os
from colorama import init, Fore, Back, Style
from random import randint
init()  # Enables colorama for windows
MAX_TRIES = 6
HANGMAN_ASCII_ART = (r"""
  /\  /\__ _ _ __   __ _ _ __ ___   __ _ _ __
 / /_/ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \
/ __  / (_| | | | | (_| | | | | | | (_| | | | |
\/ /_/ \__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                   |___/
""")


HANGMAN_PHOTOS = {
    0: Fore.RED +"""x-------x """,
    1: Fore.RED + "x-------x\n|\n|\n|\n|",
    2: Fore.GREEN +"x-------x\n|\t|\n|\t0\n|\n|\n|",
    3: Fore.BLUE +"x-------x\n|\t|\n|\t0\n|\t|\n|\n|",
    4: Fore.CYAN +"x-------x\n|\t|\n|\t0\n|\t\b /|" +"\\" +"\n|\n|",
    5: Fore.RED +"x-------x\n|\t|\n|\t0\n|\t\b /|" +"\\" +"\n|\t\b/\n|",
    6: Fore.LIGHTMAGENTA_EX +"x-------x\n|\t|\n|\t0\n|\t\b /|" +"\\" +"\n|\t\b/ \\\n|",
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


def check_valid_input(letter_guessed, old_letters_guessed, secret_word):
    """input vaildateor.
    :param letter_guessed: user's input letter
    :param old_letters_guessed: List of guessed letters
    :type letter_guessed: string(char)
    :type old_letters_guessed: list
    :return: True/False
    :rtype: Boolean
    """
    letter_guessed = letter_guessed.lower()
    if letter_guessed == 'clear' or letter_guessed in string.ascii_letters or letter_guessed == secret_word:
        if letter_guessed not in old_letters_guessed:
            return True
    else:
        return False


def try_update_letter_guessed(letter_guessed, old_letters_guessed, secret_word, num_of_tries):
    """check user input and append it to a list, increment number of tries when failed
    :param letter_guessed: user's input letter
    :param old_letters_guessed: List of guessed letters
    :param secret_word: user's chosen word
    :type letter_guessed: string(char)
    :type old_letters_guessed: list
    :type secret_word: string
    :type num_of_tries: int
    :return: num_of_tries
    :rtype: int
    """
    if not check_valid_input(letter_guessed, old_letters_guessed, secret_word):
        print('Invaild letter\n' + ' -> '.join(sorted(old_letters_guessed)))
        
    elif letter_guessed == 'clear':
        clear_screen()
        
    else:
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
    return num_of_tries


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


#def play_again():
    #print(Fore.RESET), main()


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
        num_of_tries = 0
        file_path = input(r"Enter file path: ")
        file_index = input("Enter index: ").lower()
        secret_word = choose_word(file_path, file_index)
        old_letters_guessed = []
        print(f""" Let’s start! {print_hangman(num_of_tries)}""")
    except KeyboardInterrupt:
        print('\n', 'Ctrl+C was clicked --> Exiting...')
        os._exit(0)()

    try:
        while num_of_tries < MAX_TRIES:
            guess_input = input("Enter word/letter: ")
            num_of_tries = try_update_letter_guessed(guess_input, old_letters_guessed, secret_word, num_of_tries)
            game_status = check_win(secret_word, old_letters_guessed)
            if game_status:
                break
        if not game_status:
            print('GAME OVER\r\n')
        if 'y' in input('Do u Want to play again? -> y/n '):
            print(Fore.RESET), main()
        else:
            os._exit(0)
    except (KeyboardInterrupt):
        print('\n', 'Ctrl+C was clicked --> Exiting...')
        os._exit(0)
    except EOFError:
        print('\n', 'Ctrl+Z was clicked --> Exiting...')
        os._exit(0)


if __name__ == "__main__":
    main()
