import streamlit as st
import streamlit.components.v1 as components


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