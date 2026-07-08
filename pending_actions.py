import json
import os

PENDING_FILE = 'pending_actions.json'


def load_pending():
    if os.path.exists(PENDING_FILE):
        with open(PENDING_FILE, 'r') as f:
            return json.load(f)
    return []


def save_pending(actions):
    with open(PENDING_FILE, 'w') as f:
        json.dump(actions, f, indent=2)


def add_pending_action(conflict_description, proposed_resolution):
    actions = load_pending()
    actions.append({
        'conflict': conflict_description,
        'proposed_resolution': proposed_resolution,
        'status': 'awaiting_approval'
    })
    save_pending(actions)
    print(f"Queued for approval: {conflict_description}")