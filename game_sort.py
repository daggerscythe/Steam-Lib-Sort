import requests
import time
import json
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget
import flask
import matplotlib.pyplot as plt
from datetime import datetime
from collections import OrderedDict

STEAM_API_KEY = "REMOVED"
STEAM_ID = "76561199096796604"
STEAM_API_URL = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key=REMOVED&steamid=76561199096796604&include_appinfo=true&include_played_free_games=true"


#Gets the release date of one game
def get_release_date (game_id):
    #Scraping release date from Steam's game page
    url = f"https://store.steampowered.com/app/{game_id}/"
    try:
        # Send GET request to the page
        response = requests.get(url)
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the <div> element with 'Release Date'
        release_date_div = soup.find('div', class_='release_date')
        if release_date_div:
            date = release_date_div.find('div', class_='date')
            if date:
                return date.get_text(strip=True)
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error for app {game_id}: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Error fetching data for app {game_id}: {err}")
        
    return None
    ''' 
    #SteamDB HTML Scrape method (Doesn't work, SteamDB blocks requests)
    url = f"https://steamdb.info/app/{game_id}/"
    try:
        # Send GET request to the page
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the <tr> element with 'Release Date'
        release_date_row = soup.find('tr', string=lambda text: text and 'Release Date' in text)
        
        if release_date_row:
            # Extract the date from the second <td> and remove the time part (after the ' - ')
            release_date = release_date_row.find_all('td')[1].get_text(strip=True)
            release_date = release_date.split(' - ')[0]  # Remove the time part
            return release_date
        else:
            return "Unknown"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for app {game_id}: {e}")
        return "Unknown"
    '''
    '''
    #STEAM API METHOD (UNRELIABLE, GETS WRONG DATES)
    url = f"https://store.steampowered.com/api/appdetails?appids={game_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data[str(game_id)]["success"]:
            release_info = data[str(game_id)]["data"].get("release_date", {})
            return release_info.get("date", "Unknown")
    return "Unknown"
    '''

    
#Gets the games and their IDs using the Steam ID and Steam API key
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
        game_dict = {}
        data = response.json()
        games = data.get("response", {}).get("games", []) #Gets the games

        for game in games:
            game_id = game.get("appid")
            name = game.get("name")
            if name and game_id:
                release_date = get_release_date(game_id)
                game_dict[name] = (game_id, release_date)
        return game_dict
    else:
        print(f"Error: {response.status_code}")
        return {}
    

#Stores the results
owned_games = get_steam_library(STEAM_API_KEY, STEAM_ID)

#Changes release date to datetime format for sorting
def parse_release_date(release_date):
    if release_date in ['Unknown', 'To be announced', ''] or release_date is None:
        return None
    
    for fmt in ('%b %d, %Y', '%d %b, %Y', '%Y-%m-%d', '%d %b %Y', '%b %d %Y'):
        try:
            return datetime.strptime(release_date, fmt)
        except ValueError:
            pass

    return None


#Method that sorts the games from oldest to newest releases
def sort_games(game_dict):
    #Parse release dates into datetime objects
    for name, (game_id, release_date) in game_dict.items():
        #print(f"date before parsing: {release_date}") #For debugging
        game_dict[name] = (game_id, parse_release_date(release_date))
        #print(f"date after parsing: {release_date}") #FOr debugging

    #Sort the games by release date
    sorted_games = dict(sorted(game_dict.items(), key=lambda item: (item[1][1] is None, item[1][1])))

    # Convert datetime back to string format
    for name, (game_id, release_date) in sorted_games.items():
        #print(f"Date before converting back: {release_date}") #For debugging
        if release_date is not None:
            sorted_games[name] = (game_id, release_date.strftime('%b %d, %Y'))
        else:
            sorted_games[name] = (game_id, 'Unknown')
    return sorted_games

#Prints the list of games
def print_games(game_dict):
    for game_name, (game_id, release_date) in game_dict.items():
        print(f"{game_name}, Release Date: {release_date}")

# test_games = {
#     "PAYDAY 2": ("game_1", "Aug 13, 2013"),
#     "Batman™: Arkham Origins": ("game_2", "Oct 24, 2013"),
#     "The Talos Principle": ("game_3", "Dec 11, 2014"),
#     "Grand Theft Auto V Legacy": ("game_4", "Apr 13, 2015"),
#     "Beholder": ("game_5", "Nov 09, 2016"),
#     "The Forest": ("game_6", "Apr 30, 2018"),
#     "Rec Room": ("game_7", "Sep 02, 2021"),
#     "Grand Theft Auto V Enhanced": ("game_8", "Mar 04, 2025"),
#     "Borderlands 2 RU": ("game_9", "Unknown"),
# }
# print("GAMES BEFORE SORT")
# print("----------------------------------------------------")
# print_games(owned_games)
# print("----------------------------------------------------")
# print("GAMES AFTER SORT")
# print("----------------------------------------------------")
# print_games(sort_games(owned_games))
# print("----------------------------------------------------")

