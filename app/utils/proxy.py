from dotenv import load_dotenv
import json
import os
import requests
import streamlit as st


load_dotenv()
API_URL = os.environ.get("API_URL")

def load_resource_dict(
        route: str,
        resource_id: str,
        fields: list[str]|None = None,
    ) -> dict|None:
    params: dict = {}
    if fields is not None:
        params["fields"] = fields
    response = requests.get(f"{API_URL}{route}/{resource_id}", params=params)
    if response.ok:
        resource_dict: dict = response.json()
        return resource_dict
    else:
        return None

def load_all_resources(
        route: str,
        fields: list[str]|None = None,
    ) -> list[dict]|None:
    params: dict = {}
    if fields is not None:
        params["fields"] = fields
    response = requests.get(f"{API_URL}{route}", params=params)
    if response.ok:
        dict_list: list[dict] = response.json()
        return dict_list
    else:
        return None

def get(
        route: str,
        params: dict = {},
    ) -> dict|list|None:
    response = requests.get(
        f"{API_URL}{route}",
        params = params,
    )
    if response.ok:
        return response.json()
    else:
        return None

def post(
        route: str,
        body: dict,
        params: dict = {},
    ) -> dict|list|None:
    response = requests.post(
        f"{API_URL}{route}",
        data = json.dumps(body, ensure_ascii=False),
        params = params,
    )
    if response.ok:
        print(response.json())
        return response.json()
    else:
        return None

def load_headers(route: str, fields: list[str]) -> list[dict]:
    dict_list: list[dict]|None = load_all_resources(
        route,
        fields = fields,
    )
    if dict_list is not None:
        return dict_list
    else:
        return []

@st.cache_data
def get_racer_name(racer_id: str) -> str|None:
    racer_dict: dict|None = load_resource_dict(
        "/racers",
        racer_id,
        fields = ["name"],
    )
    if racer_dict is not None:
        return racer_dict["name"]
    else:
        return None

@st.cache_data
def get_track_name(track_id: str) -> str|None:
    track_dict: dict|None = load_resource_dict(
        "/tracks",
        track_id,
        fields = ["name"],
    )
    if track_dict is not None:
        return track_dict["name"]
    else:
        return None

@st.cache_data
def get_track_length(track_id: str) -> float|None:
    track_dict: dict|None = load_resource_dict(
        "/tracks",
        track_id,
        fields = ["length"],
    )
    if track_dict is not None:
        return track_dict["length"]
    else:
        return None