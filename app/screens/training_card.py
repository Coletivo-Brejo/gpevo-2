import plotly.graph_objs as go
import streamlit as st

from .run_card import draw as draw_run
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
    
    progress_evolution_fig: go.Figure = go.Figure(
        data = training.generate_progress_evolution_traces(),
        layout = create_progress_layout("Evolução do progresso"),
    )
    st.plotly_chart(progress_evolution_fig)

    time_evolution_fig: go.Figure = go.Figure(
        data = training.generate_time_evolution_traces(),
        layout = create_progress_layout("Evolução do tempo para completar"),
    )
    st.plotly_chart(time_evolution_fig)

    iterations: int = len(training.racer_history)
    it: int = st.slider("Iteração", 0, iterations-1)

    draw_run(training.racer_history[it], training.run_data.mirrored)

    progress_fig: go.Figure = go.Figure(
        data = training.generate_progress_traces(it),
        layout = create_progress_layout("Progresso"),
    )
    st.plotly_chart(progress_fig)