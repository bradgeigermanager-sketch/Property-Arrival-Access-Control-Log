import os
import json

def generate_badge_html_snippet(badge_id, name, role, department, expiration="N/A"):
    """
    Generates a clean, printable HTML badge snippet complete with a barcode representation 
    (using SVG/Canvas or standard barcode font styling) ready for front desk printing.
    """
    badge_color = "#2b6cb0" if role == "Permanent" else "#d69e2e"
    
    html_snippet = f"""
    <div style="width: 320px; border: 2px solid #2d3748; border-radius: 10px; padding: 20px; font-family: sans-serif; background: white; margin: 10px auto;">
        <div style="background: {badge_color}; color: white; padding: 5px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; text-align: center; margin-bottom: 12px;">
            {role.upper()} ACCESS CREDENTIAL
        </div>
        <h2 style="margin: 0 0 5px 0; color: #1a365d; font-size: 20px;">{name}</h2>
        <p style="margin: 0 0 15px 0; font-size: 14px; color: #4a5568;"><strong>Department:</strong> {department}</p>
        
        <div style="background: #f7fafc; border: 1px dashed #cbd5e0; padding: 15px; text-align: center; border-radius: 6px;">
            <!-- Barcode Graphic Simulation -->
            <div style="font-family: 'Libre Barcode 39', cursive, monospace; font-size: 48px; letter-spacing: 4px; margin-bottom: 5px;">
                *{badge_id}*
            </div>
            <div style="font-size: 12px; font-weight: bold; color: #2d3748; letter-spacing: 1px;">
                {badge_id}
            </div>
        </div>
        
        <div style="margin-top: 15px; font-size: 11px; color: #718096; border-top: 1px solid #e2e8f0; pt-2;">
            <p style="margin: 5px 0 0 0;"><strong>Expires / Valid Thru:</strong> {expiration}</p>
            <p style="margin: 2px 0 0 0;">Aven Hospitality Property Management</p>
        </div>
    </div>
    """
    return html_snippet


import os
import json
from datetime import datetime, timedelta

def create_temporary_badge_slip(full_name, company_reason, escort_name, hours_valid=8):
    """
    Generates a unique temporary badge ID, saves its individual JSON file,
    and returns both the record metadata and the printable HTML snippet.
    """
    # Generate unique temporary ID based on timestamp (e.g., TEMP-1026-1430)
    now = datetime.now()
    badge_id = f"TEMP-{now.strftime('%m%d-%H%M')}"
    file_path = f"files/visitors/{badge_id}.json"
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    expiration_time = now + timedelta(hours=hours_valid)
    expires_date = expiration_time.strftime("%Y-%m-%d")
    expires_time = expiration_time.strftime("%H:%M:%S")

    visitor_data = {
        "badge_id": badge_id,
        "record_type": "Temporary",
        "visitor_info": {
            "full_name": full_name,
            "company_or_reason": company_reason,
            "escort_required": bool(escort_name),
            "escort_name": escort_name if escort_name else "None"
        },
        "credentials": {
            "barcode_payload": badge_id,
            "issue_timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Active"
        },
        "access_expiration": {
            "expires_at_date": expires_date,
            "expires_at_time": expires_time,
            "auto_revoke_on_departure": True
        },
        "permissions": {
            "security_zones": ["Public Lobby", "Authorized Visitor Corridor"],
            "synxis_access": False
        }
    }

    # Save individual file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(visitor_data, f, indent=4)

    # Generate Printable HTML Slip
    printable_html = f"""
    <div style="width: 300px; border: 2px dashed #4a5568; border-radius: 8px; padding: 15px; font-family: monospace; background: #fff; margin: auto;">
        <div style="text-align: center; border-bottom: 2px solid #2d3748; padding-bottom: 8px; margin-bottom: 10px;">
            <strong style="font-size: 14px; color: #1a365d;">AVEN HOSPITALITY</strong><br>
            <span style="font-size: 11px; background: #feebc8; color: #744210; padding: 2px 6px; border-radius: 4px;">TEMPORARY VISITOR PASS</span>
        </div>
        <p style="margin: 4px 0; font-size: 13px;"><strong>Name:</strong> {full_name}</p>
        <p style="margin: 4px 0; font-size: 13px;"><strong>Reason:</strong> {company_reason}</p>
        <p style="margin: 4px 0; font-size: 13px;"><strong>Escort:</strong> {escort_name if escort_name else 'None'}</p>
        
        <div style="margin: 15px 0; text-align: center; background: #edf2f7; padding: 10px; border-radius: 4px;">
            <div style="font-family: 'Libre Barcode 39', cursive, monospace; font-size: 42px; letter-spacing: 3px;">*{badge_id}*</div>
            <div style="font-size: 12px; font-weight: bold;">{badge_id}</div>
        </div>
        
        <div style="font-size: 10px; color: #718096; border-top: 1px solid #e2e8f0; padding-top: 6px;">
            <p style="margin: 2px 0;"><strong>Expires:</strong> {expires_date} @ {expires_time}</p>
            <p style="margin: 2px 0;">Must be returned upon departure.</p>
        </div>
    </div>
    """
    return visitor_data, printable_html
