import streamlit as st

from .brain_card import draw as draw_brain
from entities.racer import Racer


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

def draw(racer: Racer) -> None:

    st.write(f"### {racer.name}")
    draw_brain(racer.brain)