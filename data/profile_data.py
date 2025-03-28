import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")


class ProfileData:
    def __init__(self, steam_id):
        self.steam_id = steam_id
        self.data = self.get_profile_info()

    def get_profile_info(_self):
        url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={_self.steam_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["response"].get("players", [])
        return []
