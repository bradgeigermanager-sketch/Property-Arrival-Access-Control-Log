import json
import os
from datetime import datetime, timedelta

class TemporaryRecordIntake:
    def __init__(self, registry_path="identity_library.json"):
        self.registry_path = registry_path
        self.ensure_registry_exists()

    def ensure_registry_exists(self):
        """Ensures the master registry file exists with base structures."""
        if not os.path.exists(self.registry_path):
            initial_registry = {
                "registry_metadata": {
                    "organization": "Aven Hospitality Property",
                    "last_updated": "2026-10-26",
                    "total_active_records": 0
                },
                "directory": []
            }
            with open(self.registry_path, 'w', encoding='utf-8') as f:
                json.dump(initial_registry, f, indent=4)

    def create_temporary_record(self, badge_id, full_name, company_or_reason, escort_name, security_zones, hours_valid=8):
        """
        Initial entry task for temporary or on-the-spot visitor records.
        Includes access expiration details and updates the master directory.
        """
        badge_id = badge_id.strip().upper()
        file_path = f"files/visitors/{badge_id}.json"
        
        # Ensure target directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Calculate expiration timestamp based on validity window (default 8 hours / same day)
        now = datetime.now()
        issue_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        expiration_time = now + timedelta(hours=hours_valid)
        expires_date = expiration_time.strftime("%Y-%m-%d")
        expires_time_str = expiration_time.strftime("%H:%M:%S")

        # 1. Build the temporary file structure with access expiration
        visitor_file_data = {
            "badge_id": badge_id,
            "record_type": "Temporary Visitor / On-Spot Entry",
            "visitor_info": {
                "full_name": full_name,
                "company_or_reason": company_or_reason,
                "escort_required": bool(escort_name),
                "escort_name": escort_name if escort_name else "None"
            },
            "credentials": {
                "barcode_payload": badge_id,
                "issue_timestamp": issue_timestamp,
                "status": "Active"
            },
            "access_expiration": {
                "expires_at_date": expires_date,
                "expires_at_time": expires_time_str,
                "auto_revoke_on_departure": True,
                "notes": "Temporary same-day access slip generated on-site."
            },
            "permissions": {
                "security_zones": security_zones,
                "synxis_access": False
            }
        }

        # Write individual temporary file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(visitor_file_data, f, indent=4)

        # 2. Update the Master Registry Directory
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)

        directory = registry["directory"]
        existing_entry = next((item for item in directory if item["badge_id"] == badge_id), None)

        if not existing_entry:
            new_directory_entry = {
                "badge_id": badge_id,
                "name": full_name,
                "record_type": "Temporary",
                "department": company_or_reason,
                "file_path": file_path
            }
            directory.append(new_directory_entry)
            registry["registry_metadata"]["total_active_records"] = len(directory)

            # Save updated registry
            with open(self.registry_path, 'w', encoding='utf-8') as f:
                json.dump(registry, f, indent=4)

            print(f"[TEMPORARY ENTRY COMPLETE] Created visitor file for {full_name} ({badge_id}). Access expires at {expires_time_str}.")
        else:
            print(f"[NOTICE] Temporary record for {badge_id} updated in registry.")

# Example execution for an on-the-spot visitor pass
if __name__ == "__main__":
    temp_intake = TemporaryRecordIntake()
    
    temp_intake.create_temporary_record(
        badge_id="TEMP902",
        full_name="Marcus Vance",
        company_or_reason="HVAC Contractor Vendor",
        escort_name="John Doe",
        security_zones=["Public Lobby", "Maintenance Corridor B"],
        hours_valid=6
    )
