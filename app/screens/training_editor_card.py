import streamlit as st

from entities.brain import MutationSetup
from entities.racer import Racer
from entities.run import RunSetup
from entities.track import Track
from entities.training import TrainingEntry, TrainingRunSetup, TrainingSetup
from screens.racer_card import draw as draw_racer
from screens.track_card import draw as draw_track
from utils.proxy import load_all_resources, post


def load_headers(route: str, fields: list[str]) -> list[dict]:
    dict_list: list[dict]|None = load_all_resources(
        route,
        fields = fields,
    )
    if dict_list is not None:
        return dict_list
    else:
        return []

def create_training(
        racer_id: str,
        track_id: str,
        mirrored: bool,
        reflective: bool,
        stuck_timeout: float,
        run_timeout: float,
        laps: int,
        initial_temperature: float,
        cooling_rate: float,
        n_iterations: int,
        greedy: bool,
        n_clones: int,
        prob_create_neuron: float,
        prob_delete_neuron: float,
        prob_create_connection: float,
        prob_delete_connection: float,
        max_hidden_layers: int,
        max_hidden_neurons: int,
        max_connections: int,
    ) -> None:
    run_setups: list[TrainingRunSetup] = []
    run_setups.append(
        TrainingRunSetup(
            track_id,
            RunSetup(
                0., 0., stuck_timeout, run_timeout, True, True, 1., mirrored, laps,
            )
        )
    )
    if reflective:
        run_setups.insert(
            0 if mirrored else 1,
            TrainingRunSetup(
                track_id,
                RunSetup(
                    0., 0., stuck_timeout, run_timeout, True, True, 1., not mirrored, laps,
                )
            )
        )
    mutation_setup: MutationSetup = MutationSetup(
        n_clones,
        prob_create_neuron,
        prob_delete_neuron,
        prob_create_connection,
        prob_delete_connection,
        max_hidden_layers,
        max_hidden_neurons,
        max_connections,
    )
    setup: TrainingSetup = TrainingSetup(
        racer_id,
        run_setups,
        True,
        initial_temperature,
        cooling_rate,
        0.,
        0,
        n_iterations,
        0.,
        0.,
        0.,
        greedy,
        mutation_setup,
    )
    post("/trainings/new", setup.to_dict())

def draw() -> None:

    st.markdown("## Montagem de treinamento")
    st.markdown("### Geral")

    n_iterations: int = st.slider(
        "Iterações",
        min_value = 10,
        max_value = 100,
        value = 20,
    )

    initial_temperature: float = st.slider(
        "Temperatura inicial",
        min_value = 50.,
        max_value = 100.,
        value = 100.,
    )

    cooling_rate: float = st.slider(
        "Taxa de resfriamento",
        min_value = .01,
        max_value = .2,
        value = .1,
    )

    greedy: bool = st.checkbox("Otimização gulosa", True)

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

        reflective: bool = st.checkbox(
            "Treino refletido",
            help = "Realiza o treino na pista normal e espelhada ao mesmo tmepo")
        
        laps: int = 1
        if track.loops:
            laps = st.slider(
                "Número de voltas",
                min_value = 1,
                max_value = 5,
                value = 1,
            )
        
        stuck_timeout: float = st.slider(
            "Tolerância de tempo parado",
            min_value = 1.,
            max_value = 10.,
            value = 5.,
        )

        limit_run_time: bool = st.toggle("Limitar tempo de corrida", True)
        run_timeout: float = 0.
        if limit_run_time:
            run_timeout = st.slider(
                "Tempo máximo de corrida",
                min_value = 30.,
                max_value = 180.,
                value = 60.,
            )
    
    if st.button("Criar"):
        create_training(
            racer_id,
            track_id,
            st.session_state["track_mirrored_toggle"],
            reflective,
            stuck_timeout,
            run_timeout,
            laps,
            initial_temperature,
            cooling_rate,
            n_iterations,
            greedy,
            n_clones,
            prob_create_neuron,
            prob_delete_neuron,
            prob_create_connection,
            prob_delete_connection,
            max_hidden_layers,
            max_hidden_neurons,
            max_connections
        )
        st.rerun()