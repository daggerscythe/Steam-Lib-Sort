from PyQt5.QtWidgets import QApplication, QStackedWidget, QWidget, QPushButton, QMainWindow, QLabel, QVBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QComboBox
from PyQt5.QtCore import Qt, QSize, QThread, QObject, pyqtSignal
from PyQt5.QtGui import QFont, QFontDatabase, QMovie
from game_sort import sort_games, get_steam_library

# Only needed for access to command line arguments
import sys
import json
import os

# Worker class
class getGames(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(dict)

    def run(self):
        try:
            with open("user_input.txt", "r") as f:
                lines = [line.strip() for line in f.readlines()]
            if len(lines) < 2 or not lines[0] or not lines[1]:
                raise ValueError("user_input.txt is missing API key or Steam ID")
            self.api_key = lines[0].strip()
            self.steam_id = lines[1].strip()
            print("Getting the games...")
            games = get_steam_library(self.api_key, self.steam_id)
            self.result.emit(games)
        except Exception as e:
            print("error getting games: ", e)
            self.result.emit({})
        finally:
            self.finished.emit()

# Main class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("Steam Library Sort")
        self.setMinimumSize(QSize(600, 800))
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

        # Sorting dropdown
        self.sort_menu = QComboBox()
        self.sort_menu.addItems(["Oldest to Newest", "Newest to Oldest"])
        self.sort_menu.setStyleSheet("background-color: #77afdb; color: white;")
        self.sort_button = QPushButton("Sort!")
        self.sort_button.setStyleSheet("background-color: #77afdb; color: white;")
        self.sort_button.clicked.connect(self.sort)
        home_layout.addWidget(self.sort_menu)
        home_layout.addWidget(self.sort_button)

        # Home page game table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Game Title", "Release Date"])
        self.table.setStyleSheet("""
                                 QHeaderView::section{
                                    background-color: #77afdb;
                                    color:white;
                                    font-family: 'Times New Roman';
                                    font-size: 16px;
                                 }
                                 QTableWidget{
                                    color:white;
                                    background-color: #1b3448;
                                    font-family: 'Times New Roman';
                                    font-size: 16px;
                                 }
                                """)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers) # setting to read-only
        home_layout.addWidget(self.table)

        # Ending block
        self.login_page.setLayout(login_layout)
        self.home_page.setLayout(home_layout)
        self.loading_page.setLayout(loading_layout)
        self.stack.setCurrentWidget(self.login_page)
        self.setCentralWidget(self.stack)

        with open("user_input.txt", "r") as f:
            lines = [line.strip() for line in f.readlines()]
            if len(lines) >= 2 and lines[0] and lines[1]:
                self.api_key = lines[0]
                self.steam_id = lines[1]
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Question)
                msg.setWindowTitle("Use saved credentials?")
                msg.setText("Do you want to use your last saved API key and ID?")
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg.setStyleSheet("""
                                  QMessageBox{
                                    background-color: #1b3448;
                                    color: white;
                                    font: 14pt "Times New Roman";
                                  }
                                  QLabel{
                                    color: white;
                                    font: 14pt "Times New Roman";
                                  }
                                  QPushButton {
                                    background-color: #77afdb;
                                    color: white;
                                    padding: 5px;
                                  } 
                """)
                response = msg.exec()
                if response == QMessageBox.Yes:
                    self.auto_login()
                else:
                    os.remove("games.json")

    # Auto login
    def auto_login(self):
        self.API_key.setText(self.api_key)
        self.userID.setText(self.steam_id)
        self.start_fetch()

    # Saves the API key and user ID
    def save_input(self):
        api_key = self.API_key.text()
        steam_id = self.userID.text()
        with open("user_input.txt", "w") as f:
            f.write(api_key + "\n")
            f.write(steam_id)
        print("Input saved!")

    def start_fetch(self):
        if os.path.exists("games.json"):
            with open("games.json", "r", encoding="utf-8") as f:
                games = json.load(f)
            if games:
                cleaned_games = sort_games(games, "oldest")
                self.display_results(cleaned_games)
                return
            else:
                print("games.json was empty")
            self.display_results(games)
        else:
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

    def display_results(self, games):
        self.spinner.stop()
        self.stack.setCurrentWidget(self.home_page)
        self.games = games
        self.table.setRowCount(len(games))
        for row, (title, (appid, release_date)) in enumerate(games.items()):
            self.table.setItem(row, 0, QTableWidgetItem(title))
            self.table.setItem(row, 1, QTableWidgetItem(release_date))
        if games:
            with open("games.json", "w", encoding="utf-8") as f:
                json.dump(games, f, indent=2)
        else:
            print("Empty dict, no games to save")

    def sort(self):
        selected = self.sort_menu.currentText()
        if selected == "Oldest to Newest":
            sorted_games = sort_games(self.games, "oldest")
            self.display_results(sorted_games)
        else:
            sorted_games = sort_games(self.games, "newest")
            self.display_results(sorted_games)       
        
app = QApplication(sys.argv) # if not using command line arguments, you can use QApplication([])

window = MainWindow()
window.show() #WINDOWS ARE HIDDEN BY DEFAULT

app.exec() #starts the event loop

# STEAM_API_KEY = "REMOVED"
# STEAM_ID = "76561199096796604"