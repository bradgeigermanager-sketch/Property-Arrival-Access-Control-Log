import os
import json
import csv
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

REGISTRY_PATH = "identity_library.json"
LOG_FILE = "arrival_log.csv"

def load_registry():
    if not os.path.exists(REGISTRY_PATH):
        return {"registry_metadata": {"total_active_records": 0}, "directory": []}
    with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def log_arrival_to_csv(badge_id, name, role, department, file_ref, status):
    file_exists = os.path.exists(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Badge ID", "Name", "Role", "Department", "File Ref", "Status"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            badge_id, name, role, department, file_ref, status
        ])

@app.route('/api/scan', methods=['POST'])
def api_scan():
    data = request.get_json()
    badge_id = data.get("badge_id", "").strip().upper()
    
    registry = load_registry()
    directory = registry.get("directory", [])
    
    # Find matching record in directory
    record = next((item for item in directory if item["badge_id"] == badge_id), None)
    
    if record:
        status = "SUCCESS"
        response_payload = {
            "status": status,
            "badge_id": record["badge_id"],
            "name": record["name"],
            "role": record["record_type"],
            "department": record["department"],
            "file_ref": record["file_path"]
        }
    else:
        # Fallback / Unrecognized temporary guest
        status = "UNRECOGNIZED"
        response_payload = {
            "status": status,
            "badge_id": badge_id,
            "name": "Unverified Visitor / Slip",
            "role": "Temporary",
            "department": "General Access",
            "file_ref": "files/visitors/default.json"
        }
    
    # Log arrival event
    log_arrival_to_csv(
        response_payload["badge_id"],
        response_payload["name"],
        response_payload["role"],
        response_payload["department"],
        response_payload["file_ref"],
        response_payload["status"]
    )
    
    return jsonify(response_payload)

@app.route('/api/registry', methods=['GET'])
def api_get_registry():
    return jsonify(load_registry())

if __name__ == '__main__':
    print("Starting Arrival Tracking Local Server...")
    app.run(port=5000, debug=True)

@app.route('/api/file', methods=['GET'])
def api_get_file():
    file_path = request.args.get('path', '')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    else:
        return jsonify({"error": "File path not found on server", "requested_path": file_path}), 404
