from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import os

from data_manager import invalidate_entries, update_brain
from models.brain import Brain
from models.racer import Racer
from utils import (
    get_resource,
    read_resource,
    read_all_resources,
    update_resource,
)


RACERS_PATH = "{data_path}/racers".format(
    data_path = os.environ.get("DATA_PATH")
)

router = APIRouter()

@router.get("/racers")
def read_racers(
        fields: list[str] = Query(None),
    ) -> JSONResponse:
    return read_all_resources(RACERS_PATH, fields)

@router.get("/racers/{racer_id}")
def read_racer(racer_id: str):
    return read_resource(RACERS_PATH, racer_id)

@router.put("/racers/{racer_id}")
def update_racer(racer_id: str, racer: Racer):
    return update_resource(RACERS_PATH, racer_id, racer)

@router.post("racers/{racer_id}/update_brain")
def update_racer_brain(racer_id: str, brain: Brain) -> JSONResponse:
    return update_brain(racer_id, brain)

@router.get("/racers/{racer_id}/lobotomize")
def lobotomize(
        racer_id: str,
        neurons: list[str] = Query(None),
    ) -> JSONResponse:
    racer_dict: dict|None = get_resource(RACERS_PATH, racer_id)
    deleted_neurons: list[str] = []
    removed_connections: list[str] = []
    reset_weights: list[str] = []
    if racer_dict is not None:
        racer: Racer = Racer(**racer_dict)
        for neuron in racer.brain.get_hidden_neurons():
            if neurons is None or neuron.neuron_id in neurons:
                deleted_neurons.append(neuron.neuron_id)
                racer.brain.delete_neuron(neuron)
        for neuron in racer.brain.get_thruster_neurons():
            if neurons is None or neuron.neuron_id in neurons:
                if len(neuron.input_ids) > 0:
                    removed_connections.append(neuron.neuron_id)
                    racer.brain.remove_all_inputs_from_neuron(neuron, True)
                reset_weights.append(neuron.neuron_id)
                racer.brain.reset_weights_from_neuron(neuron)
        update_brain(racer_id, racer.brain)
        invalidate_entries(racer_id)
        return JSONResponse({
            "Neurônios excluídos": deleted_neurons,
            "Conexões removidas": removed_connections,
            "Parâmetros zerados": reset_weights,
        })
    return JSONResponse({"Erro": "Corredor não encontrado"})