from flask import Flask, jsonify
from game_sort import sort_games, get_steam_library

STEAM_API_KEY = "REMOVED"
STEAM_ID = "76561199096796604"

app = Flask(__name__)

@app.route('/games', methods=['GET'])
def get_games():
    games = get_steam_library(STEAM_API_KEY, STEAM_ID)
    sorted_games = sort_games(games, order=order)
    return jsonify(sorted_games)

if __name__ == "__main__":
    print("Welcome to Steam Library Sorter!")
    order = input("Do you want to sort by oldest or newest first? (Type 'oldest' or 'newest'): ").strip().lower()
    if order not in ['oldest', 'newest']:
        print("Invalid input. Defaulting to oldest.")
        order = 'oldest'
    app.run(debug=True)