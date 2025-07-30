from dotenv import load_dotenv
import json
import os
import requests


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