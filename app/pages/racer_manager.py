import streamlit as st

from entities.racer import Racer
from entities.training import TrainingInfo
from screens.leaderboard import draw as draw_leaderboard
from screens.racer_card import draw as draw_racer
from screens.training_editor import draw as draw_training_editor
from screens.training_list import draw as draw_info_list
from utils.proxy import get, load_all_resources, load_headers


@st.dialog("Tem certeza?")
def show_lobotomy_warning(
        racer_id: str,
        neurons: list[str] = [],
    ) -> None:
    if len(neurons) == 0:
        st.warning("""
            Essa ação irá desconectar todos os neurônios e é irreversível.
            Treinamentos em andamento para esse corredor serão interrompidos.
        """)
    else:
        st.warning(f"""
            Essa ação irá desconectar os neurônios {', '.join(n for n in neurons)} e é irreversível.
            Treinamentos em andamento para esse corredor serão interrompidos.
        """)
    if st.button("Sim, realizar lobotomia"):
        params: dict = {}
        if len(neurons) > 0:
            params["neurons"] = neurons
        get(f"/racers/{racer_id}/lobotomize", params)
        st.rerun()

def load_racer_labels() -> list[str]:
    racer_labels: list[str] = []
    dict_list: list[dict]|None = load_all_resources(
        "/racers",
        fields = ["racer_id", "name"],
    )
    if dict_list is not None:
        for d in dict_list:
            racer_labels.append(f"{d['racer_id']} - {d['name']}")
    return racer_labels

racer_labels: list[str] = load_racer_labels()
racer_label: str = st.selectbox("Corredor", racer_labels)
racer_id: str = racer_label.split(" - ")[0]
racer: Racer|None = Racer.load(racer_id)

if racer is not None:
    draw_racer(racer)

    lobotomy_enabled: bool = st.toggle("Medidas drásticas")
    if lobotomy_enabled:
        with st.form("lobotomy_form"):
            neurons_to_delete: list[str] = st.multiselect(
                "Neurônios a remover",
                [n.neuron_id for n in racer.brain.neurons if n.neuron_id.startswith("n")],
                default = [],
            )
            connections_to_remove: list[str] = st.multiselect(
                "Neurônios a desconectar",
                [n.neuron_id for n in racer.brain.neurons if n.neuron_id.startswith("t")],
                default = [],
            )
            if st.form_submit_button("Realizar lobotomia parcial"):
                neurons: list[str] = neurons_to_delete+connections_to_remove
                if len(neurons) > 0:
                    show_lobotomy_warning(racer_id, neurons)
        if st.button("Realizar lobotomia completa"):
            show_lobotomy_warning(racer_id)
    
    st.markdown("## Resultados")
    allowed_tracks: list[dict] = load_headers("/tracks", ["track_id", "name"])
    track_name: str = st.selectbox("Pista", (t["name"] for t in allowed_tracks), key = "racer_manager_track_picker")
    track_id: str = next((t["track_id"] for t in allowed_tracks if t["name"] == track_name), "")
    if track_id != "":
        draw_leaderboard(track_id)

    st.markdown("## Treinos")
    draw_training_editor(racer_id)
    infos_dict: dict|list|None = get("/trainings/info", {"racer_ids":[racer_id]})
    if infos_dict is not None:
        infos: list[TrainingInfo] = [TrainingInfo.from_dict(d) for d in infos_dict]
        draw_info_list(infos, ["created_at", "track", "status", "iteration", "laps", "progress", "run_bt", "results_bt"])