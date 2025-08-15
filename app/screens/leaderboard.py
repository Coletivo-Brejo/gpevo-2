import streamlit as st
from typing import TypedDict

from entities.track import LeaderboardEntry
from utils.proxy import get, get_racer_name, get_track_length, load_resource_dict


class Field(TypedDict):
    text: str
    size: int

all_fields: dict[str, Field] = {
    "ranking": Field(
        text = "Posição",
        size = 1,
    ),
    "racer": Field(
        text = "Corredor",
        size = 1,
    ),
    "brain_version": Field(
        text = "Versão do cérebro",
        size = 1,
    ),
    "progress": Field(
        text = "Progresso",
        size = 1,
    ),
    "time": Field(
        text = "Tempo",
        size = 1,
    ),
    "ran_at": Field(
        text = "Data",
        size = 1,
    ),
}

default_field_list: list[str] = ["ranking", "racer", "brain_version", "progress", "time", "ran_at"]

def draw_field(
        entry: LeaderboardEntry,
        ranking: int,
        field: str,
    ) -> None:
    if field == "ranking":
        st.markdown(ranking+1)
    elif field == "racer":
        st.markdown(get_racer_name(entry.racer_id))
    elif field == "brain_version":
        st.markdown(entry.brain_version)
    elif field == "progress":
        track_length: float|None = get_track_length(entry.track_id)
        if track_length is not None:
            fraction: float = entry.progress / track_length / entry.laps
            st.markdown(f"{fraction*100.:.0f}%")
    elif field == "time":
        if entry.finished:
            minutes: int = int(entry.time // 60.)
            seconds: float = entry.time - minutes*60.
            st.markdown(f"{minutes}:{seconds:.1f}s")
        else:
            st.markdown("-")
    elif field == "ran_at":
        st.markdown(entry.ran_at.strftime("%Y-%m-%d"))

def draw_entry_header(
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

def draw_entry_line(
        entry: LeaderboardEntry,
        ranking: int,
        fields: list[str] = [],
    ) -> None:
    if len(fields) == 0:
        fields = default_field_list
    col_sizes: list[int] = [all_fields[f]["size"] for f in fields]
    cols = st.columns(col_sizes)
    for i, col in enumerate(cols):
        with col:
            draw_field(entry, ranking, fields[i])

def draw_entry_list(
        entries: list[LeaderboardEntry],
        fields: list[str] = [],
    ) -> None:
    draw_entry_header(fields)
    for ranking, entry in enumerate(entries):
        draw_entry_line(entry, ranking, fields)

def draw(track_id: str) -> None:
    track_dict: dict|None = load_resource_dict("/tracks", track_id, fields = ["loops"])
    if track_dict is not None:
        laps_options: list[int] = [1]
        if track_dict["loops"]:
            laps_options += [3, 5]
        mirrored: bool = st.toggle("Espelhado")
        laps: int = st.selectbox("Voltas", laps_options)
        entries_list: dict|list|None = get(
            f"/tracks/{track_id}/leaderboard/entries/best",
            {"laps": laps, "mirrored": mirrored},
        )
        if entries_list is not None:
            entries: list[LeaderboardEntry] = [LeaderboardEntry.from_dict(d) for d in entries_list]
            draw_entry_list(entries)