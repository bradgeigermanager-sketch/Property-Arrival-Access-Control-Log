# Property-Arrival-Access-Control-Log
Records of arrivals and departures, cross-referenced to employee file, or social media account, etc.


Procedure: Identity Library File Generation

Step 1: Determine whether the subject is a permanent staff member or a temporary/visitor entry.

Step 2: Assign a unique badge_id matching your barcode format.

Step 3: Generate the individual JSON file using the corresponding template (Permanent vs. Temporary). For temporary records, ensure the access_expiration fields are populated (even if left blank or set to same-day auto-revoke).

Step 4: Append the new record entry into the Master Registry Index so the intake channel can successfully query and link it upon scanning.
