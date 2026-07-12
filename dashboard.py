from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
import os

app = FastAPI()


def read_json_file(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []


@app.get("/api/pending")
def get_pending():
    return read_json_file('pending_actions.json')


@app.get("/api/executed")
def get_executed():
    return read_json_file('executed_actions.json')


@app.get("/", response_class=HTMLResponse)
def dashboard():
    with open('dashboard.html', 'r') as f:
        return f.read()