import streamlit as st
import matplotlib.pyplot as plt
from visualizers.most_played import MostPlayedGames
from visualizers.profile import Profile
from visualizers.games_by_year import GamesByYear
from data.profile_data import ProfileData
from data.user_games_data import UserGamesData


# Streamlit UI
st.title("Steam Game Analytics Dashboard")
st.write("Enter your Steam ID below to fetch your game statistics.")

# User input for Steam ID
user_steam_id = st.text_input("Enter your SteamID64:", "")

if user_steam_id:
    # Profile
    profile_data = ProfileData(user_steam_id).data
    profile = Profile(profile_data)
    profile.display()

    # Data
    user_games_data = UserGamesData(user_steam_id)

    # Number of Games
    num_games = len(user_games_data.data)
    st.markdown(
        f"<h3 style='text-align: center;'>You own a total of {num_games} games.</h3>", unsafe_allow_html=True)

    # Most Played Games
    most_played_games = MostPlayedGames(user_games_data.data)
    most_played_games.display()

    # Games by Year
    games_by_year = GamesByYear(user_games_data.release_years, num_games)
    games_by_year.display()

else:
    st.write(
        "No game data found for this Steam ID. Make sure your profile is public.")
