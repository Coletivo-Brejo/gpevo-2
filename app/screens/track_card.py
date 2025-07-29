import plotly.graph_objs as go
import streamlit as st

from entities.track import Track


def create_track_layout() -> dict:
    layout: dict = {
        "height": 800.,
        "width": 800.,
        "showlegend": False,
        "xaxis": {
            "showticklabels": False,
            "showgrid": False,
            "zeroline": False,
        },
        "yaxis": {
            "autorange": "reversed",
            "showticklabels": False,
            "showgrid": False,
            "zeroline": False,
            "scaleanchor": "x",
            "scaleratio": 1.,
        },
    }
    return layout

def draw(track: Track) -> None:
    st.write(f"### {track.name}")
    mirrored: bool = st.toggle(
        "Espelhar",
        key = "track_mirrored_toggle",
    )
    traces: list[dict] = track.generate_traces(mirrored)
    layout: dict = create_track_layout()
    fig: go.Figure = go.Figure(
        data = traces,
        layout = layout
    )
    st.plotly_chart(fig)