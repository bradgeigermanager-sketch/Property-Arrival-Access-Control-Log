import cv2
from pyzbar.pyzbar import decode
from datetime import datetime
import json
import os

class BarcodeIntakeChannel:
    def __init__(self, db_file="identity_library.json", log_file="arrival_log.csv"):
        self.db_file = db_file
        self.log_file = log_file
        self.identity_db = self.load_identity_library()

    def load_identity_library(self):
        """Loads the identity and file reference library."""
        if not os.path.exists(self.db_file):
            # Create a default template library if missing
            default_data = {
                "EMP1001": {"name": "John Doe", "role": "Employee", "department": "Front Desk", "file_ref": "files/emp_1001.pdf"},
                "TEMP901": {"name": "Visitor Pass A", "role": "Temporary", "department": "Security Clearance", "file_ref": "files/temp_901.pdf"}
            }
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, indent=4)
            return default_data

        with open(self.db_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def translate_code(self, raw_data):
        """
        Translates raw barcode data into a normalized intake payload.
        Handles both permanent employee IDs and temporary security slips.
        """
        clean_id = raw_data.strip().upper()
        
        # Check if ID exists in library
        if clean_id in self.identity_db:
            record = self.identity_db[clean_id]
            return {
                "status": "SUCCESS",
                "badge_id": clean_id,
                "name": record["name"],
                "role": record["role"],
                "department": record["department"],
                "file_ref": record["file_ref"]
            }
        else:
            # Fallback handling for unlisted temporary slips or visitors
            return {
                "status": "UNRECOGNIZED",
                "badge_id": clean_id,
                "name": "Unverified Visitor / Slip",
                "role": "Temporary",
                "department": "General Access",
                "file_ref": "files/default_visitor.pdf"
            }

    def process_intake(self, raw_data):
        """Processes the translated scan through the intake channel and logs it."""
        payload = self.translate_code(raw_data)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log entry to CSV archive
        file_exists = os.path.exists(self.log_file)
        with open(self.log_file, mode='a', newline='', encoding='utf-8') as f:
            import csv
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "Badge ID", "Name", "Role", "Department", "File Ref", "Status"])
            writer.writerow([
                timestamp, 
                payload["badge_id"], 
                payload["name"], 
                payload["role"], 
                payload["department"], 
                payload["file_ref"], 
                payload["status"]
            ])
            
        print(f"[INTAKE LOGGED] {timestamp} | {payload['name']} ({payload['badge_id']}) - {payload['status']}")
        return payload

# Example usage with webcam stream
def start_camera_intake(camera_index=0):
    channel = BarcodeIntakeChannel()
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print("Error: Camera unavailable.")
        return

    print("Intake scanner active. Press 'q' to quit.")
    recent_scans = {}

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcodes = decode(gray)
        current_time = datetime.now().timestamp()

        for barcode in barcodes:
            raw_data = barcode.data.decode("utf-8")
            
            # Cooldown check (5 seconds per badge)
            if raw_data not in recent_scans or (current_time - recent_scans[raw_data]) > 5:
                channel.process_intake(raw_data)
                recent_scans[raw_data] = current_time

            # Visual overlay
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Arrival Intake Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
