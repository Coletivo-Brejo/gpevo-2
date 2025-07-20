from dotenv import load_dotenv
import streamlit as st
import os
import plotly.graph_objs as go
import requests

from entities.track import Track
from entities.training import Training


load_dotenv()
API_URL = os.environ.get("API_URL")
DATA_PATH = os.environ.get("DATA_PATH")

def request_tracks() -> list[Track]:
    response = requests.get(f"{API_URL}/tracks")
    tracks: list[Track] = []
    if response.ok:
        track_list: list[dict] = response.json()
        for t in track_list:
            tracks.append(Track.from_dict(t))
    return tracks

def request_trainings() -> list[Training]:
    response = requests.get(f"{API_URL}/trainings")
    trainings: list[Training] = []
    if response.ok:
        training_list: list[dict] = response.json()
        for t in training_list:
            trainings.append(Training.from_dict(t))
    return trainings

def create_track_plot(track: Track) -> go.Figure:
    traces: list[dict] = track.generate_traces()
    layout: dict = create_track_layout()
    return go.Figure(data = traces, layout = layout)

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

def create_progress_layout(percentage: bool = False) -> dict:
    layout: dict = {
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


st.title("Teste")

if not st.user.is_logged_in:
    st.button("Log in with Google", on_click=st.login)
    st.stop()

st.button("Log out", on_click=st.logout)
st.markdown(f"Welcome! {st.user.name}")
st.write(st.user)


st.markdown("## Pistas")

tracks: list[Track] = request_tracks()

track_name: str|None = st.selectbox("Nome da pista", [t.name for t in tracks])
selected_track: Track|None = next((t for t in tracks if t.name == track_name), None)

if selected_track is not None:
    st.plotly_chart(create_track_plot(selected_track))

st.markdown("## Treinos")

trainings: list[Training] = request_trainings()
training_id: str|None = st.selectbox("Treino", [t.training_id for t in trainings])
training: Training|None = next((t for t in trainings if t.training_id == training_id), None)

if training is not None:

    evolution_fig: go.Figure = go.Figure(
        data = training.generate_progress_evolution_traces(),
        layout = create_progress_layout(),
    )
    st.plotly_chart(evolution_fig)

    iterations: int = len(training.racer_history)
    it: int = st.slider("Iteração", 0, iterations-1)

    progress_fig: go.Figure = go.Figure(
        data = training.generate_progress_traces(it),
        layout = create_progress_layout(),
    )
    st.plotly_chart(progress_fig)

    race_fig: go.Figure = go.Figure(
        data = training.generate_history_traces(it),
        layout = create_track_layout(),
    )
    st.plotly_chart(race_fig)

# st.markdown("## Runs")

# runs: list[dict] = []
# run_endpoint: str = f"{API_URL}/runs"
# response = requests.get(run_endpoint)
# if response.ok:
#     runs = response.json()

# racers: list[dict] = []
# racer_endpoint: str = f"{API_URL}/racers"
# response = requests.get(racer_endpoint)
# if response.ok:
#     racers = response.json()

# run_id: str|None = st.selectbox("Run", [r["run_id"] for r in runs])
# selected_run: dict|None = next((r for r in runs if r["run_id"] == run_id), None)

# if selected_run is not None:
#     track: dict = next((t for t in tracks if t["track_id"] == selected_run["track_id"]))
#     racer_id: str = st.selectbox("Corredor", selected_run["racer_ids"])
#     stats: dict = next((s for s in selected_run["stats"] if s["racer_id"] == racer_id))

#     percent_progress: bool = st.checkbox("Porcentagem")
#     progress: list[float] = stats["progress_history"]
#     if percent_progress:
#         progress = [p/track["length"]/selected_run["laps"] for p in progress]

#     traces: list[dict] = [
#         {
#             "type": "scatter",
#             "mode": "lines",
#             "x": stats["time_history"],
#             "y": progress,
#         }
#     ]
#     layout: dict = {
#         "showlegend": False,
#         "xaxis": {
#             "showgrid": False,
#             "zeroline": False,
#         },
#         "yaxis": {
#             "showgrid": False,
#             "tickformat": ".0%" if percent_progress else "",
#         },
#     }
#     st.plotly_chart(
#         go.Figure(data=traces, layout=layout),
#         use_container_width = True,
#     )

#     x_scale: float = 1.
#     if selected_run["mirrored"]:
#         x_scale = -1.
#     l_xs: list[float] = [p["x"]*x_scale for p in track["l_wall"]]
#     l_ys: list[float] = [p["y"] for p in track["l_wall"]]
#     r_xs: list[float] = [p["x"]*x_scale for p in track["r_wall"]]
#     r_ys: list[float] = [p["y"] for p in track["r_wall"]]
#     history_xs: list[float] = [p["x"] for p in stats["position_history"]]
#     history_ys: list[float] = [p["y"] for p in stats["position_history"]]
#     traces: list[dict] = [
#         {
#             "type": "scatter",
#             "mode": "lines",
#             "x": l_xs,
#             "y": l_ys,
#             "line": {
#                 "color": "grey",
#             },
#         },
#         {
#             "type": "scatter",
#             "mode": "lines",
#             "x": r_xs,
#             "y": r_ys,
#             "line": {
#                 "color": "grey",
#             },
#         },
#         {
#             "type": "scatter",
#             "mode": "lines",
#             "x": [l_xs[0], r_xs[0]],
#             "y": [l_ys[0], r_ys[0]],
#             "line": {
#                 "color": "grey",
#             },
#         },
#         {
#             "type": "scatter",
#             "mode": "lines",
#             "x": [l_xs[-1], r_xs[-1]],
#             "y": [l_ys[-1], r_ys[-1]],
#             "line": {
#                 "color": "grey",
#             },
#         },
#         {
#             "type": "scatter",
#             "mode": "markers",
#             "x": history_xs,
#             "y": history_ys,
#             "marker": {
#                 "opacity": .5,
#             },
#         }
#     ]
#     layout: dict = {
#         "height": 800.,
#         "width": 800.,
#         "showlegend": False,
#         "xaxis": {
#             "showticklabels": False,
#             "showgrid": False,
#             "zeroline": False,
#         },
#         "yaxis": {
#             "autorange": "reversed",
#             "showticklabels": False,
#             "showgrid": False,
#             "zeroline": False,
#             "scaleanchor": "x",
#             "scaleratio": 1.,
#         },
#     }
#     st.plotly_chart(
#         go.Figure(data=traces, layout=layout),
#         use_container_width = True,
#     )