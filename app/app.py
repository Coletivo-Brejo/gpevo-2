from dotenv import load_dotenv
import streamlit as st
import os
import plotly.graph_objs as go
import requests


load_dotenv()
API_URL = os.environ.get("API_URL")
DATA_PATH = os.environ.get("DATA_PATH")

st.title("Teste")

if not st.user.is_logged_in:
    st.button("Log in with Google", on_click=st.login)
    st.stop()

st.button("Log out", on_click=st.logout)
st.markdown(f"Welcome! {st.user.name}")
st.write(st.user)

tracks: list[dict] = []
track_endpoint: str = f"{API_URL}/tracks"
response = requests.get(track_endpoint)
if response.ok:
    tracks = response.json()

track_name: str|None = st.selectbox("Nome da pista", [t["name"] for t in tracks])
selected_track: dict|None = next((t for t in tracks if t["name"] == track_name), None)

if selected_track is not None:
    l_xs: list[float] = [p["x"] for p in selected_track["l_wall"]]
    l_ys: list[float] = [p["y"] for p in selected_track["l_wall"]]
    r_xs: list[float] = [p["x"] for p in selected_track["r_wall"]]
    r_ys: list[float] = [p["y"] for p in selected_track["r_wall"]]
    traces: list[dict] = [
        {
            "type": "scatter",
            "mode": "lines",
            "x": l_xs,
            "y": l_ys,
            "line": {
                "color": "grey",
            },
        },
        {
            "type": "scatter",
            "mode": "lines",
            "x": r_xs,
            "y": r_ys,
            "line": {
                "color": "grey",
            },
        }
    ]
    layout: dict = {
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
        },
    }
    st.plotly_chart(go.Figure(data=traces, layout=layout))