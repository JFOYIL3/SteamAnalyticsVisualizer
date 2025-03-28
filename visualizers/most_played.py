import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from dotenv import load_dotenv
import os
import numpy as np  # Import numpy for rounding

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")


class MostPlayedGames:
    def __init__(_self, games):
        _self.games = games

    def display(_self):
        df = pd.DataFrame(_self.games)
        if not df.empty:
            # Round up to the closest int
            df["playtime_hours"] = np.ceil(df["playtime_forever"] / 60)
            df = df.sort_values(by="playtime_hours",
                                ascending=False)  # Sort by playtime

            # Select top 10 most played games
            top_games = df.nlargest(10, "playtime_hours")

            # Create the bar chart with Plotly
            fig = go.Figure()

            # Add the bars with actual playtime values
            fig.add_trace(go.Bar(
                y=top_games["name"],
                x=top_games["playtime_hours"],  # Use actual playtime values
                orientation="h",
                name="Playtime",
                marker=dict(color='rgba(255, 99, 71, 1)'),
                text=top_games["playtime_hours"],  # Add playtime hours as text
                textposition='inside',  # Position text inside the bars
                textfont=dict(color='white'),  # Set text color to white
                showlegend=False
            ))

            # Update layout for a cleaner look
            fig.update_layout(
                title="Top 10 Most Played Games",
                title_x=0,
                title_y=0.95,
                title_font=dict(size=24, color="white"),
                xaxis_title="Playtime (Hours)",

                xaxis=dict(
                    # Static x-axis range
                    range=[0, top_games["playtime_hours"].max() * 1.1],
                    tickmode='array',
                    tickvals=[i for i in range(
                        0, int(top_games["playtime_hours"].max()) + 50, 50)],
                    side='top',
                    showgrid=True,
                    linecolor='white',
                    tickcolor='white',

                ),
                yaxis_title="",
                yaxis=dict(showticklabels=True, autorange='reversed'),
                plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
                paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
                font=dict(color="white"),
                height=600,  # Increase the height of the chart
                width=800,   # Increase the width of the chart
            )

            # Use container width for better responsiveness
            st.plotly_chart(fig, use_container_width=True)
