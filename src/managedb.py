"""
Manages database read/write
"""

import os
import shutil
import sqlite3
import webbrowser
from datetime import datetime

DB_PATH = os.path.abspath(os.path.join('database', 'typespeed_data.db'))
TABLE_NAME = "TYPESPEED_RECORDS"


class ManageDB:
    def __init__(self):
        if not os.path.exists(DB_PATH):
            self.create_database()

        self.conn = sqlite3.connect(DB_PATH)
        self.c = self.conn.cursor()

    def __del__(self):
        # Close the connection to the db
        self.conn.close()

    def create_database(self):
        """
        Creates a new database at `DB_PATH` and the table `TABLE_NAME` in it
        """

        directory = os.path.split(DB_PATH)[0]

        # Remove the database file if it already exists
        if os.path.exists(DB_PATH):
            shutil.rmtree(directory)

        os.mkdir(directory)

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""CREATE TABLE %s (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_date TEXT NOT NULL,
                right_words INT NOT NULL,
                wrong_words INT NOT NULL,
                accuracy REAL NOT NULL,
                speed REAL NOT NULL)""" % TABLE_NAME)
        conn.commit()

    def save_data(self, data):
        """
        Saves the given dictionary data to the database

        Parameters:
            data - A dictionary that contains the data to be saved in the database
        """

        entry_date = datetime.now().strftime("%d/%m/%y %I:%M:%S %p")
        right_words = int(data['right'])
        wrong_words = int(data['wrong'])
        accuracy = float(data['accuracy'])
        speed = float(data['speed'])

        if not os.path.exists(DB_PATH):
            self.create_database()

        self.c.execute(
            """INSERT INTO %s (entry_date, right_words, wrong_words, accuracy, speed)
            VALUES (?, ?, ?, ?, ?)
            """ % TABLE_NAME,
            (
                entry_date,
                right_words,
                wrong_words,
                accuracy,
                speed,
            )
        )
        self.conn.commit()

    def view_records(self):
        """
        Generates an HTML file from the database records and opens it
        in the default browser
        """

        records = self.c.execute(
            "SELECT entry_date, right_words, wrong_words, accuracy, speed FROM %s ORDER BY id desc" % TABLE_NAME)

        html = \
            """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Type Speed Records</title>
    <link rel="stylesheet" href="resources/stylesheet.css" type="text/css">
    <script src="resources/show_best.js" type="text/javascript"></script>
</head>
<body>
    <div id="wrapper">
        <h1>Type Speed Records</h1>
        <h2><a href="https://github.io/areeb-beigh">github.io/areeb-beigh</a></h2>
        <div id="box">
            <table width="30%" border="0" cellpadding="10px" cellspacing="0px">
                <tr>
                    <th>Date</th>
                    <th>Right Words</th>
                    <th>Wrong Words</th>
                    <th>Accuracy</th>
                    <th>Speed</th>
                </tr>
        """

        for entry in records:
            entry = list(map(str, entry))
            row = \
                """
                <tr>
                    <td id="date">%s</td>
                    <td id="right">%s</td>
                    <td id="wrong">%s</td>
                    <td id="accuracy">%s</td>
                    <td id="speed">%s</td>
                </tr>
                """ % \
                (
                    entry[0],
                    entry[1],
                    entry[2],
                    entry[3],
                    entry[4]
                )
            html += row

        html += """</table></div>
        <input id="showButton" type="button" onclick="showBestAll()" value="Show Best">
        </div></body></html>"""

        with open("records.html", "w") as f:
            f.write(html)

        webbrowser.open("records.html")
