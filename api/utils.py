from datetime import datetime, tzinfo
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import json
import os
from pydantic import BaseModel
import pytz


load_dotenv()
IDS_FILE = "{data_path}/ids.json".format(
    data_path = os.environ.get("DATA_PATH")
)

def get_resource(
        dir: str,
        resource_id: str,
        fields: list[str]|None = None,
    ) -> dict|None:
    resource_file = f"{dir}/{resource_id}.json"
    try:
        with open(resource_file, encoding="utf-8") as f:
            resource_dict: dict = json.load(f)
            if fields is not None:
                resource_dict = {k:v for k, v in resource_dict.items() if k in fields}
            return resource_dict
    except FileNotFoundError:
        return None

def get_all_resources(
        dir: str,
        fields: list[str]|None = None,
    ) -> list[dict]:
    resources: list[dict] = []
    if os.path.exists(dir):
        for file in os.listdir(dir):
            if file.endswith(".json"):
                resource_id: str = file[:-5]
                resource_dict: dict|None = get_resource(dir, resource_id, fields)
                if resource_dict is not None:
                    resources.append(resource_dict)
    return resources

def read_resource(
        dir: str,
        resource_id: str,
        fields: list[str]|None = None,
    ) -> JSONResponse:
    resource_dict: dict|None = get_resource(dir, resource_id, fields)
    if resource_dict is not None:
        return JSONResponse(resource_dict)
    else:
        return JSONResponse("Recurso não encontrato", status_code = 404)

def read_all_resources(
        dir: str,
        fields: list[str]|None = None,
    ) -> JSONResponse:
    return JSONResponse(get_all_resources(dir, fields))

def update_resource(
        dir: str,
        resource_id: str,
        resource: BaseModel,
    ) -> JSONResponse:
    if not os.path.exists(dir):
        os.makedirs(dir)
    resource_file: str = f"{dir}/{resource_id}.json"
    with open(resource_file, "w", encoding="utf-8") as f:
        resource_json = jsonable_encoder(resource)
        json.dump(resource_json, f, ensure_ascii=False)
    return JSONResponse("Recurso atualizado")

def get_ids_dict(ids_file: str) -> dict:
    try:
        with open(ids_file, encoding="utf-8") as f:
            ids_dict: dict = json.load(f)
            return ids_dict
    except FileNotFoundError:
        return {}

def get_next_id(id_name: str, id_format: str = "{id}") -> str:
    ids_dict: dict = get_ids_dict(IDS_FILE)
    current_id: int
    if id_name in ids_dict:
        current_id = ids_dict[id_name]
        ids_dict[id_name] += 1
    else:
        current_id = 0
        ids_dict[id_name] = 1
    formatted_id: str = id_format.format(id = current_id)
    with open(IDS_FILE, "w", encoding="utf-8") as f:
        ids_json = jsonable_encoder(ids_dict)
        json.dump(ids_json, f, ensure_ascii=False)
    return formatted_id

def now() -> datetime:
    brtz: tzinfo = pytz.timezone("America/Sao_Paulo")
    return datetime.now(brtz)

def delete_resource(dir: str, resource_id: str) -> bool:
    resource_file = f"{dir}/{resource_id}.json"
    try:
        os.remove(resource_file)
        return True
    except FileNotFoundError:
        return False