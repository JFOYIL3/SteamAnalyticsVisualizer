import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from dotenv import load_dotenv
import os
import numpy as np  # Import numpy for rounding

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")


class GamesByYear:
    def __init__(_self, data, num_games):
        _self.data = data
        _self.num_games = num_games

    def display(_self):
        # Convert the dictionary into a Pandas Series
        years_count = pd.Series(_self.data)

        # Ensure index is integer (convert string years to integers) except for 'unknown'
        years_count = years_count.drop('unknown', errors='ignore')
        years_count.index = years_count.index.astype(int)

        # Determine the decade for each year
        # Get decade start year (e.g., 2006 → 2000)
        decades = (years_count.index // 10) * 10

        # Create decade labels like "2000s"
        decade_labels = [f"{decade}s" for decade in decades]

        # Group by decade and sum the values
        decade_counts = years_count.groupby(decade_labels).sum()

        # Create two columns (70% for the chart, 30% for text)
        col1, col2 = st.columns([0.7, 0.3])

        # Display chart in the left column
        with col1:
            fig = go.Figure(
                data=[go.Bar(x=decade_counts.index, y=decade_counts.values,
                             text=decade_counts.values, textposition='inside', textfont=dict(color='white'))]
            )
            fig.update_layout(title='Number of Games Played by Decade',
                              title_x=0,
                              title_y=0.95,
                              title_font=dict(size=24, color="white"),
                              xaxis_title='Decade', yaxis_title='Number of Games')
            st.plotly_chart(fig)

        # Display text in the right column
        with col2:
            st.markdown("### Insights")
            if 'unknown' in _self.data:
                year_with_most_games = max(
                    (year for year in _self.data if year != 'unknown'), key=_self.data.get)
            else:
                year_with_most_games = max(_self.data, key=_self.data.get)
            count_of_most_games = _self.data[year_with_most_games]
            ommited_games = _self.data['unknown'] if 'unknown' in _self.data else None
            st.markdown(
                f"""
                <span style='font-size: 40px; font-weight: bold; color: #FFD700; font-style: italic;'>{year_with_most_games}</span>
                <p style='font-size: 20px; '>was the year with the most games, with a count of: <span style='font-size: 20px; color: #FFD700;'>{count_of_most_games} </span>games</p>
                """, unsafe_allow_html=True)

        if ommited_games:
            st.write(
                f"Ommited {ommited_games} games with unknown release dates.")
