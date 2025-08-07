import plotly.graph_objs as go
import streamlit as st

from entities.brain import Brain


def create_brain_layout(annotations: list[dict]) -> dict:
    layout: dict = {
        "title": "Cérebro",
        "showlegend": False,
        "xaxis": {
            "autorange": "reversed",
            "showticklabels": False,
            "showgrid": False,
            "zeroline": False,
        },
        "yaxis": {
            "showticklabels": False,
            "showgrid": False,
            "zeroline": False,
        },
        "annotations": annotations,
    }
    return layout

def draw(
        brain: Brain,
        plot_key: str|None = None,
    ) -> None:
    traces, annotations = brain.generate_traces_and_annotations()
    layout = create_brain_layout(annotations)
    brain_fig: go.Figure = go.Figure(
        data = traces,
        layout = layout,
    )
    st.plotly_chart(brain_fig, key = plot_key)