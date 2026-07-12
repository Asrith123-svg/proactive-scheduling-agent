from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__)

# pending_actions.json lives in the same folder as your scheduling-agent scripts.
# This dashboard's app.py should be copied into that same folder.
PENDING_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pending_actions.json')


def load_pending():
    if os.path.exists(PENDING_FILE):
        with open(PENDING_FILE, 'r') as f:
            return json.load(f)
    return []


def save_pending(actions):
    with open(PENDING_FILE, 'w') as f:
        json.dump(actions, f, indent=2)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/actions')
def get_actions():
    actions = load_pending()
    for i, a in enumerate(actions):
        a.setdefault('status', 'awaiting_approval')
        a['id'] = i

    counts = {
        'awaiting': sum(1 for a in actions if a['status'] == 'awaiting_approval'),
        'approved': sum(1 for a in actions if a['status'] == 'approved'),
        'rejected': sum(1 for a in actions if a['status'] == 'rejected'),
        'total': len(actions),
    }
    # Most recent first
    return jsonify({'actions': list(reversed(actions)), 'counts': counts})


@app.route('/api/actions/<int:action_id>/<decision>', methods=['POST'])
def update_action(action_id, decision):
    if decision not in ('approve', 'reject'):
        return jsonify({'error': 'invalid decision'}), 400

    actions = load_pending()
    if action_id < 0 or action_id >= len(actions):
        return jsonify({'error': 'not found'}), 404

    actions[action_id]['status'] = 'approved' if decision == 'approve' else 'rejected'
    save_pending(actions)
    return jsonify({'ok': True})


if __name__ == '__main__':
    print(f"Reading from: {PENDING_FILE}")
    app.run(debug=True, port=5000)
