from dotenv import load_dotenv
import json
import os
import requests


load_dotenv()
API_URL = os.environ.get("API_URL")

def load_resource_dict(route: str, resource_id: str) -> dict|None:
    response = requests.get(f"{API_URL}{route}/{resource_id}")
    if response.ok:
        resource_dict: dict = response.json()
        return resource_dict
    else:
        return None

def load_all_resources(route: str) -> list[dict]|None:
    response = requests.get(f"{API_URL}{route}")
    if response.ok:
        dict_list: list[dict] = response.json()
        return dict_list
    else:
        return None