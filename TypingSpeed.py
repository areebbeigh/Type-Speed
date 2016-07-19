# Python Typing Speed Tester
# github.com/areeb-beigh

"""
This script measures your typing speed and returns a stats on it.
"""

import time, random, webbrowser
from threading import Timer

def getWords():
	# Returns an array of words extracted from words.txt

	words = []

	with open('words.txt', 'r') as f:
		words += f.read().split('\n')

	return words

def chooseRandomWord(array):
	# Returns a random word from the given array of words

	return random.choice(array)

def checkWord(givenWord, typedWord):
	# Compares the word the user was supposed to type and the word user typed
	# Returns true if matched and false if not

	if (givenWord == typedWord):
		return True

	return False

def getStats(correctWords, wrongWords, totalWords):
	# Computes and returns the player's typing stats

	accuracy = round(((correctWords / totalWords) * 100), 2)
	speed = float(correctWords / 2)

	stats = {
		"right": str(correctWords),
		"wrong": str(wrongWords),
		"accuracy": str(accuracy),
		"speed": str(speed)
	}

	return stats

def writeHTML(stats):
	# Writes the HTML file with the stats

	html = """<!DOCTYPE html>
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
		text-align: center;
	}

	table {
		position: relative;
		left: 485px;
		top: 50px;
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
		<h2>github.com/areeb-beigh</h2>
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
</html>""" % (
				stats["right"], 
				stats["wrong"], 
				stats["accuracy"], 
				stats["speed"])

	with open('results.html', 'w+') as f:
		f.write(html)

def endGame():
	# Ends the game and prepares the results

	global exit

	stats = getStats(correctWords, wrongWords, totalWords)
	
	print("\n")
	for key, value in stats.items():
		print(" " + key.title(), value, sep= ": ")

	writeHTML(stats)
	webbrowser.open("results.html")
	exit = True

print("Typing Speed Tester by Areeb - github.com/areeb-beigh")

print("""
	Quick guide:
		A word will come up on the screen and you'll have to type the exact same word
		and hit enter. You'll have 120 seconds to type in as many words as you can.
	""")

print("Hit enter to continue ('q' to exit)")

response = input()

if(response == "q"):
	exit()

correctWords = 0
wrongWords = 0
totalWords = 0

wordList = getWords()

t = Timer(120, endGame)	# Call endGame() after 120 seconds
t.start()				# Start the timer

exit = False

while not exit:
	randomWord = chooseRandomWord(wordList)
	totalWords += 1

	print("  ", randomWord)

	typedWord = input("> ")

	if (checkWord(randomWord, typedWord)):
		correctWords += 1
	else:
		wrongWords += 1