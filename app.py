from flask import Flask, render_template
from game_sort import sort_games, get_steam_library

STEAM_API_KEY = "REMOVED"
STEAM_ID = "76561199096796604"

app = Flask(__name__)

@app.route("/")
def home():
    return ("Hello world!")
    # sorted_games = sort_games(get_steam_library(STEAM_API_KEY, STEAM_ID)) #Fetch and sort game data
    # return render_template("index.html", games = sorted_games)

@app.route("/test")
def test():
    return "Test!"

if __name__ == "__main__":
    app.run(debug=True)