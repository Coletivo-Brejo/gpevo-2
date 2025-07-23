import streamlit as st


def show_training_options(
        allowed_racers: list[str],
        allowed_tracks: list[str],
    ) -> None:
    racer_id: str = st.selectbox("Corredor", allowed_racers)
    track_id: str = st.selectbox("Pista", allowed_tracks)
    pass