import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")


class Profile:
    def __init__(_self, data):
        _self.data = data

    def display(_self):
        df = pd.DataFrame(_self.data)
        if not df.empty:
            avatar_url = df['avatarfull'].iloc[0] if 'avatarfull' in df.columns else ""
            personaname = df['personaname'].iloc[0] if 'personaname' in df.columns else "Unknown"
            created_time = pd.to_datetime(df['timecreated'].iloc[0], unit='s').strftime(
                '%Y-%m-%d %H:%M:%S') if 'timecreated' in df.columns else "Unknown"

            personastate = df['personastate'].iloc[0] if 'personastate' in df.columns else "Unknown"
            lastlogoff = pd.to_datetime(df['lastlogoff'].iloc[0], unit='s').strftime(
                '%Y-%m-%d %H:%M:%S') if 'lastlogoff' in df.columns else "Unknown"

            profile_url = df['profileurl'].iloc[0] if 'profileurl' in df.columns else ""

            # Construct the card layout with pure HTML & CSS
            st.markdown(f"""
                <style>
                    .profile-card {{
                        border: 2px solid #ccc;
                        border-radius: 10px;
                        padding: 20px;
                        background-color: #1E1E1E;
                        text-align: center;
                        box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.2);
                        max-width: 400px;
                        margin: auto;
                        color: white;
                        font-family: Arial, sans-serif;
                        margin-bottom: 50px; /* Added margin to the bottom */
                    }}
                    .profile-avatar {{
                        border-radius: 50%;
                        width: 100px;
                        height: 100px;
                        object-fit: cover;
                        margin-bottom: 10px;
                    }}
                    .profile-name {{
                        font-size: 24px;
                        font-weight: bold;
                        margin: 5px 0;
                    }}
                    .profile-info {{
                        font-size: 16px;
                        margin-top: 5px;
                        opacity: 0.8;
                    }}
                </style>
                <div class="profile-card">
                    <img src="{avatar_url}" class="profile-avatar">
                    <div class="profile-name">{personaname}</div>
                    <div class="profile-info">Account Created: {created_time}</div>
                    <div class="profile-info"><span style="color: { 'green' if personastate == 1 else 'grey' }; font-weight: bold;">●</span> { 'Online' if personastate == 1 else 'Offline' }</div>
                    <div class="profile-info" style="display: { 'block' if personastate == 0 else 'none' };">Last Online: {lastlogoff}</div>
                    <div class="profile-info"><a href="{profile_url}" style="color: lightblue; text-decoration: none;">Link to Profile</a></div>
                </div>
            """, unsafe_allow_html=True)
