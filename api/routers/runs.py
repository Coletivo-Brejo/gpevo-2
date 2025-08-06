from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import os

from models.run import Run
from utils import (
    read_all_resources,
    read_resource,
    update_resource,
)


RUNS_PATH = "{data_path}/runs".format(
    data_path = os.environ.get("DATA_PATH")
)

router = APIRouter()

@router.get("/runs")
def read_runs(
        fields: list[str] = Query(None),
    ) -> JSONResponse:
    return read_all_resources(RUNS_PATH, fields)

@router.post("/runs")
def save_runs(runs: list[Run]) -> JSONResponse:
    for run in runs:
        run_id: str = run.run_id
        update_resource(RUNS_PATH, run_id, run)
    return JSONResponse({"Sucesso": "Runs salvas"})

@router.get("/runs/{run_id}")
def read_run(
        run_id: str,
        fields: list[str] = Query(None),
    ) -> JSONResponse:
    return read_resource(RUNS_PATH, run_id, fields)

@router.put("/runs/{run_id}")
def update_run(run_id: str, run: Run):
    return update_resource(RUNS_PATH, run_id, run)