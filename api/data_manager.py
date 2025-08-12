from fastapi.responses import JSONResponse
import os

from models.brain import Brain
from models.models import Racer
from models.training import TrainingEntry
from utils import get_resource, update_resource


RACERS_PATH = "{data_path}/racers".format(
    data_path = os.environ.get("DATA_PATH")
)

def update_brain(racer_id: str, brain: Brain) -> JSONResponse:
    racer_dict: dict|None = get_resource(RACERS_PATH, racer_id)
    if racer_dict is not None:
        racer: Racer = Racer(**racer_dict)
        racer.brain = brain
        return update_resource(RACERS_PATH, racer_id, racer)
    else:
        return JSONResponse({"Erro": "Corredor não encontrado"}, 404)