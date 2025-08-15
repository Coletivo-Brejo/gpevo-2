import streamlit as st
import streamlit.components.v1 as components
from typing import TypedDict

from entities.training import Training, TrainingInfo
from screens.training_card import draw as draw_training


@st.dialog("Treinamento", width = "large")
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

@st.dialog("Resultado", width = "large")
def show_results(training_id: str) -> None:
    training: Training|None = Training.load(training_id)
    if training is not None:
        draw_training(training)

class Field(TypedDict):
    text: str
    size: int

status_translation: dict = {
    "created": "Criado",
    "deprecated": "Depreciado",
    "interrupted": "Interrompido",
    "running": "Em execução",
    "finished": "Concluído",
}

def draw_field(info: TrainingInfo, field: str) -> None:
    if field == "created_at":
        st.markdown(info.entry.created_at.strftime("%Y-%m-%d"))
    elif field == "finished_at":
        if info.entry.finished_at is not None:
            st.markdown(info.entry.finished_at.strftime("%Y-%m-%d"))
    elif field == "status":
        st.markdown(status_translation[info.entry.status])
    elif field == "iteration":
        st.markdown(f"{info.iteration+1}/{info.n_iterations}")
    elif field == "laps":
        st.markdown(info.laps)
    elif field == "progress":
        st.markdown(f"{info.final_progress*100.:.0f}%")
    elif field == "racer":
        st.markdown(info.racer_name)
    elif field == "track":
        st.markdown(info.track_name)
    elif field == "run_bt":
        if info.entry.status in {"created", "running"}:
            if st.button("Executar", key = f"run_bt_{info.entry.training_id}"):
                run_training({
                    "mode": "training",
                    "training_id": info.entry.training_id,
                })
    elif field == "results_bt":
        if info.entry.status in {"running", "finished", "interrupted"}:
            if st.button("Resultado", key = f"results_bt_{info.entry.training_id}"):
                show_results(info.entry.training_id)

all_fields: dict[str, Field] = {
    "created_at": Field(
        text = "Criado em",
        size = 1,
    ),
    "status": Field(
        text = "Status",
        size = 1,
    ),
    "iteration": Field(
        text = "Iteração",
        size = 1,
    ),
    "laps": Field(
        text = "Voltas",
        size = 1,
    ),
    "finished": Field(
        text = "Concluído em",
        size = 1,
    ),
    "racer": Field(
        text = "Corredor",
        size = 1,
    ),
    "track": Field(
        text = "Pista",
        size = 1,
    ),
    "progress": Field(
        text = "Último resultado",
        size = 1,
    ),
    "run_bt": Field(
        text = "",
        size = 1,
    ),
    "results_bt": Field(
        text = "",
        size = 1,
    ),
}

default_field_list: list[str] = ["created_at", "status", "iteration", "laps", "progress", "racer", "track", "run_bt", "results_bt"]

def draw_info_header(
        fields: list[str] = [],
    ) -> None:
    if len(fields) == 0:
        fields = default_field_list
    col_sizes: list[int] = [all_fields[f]["size"] for f in fields]
    cols = st.columns(col_sizes)
    for i, col in enumerate(cols):
        with col:
            if all_fields[fields[i]]['text'] != "":
                st.markdown(f"**{all_fields[fields[i]]['text']}**")

def draw_info_line(
        info: TrainingInfo,
        fields: list[str] = [],
    ) -> None:
    if len(fields) == 0:
        fields = default_field_list
    col_sizes: list[int] = [all_fields[f]["size"] for f in fields]
    cols = st.columns(col_sizes)
    for i, col in enumerate(cols):
        with col:
            draw_field(info, fields[i])

def draw(
        info_list: list[TrainingInfo],
        fields: list[str] = [],
    ) -> None:
    st.markdown("### Histórico de treinos")
    draw_info_header(fields)
    for info in info_list:
        draw_info_line(info, fields)