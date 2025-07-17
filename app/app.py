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


st.markdown("## Pistas")

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


st.markdown("## Runs")

runs: list[dict] = []
run_endpoint: str = f"{API_URL}/runs"
response = requests.get(run_endpoint)
if response.ok:
    runs = response.json()

racers: list[dict] = []
racer_endpoint: str = f"{API_URL}/racers"
response = requests.get(racer_endpoint)
if response.ok:
    racers = response.json()

run_id: str|None = st.selectbox("Run", [r["run_id"] for r in runs])
selected_run: dict|None = next((r for r in runs if r["run_id"] == run_id), None)

if selected_run is not None:
    track: dict = next((t for t in tracks if t["track_id"] == selected_run["track_id"]))
    racer_id: str = st.selectbox("Corredor", selected_run["racer_ids"])
    stats: dict = next((s for s in selected_run["stats"] if s["racer_id"] == racer_id))

    percent_progress: bool = st.checkbox("Porcentagem")
    progress: list[float] = stats["progress_history"]
    if percent_progress:
        progress = [p/track["length"]/selected_run["laps"] for p in progress]

    traces: list[dict] = [
        {
            "type": "scatter",
            "mode": "lines",
            "x": stats["time_history"],
            "y": progress,
        }
    ]
    layout: dict = {
        "showlegend": False,
        "xaxis": {
            "showgrid": False,
            "zeroline": False,
        },
        "yaxis": {
            "showgrid": False,
            "tickformat": ".0%" if percent_progress else "",
        },
    }
    st.plotly_chart(
        go.Figure(data=traces, layout=layout),
        use_container_width = True,
    )

    x_scale: float = 1.
    if selected_run["mirrored"]:
        x_scale = -1.
    l_xs: list[float] = [p["x"]*x_scale for p in track["l_wall"]]
    l_ys: list[float] = [p["y"] for p in track["l_wall"]]
    r_xs: list[float] = [p["x"]*x_scale for p in track["r_wall"]]
    r_ys: list[float] = [p["y"] for p in track["r_wall"]]
    history_xs: list[float] = [p["x"] for p in stats["position_history"]]
    history_ys: list[float] = [p["y"] for p in stats["position_history"]]
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
        },
        {
            "type": "scatter",
            "mode": "lines",
            "x": [l_xs[0], r_xs[0]],
            "y": [l_ys[0], r_ys[0]],
            "line": {
                "color": "grey",
            },
        },
        {
            "type": "scatter",
            "mode": "lines",
            "x": [l_xs[-1], r_xs[-1]],
            "y": [l_ys[-1], r_ys[-1]],
            "line": {
                "color": "grey",
            },
        },
        {
            "type": "scatter",
            "mode": "markers",
            "x": history_xs,
            "y": history_ys,
            "marker": {
                "opacity": .5,
            },
        }
    ]
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
    st.plotly_chart(
        go.Figure(data=traces, layout=layout),
        use_container_width = True,
    )