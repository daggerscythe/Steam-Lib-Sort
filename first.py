import requests
import json
import wikipediaapi
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget
import flask
import matplotlib.pyplot as plt
STEAM_API_KEY = "REMOVED"
#domain name = localhost
STEAM_ID = "76561199096796604"
STEAM_API_URL = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key=REMOVED&steamid=76561199096796604&include_appinfo=true&include_played_free_games=true"

def get_steam_library (api, id):
    params = {
        "key": api,
        "steamid": id,
        "include_appinfo": True, #includes game names
        "include_played_free_games": True, #includes free games
        "format": "json"
    }

    response = requests.get(STEAM_API_URL, params = params)

    if response.status_code == 200:
        data = response.json()
        games = data.get("response", {}).get("games", [])

        game_list = [game["name"] for game in games]  # Extract names
        return game_list
    else:
        print(f"Error: {response.status_code}")
        return []
    
steam_games = get_steam_library(STEAM_API_KEY, STEAM_ID)
print(steam_games)