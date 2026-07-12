import json
import os
from datetime import datetime

EXECUTED_FILE = 'executed_actions.json'


def load_executed():
    if os.path.exists(EXECUTED_FILE):
        with open(EXECUTED_FILE, 'r') as f:
            return json.load(f)
    return []


def save_executed(actions):
    with open(EXECUTED_FILE, 'w') as f:
        json.dump(actions, f, indent=2)


def log_executed_action(conflict_description, proposed_resolution):
    actions = load_executed()
    actions.append({
        'conflict': conflict_description,
        'resolution': proposed_resolution,
        'status': 'auto_executed',
        'timestamp': datetime.now().isoformat(),
    })
    save_executed(actions)
    print(f"Logged auto-executed action: {conflict_description}")