# Author: Areeb Beigh <areebbeigh@gmail.com>
# github.com/areebbeigh

"""
TypeSpeed is a simple program that measures your typing speed and keeps
the records in a database, at the end of every typing test the database is
updated and an HTML file is generated that displays the records.

Type on!
"""

# Python imports
import random
import webbrowser
from threading import Timer

# Local imports
from src.managedb import ManageDB

db = ManageDB()
ended = False


def main():
    """ Displays available menu options """

    print("     Type Speed by Areeb - github.com/areebbeigh")
    print("\n")
    print("     1. Play")
    print("     2. View records")

    choice = int(input())

    while choice not in range(1,3):
        print("> Invalid input")
        choice = int(input())
    else:
        if choice == 1:
            start_game()
        elif choice == 2:
            db.view_records()


def get_words():
    """ Returns an array of words extracted from words.txt """

    words = []

    with open('words.txt', 'r') as f:
        words = f.read().split("\n")

    return words


def check_word(reference_word, given_word):
    """
    Compares the word the user was supposed to type and the word user typed
    Returns true if both match, false otherwise

    Parameters:
        reference_word:
            Reference word

        given_word:
            Word to check
    """

    if reference_word == given_word:
        return True

    return False


def get_stats(correct, wrong, total):
    """
    Computes and returns the player's typing stats

    Parameters:
        correct:
            Number of correct words

        wrong:
            Number of wrong words

        total:
            Total number of words
    """

    accuracy = round(((correct / total) * 100), 2)
    speed = float(correct / 2)

    stats = {
        "right": str(correct),
        "wrong": str(wrong),
        "accuracy": str(accuracy),
        "speed": str(speed)
    }

    return stats


def end_game():
    """ Ends the game and prepares the results """

    global ended
    # Need a new instance because this method is called in a
    # separate thread and can't use the old database connection
    # created in the previous instance of ManageDB()
    db = ManageDB()
    stats = get_stats(correct_words, wrong_words, total_words)
    db.save_data(stats)  # Saves the data to the database
    db.view_records()
    print("\n")
    for key, value in stats.items():
        print(" " + key.title(), value, sep=": ")
    webbrowser.open("results.html")

    ended = True


def start_game():
    """ Starts the game """

    global correct_words
    global wrong_words
    global total_words

    print("""
    Quick guide:
        A word will come up on the screen and you'll have to type the exact same word
        and hit enter. You'll have 120 seconds to type in as many words as you can.
        """)
    print("Hit enter to continue ('q' to exit_game)")

    response = input()

    if response == "q":
        exit()

    correct_words = 0
    wrong_words = 0
    total_words = 0
    word_list = get_words()
    # Call end_game() after 120 seconds
    t = Timer(120, end_game)
    t.start()

    while True:
        if ended:
            exit()
        random_word = random.choice(word_list)
        total_words += 1
        print("  ", random_word)
        typed_word = input("> ")

        if check_word(random_word, typed_word):
            correct_words += 1
        else:
            wrong_words += 1

main()
