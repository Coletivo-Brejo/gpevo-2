import streamlit as st

from entities.racer import Racer
from entities.track import Track
from screens.racer_card import draw as draw_racer
from screens.track_card import draw as draw_track
from utils.proxy import load_all_resources


def load_headers(route: str, fields: list[str]) -> list[dict]:
    dict_list: list[dict]|None = load_all_resources(
        route,
        fields = fields,
    )
    if dict_list is not None:
        return dict_list
    else:
        return []


st.markdown("## Montagem de treinamento")

st.markdown("### Corredor")

allowed_racers: list[dict] = load_headers("/racers", ["racer_id", "name"])
racer_name: str = st.selectbox("Corredor", (r["name"] for r in allowed_racers))
racer_id: str = next((r["racer_id"] for r in allowed_racers if r["name"] == racer_name), "")
racer: Racer|None = Racer.load(racer_id)

if racer is not None:
    draw_racer(racer)

st.markdown("### Mutação")

n_clones: int = st.slider(
    "Quantidade de clones",
    min_value = 5,
    max_value = 20,
    value = 10,
)

cols = st.columns(2)

with cols[0]:
    prob_create_neuron: float = st.slider(
        "Probabilidade de criação de neurônio",
        min_value = 0.,
        max_value = 1.,
        step = .05,
    )
    prob_create_connection: float = st.slider(
        "Probabilidade de criação de conexão",
        min_value = 0.,
        max_value = 1.,
        step = .05,
    )
with cols[1]:
    prob_delete_neuron: float = st.slider(
        "Probabilidade de remoção de neurônio",
        min_value = 0.,
        max_value = 1.,
        step = .05,
    )
    prob_delete_connection: float = st.slider(
        "Probabilidade de remoção de conexão",
        min_value = 0.,
        max_value = 1.,
        step = .05,
    )

limit_layers: bool = st.toggle("Limitar camadas")
max_hidden_layers: int = -1
if limit_layers:
    max_hidden_layers = st.slider(
        "Número máximo de camadas centrais",
        min_value = 0,
        max_value = 10,
        value = 0,
    )

limit_neurons: bool = st.toggle("Limitar neurônios")
max_hidden_neurons: int = -1
if limit_neurons:
    max_hidden_neurons = st.slider(
        "Número máximo de neurônios centrais",
        min_value = 0,
        max_value = 20,
        value = 0,
    )

limit_connections: bool = st.toggle("Limitar conexões")
max_connections: int = -1
if limit_connections:
    max_connections = st.slider(
        "Número máximo de conexões",
        min_value = 0,
        max_value = 100,
        value = 0,
    )

st.markdown("### Pista")

allowed_tracks: list[dict] = load_headers("/tracks", ["track_id", "name"])
track_name: str = st.selectbox("Pista", (t["name"] for t in allowed_tracks))
track_id: str = next((t["track_id"] for t in allowed_tracks if t["name"] == track_name), "")
track: Track|None = Track.load(track_id)

if track is not None:
    draw_track(track)

training_cost: float = 100.
st.sidebar.metric("Orçamento", f"${training_cost:.2f}")