import streamlit as st
import streamlit.components.v1 as components
from typing import TypedDict

from entities.training import TrainingEntry
from screens.training_editor_card import draw as draw_editor
from utils.proxy import load_all_resources, load_resource_dict


class TrainingInfo(TypedDict):
    training_id: str
    racer_id: str
    racer_name: str
    track_id: str
    track_name: str
    iteration: int
    n_iterations: int

def load_entries() -> list[TrainingEntry]:
    entries: list[TrainingEntry] = []
    entries_dict: list[dict]|None = load_all_resources("/trainings/entries")
    if entries_dict is not None:
        for d in entries_dict:
            entries.append(TrainingEntry.from_dict(d))
    return entries

def load_training_info(training_id: str) -> TrainingInfo:
    racer_id: str = ""
    racer_name: str = ""
    track_id: str = ""
    track_name: str = ""
    iteration: int = 0
    n_iterations: int = 0
    training: dict|None = load_resource_dict("/trainings", training_id, ["setup", "iteration"])
    if training is not None:
        setup: dict = training["setup"]
        racer_id = setup["racer_id"]
        racer: dict|None = load_resource_dict("/racers", racer_id, ["name"])
        if racer is not None:
            racer_name = racer["name"]
        track_id = setup["setups"][0]["track_id"]
        track: dict|None = load_resource_dict("/tracks", track_id, ["name"])
        if track is not None:
            track_name = track["name"]
        iteration = training["iteration"]
        n_iterations = setup["n_iterations"]
    info: TrainingInfo = TrainingInfo(
        training_id = training_id,
        racer_id = racer_id,
        racer_name = racer_name,
        track_id = track_id,
        track_name = track_name,
        iteration = iteration,
        n_iterations = n_iterations,
        )
    return info

def draw_entry_list_header() -> None:
    (
        dt_col, status_col, iteration_col, finished_col,
        racer_col, track_col, bt_col, results_col
    ) = st.columns([1, 1, 1, 1, 1, 1, 1, 1])
    with dt_col:
        st.markdown("**Criado em**")
    with status_col:
        st.markdown("**Status**")
    with iteration_col:
        st.markdown("**Iteração**")
    with finished_col:
        st.markdown("**Concluído em**")
    with racer_col:
        st.markdown("**Corredor**")
    with track_col:
        st.markdown("**Pista**")

def draw_entry_line(entry: TrainingEntry) -> None:
    info: TrainingInfo = load_training_info(entry.training_id)
    (
        dt_col, status_col, iteration_col, finished_col,
        racer_col, track_col, bt_col, results_col
    ) = st.columns([1, 1, 1, 1, 1, 1, 1, 1])
    with dt_col:
        st.write(entry.created_at.strftime("%Y-%m-%d"))
    with status_col:
        st.write(entry.status)
    with iteration_col:
        st.write(f"{info['iteration']}/{info['n_iterations']}")
    with finished_col:
        if entry.finished_at is not None:
            st.write(entry.finished_at.strftime("%Y-%m-%d"))
    with racer_col:
        st.write(info["racer_name"])
    with track_col:
        st.write(info["track_name"])
    with bt_col:
        if entry.status in {"created", "running"}:
            if st.button("Executar", key = f"run_bt_{entry.training_id}"):
                run_training({
                    "mode": "training",
                    "training_id": entry.training_id,
                })
    with results_col:
        if entry.status in {"running", "finished", "interrupted"}:
            if st.button("Resultados", key = f"results_bt_{entry.training_id}"):
                pass

@st.dialog("Novo treinamento", width = "large")
def draw_new_training_dialog() -> None:
    draw_editor()

@st.dialog("Treinamento", width="large")
def run_training(params: dict = {}) -> None:
    query_string: str = "&".join([f"{k}={v}" for k, v in params.items()])
    game_url: str = f"http://localhost:5000?{query_string}"
    components.html(
        f"""
        <iframe src="{game_url}"
            width="100%" height="600px"
            frameborder="0"
            allowfullscreen>
        </iframe>
        """,
        height=500,
        scrolling=False,
    )
    if st.button("Fechar e atualizar"):
        st.rerun()

st.write("## Treinamentos")

if st.button("Novo treinamento"):
    draw_new_training_dialog()

entries: list[TrainingEntry] = load_entries()
if len(entries) > 0:
    draw_entry_list_header()
    for e in entries:
        draw_entry_line(e)
else:
    st.write("Nenhum treinamento registrado")