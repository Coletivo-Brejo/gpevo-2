import plotly.graph_objs as go
import streamlit as st

from .brain_card import draw as draw_brain
from .track_card import create_track_layout
from entities.brain import Brain
from entities.training import Training


def create_progress_layout(
        title: str,
        percentage: bool = False,
        show_legend: bool = False,
        xaxis_title: str = "Iteração",
    ) -> dict:
    layout: dict = {
        "title": title,
        "showlegend": show_legend,
        "legend_orientation": "h",
        "xaxis": {
            "title": xaxis_title,
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

    progress_traces: list[dict] = []
    time_traces: list[dict] = []
    for i in range(len(training.setup.setups)):
        progress_traces.extend(training.generate_setup_progress_evolution_traces(i))
        time_traces.extend(training.generate_setup_time_evolution_traces(i))

    progress_evolution_fig: go.Figure = go.Figure(
        data = progress_traces,
        layout = create_progress_layout("Evolução do progresso", show_legend=True),
    )
    st.plotly_chart(progress_evolution_fig)

    time_evolution_fig: go.Figure = go.Figure(
        data = time_traces,
        layout = create_progress_layout("Evolução do tempo para completar", show_legend=True),
    )
    st.plotly_chart(time_evolution_fig)

    iterations: int = len(training.run_history)
    it: int = st.slider("Iteração", 0, iterations)

    brain: Brain = training.brain_history[it]
    draw_brain(brain)

    cols = st.columns(len(training.setup.setups))

    for setup_idx, col in enumerate(cols):
        with col:

            race_fig: go.Figure = go.Figure(
                data = training.generate_history_traces(setup_idx, it),
                layout = create_track_layout(),
            )
            st.plotly_chart(race_fig, key=f"{setup_idx}_run_history")

            progress_fig: go.Figure = go.Figure(
                data = training.generate_progress_traces(setup_idx, it),
                layout = create_progress_layout("Progresso", xaxis_title = "Tempo"),
            )
            st.plotly_chart(progress_fig, key=f"{setup_idx}_run_progress")

            eeg_fig: go.Figure = go.Figure(
                data = training.generate_eeg_traces(setup_idx, it),
                layout = create_progress_layout(
                    "Ativação neuronal",
                    show_legend = True,
                    xaxis_title = "Tempo"),
            )
            st.plotly_chart(eeg_fig, key=f"{setup_idx}_run_eeg")