import streamlit as st
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
    training: dict|None = load_resource_dict("/trainings", training_id, ["setup"])
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
    info: TrainingInfo = TrainingInfo(
        training_id = training_id,
        racer_id = racer_id,
        racer_name = racer_name,
        track_id = track_id,
        track_name = track_name,
        )
    return info

def draw_entry_list_header() -> None:
    dt_col, status_col, racer_col, track_col, bt_col = st.columns([1, 1, 1, 1, 1])
    with dt_col:
        st.write("Criado em")
    with status_col:
        st.write("Status")
    with racer_col:
        st.write("Corredor")
    with track_col:
        st.write("Pista")

def draw_entry_line(entry: TrainingEntry) -> None:
    info: TrainingInfo = load_training_info(entry.training_id)
    dt_col, status_col, racer_col, track_col, bt_col = st.columns([1, 1, 1, 1, 1])
    with dt_col:
        st.write(entry.created_at.strftime("%Y-%m-%d"))
    with status_col:
        st.write(entry.status)
    with racer_col:
        st.write(info["racer_name"])
    with track_col:
        st.write(info["track_name"])
    with bt_col:
        st.button("Teste", key = f"run_bt_{entry.training_id}")

@st.dialog("Novo treinamento", width = "large")
def draw_new_training_dialog() -> None:
    draw_editor()

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