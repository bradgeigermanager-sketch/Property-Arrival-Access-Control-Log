# Property-Arrival-Access-Control-Log
Records of arrivals and departures, cross-referenced to employee file, or social media account, etc.


Procedure: Identity Library File Generation

Step 1: Determine whether the subject is a permanent staff member or a temporary/visitor entry.

Step 2: Assign a unique badge_id matching your barcode format.

Step 3: Generate the individual JSON file using the corresponding template (Permanent vs. Temporary). For temporary records, ensure the access_expiration fields are populated (even if left blank or set to same-day auto-revoke).

Step 4: Append the new record entry into the Master Registry Index so the intake channel can successfully query and link it upon scanning.


Procedure: Regular Records Initial Entry
Data Collection: Gather new staff member credentials (Full Name, Department, Role, Extension, and permitted security zones).

Execution: Input details into the create_permanent_record() module function with a unique badge_id.

File Generation: The script automatically generates a dedicated JSON file under files/personnel/{badge_id}.json using the permanent schema template.

Registry Sync: The script appends the new record into the central identity_library.json directory list, updating active totals and making it instantly searchable by the arrival intake scanner.


Procedure: Temporary & Same-Day Visitor Entry
Credential Assignment: Issue a temporary printed barcode slip and assign a unique identifier (e.g., TEMP902).

Data Capture: Input visitor details, company/reason, escort requirements, permitted security zones, and duration window into the create_temporary_record() function.

Timed File Generation: The script generates an isolated JSON schema containing the access_expiration section, ensuring automatic privilege revocation parameters are clearly established.

Directory Registration: Appends the visitor entry to the master index so that scanning the temporary slip at entry checkpoints instantly flags expiration rules and links back to the visitor's file record.

Procedure: Badge Generation & Printing
Record Selection: Access an existing record via the Master Registry directory or create a new permanent/temporary entry.

Slip Rendering: Invoke the badge generator endpoint (/api/generate-badge) passing the payload ID, name, department, and expiration rules.

Print Execution: Output the formatted Code 39 barcode ticket to a local receipt or badge printer for physical issuance at the security or front desk checkpoint.
