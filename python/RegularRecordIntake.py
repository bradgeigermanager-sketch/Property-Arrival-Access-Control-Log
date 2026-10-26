import json
import os

class RegularRecordIntake:
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

    def create_permanent_record(self, badge_id, full_name, department, role, contact_extension, security_zones):
        """
        Initial entry task for regular permanent employee records.
        Creates the individual file and updates the master directory registry.
        """
        badge_id = badge_id.strip().upper()
        file_path = f"files/personnel/{badge_id}.json"
        
        # Ensure target directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 1. Build the individual permanent file structure
        employee_file_data = {
            "badge_id": badge_id,
            "record_type": "Permanent Employee",
            "personal_info": {
                "full_name": full_name,
                "department": department,
                "role": role,
                "contact_extension": contact_extension
            },
            "credentials": {
                "barcode_payload": badge_id,
                "status": "Active"
            },
            "permissions": {
                "security_zones": security_zones,
                "synxis_access": True
            },
            "audit_trail": {
                "created_date": "2026-10-26",
                "last_reviewed": "2026-10-26"
            }
        }

        # Write individual file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(employee_file_data, f, indent=4)

        # 2. Update the Master Registry Directory
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)

        # Check if already in directory to avoid duplicates
        directory = registry["directory"]
        existing_entry = next((item for item in directory if item["badge_id"] == badge_id), None)

        if not existing_entry:
            new_directory_entry = {
                "badge_id": badge_id,
                "name": full_name,
                "record_type": "Permanent",
                "department": department,
                "file_path": file_path
            }
            directory.append(new_directory_entry)
            registry["registry_metadata"]["total_active_records"] = len(directory)

            # Save updated registry
            with open(self.registry_path, 'w', encoding='utf-8') as f:
                json.dump(registry, f, indent=4)

            print(f"[REGULAR ENTRY COMPLETE] Created and registered file for {full_name} ({badge_id}).")
        else:
            print(f"[NOTICE] Record for {badge_id} already exists in registry. Individual file updated.")

# Example execution of the initial entry task
if __name__ == "__main__":
    intake_module = RegularRecordIntake()
    
    # Simulating initial entry for a new regular staff member
    intake_module.create_permanent_record(
        badge_id="EMP1004",
        full_name="Sarah Jenkins",
        department="Front Desk",
        role="Guest Services Agent",
        contact_extension="402",
        security_zones=["Front Desk", "Back Office"]
    )
