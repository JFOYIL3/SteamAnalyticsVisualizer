import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")


class UserGamesData:
    def __init__(self, steam_id):
        self.steam_id = steam_id
        self.data = []
        self.developers = {}
        self.publishers = {}
        self.genres = {}
        self.release_years = {}

        USER_GAME_URL = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={steam_id}&include_appinfo=true&format=json"

        data_response = requests.get(USER_GAME_URL)
        if data_response.status_code == 200:
            self.data = data_response.json()["response"].get("games", [])

        i = 0
        for game in self.data:
            try:
                game_data = requests.get(
                    f"https://store.steampowered.com/api/appdetails?appids={game['appid']}").json()[str(game['appid'])].get('data', {})

                developers = game_data.get('developers', [])
                publishers = game_data.get('publishers', [])
                genres = game_data.get('genres', [])
                try:
                    release_year = game_data.get('release_date', {}).get(
                        'date', '').split(',')[1].strip()
                except Exception as e:
                    release_year = 'unknown'

                for developer in developers:
                    if developer not in self.developers:
                        self.developers[developer] = 1
                    else:
                        self.developers[developer] += 1

                for publisher in publishers:
                    if publisher not in self.publishers:
                        self.publishers[publisher] = 1
                    else:
                        self.publishers[publisher] += 1

                for genre in genres:
                    if genre['description'] not in self.genres:
                        self.genres[genre['description']] = 1
                    else:
                        self.genres[genre['description']] += 1

                if release_year:
                    if release_year not in self.release_years:
                        self.release_years[release_year] = 1
                    else:
                        self.release_years[release_year] += 1
            except Exception as e:
                print(game)
                print(e)
            # i += 1
            # if i > 30:
            #     break

            # @st.cache_data

    def get_steam_games(_self):
        url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={_self.steam_id}&include_appinfo=true&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["response"].get("games", [])
        return []
