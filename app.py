from PyQt5.QtWidgets import QApplication, QStackedWidget, QWidget, QPushButton, QMainWindow, QLabel, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt, QSize, QThread, QObject, pyqtSignal
from PyQt5.QtGui import QFont, QFontDatabase, QMovie
from game_sort import sort_games, get_steam_library

# Only needed for access to command line arguments
import sys

# Worker class
class getGames(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(str)

    def run(self):
        with open("user_input.txt", "r") as f:
            lines = f.readlines()
        api_key = lines[0].strip()
        print(api_key)
        steam_id = lines[1].strip()
        print(steam_id)
        print("Getting the games...")
        games = get_steam_library(api_key, steam_id)
        self.result.emit("Game data loaded!")
        print(games)
        self.finished.emit()

# Main class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("Steam Library Sort")
        self.setFixedSize(QSize(600, 800))
        self.setStyleSheet("background-color: #1b3448")

        # Stacked Widgets
        self.stack = QStackedWidget()
        self.login_page = QWidget()
        self.home_page = QWidget()
        self.loading_page = QWidget()
        self.stack.addWidget(self.login_page) # index 0
        self.stack.addWidget(self.home_page) # index 1
        self.stack.addWidget(self.loading_page) # index 2
    
        # Layout
        login_layout = QVBoxLayout()
        home_layout = QVBoxLayout()
        loading_layout = QVBoxLayout()

        # Login Header
        login_header = QLabel("Steam Library Sorter")
        login_header.setFont(QFont("Times New Roman", 30))
        login_header.setAlignment(Qt.AlignTop)
        login_header.setStyleSheet("color: white;")
        login_layout.addWidget(login_header)

        # Home Header
        home_header = QLabel("Steam Library Sorter")
        home_header.setFont(QFont("Times New Roman", 30))
        home_header.setAlignment(Qt.AlignTop)
        home_header.setStyleSheet("color: white;")
        home_layout.addWidget(home_header)

        # Loading Header
        loading_header = QLabel("Steam Library Sorter")
        loading_header.setFont(QFont("Times New Roman", 30))
        loading_header.setAlignment(Qt.AlignTop)
        loading_header.setStyleSheet("color: white;")
        loading_layout.addWidget(loading_header)

        # Info line
        info = QLabel("Enter your API key and user ID to begin sorting:")
        info.setFont(QFont("Times New Roman", 15))
        info.setStyleSheet("color: white")
        login_layout.addWidget(info)

        # Steam API key input
        self.API_key = QLineEdit()
        self.API_key.setPlaceholderText("Enter your Steam API key")
        self.API_key.setStyleSheet("background-color: #77afdb; color: black")
        self.API_key.setGeometry(300, 400, 600, 30) # Configure later
        login_layout.addWidget(self.API_key)

        # Steam ID input
        self.userID = QLineEdit()
        self.userID.setPlaceholderText("Enter your Steam User ID")
        self.userID.setStyleSheet("background-color: #77afdb; color: black")
        self.userID.setGeometry(300, 400, 600, 30) # Configure later
        login_layout.addWidget(self.userID)

        # Submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.save_input)
        submit_button.clicked.connect(self.start_fetch)
        submit_button.setStyleSheet("background-color: white; color: black")
        login_layout.addWidget(submit_button)

        # Loading text
        loading_text = QLabel("Getting your games...")
        loading_text.setFont(QFont("Times New Roman", 20))
        loading_text.setStyleSheet("color: white")
        loading_text.setAlignment(Qt.AlignCenter)
        loading_layout.addWidget(loading_text) 

        # Loading spinner gif
        spinner_label = QLabel()
        self.spinner = QMovie("spinner.gif")
        spinner_label.setMovie(self.spinner)
        spinner_label.setAlignment(Qt.AlignCenter)
        loading_layout.addWidget(spinner_label)

        # Home page
        self.results = QLabel("Results will appear here")
        self.results.setFont(QFont("Times New Roman", 20))
        home_layout.addWidget(self.results)

        # Ending block
        self.login_page.setLayout(login_layout)
        self.home_page.setLayout(home_layout)
        self.loading_page.setLayout(loading_layout)
        self.stack.setCurrentWidget(self.login_page)
        self.setCentralWidget(self.stack)

    # Saves the API key and user ID
    def save_input(self):
        api = self.API_key.text()
        id = self.userID.text()
        with open("user_input.txt", "w") as f:
            f.write(api)
            f.write("\n")
            f.write(id)
        print("Input saved!")

    def start_fetch(self):
        self.stack.setCurrentWidget(self.loading_page)
        self.spinner.start()

        # Thread and worker
        self.thread = QThread()
        self.worker = getGames()
        self.worker.moveToThread(self.thread)

        # Connecting the signals
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.result.connect(self.display_results)

        self.thread.start()

    def display_results(self, data):
        self.results.setText(data)
        self.stack.setCurrentWidget(self.home_page)
        self.spinner.stop()




app = QApplication(sys.argv) # if not using command line arguments, you can use QApplication([])

window = MainWindow()
window.show() #WINDOWS ARE HIDDEN BY DEFAULT

app.exec() #starts the event loop


# STEAM_API_KEY = "REMOVED"
# STEAM_ID = "76561199096796604"

# def get_games():
#     games = get_steam_library(STEAM_API_KEY, STEAM_ID)
#     sorted_games = sort_games(games, order=order)
#     return jsonify(sorted_games)