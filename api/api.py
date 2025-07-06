from dotenv import load_dotenv
from fastapi import FastAPI
import os
from typing import Union


load_dotenv()
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World", "path": os.environ.get("DATA_PATH")}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}