from flask import Flask, request, jsonify
import json
import datetime

app = Flask(__name__)
history_file = "history.json"

def load_history():
    try:
        with open(history_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

history = load_history()

@app.route('/history/add', methods=['POST'])
def add_history():
    global history
    data = request.json
    if not data or "file" not in data or "action" not in data:
        return jsonify({"error": "Invalid data"}), 400
    entry = {"file": data["file"], "action": data["action"], "timestamp": datetime.datetime.now().isoformat()}
    history.append(entry)
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=4)
    return jsonify({"status": "History updated"})

if __name__ == "__main__":
    app.run(port=5003, debug=True)