import streamlit as st
import streamlit.components.v1 as components
from typing import Iterable

from entities.training import Training, TrainingInfo
from screens.training_card import draw as draw_training
from screens.training_editor import draw as draw_editor
from screens.training_list import draw as draw_info_list
from utils.proxy import get


st.write("## Treinamentos")

draw_editor()

infos_dict: dict|list|None = get("/trainings/info", {})
if infos_dict is not None:
    infos: list[TrainingInfo] = [TrainingInfo.from_dict(d) for d in infos_dict]
    draw_info_list(infos, ["created_at", "racer", "track", "status", "iteration", "run_bt", "results_bt"])