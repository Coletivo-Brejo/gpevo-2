import streamlit as st

from entities.racer import Racer
from entities.track import Track
from entities.training import Training
from screens.racer_card import draw as draw_racer
from screens.track_card import draw as draw_track
from screens.training_card import draw as draw_training
from utils.proxy import load_all_resources


def load_racers() -> list[Racer]:
    racers: list[Racer] = []
    dict_list: list[dict]|None = load_all_resources("/racers")
    if dict_list is not None:
        for d in dict_list:
            racer: Racer = Racer.from_dict(d)
            if racer is not None:
                racers.append(racer)
    return racers

def load_tracks() -> list[Track]:
    tracks: list[Track] = []
    dict_list: list[dict]|None = load_all_resources("/tracks")
    if dict_list is not None:
        for d in dict_list:
            track: Track = Track.from_dict(d)
            if track is not None:
                tracks.append(track)
    return tracks

def load_trainings() -> list[Training]:
    trainings: list[Training] = []
    dict_list: list[dict]|None = load_all_resources("/trainings")
    if dict_list is not None:
        for d in dict_list:
            training: Training = Training.from_dict(d)
            if training is not None:
                trainings.append(training)
    return trainings

st.markdown("## Corredores")

racers: list[Racer] = load_racers()
for r in racers:
    with st.expander(f"{r.name}"):
        draw_racer(r)

st.markdown("## Pistas")

tracks: list[Track] = load_tracks()

track_name: str|None = st.selectbox("Nome da pista", [t.name for t in tracks])
selected_track: Track|None = next((t for t in tracks if t.name == track_name), None)

if selected_track is not None:
    draw_track(selected_track)

st.markdown("## Treinos")

trainings: list[Training] = load_trainings()
training_id: str|None = st.selectbox("Treino", [t.training_id for t in trainings])
training: Training|None = next((t for t in trainings if t.training_id == training_id), None)

if training is not None:
    draw_training(training)