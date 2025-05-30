from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt5.QtCore import Qt, QSize

# Only needed for access to command line arguments
import sys
from random import choice

window_titles = [
    'My App',
    'My App',
    'Still My App',
    'Still My App',
    'What on earth',
    'What on earth',
    'This is surprising',
    'This is surprising',
    'Something went wrong'
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.n_times_clickedd = 0

        self.setWindowTitle("My App")
        self.setFixedSize(QSize(600, 600))

        self.button = QPushButton("Press Me!")
        self.button.clicked.connect(self.the_button_was_clicked)

        self.windowTitleChanged.connect(self.the_window_title_changed)
                     
        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        print("Clicked")
        new_window_title = choice(window_titles)
        print("Setting title: %s" % new_window_title)
        self.setWindowTitle(new_window_title)

    def the_window_title_changed(self, window_title):
        print("Window title changed: %s" % window_title)

        if window_title == "Something went wrong":
            self.button.setDisabled(True)


app = QApplication(sys.argv) # if not using command line arguments, you can use QApplication([])

window = MainWindow()
window.show() #WINDOWS ARE HIDDEN BY DEFAULT

app.exec() #starts the event loop






# from flask import Flask, jsonify
# from game_sort import sort_games, get_steam_library

# STEAM_API_KEY = "REMOVED"
# STEAM_ID = "76561199096796604"

# app = Flask(__name__)

# @app.route('/games', methods=['GET'])
# def get_games():
#     games = get_steam_library(STEAM_API_KEY, STEAM_ID)
#     sorted_games = sort_games(games, order=order)
#     return jsonify(sorted_games)

# if __name__ == "__main__":
#     print("Welcome to Steam Library Sorter!")
#     order = input("Do you want to sort by oldest or newest first? (Type 'oldest' or 'newest'): ").strip().lower()
#     if order not in ['oldest', 'newest']:
#         print("Invalid input. Defaulting to oldest.")
#         order = 'oldest'
#     app.run(debug=True)