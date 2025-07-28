import plotly.graph_objs as go
import streamlit as st

from .track_card import create_track_layout
from entities.training import Training


def create_progress_layout(
        title: str,
        percentage: bool = False
    ) -> dict:
    layout: dict = {
        "title": title,
        "showlegend": False,
        "xaxis": {
            "showgrid": False,
            "zeroline": False,
        },
        "yaxis": {
            "showgrid": False,
            "tickformat": ".0%" if percentage else "",
        },
    }
    return layout

def draw(training: Training) -> None:

    cols = st.columns(len(training.setups))

    for setup_idx, col in enumerate(cols):
        with col:

            progress_evolution_fig: go.Figure = go.Figure(
                data = training.generate_setup_progress_evolution_traces(setup_idx),
                layout = create_progress_layout("Evolução do progresso"),
            )
            st.plotly_chart(progress_evolution_fig, key=f"{setup_idx}_progress_evo")

            time_evolution_fig: go.Figure = go.Figure(
                data = training.generate_setup_time_evolution_traces(setup_idx),
                layout = create_progress_layout("Evolução do tempo para completar"),
            )
            st.plotly_chart(time_evolution_fig, key=f"{setup_idx}_time_evo")

    iterations: int = len(training.run_history)
    it: int = st.slider("Iteração", 0, iterations, key=f"{setup_idx}_it_slider")

    cols = st.columns(len(training.setups))

    for setup_idx, col in enumerate(cols):
        with col:

            race_fig: go.Figure = go.Figure(
                data = training.generate_history_traces(setup_idx, it),
                layout = create_track_layout(),
            )
            st.plotly_chart(race_fig, key=f"{setup_idx}_run_history")

            progress_fig: go.Figure = go.Figure(
                data = training.generate_progress_traces(setup_idx, it),
                layout = create_progress_layout("Progresso"),
            )
            st.plotly_chart(progress_fig, key=f"{setup_idx}_run_progress")