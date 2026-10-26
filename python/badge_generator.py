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
