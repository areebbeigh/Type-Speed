# Author: Areeb Beigh
# github.com/areeb-beigh

"""
This script measures your typing speed and returns a stats on it.
"""

import random
import webbrowser

from threading import Timer


def get_words():
    """ Returns an array of words extracted from words.txt """

    words = []

    with open('words.txt', 'r') as f:
        words = f.read().split("\n")

    return words


def choose_random_word(array):
    """
    Returns a random word from the given array of words

    Parameters:
        array: Array to chose from
    """

    return random.choice(array)


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
        "right":     str(correct),
        "wrong":     str(wrong),
        "accuracy":  str(accuracy),
        "speed":     str(speed)
    }

    return stats


def write_html(stats):
    """
    Writes the HTML file with the stats

    Parameters:
        stats:
            Typing stats
    """

    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Type Speed by Areeb</title>
</head>
<style>
    * {
        font-family: calibri
    }

    body {
        margin-left: auto;
        margin-right: auto;
        max-width: 1000px;
        text-align: center;
        padding: 0 30px 30px;
    }

    table {
        width: 100%%;
        text-align: justify;
        font-size: 20px;
        border: none;
        border-radius: 0.1em;
    }

    table td {
        border-spacing: 1px;
        border: 1px solid white;
        border-color: white;
    }
</style>
<body>
    <div id="wrapper">
        <h1>Type Speed Tester by Areeb</h1>
        <h2>https://github.com/areeb-beigh</h2>
        <div id="box">
            <table width="30%%" border="0" cellpadding="10px" cellspacing="0px" bgcolor="pink">
                <tr><td>Right Words</td><td>%s</td></tr>
                <tr><td>Wrong Words</td><td>%s</td></tr>
                <tr><td>Accuracy</td><td>%s%%</td></tr>
                <tr><td>Speed</td><td>%s WPM</td></tr>
            </table>
        </div>
    </div>
</body>
</html>
""" % (stats["right"],
       stats["wrong"],
       stats["accuracy"],
       stats["speed"])

    with open('results.html', 'w+') as f:
        f.write(html)


def end_game():
    """ Ends the game and prepares the results """

    global exit_game

    stats = get_stats(correct_words, wrong_words, total_words)

    print("\n")
    for key, value in stats.items():
        print(" " + key.title(), value, sep= ": ")

    write_html(stats)
    webbrowser.open("results.html")
    exit_game = True

print("Typing Speed Tester by Areeb - github.com/areeb-beigh")
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
wordList = get_words()
t = Timer(120, end_game)  # Call end_game() after 120 seconds
t.start()  # Start the timer

exit_game = False

while not exit_game:
    random_word = choose_random_word(wordList)
    total_words += 1
    print("  ", random_word)
    typed_word = input("> ")

    if check_word(random_word, typed_word):
        correct_words += 1
    else:
        wrong_words += 1