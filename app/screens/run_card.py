import plotly.graph_objs as go
import streamlit as st

from .track_card import create_track_layout
from entities.run import RunStats


def draw(stats: RunStats, mirrored: bool = False) -> None:
    race_fig: go.Figure = go.Figure(
        data = stats.generate_history_traces(mirrored),
        layout = create_track_layout(),
    )
    st.plotly_chart(race_fig)